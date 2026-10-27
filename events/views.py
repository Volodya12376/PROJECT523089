
from calendar import monthrange
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from .models import Event
from .forms import EventForm


class EventListView(ListView):
    model = Event
    template_name = "events.html"
    context_object_name = "events"


class EventCalendarView(TemplateView):
    template_name = "events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()
        year = today.year
        month = today.month

        first_day = date(year, month, 1)
        last_day = date(year, month, monthrange(year, month)[1])

        context["events"] = Event.objects.filter(
            starts_at__date__gte=first_day,
            starts_at__date__lte=last_day,
        ).order_by("starts_at")

        context["calendar_year"] = year
        context["calendar_month"] = month

        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"
    context_object_name = "event"


class ModeratorOrAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role
            in ("moderator", "administrator")
        )


class EventCreateView(ModeratorOrAdminMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_form.html"
    success_url = reverse_lazy("events:event_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EventUpdateView(ModeratorOrAdminMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event_form.html"
    success_url = reverse_lazy("events:event_list")


class EventDeleteView(ModeratorOrAdminMixin, DeleteView):
    model = Event
    template_name = "event_confirm_delete.html"
    success_url = reverse_lazy("events:event_list")
