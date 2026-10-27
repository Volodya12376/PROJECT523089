
from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "location",
            "starts_at",
            "ends_at",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Назва події",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Опис події",
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Місце проведення",
            }),
            "starts_at": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "ends_at": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["starts_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["ends_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["ends_at"].required = False
