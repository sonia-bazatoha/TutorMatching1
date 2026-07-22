from django.db import models
from accounts.models import TutorProfile, StudentProfile


class Programme(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255, default="Faculty of Science and Technology")
    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    number = models.PositiveIntegerField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Year {self.number}"


class Semester(models.Model):
    number = models.PositiveIntegerField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Semester {self.number}"


class Subject(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    programme = models.ForeignKey(
        Programme,
        on_delete=models.CASCADE,
        related_name='subjects',
    )
    year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='subjects',
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='subjects',
    )

    class Meta:
        unique_together = ('code', 'programme', 'year', 'semester')
        ordering = ['year', 'semester', 'name']

    def __str__(self):
        return f"{self.name} ({self.programme.code} Y{self.year.number} S{self.semester.number})"


class Availability(models.Model):
    DAYS = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    tutor = models.ForeignKey(
        TutorProfile,
        on_delete=models.CASCADE,
        related_name="availabilities",
    )
    day = models.CharField(max_length=20, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.tutor.user.username} - {self.day}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Declined", "Declined"),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    tutor = models.ForeignKey(
        TutorProfile,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
    )
    booking_date = models.DateField()
    booking_time = models.TimeField()
    
    DURATION_CHOICES = [
    (30, '30 minutes'),
    (60, '1 hour'),
    (90, '1.5 hours'),
    (120, '2 hours'),
  ]

    duration = models.PositiveIntegerField(
    choices=DURATION_CHOICES,
    default=60,
)
    learning_goal = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )
    cancellation_reason = models.TextField(blank=True)
    proposed_date = models.DateField(null=True, blank=True)
    proposed_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} -> {self.tutor.user.username}"   
    
class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('Visa', 'Visa'),
        ('Mastercard', 'Mastercard'),
        ('Mobile Money', 'Mobile Money'),
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    CURRENCY_CHOICES = [
        ('UGX', 'UGX — Ugandan Shilling'),
        ('USD', 'USD — US Dollar'),
        ('EUR', 'EUR — Euro'),
        ('GBP', 'GBP — British Pound'),
        ('KES', 'KES — Kenyan Shilling'),
        ('TZS', 'TZS — Tanzanian Shilling'),
    ]

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment',
    )
    method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='UGX',
    )
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id} via {self.method}"
        
class Message(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} on booking {self.booking.id}"


class Review(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
    )
    tutor = models.ForeignKey(
        TutorProfile,
        on_delete=models.CASCADE,
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.rating}"
    
    
class Complaint(models.Model):

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('tutor', 'Tutor'),
    ]

    REPORT_TYPE_CHOICES = [
        ('tutor', 'A Tutor'),
        ('student', 'A Student'),
        ('platform', 'Platform Issue'),
    ]

    REASON_CHOICES = [
        ('bad_behavior', 'Bad Behaviour'),
        ('spam', 'Spam'),
        ('fake_account', 'Fake Account'),
        ('inappropriate_content', 'Inappropriate Content'),
        ('other', 'Other'),
    ]

    reporter = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='complaints_made',
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    target_user = models.CharField(max_length=100, blank=True)
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Complaint by {self.reporter.username} — {self.reason}"
    
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} — {self.subject}"