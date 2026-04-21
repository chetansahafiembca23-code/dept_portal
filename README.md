# 🏛️ CA-DEPT-HUB — Department Portal

> **Future Institute of Engineering and Management (FIEM), Kolkata**
> A full-featured departmental web portal built with Django — managing students, faculty, events, and more under one roof.

---

## 📌 Overview

**CA-DEPT-HUB** is the official department portal for the Computer Applications department at **FIEM, Kolkata**. It serves as a centralized hub for students, faculty, and administrators to manage academic activities, events, notices, and resources in a single unified platform.

---

## ✨ Features

- 👤 **User Management** — Student and faculty registration, login, and profile management
- 📅 **Events Module** — Create, manage, and display departmental events
- 💳 **Payment Integration** — Online fee / event payments via **Razorpay**
- 📄 **PDF Generation** — Generate receipts, reports, and documents using **ReportLab**
- 🖼️ **Media Uploads** — Profile pictures and document uploads powered by **Pillow**
- 🗄️ **Database** — SQLite for development (easily swappable for PostgreSQL/MySQL in production)
- 🌐 **Responsive UI** — HTML/CSS templates for a clean, accessible interface

---

## 🗂️ Project Structure

```
dept_portal/
│
├── config/          # Project settings, URLs, WSGI/ASGI config
├── core/            # Core app — homepage, notices, main logic
├── events/          # Events app — event listing, registration
├── users/           # Users app — auth, profiles, roles
├── templates/       # HTML templates (Jinja/Django templating)
├── media/           # User-uploaded files (images, documents)
├── manage.py        # Django management entry point
├── requirements.txt # Python dependencies
└── db.sqlite3       # SQLite database (dev only)
```

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, Django 6                  |
| Frontend   | HTML, CSS, JavaScript             |
| Database   | SQLite (dev) / PostgreSQL (prod)  |
| Payments   | Razorpay                          |
| PDF        | ReportLab                         |
| Images     | Pillow                            |

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/chetansahafiembca23-code/dept_portal.git
cd dept_portal

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser (admin)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 🔑 Environment Variables

Create a `.env` file in the root directory and configure the following:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

> ⚠️ Never commit your `.env` file or `SECRET_KEY` to version control.

---

## 🚀 Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Configure a production database (PostgreSQL recommended)
3. Run `python manage.py collectstatic`
4. Use a WSGI server like **Gunicorn** with **Nginx** as a reverse proxy

---

## 📦 Dependencies

```
Django==6.0.3
pillow==12.1.1
razorpay==2.0.1
reportlab==4.4.10
requests==2.32.5
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2025.3
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Chetan Saha**
BCA 2023 — Future Institute of Engineering and Management, Kolkata
[GitHub](https://github.com/chetansahafiembca23-code)

---

## 📄 License

This project is intended for academic and institutional use at FIEM, Kolkata.

---

<p align="center">Made with ❤️ at FIEM, Kolkata</p>
