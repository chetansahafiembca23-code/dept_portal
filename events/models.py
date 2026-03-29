from django.db import models
from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('solo', 'Solo'),
        ('group', 'Group'),
        ('volunteer', 'Volunteer'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=ACTIVITY_TYPES, default='solo')
    description = models.TextField(blank=True)
    max_participants = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.event.title})"


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)

    # Activity details
    team_name = models.CharField(max_length=100, blank=True, null=True)
    participants_list = models.TextField(help_text="Names of group members", blank=True)

    # Payment tracking
    payment_status = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True)

    # Razorpay fields
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class EventGallery(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='event_gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.event.title}"