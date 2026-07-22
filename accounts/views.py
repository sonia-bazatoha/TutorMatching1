from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta, date as date_type
import json

from .models import User, StudentProfile, TutorProfile
from .forms import (
    StudentRegistrationForm,
    TutorRegistrationForm,
    TutorProfileEditForm,
    StudentProfileEditForm,
)
from .utils import process_profile_picture

from tutoring.models import (
    Booking,
    Review,
    Subject,
    Availability,
    Programme,
    AcademicYear,
    Semester,
    Payment,
    Message,
    Complaint,
    ContactMessage,
)
from tutoring.forms import BookingForm, AvailabilityForm, ReviewForm, PaymentForm, ComplaintForm, ContactForm


# ─────────────────────────────────────────
# PUBLIC VIEWS
# ─────────────────────────────────────────

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == User.STUDENT:
                return redirect('student_dashboard')
            elif user.role == User.TUTOR:
                return redirect('tutor_dashboard')
            elif user.role == User.ADMIN:
                return redirect('/admin/')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.STUDENT
            user.save()
            StudentProfile.objects.create(
                user=user,
                university=form.cleaned_data['university'],
                programme=form.cleaned_data['programme'],
                year_of_study=form.cleaned_data['year_of_study'],
            )
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'student_register.html', {'form': form})


def tutor_register(request):
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.TUTOR
            user.phone_number = form.cleaned_data.get('phone_number', '')
            user.save()
            TutorProfile.objects.create(
                user=user,
                qualification=form.cleaned_data['qualification'],
                years_of_experience=form.cleaned_data['years_of_experience'],
                hourly_rate=form.cleaned_data['hourly_rate'],
                biography='',
            )
            messages.success(request, "Tutor account created successfully. Please log in.")
            return redirect('login')
    else:
        form = TutorRegistrationForm()
    return render(request, 'tutor_register.html', {'form': form})


def tutor_detail(request, tutor_id):
    tutor = get_object_or_404(TutorProfile, id=tutor_id)
    reviews = Review.objects.filter(tutor=tutor)
    availabilities = tutor.availabilities.all()
    subject_id = request.GET.get('subject', '')
    return render(request, 'tutor_detail.html', {
        'tutor': tutor,
        'reviews': reviews,
        'availabilities': availabilities,
        'subject_id': subject_id,
    })


@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.reporter = request.user
            complaint.save()
            messages.success(request, "Your complaint has been submitted. Our admin team will review it shortly.")
            return redirect('home')
    else:
        initial = {}
        if request.user.role == User.STUDENT:
            initial['role'] = 'student'
        elif request.user.role == User.TUTOR:
            initial['role'] = 'tutor'
        form = ComplaintForm(initial=initial)
    return render(request, 'complain.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us. We will get back to you shortly.")
            return redirect('contact')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['name'] = f"{request.user.first_name} {request.user.last_name}".strip()
            initial['email'] = request.user.email
        form = ContactForm(initial=initial)
    return render(request, 'contact.html', {'form': form})


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)


# ─────────────────────────────────────────
# STUDENT VIEWS
# ─────────────────────────────────────────

