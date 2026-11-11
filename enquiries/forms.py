import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, inlineformset_factory

from catalogue.models import Category, Product

from .models import QuoteItem, QuoteRequest


class QuoteRequestForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput, max_length=0)

    class Meta:
        model = QuoteRequest
        fields = ("name", "company", "email", "phone", "location", "notes")
        labels = {"phone": "International phone", "notes": "Additional details (optional)"}
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "minlength": 2, "maxlength": 100}),
            "company": forms.TextInput(attrs={"autocomplete": "organization", "minlength": 2, "maxlength": 150}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "maxlength": 254}),
            "phone": forms.TelInput(attrs={"autocomplete": "tel", "placeholder": "+971…", "pattern": r"\+[1-9][0-9]{7,14}"}),
            "location": forms.TextInput(attrs={"autocomplete": "address-level2", "minlength": 2, "maxlength": 150}),
            "notes": forms.Textarea(attrs={"rows": 4, "maxlength": 5000}),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r"\+[1-9]\d{7,14}", phone):
            raise ValidationError("Enter an international phone number, for example +971…")
        return phone


class QuoteItemForm(forms.ModelForm):
    class Meta:
        model = QuoteItem
        fields = ("category", "product", "requested_product", "quantity", "unit")
        labels = {"requested_product": "Product requirements", "product": "Catalogue product (optional)"}
        widgets = {
            "requested_product": forms.TextInput(
                attrs={"placeholder": "Preferred brand, format or packaging", "maxlength": 500}
            ),
            "quantity": forms.NumberInput(attrs={"min": "0.01", "max": "100000000", "step": "any"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(published=True)
        self.fields["product"].queryset = Product.objects.filter(
            published=True, archived=False, category__published=True
        ).select_related("category")
        self.fields["product"].required = False

    def clean(self):
        cleaned = super().clean()
        category = cleaned.get("category")
        product = cleaned.get("product")
        if product and category and product.category_id != category.id:
            self.add_error("product", "Choose a product from the selected category.")
        if product and not cleaned.get("requested_product"):
            cleaned["requested_product"] = product.name
        return cleaned


class BaseQuoteItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        if not any(
            form.cleaned_data and not form.cleaned_data.get("DELETE")
            for form in self.forms
        ):
            raise ValidationError("Add at least one requested category or product.")


QuoteItemFormSet = inlineformset_factory(
    QuoteRequest,
    QuoteItem,
    form=QuoteItemForm,
    formset=BaseQuoteItemFormSet,
    extra=1,
    max_num=20,
    validate_max=True,
    can_delete=True,
)
