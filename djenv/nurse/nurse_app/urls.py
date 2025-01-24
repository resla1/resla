from django.urls import path
from . import views

urlpatterns = [
    # User Management URLs
   path('',views.home,name='home'),
  path('register',views.register,name="register"),
  path('login',views.login_view,name='login'),
  path('addnurse',views.add_nurse,name='addnurse'),
  path('patientprofile',views.patient_profile,name="patientprofile"),
  path('servicerequest',views.add_service_request,name="servicerequest"),
  path('patientservice',views.view_service_requests,name='patientservice'),
  path('adminservicerequest',views.admin_service_requests,name="adminservicerequest"),
  path('update-service-request-status/<int:request_id>/', views.update_service_request_status, name='update_service_request_status'),
  path('assignnurse/<int:request_id>/',views.assign_nurse,name="assignnurse"),
  path('nursepatient',views.nurse_patient_view,name="nursepatient"),
  path('contact',views.contact,name="contact"),
  path('service',views.service,name="service"),
  path('about',views.about,name="about"),
  path('nurses',views.nurse,name="nurse"),
  path("adminhome",views.adminhome,name="adminhome"),
  path("nursehome",views.nursehome,name="nursehome"),
  path("patienthome",views.patienthome,name="patienthome"),
  path('logout',views.logout_view,name="logout"),

]