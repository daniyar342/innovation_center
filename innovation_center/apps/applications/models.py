# applications/models.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


class Application(models.Model):
    APPLICATION_TYPES = [
        ('startup', 'Стартап'),
        ('investor', 'Инвестор'),
        ('support_organization', 'Организация поддержки'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Подана'),
        ('under_review', 'Рассматривается'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
        ('additional_info_required', 'Ожидает дополнительной информации'),
        ('completed', 'Завершена'),
    ]
    fullname = models.CharField(max_length='50', verbose_name='ФИО')
    type = models.CharField(max_length=50, choices=APPLICATION_TYPES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    details = models.TextField()


@receiver(post_save, sender=Application)
def set_default_status(sender, instance, **kwargs):
    """
    Сигнал, который устанавливает статус "Рассматривается" после сохранения заявки.
    """
    if instance.status == 'pending':
        instance.status = 'under_review'
        instance.save()
