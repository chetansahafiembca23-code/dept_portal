from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from events.models import Event, Enrollment, EventGallery
from .models import Faculty, MonthlyNewspaper, Achievement, SliderImage

User = get_user_model()

# ── Helper ────────────────────────────────────────────────────────────────────
def is_admin(user):
    """Check if the user is an admin or superuser."""
    return user.is_superuser or (hasattr(user, 'role') and user.role == 'admin')

# ── Public views ──────────────────────────────────────────────────────────────
def home(request):
    """Public home page with sliders, events, faculty, achievements, newsletters, and next event countdown."""
    next_event = Event.objects.filter(date__gte=timezone.now()).order_by('date').first()  # Closest upcoming event

    context = {
        'next_event':    next_event,  # For countdown timer
        'sliders':       SliderImage.objects.filter(is_active=True),
        'events':        Event.objects.all().order_by('date')[:3],  # Latest 3 events
        'faculty':       Faculty.objects.all(),  # All faculty members
        'achievements':  Achievement.objects.all().order_by('-date_awarded')[:5],  # Latest 5 achievements
        'newsletters':   MonthlyNewspaper.objects.all().order_by('-uploaded_at')[:3],  # Latest 3 newsletters
    }
    return render(request, 'core/home.html', context)

def community_updates(request):
    """Community updates page with newsletters and achievements."""
    context = {
        'newspapers':   MonthlyNewspaper.objects.all().order_by('-uploaded_at'),
        'achievements': Achievement.objects.all().order_by('-date_awarded'),
    }
    return render(request, 'core/community.html', context)

def common_gallery(request):
    """Gallery page with all event photos."""
    context = {
        'photos': EventGallery.objects.all().order_by('-id'),
    }
    return render(request, 'core/gallery.html', context)

# ── Student dashboard ─────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    """Student dashboard with enrollments and latest newsletter."""
    context = {
        'enrollments':      Enrollment.objects.filter(
                                user=request.user,
                                payment_status=True
                            ).select_related('event').order_by('-enrolled_at'),
        'latest_newspaper': MonthlyNewspaper.objects.order_by('-uploaded_at').first(),
    }
    return render(request, 'core/dashboard.html', context)

# ── Admin dashboard ───────────────────────────────────────────────────────────
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with stats, revenue, enrollments, and events."""
    paid_enrollments = Enrollment.objects.filter(payment_status=True)

    context = {
        'total_students':     User.objects.filter(role='student').count(),
        'total_events':       Event.objects.count(),
        'total_revenue':      paid_enrollments.aggregate(Sum('event__fee'))['event__fee__sum'] or 0,
        'recent_enrollments': paid_enrollments.select_related('user', 'event').order_by('-enrolled_at')[:10],
        'upcoming_events':    Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5],  # Only upcoming
    }
    return render(request, 'admin/admin_dashboard.html', context)