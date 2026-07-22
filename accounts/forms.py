from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import User, TutorProfile
from .models import User, TutorProfile, StudentProfile


from tutoring.models import Programme

class StudentRegistrationForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    university = forms.CharField(max_length=255)

    programme = forms.ModelChoiceField(
        queryset=Programme.objects.all(),
        empty_label="Select your programme",
    )
    year_of_study = forms.IntegerField()

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password1',
            'password2',
        ]      
        
class TutorRegistrationForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)

    qualification = forms.CharField(max_length=255)
    years_of_experience = forms.IntegerField()
    hourly_rate = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password1',
            'password2',
        ]
        
class TutorProfileEditForm(forms.ModelForm):

    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = TutorProfile
        fields = ['biography', 'qualification', 'years_of_experience', 'hourly_rate']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(),
        }
        
        
        

class StudentProfileEditForm(forms.ModelForm):

    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = StudentProfile
        fields = ['university', 'programme', 'year_of_study']
        widgets = {
            'programme': forms.Select(),
        }
