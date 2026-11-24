from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
urlpatterns = [
 path('',views.dashboard,name='dashboard'), path('register/',views.register,name='register'),
 path('login/',views.ApprovedLoginView.as_view(),name='login'), path('logout/',LogoutView.as_view(),name='logout'),
 path('members/',views.members,name='members'), path('members/add/',views.add_member,name='add_member'),
 path('payments/',views.payments,name='payments'), path('payments/add/',views.add_payment,name='add_payment'),
 path('payments/<int:pk>/verify/',views.verify_payment,name='verify_payment'),
 path('meetings/',views.meetings,name='meetings'), path('meetings/add/',views.add_meeting,name='add_meeting'),
 path('notices/',views.notices,name='notices'), path('notices/add/',views.add_notice,name='add_notice'),
]
