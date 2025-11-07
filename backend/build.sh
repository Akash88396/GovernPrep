
#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Pip se saare packages install karein
pip install -r requirements.txt

# 2. Static files ko collect karein
python manage.py collectstatic --no-input

# 3. Database mein badlav (migrations) apply karein
# Yeh tables banayega (jaise User table)
python manage.py migrate

# 4. Automatic Superuser Banane ka Naya Code
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')

if username and password and email and not User.objects.filter(username=username).exists():
    print(f"Creating superuser: {username}")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully.")
else:
    print("Superuser already exists or environment variables not set. Skipping.")
EOF

