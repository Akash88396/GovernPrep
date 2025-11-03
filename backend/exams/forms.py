# exams/forms.py
from django import forms

class CsvUploadForm(forms.Form):
    # File upload field
    csv_file = forms.FileField(label="Select CSV File")

    # Naye options (Append ya Replace)
    UPLOAD_CHOICES = [
        ("append", "Add new questions to the existing bank (Safe)"),
        ("replace", "Delete ALL old questions & mock tests and replace with this file (Dangerous)"),
    ]

    upload_type = forms.ChoiceField(
        choices=UPLOAD_CHOICES,
        widget=forms.RadioSelect, # Radio buttons ki tarah dikhayein
        initial="append", # Default mein "append" select rahega
        label="Select Upload Method"
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Full Name'
        })
    )
    mobile_number =forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your phone number'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email Address'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your Message',
            'rows': 5
        })
    )
    