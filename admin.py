from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FamilyMember, ContributionType, Payment, Meeting, Attendance, Notice
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Family permissions', {'fields':('role','approved','phone')}),)
    list_display = ('username','first_name','last_name','role','approved','is_staff')
@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display=('member_code','full_name','phone')
    search_fields=('member_code','full_name','phone')
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=('member','contribution_type','amount','paid_at','method','verified')
    list_filter=('verified','method','contribution_type')
    search_fields=('member__full_name','transaction_ref')
admin.site.register(ContributionType)
admin.site.register(Meeting)
admin.site.register(Attendance)
admin.site.register(Notice)
