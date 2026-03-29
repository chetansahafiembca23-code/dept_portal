import razorpay
import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .models import Event, Activity, Enrollment

# ── Razorpay client ───────────────────────────────────────────────────────────
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# ── Helper ────────────────────────────────────────────────────────────────────
def is_admin(user):
    return user.is_superuser or (hasattr(user, 'role') and user.role == 'admin')


# ── Public views ──────────────────────────────────────────────────────────────
def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})


# ── Enrollment ────────────────────────────────────────────────────────────────
@login_required
def enroll_activity(request, activity_id):
    if not request.user.is_profile_complete:
        messages.warning(request, "Please complete your profile details before enrolling in an event.")
        return redirect('profile')

    activity = get_object_or_404(Activity, id=activity_id)
    event = activity.event

    already_paid = Enrollment.objects.filter(
        user=request.user,
        event=event,
        payment_status=True
    ).exists()

    if request.method == 'POST':
        enrollment = Enrollment.objects.create(
            user=request.user,
            event=event,
            activity=activity,
            team_name=request.POST.get('team_name', ''),
            participants_list=request.POST.get('members', ''),
            payment_status=already_paid,
        )

        if already_paid or event.fee == 0:
            messages.success(request, f"Successfully enrolled in {activity.name} for free!")
            return redirect('enrollment_success', enrollment_id=enrollment.id)

        amount_in_paise = int(event.fee * 100)
        razorpay_order = client.order.create(data={
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": f"receipt_{enrollment.id}",
        })

        enrollment.razorpay_order_id = razorpay_order['id']
        enrollment.save()

        return render(request, 'events/payment_checkout.html', {
            'enrollment': enrollment,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount_in_paise,
        })

    return render(request, 'events/enroll_form.html', {
        'activity': activity,
        'already_paid': already_paid,
    })


# ── Payment verification (Razorpay callback) ──────────────────────────────────
@csrf_exempt
def payment_verify(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id   = request.POST.get('razorpay_order_id', '')
        signature  = request.POST.get('razorpay_signature', '')

        enrollment = get_object_or_404(Enrollment, razorpay_order_id=order_id)

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id':   order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature':  signature,
            })

            enrollment.payment_status      = True
            enrollment.razorpay_payment_id = payment_id
            enrollment.razorpay_signature  = signature
            enrollment.save()

            messages.success(request, "Payment Successful!")
            return redirect('enrollment_success', enrollment_id=enrollment.id)

        except razorpay.errors.SignatureVerificationError:
            enrollment.delete()
            messages.error(request, "Payment verification failed. Please try again.")
            return redirect('dashboard')

    return redirect('home')


# ── Post-enrollment success page ──────────────────────────────────────────────
@login_required
def enrollment_success(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)

    # Security gate: unpaid enrollments cannot view the success page
    if not enrollment.payment_status:
        return redirect('dashboard')

    return render(request, 'events/success.html', {'enrollment': enrollment})


# ── PDF receipt download ───────────────────────────────────────────────────────
@login_required
def download_receipt(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)

    # Security gate: block unpaid enrollments from downloading a receipt
    if not enrollment.payment_status:
        messages.error(request, "Access Denied: Payment has not been completed for this event.")
        return redirect('dashboard')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Receipt_{enrollment.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 50, "DEPT-HUB PORTAL")
    p.setFont("Helvetica", 12)
    p.drawCentredString(width / 2, height - 70, "Official Payment Receipt")
    p.line(50, height - 80, width - 50, height - 80)

    # Receipt details
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 120, f"Receipt ID: #REC-{enrollment.id}")

    p.setFont("Helvetica", 12)
    p.drawString(100, height - 150, f"Student Name : {enrollment.user.username}")
    p.drawString(100, height - 170, f"Roll Number  : {enrollment.user.roll_number}")
    p.drawString(100, height - 190, f"Event        : {enrollment.event.title}")
    p.drawString(100, height - 210,
        f"Activity     : {enrollment.activity.name if enrollment.activity else 'General Entry'}")

    if enrollment.razorpay_payment_id:
        p.drawString(100, height - 230, f"Payment ID   : {enrollment.razorpay_payment_id}")

    # Amount box
    p.setFillColor(colors.lightgrey)
    p.rect(100, height - 290, 400, 40, fill=1)
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(120, height - 275, f"Amount Paid  : ₹{enrollment.event.fee}")
    p.drawString(320, height - 275, "Status: PAID")

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(100, height - 330,
        f"Date of Issue: {enrollment.enrolled_at.strftime('%d-%m-%Y %H:%M')}")
    p.drawCentredString(width / 2, 50, "This is a computer-generated receipt.")

    p.showPage()
    p.save()
    return response


# ── Admin: export enrollments as CSV ─────────────────────────────────────────
@user_passes_test(is_admin)
def export_enrollments_csv(request, event_id):
    event       = get_object_or_404(Event, id=event_id)
    enrollments = Enrollment.objects.filter(event=event, payment_status=True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{event.title}_students.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Student Name', 'Roll Number', 'Email',
        'Activity', 'Team Name', 'Razorpay Payment ID', 'Date Enrolled',
    ])

    for en in enrollments:
        writer.writerow([
            en.user.username,
            en.user.roll_number,
            en.user.email,
            en.activity.name if en.activity else "Entry Only",
            en.team_name or "N/A",
            en.razorpay_payment_id or "N/A",
            en.enrolled_at.strftime('%Y-%m-%d'),
        ])

    return response