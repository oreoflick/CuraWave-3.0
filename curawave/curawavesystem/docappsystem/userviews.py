from django.shortcuts import render, redirect, HttpResponse
from dasapp.models import DoctorReg, Specialization, CustomUser, Appointment, Page
import random
from datetime import datetime, time, timedelta
from django.contrib import messages
from django.utils import timezone

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
                time_of_appointment=time_of_appointment,
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
            appointment.save()
            
            messages.success(request, f'Appointment booked successfully! Your appointment number is: {appointmentnumber}')
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

def View_Appointment_Details(request, id):
    page = Page.objects.all()
    patientdetails = Appointment.objects.filter(id=id)
    context = {
        'patientdetails': patientdetails,
        'page': page
    }

    return render(request, 'user_appointment-details.html', context)




