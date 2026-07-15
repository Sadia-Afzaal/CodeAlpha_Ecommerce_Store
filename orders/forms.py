from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "postal_code",
            "country",
            "notes",
        )
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Jane Doe"}),
            "email": forms.EmailInput(attrs={"placeholder": "jane@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+1 555 010 1234"}),
            "address": forms.TextInput(attrs={"placeholder": "123 Market Street"}),
            "city": forms.TextInput(attrs={"placeholder": "San Francisco"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "94103"}),
            "country": forms.TextInput(attrs={"placeholder": "United States"}),
            "notes": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Delivery notes (optional)"}
            ),
        }
