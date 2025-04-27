from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FileUpload
from django.core.mail import send_mail

@receiver(post_save, sender=FileUpload)
def send_upload_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'Yangi fayl yuklandi'
        message = f'Hurmatli {instance.user.username},\n\nSiz "{instance.title}" nomli faylni muvaffaqiyatli yukladingiz.'
        from_email = 'no-reply@example.com'
        recipient_list = [instance.user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)