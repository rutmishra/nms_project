from django.core.mail import send_mail

def send_email_alert(device_name):
    send_mail("Device Down Alert", f"{device_name} is DOWN!", "admin@nms.com", ["user@example.com"])
