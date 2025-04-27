from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    image = models.ImageField(
        upload_to='profile_images/',
        default='profile_images/default.jpg',
        verbose_name=_('Profile Image')
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_('Bio')
    )
    phone = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,12}$', message=_('Invalid phone number'))],
        verbose_name=_('Phone Number')
    )

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f"{self.user.username}'s Profile"