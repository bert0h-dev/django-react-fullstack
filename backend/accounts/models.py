from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
  def create_user(self, email, username, first_name, last_name, first_surname, last_surname, password=None, **extra_fields):
    if not email:
      raise ValueError('El campo de correo electrónico es obligatorio')
    if not username:
      raise ValueError('El campo de nombre de usuario es obligatorio')
    if not first_name:
      raise ValueError('El campo de nombre es obligatorio')
    if not first_surname:
      raise ValueError('El campo de apellido es obligatorio')

    user = self.model( email=self.normalize_email(email), username=username, first_name=first_name, last_name=last_name, first_surname=first_surname, last_surname=last_surname, **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, username, first_name, last_name, first_surname, last_surname, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_verified', True)

    return self.create_user(email=email, username=username, first_name=first_name, last_name=last_name, first_surname=first_surname, last_surname=last_surname, password=password, **extra_fields)

# Se crea modelo para el manejo del usuario personalizado
class User(AbstractUser, PermissionsMixin):
  #Identificacion
  email = models.EmailField(unique=True, verbose_name='email')
  username = models.CharField(max_length=150, unique=True, null=True, blank=True, verbose_name='username')
  first_name = models.CharField(max_length=150, verbose_name='first name')
  last_name = models.CharField(max_length=150, null=True, blank=True, verbose_name='last name')
  first_surname = models.CharField(max_length=150, verbose_name='first surname')
  last_surname = models.CharField(max_length=150, null=True, blank=True, verbose_name='last surname')

  # Perfil
  phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name='phone number')
  department = models.CharField(max_length=50, null=True, blank=True, verbose_name='department')
  position = models.CharField(max_length=50, null=True, blank=True, verbose_name='position')

  # Preferencias
  # language = models.CharField(max_length=10, default='es', verbose_name='language')
  # timezone = models.CharField(max_length=50, default='America/Mexico_City', verbose_name='timezone')

  # Seguridad
  is_verified = models.BooleanField(default=False, verbose_name='is verified')
  requires_password_reset = models.BooleanField(default=True, verbose_name='requires password reset')
  password_changed = models.BooleanField(default=False, verbose_name='password changed')
  last_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='last ip')

  # Sistema
  is_active = models.BooleanField(default=True, verbose_name='is active')
  is_staff = models.BooleanField(default=False, verbose_name='is staff')
  date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
  last_activity = models.DateTimeField(null=True, blank=True, verbose_name='last activity')

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'first_surname', 'last_surname']

  def __str__(self):
    return self.email
  
  def get_full_name(self):
    return f"{self.first_name} {self.last_name} {self.first_surname} {self.last_surname}"
  
  def set_password(self, raw_password):
    super().set_password(raw_password)
    self.password_changed = True
    self.requires_password_reset = False
    self.save()