@login_required
def student_dashboard(request):
    if request.user.role != User.STUDENT:
        return redirect('home')

    from django.core.paginator import Paginator
    from django.utils import timezone

    profile = request.user.student_profile
    programme = profile.programme
    year_of_study = profile.year_of_study

    semesters = Semester.objects.all()
    selected_semester = request.GET.get('semester')
    selected_subject = request.GET.get('subject')

    subjects = Subject.objects.none()
    if selected_semester and programme:
        subjects = Subject.objects.filter(
            programme=programme,
            year__number=year_of_study,
            semester__number=selected_semester,
        )

    tutors = TutorProfile.objects.none()
    if selected_subject:
        try:
            selected_subject_obj = Subject.objects.get(id=selected_subject)
            matching_subject_ids = Subject.objects.filter(
                name=selected_subject_obj.name
            ).values_list('id', flat=True)
            tutors = TutorProfile.objects.select_related('user').prefetch_related('subjects').filter(
                subjects__id__in=matching_subject_ids
            ).distinct()
        except Subject.DoesNotExist:
            tutors = TutorProfile.objects.none()
    elif selected_semester and programme:
        all_subject_names = subjects.values_list('name', flat=True)
        matching_subject_ids = Subject.objects.filter(
            name__in=all_subject_names
        ).values_list('id', flat=True)
        tutors = TutorProfile.objects.select_related('user').prefetch_related('subjects').filter(
            subjects__id__in=matching_subject_ids
        ).distinct()

    all_bookings = Booking.objects.filter(student=profile).order_by('-booking_date', '-booking_time')
    today = timezone.now().date()
    pending_count = all_bookings.filter(status='Pending').count()

    upcoming_sessions = all_bookings.filter(
        status='Accepted',
        booking_date__gte=today,
    ).order_by('booking_date', 'booking_time')

    from django.core.paginator import Paginator
    paginator = Paginator(all_bookings, 5)
    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)

    for b in bookings:
        b.unread_count = (
            b.messages.filter(is_read=False).exclude(sender=request.user).count()
            if b.status == 'Accepted' else 0
        )

    return render(request, 'student_dashboard.html', {
        'profile': profile,
        'tutors': tutors,
        'bookings': bookings,
        'subjects': subjects,
        'semesters': semesters,
        'selected_semester': selected_semester,
        'selected_subject': selected_subject,
        'pending_count': pending_count,
        'upcoming_sessions': upcoming_sessions,
        'programme': programme,
        'year_of_study': year_of_study,
    })


@login_required
def edit_student_profile(request):
    if request.user.role != User.STUDENT:
        return redirect('home')

    student = request.user.student_profile

    if request.method == 'POST':
        form = StudentProfileEditForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            picture = request.FILES.get('profile_picture')
            if picture:
                request.user.profile_picture = process_profile_picture(picture)
                request.user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('edit_student_profile')
    else:
        form = StudentProfileEditForm(instance=student)

    return render(request, 'edit_student_profile.html', {'form': form})


