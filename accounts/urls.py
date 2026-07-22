from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('register/student/', views.student_register, name='student_register'),
    path('register/tutor/', views.tutor_register, name='tutor_register'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('tutor/dashboard/', views.tutor_dashboard, name='tutor_dashboard'),

    path('tutor/availability/', views.manage_availability, name='manage_availability'),
    path('tutor/profile/edit/', views.edit_tutor_profile, name='edit_tutor_profile'),

    # API URLs must come before tutor/<int:tutor_id>/ to avoid conflict
    path('api/tutors/', views.tutor_search_api, name='tutor_search_api'),
    path('api/subjects/filter/', views.subject_filter_api, name='subject_filter_api'),

    # This must come after all tutor/ fixed paths
    path('tutor/<int:tutor_id>/', views.tutor_detail, name='tutor_detail'),

    path('book/<int:tutor_id>/', views.create_booking, name='create_booking'),

    path('booking/<int:booking_id>/accept/', views.accept_booking, name='accept_booking'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),

    path('review/<int:tutor_id>/', views.create_review, name='create_review'),

    path('student/profile/edit/', views.edit_student_profile, name='edit_student_profile'),
    path('tutor/subjects/remove/<int:subject_id>/', views.remove_subject, name='remove_subject'),
    
    path('booking/<int:booking_id>/cancel/student/', views.cancel_booking_student, name='cancel_booking_student'),
    path('booking/<int:booking_id>/cancel/tutor/', views.cancel_booking_tutor, name='cancel_booking_tutor'),
    path('booking/<int:booking_id>/delete/', views.delete_booking, name='delete_booking'),
    path('booking/<int:booking_id>/pay/', views.pay_booking, name='pay_booking'),
    path('booking/<int:booking_id>/chat/', views.booking_chat, name='booking_chat'),
    path('api/booking/<int:booking_id>/chat/', views.booking_chat_api, name='booking_chat_api'),
    path('complaint/', views.submit_complaint, name='submit_complaint'),
    path('contact/', views.contact, name='contact'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    path('booking/<int:booking_id>/accept-proposed/', views.accept_proposed_time, name='accept_proposed_time'),
    path('availability/<int:availability_id>/delete/', views.delete_availability, name='delete_availability'),
    path('chat/message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
]