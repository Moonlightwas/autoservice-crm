from django.db import models
from django.utils import timezone
from django.conf import settings


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "confirmed"
        IN_WORK = "in_work", "In work"
        READY = "ready", "Ready"
        PAYMENT = "payment", "Payment"
        COMPLITED = "complited", "Complited"
        CANCELED = "canceled", "Canceled"

    class Source(models.TextChoices):
        MANAGER = "manager", "Manager"
        ONLINE = "online", "Online"
        PHONE = "phone", "Phone"

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="client_orders",
        on_delete=models.CASCADE
    )
    car = models.ForeignKey(
        "cars.Car",
        related_name="orders",
        on_delete=models.CASCADE
    )
    status = models.CharField(choices=Status.choices, default=Status.PENDING)
    source = models.CharField(choices=Source.choices)
    mechanic = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="mechanic_orders",
        blank=True
    )
    description = models.TextField()
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ready_at = models.DateTimeField(null=True, blank=True)
    confirmed_pay_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.status} - {self.client.id}"

    def set_status_force(self, new_status):
        if new_status not in dict(self.Status.choices):
            return False

        order_status = (
            "pending",
            "confirmed",
            "in_work",
            "ready",
            "payment",
            "complited",
            "canceled"
        )
        new_index = order_status.index(new_status)
        old_index = order_status.index(self.status)

        date_fields = {
            "confirmed": "confirmed_at",
            "in_work": "started_at",
            "ready": "ready_at",
            "payment": "confirmed_pay_at",
            "complited": "completed_at",
            "canceled": "canceled_at"
        }

        # Change status time back to None from old to new
        if new_index < old_index:
            for status_name, field_name in date_fields.items():
                status_index = order_status.index(status_name)
                if new_index < status_index <= old_index:
                    setattr(self, field_name, None)
        # Change status time forward to now from old to new
        elif new_index > old_index:
            now = timezone.now()
            for status_name, field_name in date_fields.items():
                status_index = order_status.index(status_name)
                if old_index < status_index <= new_index:
                    setattr(self, field_name, now)

        self.status = new_status
        self.save()
        return True

    def confirm(self):
        if self.status == self.Status.PENDING:
            self.status = self.Status.CONFIRMED
            self.confirmed_at = timezone.now()
            self.save()
            return True
        return False

    def start_work(self):
        if self.status == self.Status.CONFIRMED:
            self.status = self.Status.IN_WORK
            self.started_at = timezone.now()
            self.save()
            return True
        return False

    def ready(self):
        if self.status == self.Status.IN_WORK:
            self.status = self.Status.READY
            self.ready_at = timezone.now()
            self.save()
            return True
        return False

    def confirm_pay(self):
        if self.status == self.Status.READY:
            self.status = self.Status.PAYMENT
            self.confirmed_pay_at = timezone.now()
            self.save()
            return True
        return False

    def complete(self):
        if self.status == self.Status.PAYMENT:
            self.status = self.Status.COMPLITED
            self.completed_at = timezone.now()
            self.save()
            return True
        return False

    def cancel(self):
        if self.status != self.Status.COMPLITED:
            self.status = self.Status.CANCELED
            self.canceled_at = timezone.now()
            self.save()
            return True
        return False
