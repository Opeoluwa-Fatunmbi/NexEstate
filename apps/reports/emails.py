from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from . import models as accounts_models
import random, threading
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)
from nexestate.settings.base import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    async def send_property_valuation_report(property, user, report):
        subject = "Your property valuation report"
        message = render_to_string(
            "property-valuation-report.html",
            {
                "name": user.full_name,
                "report": report,
            },
        )

        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()
