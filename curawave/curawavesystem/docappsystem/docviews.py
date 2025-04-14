from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from dasapp.models import DoctorReg,Specialization,CustomUser,Appointment
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
def DOCSIGNUP(request):
    specialization = Specialization.objects.all()
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        specialization_id = request.POST.get('specialization_id')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exist')
            return redirect('docsignup')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username already exist')
            return redirect('docsignup')
        else:
            user = CustomUser(
               first_name=first_name,
               last_name=last_name,
               username=username,
               email=email,
               user_type=2,
               profile_pic = pic,
            )
            user.set_password(password)
            user.save()
            spid =Specialization.objects.get(id=specialization_id)
            doctor = DoctorReg(
                admin = user,
                
                mobilenumber = mobno,
                specialization_id = spid,
                
            )
            doctor.save()            
            messages.success(request,'Signup Successfully')
            return redirect('docsignup')
    
    context = {
        'specialization':specialization
    }

    return render(request,'doc/docreg.html',context)

@login_required(login_url='/')
def DOCTORHOME(request):
    try:
        doctor_admin = request.user
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
        
        context = {
            'allaptcount': Appointment.objects.get_doctor_appointments(doctor_reg).count(),
            'newaptcount': Appointment.objects.get_pending_appointments(doctor_reg).count(),
            'appaptcount': Appointment.objects.get_approved_appointments(doctor_reg).count(),
            'canaptcount': Appointment.objects.get_cancelled_appointments(doctor_reg).count(),
            'comaptcount': Appointment.objects.get_completed_appointments(doctor_reg).count(),
            'upcoming_appointments': Appointment.objects.get_pending_appointments(doctor_reg)[:5],
        }
        return render(request, 'doc/dochome.html', context)
    except DoctorReg.DoesNotExist:
        messages.error(request, "Please complete your registration first")
        return redirect('docsignup')

@login_required(login_url='/')
def View_Appointment(request):
    try:
        doctor_admin = request.user
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
        view_appointment = Appointment.objects.get_doctor_appointments(doctor_reg)

        # Pagination
        paginator = Paginator(view_appointment, 5)  # Show 5 appointments per page
        page = request.GET.get('page')
        try:
            view_appointment = paginator.page(page)
        except PageNotAnInteger:
            view_appointment = paginator.page(1)
        except EmptyPage:
            view_appointment = paginator.page(paginator.num_pages)

        context = {'view_appointment': view_appointment}
    except Exception as e:
        context = {'error_message': str(e)}

    return render(request, 'doc/view_appointment.html', context)


def Patient_Appointment_Details(request,id):
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails

    }

    return render(request,'doc/patient_appointment_details.html',context)


def Patient_Appointment_Details_Remark(request):
    if request.method == 'POST':
        try:
            patient_id = request.POST.get('pat_id')
            remark = request.POST.get('remark')
            status = request.POST.get('status')
            
            if not all([patient_id, remark, status]):
                messages.error(request, "All fields are required")
                return redirect('view_appointment')
                
            patientaptdet = Appointment.objects.get(id=patient_id)
            patientaptdet.remark = remark
            patientaptdet.status = status
            patientaptdet.save()
            messages.success(request, "Status Updated successfully")
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('view_appointment')
    
    # If not POST, redirect to view appointment
    return redirect('view_appointment')

@login_required(login_url='/')
def Patient_Approved_Appointment(request):
    try:
        doctor_admin = request.user
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
        patientdetails1 = Appointment.objects.get_approved_appointments(doctor_reg)
        context = {'patientdetails1': patientdetails1}
        return render(request, 'doc/patient_app_appointment.html', context)
    except DoctorReg.DoesNotExist:
        messages.error(request, "Doctor profile not found")
        return redirect('doctor_home')

@login_required(login_url='/')
def Patient_Cancelled_Appointment(request):
    try:
        doctor_admin = request.user
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
        patientdetails1 = Appointment.objects.get_cancelled_appointments(doctor_reg)
        context = {'patientdetails1': patientdetails1}
        return render(request, 'doc/patient_app_appointment.html', context)
    except DoctorReg.DoesNotExist:
        messages.error(request, "Doctor profile not found")
        return redirect('doctor_home')

@login_required(login_url='/')
def Patient_New_Appointment(request):
    try:
        doctor_admin = request.user
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
        patientdetails1 = Appointment.objects.get_pending_appointments(doctor_reg)
        context = {'patientdetails1': patientdetails1}
        return render(request, 'doc/patient_app_appointment.html', context)
    except DoctorReg.DoesNotExist:
        messages.error(request, "Doctor profile not found")
        return redirect('doctor_home')

@login_required(login_url='/')
def Patient_List_Approved_Appointment(request):
    try:
        doctor_admin = request.user
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
        patientdetails1 = Appointment.objects.get_approved_appointments(doctor_reg)
        context = {'patientdetails1': patientdetails1}
        return render(request, 'doc/patient_list_app_appointment.html', context)
    except DoctorReg.DoesNotExist:
        messages.error(request, "Doctor profile not found")
        return redirect('doctor_home')

def DoctorAppointmentList(request,id):
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails

    }

    return render(request,'doc/doctor_appointment_list_details.html',context)

def Patient_Appointment_Prescription(request):
    if request.method == 'POST':
        patient_id = request.POST.get('pat_id')
        prescription = request.POST['prescription']
        recommendedtest = request.POST['recommendedtest']
        status = request.POST['status']
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.prescription = prescription
        patientaptdet.recommendedtest = recommendedtest
        patientaptdet.status = status
        patientaptdet.save()
        messages.success(request,"Status Update successfully")
        return redirect('view_appointment')
    return render(request,'doc/patient_list_app_appointment.html',context)


def Patient_Appointment_Completed(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status='Completed',doctor_id=doctor_reg)
    context = {'patientdetails1': patientdetails1}
    return render(request, 'doc/patient_list_app_appointment.html', context)

def Search_Appointments(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query) & Appointment.objects.filter(doctor_id=doctor_reg)
            messages.success(request, "Search against " + query)
            return render(request, 'doc/search-appointment.html', {'patient': patient, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'doc/search-appointment.html', {})

def Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    patient = []
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'doc/between-dates-report.html', {'visitor': visitor, 'error_message': 'Invalid date format'})

        # Filter Appointment between the given date range
        patient = Appointment.objects.filter(created_at__range=(start_date, end_date)) & Appointment.objects.filter(doctor_id=doctor_reg)

    return render(request, 'doc/between-dates-report.html', {'patient': patient,'start_date':start_date,'end_date':end_date})
