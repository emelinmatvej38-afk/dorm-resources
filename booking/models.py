from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
class University(models.Model):
    name = models.CharField('Название', max_length=200)
    short_name = models.CharField('Короткое название',max_length=50, blank=True)
    city = models.CharField('Город',max_length=100, blank=True)
    description = models.TextField('Описание',blank=True)


    class Meta:
        verbose_name = 'Вуз'
        verbose_name_plural = 'Вузы'

    def __str__(self):
        return self.name


class Dormitory(models.Model):
    name = models.CharField("Название", max_length=100)
    address = models.CharField("Адрес",max_length=200,blank=True)

    university = models.ForeignKey(
        University, on_delete=models.CASCADE, related_name='dormitories',
        verbose_name='Вуз'
    )

    class Meta:
        verbose_name = 'Общежитие'
        verbose_name_plural = 'Общежития'


    def __str__(self):
        return self.name

class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Студент'
        MANAGER = 'manager', 'Комендант'
        ADMIN = 'admin', 'Администратор вуза'


    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Вуз'
    )
    dormitory = models.ForeignKey(
        Dormitory, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Общежитие'
    )

    role = models.CharField('Роль', max_length=20, choices=Role.choices, default=Role.STUDENT)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"{self.user} ({self.get_role_display()})"

class Resource(models.Model):
    class Kind(models.TextChoices):
        LAUNDRY = 'laundry', 'Быт'
        KITCHEN = 'kitchen', 'Кухня'
        STUDY = 'study', 'Учеба'
        GYM = 'gym', 'Спорт'
        OTHER = 'other', 'Другое'

    dormitory = models.ForeignKey(
        Dormitory, on_delete=models.CASCADE, related_name='resources',
        verbose_name='Общежитие'
    )
    name = models.CharField('Название', max_length=100)
    kind = models.CharField('Тип', max_length=20, choices=Kind.choices, default=Kind.OTHER)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Доступен', default=True)

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'


    def __str__(self):
        return f'{self.name} ({self.dormitory})'

class Booking(models.Model):
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name='bookings',
        verbose_name='Ресурс'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings',
        verbose_name='Пользователь'
    )
    start = models.DateTimeField('Начало')
    end = models.DateTimeField('Окончание')
    created_at = models.DateTimeField('Создано', auto_now_add=True)


    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        ordering = ['start']

    def __str__(self):
        return f'{self.resource} - {self.start:%d.%m.%Y %H:%M}'

    def clean(self):
        if not (self.resource_id and self.start and self.end):
            return
        if self.end <= self.start:
            raise ValidationError('Время окончания должно быть позже начала.')
        conflicts = Booking.objects.filter(
            resource_id=self.resource_id,
            start__lt=self.end,
            end__gt=self.start,
        ).exclude(pk=self.pk)
        if conflicts.exists():
            raise ValidationError('Это время уже занято.')


