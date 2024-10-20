"""This module defines the views for the notifications app.

Views:
    NotificationListView: A view to list all notifications.
    NotificationCreateView: A view to create a new notification.
    NotificationUpdateView: A view to update an existing notification.
    NotificationDeleteView: A view to delete a notification.
"""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import NotificationForm
from .models import Notification


class NotificationListView(ListView):
    """A view to list all notifications.

    Attributes:
        model (Model): The model associated with the view.
        template_name (str): The template to render.
        context_object_name (str): The context object name for the template.
    """

    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"


class NotificationCreateView(CreateView):
    """A view to create a new notification.

    Attributes:
        model (Model): The model associated with the view.
        form_class (Form): The form class to use for creating a notification.
        template_name (str): The template to render.
        success_url (str): The URL to redirect to on successful creation.
    """

    model = Notification
    form_class = NotificationForm
    template_name = "notifications/notification_form.html"
    success_url = reverse_lazy("notifications:notification_list")


class NotificationUpdateView(UpdateView):
    """A view to update an existing notification.

    Attributes:
        model (Model): The model associated with the view.
        form_class (Form): The form class to use for updating a notification.
        template_name (str): The template to render.
        success_url (str): The URL to redirect to on successful update.
    """

    model = Notification
    form_class = NotificationForm
    template_name = "notifications/notification_form.html"
    success_url = reverse_lazy("notifications:notification_list")


class NotificationDeleteView(DeleteView):
    """A view to delete a notification.

    Attributes:
        model (Model): The model associated with the view.
        template_name (str): The template to render.
        success_url (str): The URL to redirect to on successful deletion.
    """

    model = Notification
    template_name = "notifications/notification_confirm_delete.html"
    success_url = reverse_lazy("notifications:notification_list")
