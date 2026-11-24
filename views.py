from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import User, FamilyMember, Payment, Meeting, Notice
from .forms import RegisterForm, FamilyMemberForm, PaymentForm, MeetingForm, NoticeForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False); user.approved = False; user.role = 'MEMBER'; user.save()
            messages.success(request, 'Ombi lako la usajili limepokelewa. Litasubiri uthibitisho wa uongozi.')
            return redirect('login')
    else: form = RegisterForm()
    return render(request,'family/form.html',{'form':form,'title':'Jisajili'})
class ApprovedLoginView(LoginView):
    template_name = 'family/login.html'
    def form_valid(self, form):
        if not form.get_user().is_superuser and not form.get_user().approved:
            form.add_error(None, 'Akaunti yako bado haijaidhinishwa na uongozi.')
            return self.form_invalid(form)
        return super().form_valid(form)

def approved_required(view):
    from django.contrib.auth.decorators import user_passes_test
    return login_required(user_passes_test(lambda u: u.is_superuser or u.approved)(view))

@login_required
def dashboard(request):
    if not request.user.is_superuser and not request.user.approved:
        return render(request,'family/pending.html')
    context = {
      'members': FamilyMember.objects.count(),
      'payments_total': Payment.objects.filter(verified=True).aggregate(s=Sum('amount'))['s'] or 0,
      'unverified': Payment.objects.filter(verified=False).count(),
      'meetings': Meeting.objects.filter(meeting_date__gte=timezone.now()).count(),
      'notices': Notice.objects.filter(active=True).order_by('-published_at')[:5],
      'recent_payments': Payment.objects.select_related('member','contribution_type').order_by('-paid_at')[:5],
    }
    return render(request,'family/dashboard.html',context)

@login_required
def members(request):
    if not request.user.is_superuser and not request.user.approved: return render(request,'family/pending.html')
    qs = FamilyMember.objects.all().order_by('full_name')
    return render(request,'family/members.html',{'members':qs,'can_manage':request.user.is_superuser or request.user.role in ['ADMIN','CHAIR','SECRETARY']})

@login_required
def add_member(request):
    if not (request.user.is_superuser or request.user.role in ['ADMIN','CHAIR','SECRETARY']): return redirect('members')
    form = FamilyMemberForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(); messages.success(request,'Mwanaukoo amesajiliwa.'); return redirect('members')
    return render(request,'family/form.html',{'form':form,'title':'Sajili mwanaukoo'})

@login_required
def payments(request):
    if not request.user.is_superuser and not request.user.approved: return render(request,'family/pending.html')
    qs = Payment.objects.select_related('member','contribution_type').order_by('-paid_at')
    if request.user.role == 'MEMBER' and not request.user.is_superuser:
        qs = qs.filter(member__user=request.user)
    return render(request,'family/payments.html',{'payments':qs,'can_manage':request.user.is_superuser or request.user.role in ['ADMIN','TREASURER']})

@login_required
def add_payment(request):
    if not (request.user.is_superuser or request.user.role in ['ADMIN','TREASURER']): return redirect('payments')
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False); obj.recorded_by=request.user; obj.save()
        messages.success(request,'Malipo yamehifadhiwa na yanasubiri uthibitisho.'); return redirect('payments')
    return render(request,'family/form.html',{'form':form,'title':'Rekodi malipo'})

@login_required
def verify_payment(request, pk):
    if not (request.user.is_superuser or request.user.role in ['ADMIN','TREASURER']): return redirect('payments')
    p=get_object_or_404(Payment,pk=pk); p.verified=True; p.save(update_fields=['verified']); messages.success(request,'Malipo yamethibitishwa.')
    return redirect('payments')

@login_required
def meetings(request):
    if not request.user.is_superuser and not request.user.approved: return render(request,'family/pending.html')
    return render(request,'family/meetings.html',{'meetings':Meeting.objects.order_by('-meeting_date'),'can_manage':request.user.is_superuser or request.user.role in ['ADMIN','CHAIR','SECRETARY']})

@login_required
def add_meeting(request):
    if not (request.user.is_superuser or request.user.role in ['ADMIN','CHAIR','SECRETARY']): return redirect('meetings')
    form=MeetingForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False); obj.created_by=request.user; obj.save(); messages.success(request,'Kikao kimehifadhiwa.'); return redirect('meetings')
    return render(request,'family/form.html',{'form':form,'title':'Panga kikao'})

@login_required
def notices(request):
    if not request.user.is_superuser and not request.user.approved: return render(request,'family/pending.html')
    return render(request,'family/notices.html',{'notices':Notice.objects.filter(active=True).order_by('-published_at'),'can_manage':request.user.is_superuser or request.user.role in ['ADMIN','CHAIR','SECRETARY']})

@login_required
def add_notice(request):
    if not (request.user.is_superuser or request.user.role in ['ADMIN','CHAIR','SECRETARY']): return redirect('notices')
    form=NoticeForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False); obj.created_by=request.user; obj.save(); messages.success(request,'Tangazo limechapishwa.'); return redirect('notices')
    return render(request,'family/form.html',{'form':form,'title':'Tengeneza tangazo'})