@login_required
def create_booking(request, tutor_id):
    tutor = get_object_or_404(TutorProfile, id=tutor_id)
    student_profile = request.user.student_profile
    programme = student_profile.programme
    year_of_study = student_profile.year_of_study

    availabilities = Availability.objects.filter(tutor=tutor).order_by('day', 'start_time')

    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
    else:
        subject_id = request.GET.get('subject')

    subject = get_object_or_404(Subject, id=subject_id) if subject_id else None

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    smart_slots = []
    today = date_type.today()

    for availability in availabilities:
        day_name = availability.day
        day_index = day_order.index(day_name)
        days_ahead = (day_index - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        next_date = today + timedelta(days=days_ahead)

        dates_for_day = []
        for week in range(4):
            dates_for_day.append(next_date + timedelta(weeks=week))

        time_slots = []
        current = datetime.combine(today, availability.start_time)
        end = datetime.combine(today, availability.end_time)
        while current <= end:
            time_slots.append(current.strftime('%H:%M'))
            current += timedelta(minutes=30)

        smart_slots.append({
            'availability': availability,
            'dates': dates_for_day,
            'time_slots': time_slots,
        })

    if request.method == 'POST':
        if not subject:
            messages.error(request, "No subject selected.")
            return redirect('student_dashboard')

        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        learning_goal = request.POST.get('learning_goal', '').strip()
        duration = int(request.POST.get('duration', 60))

        try:
            parsed_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date.")
            return render(request, 'create_booking.html', {
                'tutor': tutor, 'subject': subject,
                'availabilities': availabilities,
                'smart_slots': smart_slots,
                'programme': programme,
                'year_of_study': year_of_study,
                'subject_id': subject_id,
            })

        if parsed_date < date_type.today():
            messages.error(request, "Booking date cannot be in the past.")
            return render(request, 'create_booking.html', {
                'tutor': tutor, 'subject': subject,
                'availabilities': availabilities,
                'smart_slots': smart_slots,
                'programme': programme,
                'year_of_study': year_of_study,
                'subject_id': subject_id,
            })

        # Prevent the same student from having more than one active
        # request for the same subject, regardless of which tutor.
        existing_active_booking = Booking.objects.filter(
            student=student_profile,
            subject=subject,
            status__in=['Pending', 'Accepted'],
        ).first()

        if existing_active_booking:
            messages.error(
                request,
                f"You already have a {existing_active_booking.status.lower()} request for "
                f"{subject.name} with {existing_active_booking.tutor.user.first_name}. "
                "Please wait for a response or cancel it before booking this subject again."
            )
            return render(request, 'create_booking.html', {
                'tutor': tutor, 'subject': subject,
                'availabilities': availabilities,
                'smart_slots': smart_slots,
                'programme': programme,
                'year_of_study': year_of_study,
                'subject_id': subject_id,
            })

        booking_day = parsed_date.strftime("%A")
        availability = Availability.objects.filter(
            tutor=tutor,
            day=booking_day,
            start_time__lte=booking_time,
            end_time__gte=booking_time,
        ).first()

        if not availability:
            messages.error(request, "This tutor is not available at the selected date and time.")
        else:
            new_start = datetime.combine(parsed_date, datetime.strptime(booking_time, '%H:%M').time())
            new_end = new_start + timedelta(minutes=duration)

            existing_bookings = Booking.objects.filter(
                tutor=tutor,
                booking_date=parsed_date,
                status__in=['Pending', 'Accepted'],
            ).exclude(student=student_profile)

            overlap = False
            for existing in existing_bookings:
                existing_start = datetime.combine(parsed_date, existing.booking_time)
                existing_end = existing_start + timedelta(minutes=existing.duration)
                if new_start < existing_end and new_end > existing_start:
                    overlap = True
                    break

            Booking.objects.create(
                student=student_profile,
                tutor=tutor,
                subject=subject,
                booking_date=parsed_date,
                booking_time=booking_time,
                learning_goal=learning_goal,
                duration=duration,
                status='Pending',
            )

            if overlap:
                messages.success(request, "Booking created. Note: the tutor has another session close to this time — they will confirm availability.")
            else:
                messages.success(request, "Booking created successfully.")

            return redirect('student_dashboard')

    return render(request, 'create_booking.html', {
        'tutor': tutor,
        'subject': subject,
        'availabilities': availabilities,
        'smart_slots': smart_slots,
        'programme': programme,
        'year_of_study': year_of_study,
        'subject_id': subject_id,
    })

@login_required
def create_review(request, tutor_id):
    tutor = get_object_or_404(TutorProfile, id=tutor_id)
    student = request.user.student_profile

    has_booking = Booking.objects.filter(
        student=student,
        tutor=tutor,
        status='Accepted'
    ).exists()

    if not has_booking:
        messages.error(request, "You can only review a tutor after an accepted session.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.student = student
            review.tutor = tutor
            review.save()
            messages.success(request, "Review submitted successfully.")
            return redirect('student_dashboard')
    else:
        form = ReviewForm()

    return render(request, 'create_review.html', {
        'form': form,
        'tutor': tutor,
    })


@login_required
def accept_proposed_time(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student__user=request.user)

    if booking.status != 'Declined' or not booking.proposed_date:
        messages.error(request, "No proposed time to accept.")
        return redirect('student_dashboard')

    booking.booking_date = booking.proposed_date
    booking.booking_time = booking.proposed_time
    booking.status = 'Pending'
    booking.cancellation_reason = ''
    booking.proposed_date = None
    booking.proposed_time = None
    booking.save()

    messages.success(request, "New time accepted. The tutor will confirm shortly.")
    return redirect('student_dashboard')


@login_required
def cancel_booking_student(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student__user=request.user)
    if booking.status in ['Pending', 'Accepted']:
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.error(request, "This booking cannot be cancelled.")
    return redirect('student_dashboard')


@login_required
def pay_booking(request, booking_id):
    if request.user.role != User.STUDENT:
        return redirect('home')

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        student__user=request.user,
        status='Accepted',
        is_paid=False,
    )

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()
            booking.is_paid = True
            booking.save()
            messages.success(request, "Payment recorded successfully. Your session is confirmed!")
            return redirect('student_dashboard')
    else:
        form = PaymentForm(initial={'amount': booking.tutor.hourly_rate})

    return render(request, 'payment.html', {
        'form': form,
        'booking': booking,
    })


@login_required
def delete_booking(request, booking_id):
    if request.user.role == User.STUDENT:
        booking = get_object_or_404(Booking, id=booking_id, student__user=request.user)
        booking.delete()
        messages.success(request, "Booking removed successfully.")
        return redirect('student_dashboard')
    elif request.user.role == User.TUTOR:
        booking = get_object_or_404(Booking, id=booking_id, tutor__user=request.user)
        if booking.status in ['Cancelled', 'Declined']:
            booking.delete()
            messages.success(request, "Booking removed successfully.")
        return redirect('tutor_dashboard')
    return redirect('home')


# ─────────────────────────────────────────
# TUTOR VIEWS
# ─────────────────────────────────────────

@login_required
def tutor_dashboard(request):
    if request.user.role != User.TUTOR:
        return redirect('home')

    from django.core.paginator import Paginator

    profile = request.user.tutor_profile
    all_bookings = Booking.objects.filter(tutor=profile).order_by('-booking_date', '-booking_time')

    # Detect overlapping bookings using duration
    overlapping_ids = set()
    pending_bookings_list = list(all_bookings.filter(status='Pending'))

    for i, b1 in enumerate(pending_bookings_list):
        b1_start = datetime.combine(b1.booking_date, b1.booking_time)
        b1_end = b1_start + timedelta(minutes=b1.duration)
        for b2 in pending_bookings_list[i + 1:]:
            if b1.booking_date == b2.booking_date:
                b2_start = datetime.combine(b2.booking_date, b2.booking_time)
                b2_end = b2_start + timedelta(minutes=b2.duration)
                if b1_start < b2_end and b1_end > b2_start:
                    overlapping_ids.add(b1.id)
                    overlapping_ids.add(b2.id)

    total_bookings = all_bookings.count()
    pending_bookings = all_bookings.filter(status='Pending').count()
    accepted_bookings = all_bookings.filter(status='Accepted').count()
    completed_bookings = all_bookings.filter(status='Completed').count()
    availability_count = Availability.objects.filter(tutor=profile).count()

    pending_requests = list(all_bookings.filter(status='Pending'))

    for b in pending_requests:
        b_start = datetime.combine(b.booking_date, b.booking_time)
        b_end = b_start + timedelta(minutes=b.duration)
        overlap_count = 0
        for other in pending_requests:
            if other.id == b.id:
                continue
            if other.booking_date != b.booking_date:
                continue
            other_start = datetime.combine(other.booking_date, other.booking_time)
            other_end = other_start + timedelta(minutes=other.duration)
            if b_start < other_end and b_end > other_start:
                overlap_count += 1
        b.same_slot_count = overlap_count + 1 if overlap_count > 0 else 1

    tutor_faculties = sorted({
        s.programme.faculty for s in profile.subjects.all()
    })

    reviews = Review.objects.filter(tutor=profile)
    average_rating = round(
        sum(r.rating for r in reviews) / reviews.count(), 1
    ) if reviews.exists() else 0

    paginator = Paginator(all_bookings, 5)
    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)

    for b in bookings:
        b.unread_count = (
            b.messages.filter(is_read=False).exclude(sender=request.user).count()
            if b.status == 'Accepted' else 0
        )

    return render(request, 'tutor_dashboard.html', {
        'profile': profile,
        'bookings': bookings,
        'pending_requests': pending_requests,
        'tutor_faculties': tutor_faculties,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'accepted_bookings': accepted_bookings,
        'completed_bookings': completed_bookings,
        'availability_count': availability_count,
        'average_rating': average_rating,
        'overlapping_ids': overlapping_ids,
    })


