# Third Party Stuff
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from versatileimagefield.fields import VersatileImageField

# milife-back Stuff
from milife_back.base.models import UUIDModel, ImageMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, is_staff: bool, is_superuser: bool, **extra_fields):
        """Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, UUIDModel, PermissionsMixin, ImageMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'I would rather not say')
    )
    WEIGHT_UNIT_CHOICES = (
        ('metric', 'metric'),
        ('imperial','imperial'),
    )
    HEIGHT_UNIT_CHOICES = (
        ('metric', 'metric'),
        ('imperial','imperial'),
    )
    accuniq_id = models.CharField(_("Accuniq Id"), max_length=100)
    first_name = models.CharField(_('First Name'), max_length=120, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=120, blank=True)
    number = models.CharField(_('Number'), max_length=120, blank=True)
    # https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/fields/#citext-fields
    email = CIEmailField(_('email address'), unique=True, db_index=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text='Designates whether the user can log into the admin site.')

    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_verified = models.BooleanField(_('email verified'), default=False)
    invited = models.BooleanField(_("Invited"), default=False)

    gender = models.CharField(_('Gender'), max_length=4, choices=GENDER_CHOICES, blank=True)
    height_cm = models.DecimalField(_('Height'), max_digits=5, decimal_places=2, blank=True, null=True)
    height_unit = models.CharField(_('Height unit preference'), max_length=10, choices=HEIGHT_UNIT_CHOICES, blank=True)
    weight_kg = models.DecimalField(_('Weight'), max_digits=5, decimal_places=2, blank=True, null=True)
    weight_unit = models.CharField(_('Weight unit preference'), max_length=10, choices=WEIGHT_UNIT_CHOICES, blank=True)
    date_of_birth = models.DateField(_('Date Of Birth'), null=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined', )

    def __str__(self):
        return str(self.id)

    def get_full_name(self) -> str:
        """Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str:
        """Returns the short name for the user.
        """
        return self.first_name.strip()
