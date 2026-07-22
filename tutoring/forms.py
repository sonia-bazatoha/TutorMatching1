from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import Booking, Review, Availability,Complaint, ContactMessage



class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'subject',
            'booking_date',
            'booking_time',
        ]

        widgets = {
            'booking_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'booking_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
        }

    def clean_booking_date(self):

        booking_date = self.cleaned_data['booking_date']

        if booking_date < date.today():
            raise ValidationError(
                "Booking date cannot be in the past."
            )

        return booking_date
    
class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            'rating',
            'comment',
        ]
        
        
class AvailabilityForm(forms.ModelForm):

    class Meta:
        model = Availability

        fields = [
            'day',
            'start_time',
            'end_time',
        ]

        widgets = {
            'start_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),

            'end_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
        }
        
        
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method', 'currency', 'amount']
        widgets = {
            'method': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['role', 'report_type', 'target_user', 'reason', 'description']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'target_user': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the name or ID of the user being reported'
            }),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Explain the issue in as much detail as possible. Include dates, times, and what happened…',
                'style': 'min-height:160px;'
            }),
        }
        


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What is this about?'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message here…',
                'style': 'min-height:160px;'
            }),
        }