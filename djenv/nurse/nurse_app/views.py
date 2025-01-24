
# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import logout


def home(request):
    return render(request,"home.html")
def logout_view(request):
    logout(request)
    return redirect(home)

def register(request):
    if request.method=="POST":
        name=request.POST.get("name")
        mob=request.POST.get("mob")
        email=request.POST.get("email")
        password=request.POST.get("password")
        obj=reg_tbl.objects.create(fname=name,mob=mob,email=email,password=password)
        obj.save()
        if obj:
            msg="successfully registered"
            return render(request,"login.html")
        else:
            return render(request,"register.html")
    return render(request,"register.html")

def login_view(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        obj=reg_tbl.objects.filter(email=email,password=password)
        if obj:
            for i in obj:
                idno=i.id
                username=i.fname
                usermob=i.mob
                useremail=i.email
                userpass=i.password
                usertype=i.user_type
            request.session['id']=idno
            request.session['name']=username
            request.session['mob']=usermob
            request.session['email']=useremail
            request.session['password']=userpass
            request.session['type']=usertype
            if usertype=="admin":
                return render(request,"adminhome.html")
            elif usertype=="nurse":
                return render(request,"nursehome.html")
            else:
                return render(request,"patienthome.html")
        else:
            msg="invalid login"
            return render(request,"login.html",{'msg':msg})
    return render(request,"login.html")


def add_nurse(request):
    if request.method == "POST":
        # Retrieve form data
        name = request.POST.get("name")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        qualification = request.POST.get("qualification")
        experience = request.POST.get("experience")
        specialization = request.POST.get("specialization")
        available_days = request.POST.get("available_days")
        password = request.POST.get("password")
        status = request.POST.get("status")

        # Save to Nurse model
        try:
            nurse = Nurse.objects.create(
                name=name,
                dob=dob,
                gender=gender,
                address=address,
                email=email,
                phone=phone,
                qualification=qualification,
                experience=experience,
                specialization=specialization,
                available_days=available_days,
                password=password,
                status=status,
            )
            nurse.save()

            # Automatically create or update entry in reg_tbl
            reg_entry, created = reg_tbl.objects.update_or_create(
                email=email,
                defaults={
                    "fname": name,
                    "mob": phone,
                    "email":email,
                    "password": password,
                    "user_type": "nurse",
                },
            )

            messages.success(request, "Nurse added successfully!")
            return render(request, "addnurse.html")  # Redirect to the add nurse page or another page
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return render(request, "addnurse.html")  # Render the form again with error message

    return render(request, "addnurse.html")  # Render the add nurse form

def patient_profile(request):
    if request.method=="POST":
        name=request.POST.get("name")
        dob=request.POST.get("dob")
        gender=request.POST.get("gender")
        address=request.POST.get("address")
        mob=request.POST.get("phone")
        email=request.POST.get("email")
        medical=request.POST.get("medical")
        user_id=request.session.get("id")
        user=reg_tbl.objects.get(id=user_id)
        obj=Patient.objects.create(name=name,dob=dob,gender=gender,address=address,phone=mob,email=email,medical_history=medical,user=user)
        obj.save()
        msg="Profile created successfully"
        return render(request,"patientprofile.html",{'msg':msg})
    user_name=request.session.get('name')
    user_mob=request.session.get('mob')
    user_email=request.session.get('email')
    return render(request,"patientprofile.html",{'name':user_name,'mob':user_mob,'email':user_email})
    


def add_service_request(request):
    if request.method == "POST":
        service_type = request.POST.get("service_type")
        description = request.POST.get("description")
        user_id = request.session.get("id")  # Get logged-in user ID
        try:
            patient = Patient.objects.get(user_id=user_id)  # Find the associated Patient record
            request_obj = ServiceRequest.objects.create(
                patient=patient,
                service_type=service_type,
                description=description,
            )
            request_obj.save()
            messages.success(request, "Service request submitted successfully!")
            return render(request, "addservicerequest.html")  # Redirect to view all service requests
        except Patient.DoesNotExist:
            messages.error(request, "Patient profile not found. Please complete your profile first.")
            return render(request, "addservicerequest.html") 

    return render(request, "addservicerequest.html") 
def view_service_requests(request):
    user_id = request.session.get("id")  # Get logged-in user ID
    try:
        patient = Patient.objects.get(user_id=user_id)  # Find the associated Patient record
        service_requests = ServiceRequest.objects.filter(patient=patient)  # Filter requests by patient
        return render(request, "patientservicerequest.html", {'service_requests': service_requests})
    except Patient.DoesNotExist:
        messages.error(request, "Patient profile not found.")
        return render(request, "patientservicerequest.html")

def admin_service_requests(request):
    service_requests = ServiceRequest.objects.all()  # Fetch all service requests

    # Add available nurses to each service request for filtering
    for service_request in service_requests:
        service_request.available_nurses = Nurse.objects.filter(
            status="Active",
            specialization=service_request.service_type  # Match nurse specialization with service type
        )

    return render(request, "adminservicerequest.html", {'service_requests': service_requests})

def update_service_request_status(request, request_id):
    if request.method == "POST":
        try:
            service_request = ServiceRequest.objects.get(id=request_id)
            action = request.POST.get('action')  # Action can be 'approve' or 'reject'

            if action == 'approve':
                service_request.status = 'Approved'
            elif action == 'reject':
                service_request.status = 'Rejected'
            else:
                messages.error(request, "Invalid action.")
                return redirect('adminservicerequest')

            service_request.save()
            messages.success(request, f"Service request {action}d successfully.")
        except ServiceRequest.DoesNotExist:
            messages.error(request, "Service request not found.")
        return redirect('adminservicerequest')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('adminservicerequest')

def assign_nurse(request, request_id):
    if request.method == "POST":
        nurse_id = request.POST.get("nurse_id")
        try:
            service_request = ServiceRequest.objects.get(id=request_id)
            nurse = Nurse.objects.get(id=nurse_id, status="Active", specialization=service_request.service_type)

            service_request.nurse_assigned = nurse
            service_request.nurse_assignment_status = "Assigned"
            service_request.save()
            messages.success(request, f"Nurse {nurse.name} assigned successfully!")
            nurse.status = "Inactive"
            nurse.save()

            messages.success(request, f"Nurse {nurse.name} assigned and marked as inactive successfully!")
        except ServiceRequest.DoesNotExist:
            messages.error(request, "Service request not found.")
        except Nurse.DoesNotExist:
            messages.error(request, "Invalid nurse selected or criteria not matched.")
    return redirect('adminservicerequest') 
def nurse_patient_view(request):
        nurse_name = request.session.get("name")  # Get logged-in user ID
        nurse = Nurse.objects.get(name=nurse_name)  # Find the associated Patient record
        data = ServiceRequest.objects.filter(nurse_assigned=nurse,nurse_assignment_status="Assigned")
        if request.method == "POST":
            service_id = request.POST.get("service_id")
            status = request.POST.get("status")
            service_request = ServiceRequest.objects.get(id=service_id)
            service_request.completestatus = status
            service_request.save()
            nurse.status = "Active"
            nurse.save()  # Filter requests by patient
        return render(request, "nursepatient.html", {'data': data})

def contact(request):
    return render(request,"contact.html")
def about(request):
    return render(request,"about.html")
def service(request):
    return render(request,"service.html")
def nurse(request):
    return render(request,"Nurses.html")
def adminhome(request):
    return render(request,"adminhome.html")
def nursehome(request):
    return render(request,'nursehome.html')
def patienthome(request):
    return render(request,"patienthome.html")

    
        
 