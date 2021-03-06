from decimal import Decimal
from secrets import token_urlsafe

from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


class EshopUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    deactivated = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    @property
    def is_active(self):
        return self.deactivated is None


class classproperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner, cls):
        return self.fget(cls)


class Price(models.Model):
    massage_type = models.CharField(max_length=100)
    duration = models.DurationField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    start_date = models.DateTimeField(auto_now=True)

    @classproperty
    def current_prices_pk(cls):
        return cls.objects.values('massage_type', 'duration').annotate(pk=models.Max('pk')).values('pk')

    @classproperty
    def current_prices(cls):
        return cls.objects.filter(pk__in=models.Subquery(cls.current_prices_pk))

    class Meta:
        indexes = [
            models.Index(fields=['massage_type', 'duration', 'start_date']),
        ]

    def __str__(self):
        return f'<{self.massage_type} {self.duration.seconds // 60} min ${self.price}>'

class Discount(models.Model):
    code = models.CharField(max_length=20)
    per_item = models.DecimalField(decimal_places=2, max_digits=10)
    percent = models.DecimalField(decimal_places=5, max_digits=10)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return f'<{self.code}>'

    class Meta:
        indexes = [
            models.Index(fields=['code', 'end_date'])
        ]


# TODO: DiscountValid Table shows which Discount applies to which Price

def generate_token():
    return token_urlsafe(32) #bytes


class Purchase(models.Model):

    token = models.SlugField(default=generate_token, unique=True)
    user = models.ForeignKey('EshopUser', models.PROTECT)
    timestamp = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField('Price', through='Item')

    class Meta:
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'timestamp'])
        ]

    def save(self, *args, **kwargs):
        while True:
            try:
                return super().save(*args, kwargs)
            except IntegrityError:
                self.token = generate_token()

    def __str__(self):
        return f'<{self.token}>'

class Item(models.Model):
    price = models.ForeignKey('Price', models.PROTECT)
    discount = models.ForeignKey('Discount', models.PROTECT, default=None, null=True)
    purchase = models.ForeignKey('Purchase', models.PROTECT)
    redeemed = models.DateTimeField(null=True, blank=True)
    redeemed_by = models.ForeignKey('EshopUser', models.PROTECT, null=True, blank=True)

    def save(self, **kwargs):
        if self.redeemed:
            if not self.redeemed_by:
                raise ValueError('Must Assign Redeemed By field')
            if not self.redeemed_by.is_staff:
                raise ValueError('Must be redeemed by staff')
        super().save(**kwargs)

    @property
    def net_price(self):
        gross = self.price.price
        if not self.discount: return gross
        return gross*(1 - self.discount.percent * Decimal('0.01')) - self.discount.per_item


    def __str__(self):
        return f'<{self.purchase.token} {self.price.massage_type} {self.price.duration.seconds//60} min ${self.net_price}>'

    class Meta:
        indexes = [
            models.Index(fields=['purchase'])
        ]


class Booking(models.Model):
    item = models.OneToOneField('Item', models.PROTECT, related_name='booking', null=True)
    start_time = models.DateTimeField()
    note = models.TextField(null=True)

    def __str__(self):
        return f'<{" ".join([self.start_time.strftime("%H:%M %d %b"), self.note or ""])}>'

    class Meta:
        indexes = [
            models.Index(fields=['start_time']),
            models.Index(fields=['item', 'start_time'])
        ]

class Payment(models.Model):
    token = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=10)
    createdAt = models.DateTimeField(auto_now=True)
    orderId = models.OneToOneField('Purchase', models.PROTECT, to_field='token')
    gatewayResponseCode = models.CharField(max_length=5, null=True)
    errorCode = models.CharField(max_length=3, null=True)
    response = models.JSONField()


    class Meta:
        indexes = [
            models.Index(fields=['orderId']),
        ]
