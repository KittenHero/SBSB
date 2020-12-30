from datetime import datetime, timedelta

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.timezone import make_aware
from django.utils.html import format_html

from .forms import EshopUserCreationForm, EshopUserChangeForm, ItemChangeForm
from .models import (
    EshopUser,
    Price,
    Discount,
    Purchase,
    Item,
    Booking,
    Payment,
)


@admin.register(EshopUser)
class EshopUserAdmin(UserAdmin):
    add_form = EshopUserCreationForm
    form = EshopUserChangeForm
    model = EshopUser

    list_display = 'email', 'is_staff', 'deactivated'
    list_filter = 'email', 'is_staff', 'deactivated'
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Permissions', {'fields': ['is_staff', 'groups','deactivated']}),
    ]
    add_fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'password1', 'password2', 'is_staff', 'deactivated']
        }),
    )
    search_fields = 'email',
    ordering = 'email',

    @staticmethod
    def has_add_permission(request, obj=None):
        return request.user.is_superuser

    @staticmethod
    def has_change_permission(request, obj=None):
        return request.user.is_superuser

    @staticmethod
    def has_delete_permission(request, obj=None):
        return request.user.is_superuser


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    class ActiveListFilter(admin.SimpleListFilter):
        title = 'active'
        parameter_name = 'active'

        def lookups(self, queryset, model_admin):
            return [('t', 'Current Prices'), ('f', 'Old Prices')]

        def queryset(self, request, queryset):
            active = self.value()
            if active == 't':
                return queryset.filter(pk__in=Price.current_prices_pk)
            if active == 'f':
                return queryset.exclude(pk__in=Price.current_prices_pk)

    list_display = 'massage_type', 'duration', 'price'
    list_filter = ActiveListFilter, 'massage_type', 'duration'

    @staticmethod
    def has_change_permission(request, obj=None):
        return False

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = 'code', 'per_item', 'percent', 'start_date', 'end_date'

    @staticmethod
    def has_change_permission(request, obj=None):
        return False

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    class BookingListFilter(admin.SimpleListFilter):
        title = 'start_time'
        parameter_name = 'start'

        def lookups(self, request, model_admin):
            return [
                ('today', 'Today'),
                ('tomorrow', 'Tomorrow'),
                ('week', 'This week'),
                ('nextweek', 'Next week'),
                ('month', 'This month'),
                ('nextmonth', 'Next month'),
            ]

        def queryset(self, request, queryset):
            query = self.value()
            if not query:
                return queryset
            start = {
                'today': today(),
                'tomorrow': tomorrow(),
                'week': this_week(),
                'nextweek': next_week(),
                'month': this_month(),
                'nextmonth': next_month()
            }[query]
            end = {
                'today': tomorrow,
                'tomorrow': tomorrow,
                'week': next_week,
                'next_week': next_week,
                'month': next_month,
                'nextmonth': next_month,
            }[query](start)
            return queryset.filter(
                start_time__gte=make_aware(start),
                start_time__lte=make_aware(end),
            )

    def item_link(self, obj):
        item = obj.item
        link = reverse('admin:EShop_item_change', args=[item.pk])
        return format_html('<a href="{}">{}</a>', link, str(item))

    list_display = 'start_time', 'note', 'item_link'
    list_filter = BookingListFilter, 'item'
    search_fields = 'item__purchase__token', 'item__purchase__user__email', 'item__price__massage_type'

    fieldsets = [(None, {'fields': ['start_time', 'note', 'item_link']})]
    readonly_fields = 'item_link',

    @staticmethod
    def has_add_permission(request, obj=None):
        return True

    @staticmethod
    def has_change_permission(request, obj=None):
        return True

    @staticmethod
    def has_delete_permission(request, obj=None):
        return True


class BookingInline(admin.StackedInline):
    model = Booking
    readonly_fields = 'start_time', 'note'

    @staticmethod
    def has_add_permission(request, obj=None):
        return False

    @staticmethod
    def has_change_permission(request, obj=None):
        return True

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = 'purchase', 'price', 'discount'
    form = ItemChangeForm
    readonly_fields = 'redeemed', 'redeemed_by', 'purchase', 'price', 'discount'
    inlines = [ BookingInline ]

    def save_model(self, request, obj, form, change):
        if change:
            if form.cleaned_data['redeem']:
                obj.redeemed = make_aware(datetime.now())
                obj.redeemed_by = request.user
            else:
                obj.redeemed = None
                obj.redeemed_by = None
        super().save_model(request, obj, form, change)

    @staticmethod
    def has_add_permission(request, obj=None):
        return False

    @staticmethod
    def has_change_permission(request, obj=None):
        return True

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


class ItemInline(admin.StackedInline):
    model = Item
    form = ItemChangeForm
    readonly_fields = 'redeemed', 'redeemed_by', 'purchase', 'price', 'discount'

    @staticmethod
    def has_add_permission(request, obj=None):
        return False

    @staticmethod
    def has_change_permission(request, obj=None):
        return True

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = 'user', 'token', 'timestamp'
    search_fields = 'token', 'user__email'
    readonly_fields = 'user', 'token', 'timestamp'
    inlines = [ ItemInline ]

    def save_formset(self, request, form, formset, change):
        formset.save(commit=False)
        for form in formset.forms:
            if not isinstance(form, ItemChangeForm) or not form.has_changed():
                continue
            item = form.save(commit=False)
            if form.cleaned_data['redeem']:
                item.redeemed = make_aware(datetime.now())
                item.redeemed_by = request.user
            else:
                item.redeemed = None
                item.redeemed_by = None
            item.save()

    @staticmethod
    def has_add_permission(request, obj=None):
        return False

    @staticmethod
    def has_change_permission(request, obj=None):
        return True

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = 'status', 'token', 'createdAt'

    @staticmethod
    def has_add_permission(request, obj=None):
        return False

    @staticmethod
    def has_change_permission(request, obj=None):
        return False

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


def today():
    return datetime.today()


def tomorrow(date=None):
    return timedelta(days=1) + (date or today())


def this_week():
    return today() - timedelta(days=today().isocalendar().weekday - 1)


def next_week(date=None):
    return timedelta(days=7) + (date or this_week())


def this_month():
    return today() - timedelta(days=today().day - 1)


def next_month(date=None):
    date = date or this_month()
    if date.month == 12:
        return date.replace(year=date.year+1, month=1)
    return date.replace(month=date.month+1)
