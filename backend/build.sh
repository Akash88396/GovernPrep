#!/usr/bin/env bash
# exit on error
set -o errexit

# Poetry (agar use kar rahe hain)
# pip install poetry
# poetry install

# Pip (jo hum use kar rahe hain)
pip install -r requirements.txt

# Static files ko collect karein
python manage.py collectstatic --no-input

# Database migrations ko apply karein
python manage.py migrate
```

---
### **Phase 2: Project ko GitHub par Daalna**

1.  **GitHub.com** par jaiye aur ek naya account banayein (agar nahi hai).
2.  Ek **"New repository"** (naya folder) banayein. Ise `governprep-backend` jaisa koi naam dein.
3.  Repository ko **"Private"** select karein. Yeh bahut zaroori hai.
4.  Ab apne local computer par terminal kholein aur project folder mein jaakar yeh commands chalaaiye:
    ```bash
    git init
    git add .
    git commit -m "First commit: Project ready for deployment"
    git branch -M main
    git remote add origin https://github.com/aapka_username/governprep-backend.git
    git push -u origin main
    
