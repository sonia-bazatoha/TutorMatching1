from django.contrib import admin
from .models import Programme, AcademicYear, Semester, Subject, Availability, Booking, Review,Complaint, ContactMessage

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['number']

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['number']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'programme', 'year', 'semester']
    list_filter = ['programme', 'year', 'semester']
    search_fields = ['name', 'code']
    
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'role', 'report_type', 'reason', 'submitted_at', 'is_resolved']
    list_filter = ['role', 'report_type', 'reason', 'is_resolved']
    search_fields = ['reporter__username', 'target_user', 'description']
    list_editable = ['is_resolved']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at', 'is_read']
    list_filter = ['is_read']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']

admin.site.register(Availability)
admin.site.register(Booking)
admin.site.register(Review)