@login_required
def edit_tutor_profile(request):
    if request.user.role != User.TUTOR:
        return redirect('home')

    tutor = request.user.tutor_profile

    if request.method == 'POST':
        form = TutorProfileEditForm(request.POST, request.FILES, instance=tutor)
        availability_form = AvailabilityForm(request.POST)

        if 'save_profile' in request.POST and form.is_valid():
            form.save()
            picture = request.FILES.get('profile_picture')
            if picture:
                request.user.profile_picture = process_profile_picture(picture)
                request.user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('edit_tutor_profile')

        if 'add_availability' in request.POST and availability_form.is_valid():
            availability = availability_form.save(commit=False)
            availability.tutor = tutor
            availability.save()
            messages.success(request, "Availability added successfully.")
            return redirect('edit_tutor_profile')

        if 'save_subjects' in request.POST:
            subject_ids = request.POST.getlist('subject_ids')
            if subject_ids:
                current_count = tutor.subjects.count()
                new_subjects = Subject.objects.filter(id__in=subject_ids)
                slots_remaining = 10 - current_count
                if slots_remaining <= 0:
                    messages.error(request, "You have reached the maximum of 10 subjects. Remove some before adding new ones.")
                else:
                    subjects_to_add = new_subjects[:slots_remaining]
                    tutor.subjects.add(*subjects_to_add)
                    if len(subject_ids) > slots_remaining:
                        messages.error(request, f"Only {slots_remaining} slot(s) remaining. Added {slots_remaining} subject(s) — remove some to add more.")
                    else:
                        messages.success(request, f"{subjects_to_add.count()} subject(s) added. {10 - tutor.subjects.count()} slot(s) remaining.")
            return redirect('edit_tutor_profile')

    else:
        form = TutorProfileEditForm(instance=tutor)
        availability_form = AvailabilityForm()

    availabilities = Availability.objects.filter(tutor=tutor)
    programmes = Programme.objects.all()
    years = AcademicYear.objects.all()
    semesters = Semester.objects.all()
    saved_subject_ids = list(tutor.subjects.values_list('id', flat=True))
    subject_count = tutor.subjects.count()
    slots_remaining = 10 - subject_count

    return render(request, 'edit_tutor_profile.html', {
        'form': form,
        'availability_form': availability_form,
        'availabilities': availabilities,
        'tutor': tutor,
        'programmes': programmes,
        'years': years,
        'semesters': semesters,
        'saved_subject_ids_json': json.dumps(saved_subject_ids),
        'subject_count': subject_count,
        'slots_remaining': slots_remaining,
    })


