from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models

from utils.utils import get_age


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)

        weight = extra_fields['weight']
        height = extra_fields['height']
        age = get_age(extra_fields['birthday'])

        if extra_fields['sex'] == 'M':
            user.max_calories = (13.75 * weight) + (5 * height) - (6.76 * age) + 66.5
        elif extra_fields['sex'] == 'F':
            user.max_calories = (9.56 * weight) + (1.85 * height) - (4.68 * age) + 665

        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser precisa precisa estar como True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff precisa precisa estar como True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('E-mail'), unique=True)
    name = models.CharField(_('Name'), max_length=150)
    is_staff = models.BooleanField(_('Staff'), default=False)
    height = models.PositiveIntegerField(_('Altura em cm'))
    weight = models.IntegerField(_('Peso em kg'))
    birthday = models.DateField()
    max_calories = models.PositiveIntegerField(_('Meta de calorias'), default=0)
    sex = models.CharField(max_length=2, choices=[
        ('M', _('MASCULINO')),
        ('F', _('FEMININO')),
    ])

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'height', 'weight', 'birthday', 'sex']

    def get_url_profile(self):
        name_parts = self.name.split(' ')
        first_name = name_parts[0]
        last_name = None

        if len(name_parts) > 1:
            last_name = name_parts[1]

        if last_name:
            return f'https://ui-avatars.com/api/?name={first_name}+{last_name}&background=27272A&color=fff&format=png&font-size=0.5'
        return f'https://ui-avatars.com/api/?name={first_name}&background=27272A&color=fff&format=png&font-size=0.5'

    def __str__(self):
        return self.email

    def first_name(self):
        return self.name.split(' ')[0]
