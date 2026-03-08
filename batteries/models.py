from django.db import models
from django.conf import settings

from .cities import CITY_ABSENT


class BatterySubmission(models.Model):
    """Запись о сданных пользователем батарейках."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='battery_submissions',
        verbose_name='Пользователь',
    )
    count = models.PositiveIntegerField(verbose_name='Количество батареек')
    city = models.CharField(
        max_length=100,
        verbose_name='Город сдачи',
        default=CITY_ABSENT,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Сдача батареек'
        verbose_name_plural = 'Сдачи батареек'

    def __str__(self):
        return f'{self.user.username}: {self.count} шт. ({self.city})'