def _availability_has_upcoming_bookings(tutor, availability):
    candidates = Booking.objects.filter(
        tutor=tutor,
        booking_date__gte=date_type.today(),
        booking_time__gte=availability.start_time,
        booking_time__lte=availability.end_time,
        status__in=['Pending', 'Accepted'],
    )
    return any(
        b.booking_date.strftime('%A') == availability.day
        for b in candidates
    )


@login_required
def manage_availability(request):
    if request.user.role != User.TUTOR:
        return redirect('home')

    tutor = request.user.tutor_profile

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.tutor = tutor
            availability.save()
            return redirect('manage_availability')
    else:
        form = AvailabilityForm()

    availabilities = Availability.objects.filter(tutor=tutor)
    return render(request, 'manage_availability.html', {
        'form': form,
        'availabilities': availabilities,
    })


@login_required
def delete_availability(request, availability_id):
    if request.user.role != User.TUTOR:
        return redirect('home')

    tutor = request.user.tutor_profile
    availability = get_object_or_404(Availability, id=availability_id, tutor=tutor)

    if _availability_has_upcoming_bookings(tutor, availability):
        messages.error(request, "This slot has an upcoming booking and can't be deleted.")
    else:
        availability.delete()
        messages.success(request, "Availability slot removed.")

    return redirect('edit_tutor_profile')


@login_required
def cancel_booking_tutor(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, tutor__user=request.user)
    if booking.status == 'Accepted':
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, "Session cancelled successfully.")
    else:
        messages.error(request, "Only accepted sessions can be cancelled.")
    return redirect('tutor_dashboard')


@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, tutor__user=request.user)
    booking.status = 'Accepted'
    booking.save()
    messages.success(request, "Booking accepted successfully.")
    return redirect('tutor_dashboard')


@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, tutor__user=request.user)

    if request.method == 'POST':
        cancellation_reason = request.POST.get('cancellation_reason', '').strip()
        proposed_date = request.POST.get('proposed_date', '').strip()
        proposed_time = request.POST.get('proposed_time', '').strip()

        booking.status = 'Declined'
        booking.cancellation_reason = cancellation_reason

        if proposed_date:
            booking.proposed_date = datetime.strptime(proposed_date, '%Y-%m-%d').date()
        if proposed_time:
            booking.proposed_time = proposed_time

        booking.save()
        messages.success(request, "Booking declined and student has been notified.")
        return redirect('tutor_dashboard')

    return render(request, 'decline_booking.html', {'booking': booking})


# ─────────────────────────────────────────
# API VIEWS
# ─────────────────────────────────────────

@login_required
def subject_filter_api(request):
    programme_id = request.GET.get('programme', '').strip()
    year_number = request.GET.get('year', '').strip()
    semester_number = request.GET.get('semester', '').strip()

    if not programme_id or not year_number or not semester_number:
        return JsonResponse({'subjects': []})

    subjects = Subject.objects.filter(
        programme__id=programme_id,
        year__number=year_number,
        semester__number=semester_number,
    ).values('id', 'name', 'code')

    return JsonResponse({'subjects': list(subjects)})


