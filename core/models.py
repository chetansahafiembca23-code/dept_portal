from django.db import models


class MonthlyNewspaper(models.Model):
    title = models.CharField(max_length=100)
    month_year = models.DateField(help_text="Select any day in the month")
    pdf_file = models.FileField(upload_to='newspapers/')
    cover_image = models.ImageField(upload_to='newspaper_covers/', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.month_year.strftime('%B %Y')}"


class Achievement(models.Model):
    student_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/')
    date_awarded = models.DateField()

    def __str__(self):
        return self.student_name


class SliderImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sliders/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100) # e.g., HOD, Assistant Professor
    image = models.ImageField(upload_to='faculty/')
    department = models.CharField(max_length=50, choices=[('BCA', 'BCA'), ('MCA', 'MCA')])
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return self.name