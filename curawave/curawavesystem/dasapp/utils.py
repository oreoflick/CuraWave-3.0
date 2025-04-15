from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_appointment_email(appointment, template_name, subject):
    """
    Send email notification for appointment status changes
    """
    context = {
        'appointment': appointment,
        'doctor_name': f"Dr. {appointment.doctor_id.admin.get_full_name()}",
        'patient_name': appointment.fullname,
        'appointment_date': appointment.date_of_appointment,
        'appointment_time': appointment.time_of_appointment,
    }
    
    html_message = render_to_string(f'emails/{template_name}.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.email],
        html_message=html_message,
        fail_silently=False,
    )