@login_required
def booking_chat(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    is_student = request.user == booking.student.user
    is_tutor = request.user == booking.tutor.user
    if not (is_student or is_tutor):
        messages.error(request, "You don't have access to this chat.")
        return redirect('home')

    if booking.status != 'Accepted':
        messages.error(request, "Chat is only available for accepted bookings.")
        if request.user.role == User.STUDENT:
            return redirect('student_dashboard')
        return redirect('tutor_dashboard')

    booking.messages.exclude(sender=request.user).update(is_read=True)
    return render(request, 'booking_chat.html', {'booking': booking})


@login_required
def booking_chat_api(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    is_student = request.user == booking.student.user
    is_tutor = request.user == booking.tutor.user
    if not (is_student or is_tutor):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if booking.status != 'Accepted':
        return JsonResponse({'error': 'Chat is not available yet.'}, status=403)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(booking=booking, sender=request.user, text=text)
        return JsonResponse({'ok': True})

    chat_messages = booking.messages.all()
    data = [
        {    
         
            'id': m.id,
            'sender': m.sender.first_name or m.sender.username,
            'is_me': m.sender_id == request.user.id,
            'text': m.text,
            'timestamp': m.timestamp.strftime('%b %d, %H:%M'),
        }
        for m in chat_messages
    ]
    return JsonResponse({'messages': data})


@login_required
def delete_message(request, message_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    message = get_object_or_404(Message, id=message_id)
    booking = message.booking

    is_student = request.user == booking.student.user
    is_tutor = request.user == booking.tutor.user
    if not (is_student or is_tutor):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    if message.sender_id != request.user.id:
        return JsonResponse({'error': 'You can only delete your own messages.'}, status=403)

    if booking.status != 'Accepted':
        return JsonResponse({'error': 'Chat is not available.'}, status=403)

    message.delete()
    return JsonResponse({'ok': True})


@login_required
def remove_subject(request, subject_id):
    if request.user.role != User.TUTOR:
        return redirect('home')

    tutor = request.user.tutor_profile
    subject = get_object_or_404(Subject, id=subject_id)
    tutor.subjects.remove(subject)
    messages.success(request, f'"{subject.name}" removed from your subjects.')
    return redirect('edit_tutor_profile')


@login_required
def tutor_search_api(request):
    if request.user.role != User.STUDENT:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    profile = request.user.student_profile
    programme = profile.programme
    year_of_study = profile.year_of_study

    query = request.GET.get('q', '').strip()
    subject_id = request.GET.get('subject', '').strip()
    semester_number = request.GET.get('semester', '').strip()

    tutors = TutorProfile.objects.select_related('user').prefetch_related('subjects')

    if subject_id:
        try:
            selected_subject_obj = Subject.objects.get(id=subject_id)
            matching_subject_ids = Subject.objects.filter(
                name=selected_subject_obj.name
            ).values_list('id', flat=True)
            tutors = tutors.filter(subjects__id__in=matching_subject_ids)
        except Subject.DoesNotExist:
            return JsonResponse({'tutors': []})
    elif semester_number and programme:
        semester_subjects = Subject.objects.filter(
            programme=programme,
            year__number=year_of_study,
            semester__number=semester_number,
        )
        all_subject_names = semester_subjects.values_list('name', flat=True)
        matching_subject_ids = Subject.objects.filter(
            name__in=all_subject_names
        ).values_list('id', flat=True)
        tutors = tutors.filter(subjects__id__in=matching_subject_ids)
    else:
        return JsonResponse({'tutors': []})

    if query:
        tutors = (
            tutors.filter(user__first_name__icontains=query) |
            tutors.filter(user__last_name__icontains=query)
        )

    tutors = tutors.distinct()

    data = [{
        'id': t.id,
        'name': f"{t.user.first_name} {t.user.last_name}",
        'qualification': t.qualification,
        'years_of_experience': t.years_of_experience,
        'hourly_rate': str(t.hourly_rate),
        'subjects': [s.name for s in t.subjects.all()],
        'profile_picture': t.user.profile_picture.url if t.user.profile_picture else None,
    } for t in tutors]

    return JsonResponse({'tutors': data})