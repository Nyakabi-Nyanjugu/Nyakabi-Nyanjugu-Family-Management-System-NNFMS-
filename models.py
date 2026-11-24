from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [('ADMIN','Super Administrator'),('CHAIR','Chairperson'),('SECRETARY','Secretary'),('TREASURER','Treasurer'),('MEMBER','Family Member')]
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default='MEMBER')
    approved = models.BooleanField(default=False)
    phone = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username

class FamilyMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='family_profile')
    member_code = models.CharField(max_length=24, unique=True)
    full_name = models.CharField(max_length=180)
    sex = models.CharField(max_length=10, choices=[('MALE','Mwanaume'),('FEMALE','Mwanamke'),('OTHER','Nyingine')], blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    residence = models.CharField(max_length=180, blank=True)
    father_name = models.CharField(max_length=180, blank=True)
    mother_name = models.CharField(max_length=180, blank=True)
    grandfather_name = models.CharField(max_length=180, blank=True)
    grandmother_name = models.CharField(max_length=180, blank=True)
    father = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children_as_father')
    mother = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children_as_mother')
    photo = models.ImageField(upload_to='family_photos/', blank=True)
    consent_to_store = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.full_name} ({self.member_code})'

class ContributionType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    def __str__(self): return self.name

class Payment(models.Model):
    METHOD = [('CASH','Cash'),('MPESA','M-Pesa'),('MIXX','Mixx by Yas'),('AIRTEL','Airtel Money'),('BANK','Bank'),('OTHER','Other')]
    member = models.ForeignKey(FamilyMember, on_delete=models.PROTECT, related_name='payments')
    contribution_type = models.ForeignKey(ContributionType, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=10, choices=METHOD)
    transaction_ref = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)
    recorded_by = models.ForeignKey(User, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.member.full_name} - {self.amount}'

class Meeting(models.Model):
    title = models.CharField(max_length=180)
    meeting_date = models.DateTimeField()
    venue = models.CharField(max_length=180, blank=True)
    agenda = models.TextField(blank=True)
    minutes = models.TextField(blank=True)
    resolutions = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self): return self.title

class Attendance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendances')
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    class Meta: unique_together = [('meeting','member')]

class Notice(models.Model):
    title = models.CharField(max_length=180)
    message = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    def __str__(self): return self.title
