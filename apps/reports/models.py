# from django.db import models
# from django.contrib.auth.models import User
# from apps.properties.models import Property
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from apps.common.models import BaseModel


# Create your models here.


#
# class PropertyValuationReport(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     property = models.ForeignKey(Property, on_delete=models.CASCADE)
#     report = models.TextField(_("Report"), blank=True, null=True)
#     generated = models.BooleanField(_("Generated"), default=False)
#
#     class Meta:
#         verbose_name = _("Property valuation report")
#         verbose_name_plural = _("Property valuation reports")
#
#     def __str__(self):
#         return f"{self.property.title} - {self.user.email}"
