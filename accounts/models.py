from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    
    STUDENT = 'student'
    TUTOR = 'tutor'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TUTOR, 'Tutor'),
        (ADMIN, 'Admin'),

    ]

     
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT,)
    
    phone_number = models.CharField(max_length=20, blank=True, null=True,)
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return self.username
    
    
    
class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    university = models.CharField(max_length=255)

    programme = models.ForeignKey(
        'tutoring.Programme',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
    )

    year_of_study = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - Student Profile"
    
class TutorProfile(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="tutor_profile",
        
    )
    
    biography = models.TextField()
    
    qualification = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField(default=0)
    
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    
    subjects = models.ManyToManyField(
        "tutoring.Subject",
        related_name = "tutors",
        
    )
    
    def __str__(self):
        return f"{self.user.username} - Tutor Profile"
    
    