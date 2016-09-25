from django.db import models
from django.contrib.postgres.fields import ArrayField


class Faculty(models.Model):
    name_fac = models.CharField(max_length=80)
    def __unicode__(self):
        return self.name_fac

    def __str__(self):
        return self.name_fac

class Group(models.Model):
    name_group = models.CharField(max_length=80)
    facult_key = models.ForeignKey(Faculty)

    def __unicode__(self):
        return self.name_group

    def __str__(self):
        return self.name_group

class Schedule(models.Model):
    group_key = models.ForeignKey(Group)
    date = models.DateTimeField(auto_now=True)
    schedule = ArrayField(ArrayField(
        models.TextField(blank=True),size=15
        ),
        size=9
    )
    class Meta:
        ordering = ['-id']





# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
#
# def validate_even(value):
#     print(value)
#     if True:
#         raise ValidationError(
#             _('is not an even number')
#         )
