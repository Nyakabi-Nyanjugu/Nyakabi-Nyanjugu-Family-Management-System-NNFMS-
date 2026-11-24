from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, FamilyMember, Payment, Meeting, Notice
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Jina la kwanza')
    last_name = forms.CharField(label='Jina la mwisho')
    phone = forms.CharField(label='Namba ya simu')
    class Meta:
        model = User
        fields = ('username','first_name','last_name','phone')
class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        exclude = ('user',)
        widgets = {'date_of_birth': forms.DateInput(attrs={'type':'date'}), 'consent_to_store': forms.CheckboxInput()}
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('member','contribution_type','amount','method','transaction_ref','notes')
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ('title','meeting_date','venue','agenda')
        widgets = {'meeting_date': forms.DateTimeInput(attrs={'type':'datetime-local'})}
class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title','message','active')
