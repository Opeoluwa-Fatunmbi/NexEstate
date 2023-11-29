from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    async def send_enquiry(user):
        subject = "Enquiry"
        message = render_to_string(
            "enquiry.html",
            {
                "name": user.name,
                "email": user.email,
                "phone_number": user.phone_number,
                "subject": user.subject,
                "message": user.message,
            },
        )
        email_message = EmailMessage(
            subject=subject, body=message, to=[user.is_admin.email]
        )
        EmailThread(email_message).start()
