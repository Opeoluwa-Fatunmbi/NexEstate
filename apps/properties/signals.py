from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.properties.models import Property
import google.generativeai as genai
import logging
from nexestate.settings.base import GOOGLE_API_KEY

logger = logging.getLogger(__name__)
genai.configure(api_key=GOOGLE_API_KEY)


@receiver(post_save, sender=Property)
def create_property_description(sender, instance, created, **kwargs):
    if created:
        try:
            # Generate description using Gemini Pro
            model = genai.GenerativeModel("gemini-pro")

            generated_description = model.generate_content(
                f"Describe a {instance.advert_type} with {instance.bedrooms} bedrooms, {instance.bathrooms} bathrooms, in {instance.city}. This architectural_style home is perfect for the target_audience and boasts of serenity. Imagine the feeling of activities in this charming space. The title of this property is {instance.title} and it is located at {instance.street_address}, {instance.city}, {instance.country}."
            ).text
            # Update property description with generated content
            instance.description = generated_description

            # Save property instance
            instance.save()

            logger.info("Property description saved")
            print("Property description saved")

        except Exception as e:
            logger.error(f"Error generating property description: {str(e)}")
            print("Error generating property description")
    else:
        logger.info("Property description not saved")
        print("Property description not saved")
