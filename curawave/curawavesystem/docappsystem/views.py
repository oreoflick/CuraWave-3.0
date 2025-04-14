from django.shortcuts import render,redirect,HttpResponse
from dasapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dasapp.models import CustomUser
from django.contrib.auth import get_user_model
from datetime import datetime
User = get_user_model()

def BASE(request):
    return render(request,'base.html')

def LOGIN(request):
    return render(request,'login.html')

def DOCTOR_LOGIN(request):
    return render(request, 'doc/login.html')

def PATIENT_LOGIN(request):
    return render(request, 'patient/login.html')

def doLogout(request):
    logout(request)
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        if not all([email, password, user_type]):
            messages.error(request, 'Please provide all required information')
            return redirect('login')
            
        try:
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if user.is_active:
                    if user.user_type == user_type:
                        login(request, user)
                        if user_type == '1':
                            return redirect('admin_home')
                        elif user_type == '2':
                            return redirect('doctor_home')
                        elif user_type == '3':
                            return redirect('patient_dashboard')
                    else:
                        messages.error(request, f'This login is for {user_type} only')
                        return redirect('login')
                else:
                    messages.error(request, 'Your account is not active')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid Email or Password')
                return redirect('login')
                
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('login')
            
    return redirect('login')

@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    
    context = {
        "user": user,
    }

    if user.user_type == '2':  # Doctor
        try:
            doctor = DoctorReg.objects.get(admin=user)
            context['doctor'] = doctor
        except DoctorReg.DoesNotExist:
            messages.error(request, "Doctor profile not found")
            return redirect('docsignup')
    elif user.user_type == '3':  # Patient
        try:
            patient = Patient.objects.get(user=user)
            context['patient'] = patient
        except Patient.DoesNotExist:
            messages.error(request, "Patient profile not found")
            return redirect('patient_signup')

    return render(request, 'profile.html', context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        user = CustomUser.objects.get(id=request.user.id)
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        try:
            # Update base user info
            user.first_name = first_name
            user.last_name = last_name
            
            if profile_pic:
                user.profile_pic = profile_pic
            
            user.save()

            # Update role-specific info
            if user.user_type == '2':  # Doctor
                doctor = DoctorReg.objects.get(admin=user)
                doctor.mobilenumber = request.POST.get('mobile')
                doctor.specialization_id_id = request.POST.get('specialization')
                doctor.save()
            elif user.user_type == '3':  # Patient
                patient = Patient.objects.get(user=user)
                patient.mobile_number = request.POST.get('mobile')
                patient.address = request.POST.get('address')
                patient.blood_group = request.POST.get('blood_group')
                patient.date_of_birth = request.POST.get('date_of_birth')
                patient.save()

            messages.success(request, 'Your Profile Updated Successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Failed to Update Your Profile: {str(e)}')
            return redirect('profile')

    return redirect('profile')

def CHANGE_PASSWORD(request):
    context = {}
    ch = User.objects.filter(id = request.user.id)
     
    if len(ch) > 0:
        data = User.objects.get(id = request.user.id)
        context["data"] = data            
    if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            messages.success(request,'Password Changed Successfully!')
            user = User.objects.get(username=un)
            login(request,user)
        else:
            messages.error(request,'Current Password is incorrect!')
            return redirect("change_password")
    return render(request,'change-password.html', context)
