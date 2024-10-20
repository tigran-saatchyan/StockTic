from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import NotificationForm
from .models import Notification


class NotificationListView(ListView):
    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"


class NotificationCreateView(CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = "notifications/notification_form.html"
    success_url = reverse_lazy("notifications:notification_list")


class NotificationUpdateView(UpdateView):
    model = Notification
    form_class = NotificationForm
    template_name = "notifications/notification_form.html"
    success_url = reverse_lazy("notifications:notification_list")


class NotificationDeleteView(DeleteView):
    model = Notification
    template_name = "notifications/notification_confirm_delete.html"
    success_url = reverse_lazy("notifications:notification_list")
