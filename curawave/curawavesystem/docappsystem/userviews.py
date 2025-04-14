from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from dasapp.models import DoctorReg, Specialization, CustomUser, Appointment, Page, Patient
import random
from datetime import datetime, time, timedelta

def USERBASE(request):
    return render(request, 'userbase.html')

def Index(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()
    context = {
        'doctorview': doctorview,
        'page': page,
    }
    return render(request, 'index.html', context)

def create_appointment(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()
    today = timezone.localtime(timezone.now())

    context = {
        'doctorview': doctorview,
        'page': page,
        'today_date': today.strftime('%Y-%m-%d'),
        'min_time': '09:00',
        'max_time': '17:00',
    }

    # If user is logged in as patient, pre-fill their information
    if request.user.is_authenticated and request.user.user_type == '3':
        try:
            patient = Patient.objects.get(user=request.user)
            context.update({
                'patient': patient,
            })
        except Patient.DoesNotExist:
            pass

    if request.method == "POST":
        try:
            appointmentnumber = random.randint(100000000, 999999999)
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            mobilenumber = request.POST.get('mobilenumber')
            date_of_appointment = request.POST.get('date_of_appointment')
            time_of_appointment = request.POST.get('time_of_appointment')
            doctor_id = request.POST.get('doctor_id')
            additional_msg = request.POST.get('additional_msg')

            # Convert strings to datetime objects
            appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(time_of_appointment, '%H:%M').time()
            
            # Validate appointment date
            if appointment_date < today.date():
                messages.error(request, 'Please select a future date for your appointment')
                return redirect('appointment')

            # Validate weekday
            if appointment_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                messages.error(request, 'Appointments are only available on weekdays (Monday-Friday)')
                return redirect('appointment')

            # Validate business hours (9 AM - 5 PM)
            business_start = time(9, 0)
            business_end = time(17, 0)
            if appointment_time < business_start or appointment_time > business_end:
                messages.error(request, 'Appointments are only available between 9:00 AM and 5:00 PM')
                return redirect('appointment')

            # Check for existing appointments
            doctor = DoctorReg.objects.get(id=doctor_id)
            existing_appointment = Appointment.objects.filter(
                doctor_id=doctor,
                date_of_appointment=appointment_date,
                time_of_appointment=appointment_time,
                status__in=['0', 'Approved']  # Check pending and approved appointments
            ).exists()

            if existing_appointment:
                messages.error(request, 'This time slot is already booked. Please select a different time.')
                return redirect('appointment')

            # Create new appointment
            appointment = Appointment(
                appointmentnumber=appointmentnumber,
                fullname=fullname,
                email=email,
                mobilenumber=mobilenumber,
                doctor_id=doctor,
                date_of_appointment=date_of_appointment,
                time_of_appointment=time_of_appointment,
                additional_msg=additional_msg,
                status='0'
            )

            # Associate appointment with logged-in patient if applicable
            if request.user.is_authenticated and request.user.user_type == '3':
                try:
                    patient = Patient.objects.get(user=request.user)
                    appointment.patient = patient
                except Patient.DoesNotExist:
                    pass

            appointment.save()
            
            messages.success(request, f'Appointment booked successfully! Your appointment number is: {appointmentnumber}')
            if request.user.is_authenticated and request.user.user_type == '3':
                return redirect('patient_dashboard')
            return redirect('appointment')

        except DoctorReg.DoesNotExist:
            messages.error(request, 'Selected doctor not found')
        except ValueError:
            messages.error(request, 'Invalid date or time format')
        except Exception as e:
            messages.error(request, f'An error occurred while booking your appointment: {str(e)}')
        
        return redirect('appointment')

    return render(request, 'appointment.html', context)

def User_Search_Appointments(request):
    page = Page.objects.all()
    
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query)
            messages.info(request, "Search against " + query)
            context = {'patient': patient, 'query': query, 'page': page}
            return render(request, 'search-appointment.html', context)
        else:
            print("No Record Found")
            context = {'page': page}
            return render(request, 'search-appointment.html', context)
    
    # If the request method is not GET
    context = {'page': page}
    return render(request, 'search-appointment.html', context)

@login_required(login_url='login')
def View_Appointment_Details(request, id):
    try:
        appointment = Appointment.objects.get(id=id)
        
        # Only allow viewing if the user is the patient who made the appointment
        # or if it's an anonymous appointment (no patient linked)
        if appointment.patient and appointment.patient.user != request.user:
            messages.error(request, "You don't have permission to view this appointment")
            return redirect('patient_dashboard')
        
        context = {
            'appointment': appointment,
        }
        
        return render(request, 'patient/appointment_details.html', context)
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found")
        return redirect('patient_dashboard')

def privacy_policy(request):
    page = Page.objects.all()
    context = {
        'page': page,
    }
    return render(request, 'privacy-policy.html', context)

def terms_and_conditions(request):
    page = Page.objects.all()
    context = {
        'page': page,
    }
    return render(request, 'terms-and-conditions.html', context)

def patient_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        address = request.POST.get('address')
        blood_group = request.POST.get('blood_group')
        date_of_birth = request.POST.get('date_of_birth')

        # Check if user already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('patient_signup')

        try:
            user = CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,
                password=make_password(password),
                user_type='3'
            )

            patient = Patient.objects.create(
                user=user,
                mobile_number=mobile,
                address=address,
                blood_group=blood_group,
                date_of_birth=date_of_birth
            )

            messages.success(request, "Account created successfully!")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('patient_signup')

    return render(request, 'patient/signup.html')

@login_required(login_url='login')
def patient_dashboard(request):
    if request.user.user_type != '3':
        messages.error(request, "Access Denied!")
        return redirect('login')
    
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-created_at')
    
    context = {
        'patient': patient,
        'appointments': appointments,
    }
    return render(request, 'patient/dashboard.html', context)

@login_required(login_url='login')
def patient_profile(request):
    if request.user.user_type != '3':
        messages.error(request, "Access Denied!")
        return redirect('login')
    
    patient = Patient.objects.get(user=request.user)
    
    if request.method == 'POST':
        patient.user.first_name = request.POST.get('first_name')
        patient.user.last_name = request.POST.get('last_name')
        patient.mobile_number = request.POST.get('mobile')
        patient.address = request.POST.get('address')
        patient.blood_group = request.POST.get('blood_group')
        patient.date_of_birth = request.POST.get('date_of_birth')
        
        if request.FILES.get('profile_pic'):
            patient.user.profile_pic = request.FILES['profile_pic']
            
        patient.user.save()
        patient.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('patient_profile')
    
    return render(request, 'patient/profile.html', {'patient': patient})

@login_required(login_url='login')
def cancel_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Check if the appointment belongs to the logged-in user
        if appointment.patient and appointment.patient.user != request.user:
            messages.error(request, "You don't have permission to cancel this appointment")
            return redirect('patient_dashboard')
            
        # Only allow cancellation of pending appointments
        if appointment.status != '0':
            messages.error(request, "This appointment cannot be cancelled")
            return redirect('viewappointmentdetails', appointment.id)
            
        appointment.status = 'Cancelled'
        appointment.save()
        
        messages.success(request, "Appointment cancelled successfully")
        return redirect('patient_dashboard')
        
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found")
        return redirect('patient_dashboard')




