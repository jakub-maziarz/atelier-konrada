# Atelier Konrada 

This project aimed to develop a web application that allows performing basic operations related to running an online store, such as accepting orders and managing the current offer.

[Live version](https://atelier-konrada.up.railway.app/)

## About The Project

![Atelier Konrada GIF](https://github.com/jakub-maziarz/atelier-konrada/blob/main/atelier-konrada-animation.gif)

The created application allows filtering and sorting of the available products that can be added to the virtual basket. After providing the data, the customer may place an order with the e-mail confirmation received. In addition, by subscribing to the weekly newsletter, the customer will receive notifications about new store offers. Store management is possible after logging in to the administration panel.

### Built With

* [![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
* [![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
* [![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)](https://jquery.com/)

## Getting Started

### Prerequisites

* Python (3.10)
* Database such as PostgreSQL or MySQL
* Redis

### Installation

1. Clone the repo
```sh
git clone https://github.com/jakub-maziarz/atelier-konrada.git
```

2. Create a virtual environment
```sh
python -m venv venv
```

3. Activate the virtual environment
```sh
venv\Scripts\activate
```

4. Install requirements
```sh
pip install -r requirements.txt
```

5. Set up a database (settings\base.py)
```python
DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'HOST': '',
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
    }
}
```
More on that topic [here](https://docs.djangoproject.com/en/3.2/ref/databases/)

6. Set up credentials for Gmail (settings\base.py)
```python
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
```
Getting credentials for an app is explained [here](https://www.benchatronics.com/detail/how-to-send-email-in-django-using-gmail)

7. Perform migrations
```sh
python manage.py migrate
```

8. Create a superuser account (for the admin page)
```sh
python manage.py createsuperuser
``` 

9. Run the Django server
```sh
python manage.py runserver
```

10. Run Celery worker (to execute tasks, i.e. sending emails)
```sh
celery -A atelier.celery worker --pool=solo -l INFO
```

11. Run Celery Beat (for scheduled tasks like a newsletter)
```sh
celery -A atelier beat -l INFO
```

## Usage

![atelier-konrada-usage-view](https://user-images.githubusercontent.com/118571317/204529208-6ea23714-8163-40c8-8008-727762e52f9e.png)

## Contact

Jakub Maziarz - [Linkedin](https://www.linkedin.com/in/j-maziarz/) - jakub.maziarz@outlook.com

Project Link: [https://github.com/jakub-maziarz/atelier-konrada](https://github.com/jakub-maziarz/atelier-konrada)

## Acknowledgments

* [Celery](https://docs.celeryq.dev/en/stable/)
* [Cloudinary](https://cloudinary.com/)
* [Django-Jazzmin](https://django-jazzmin.readthedocs.io/)
* [Font Awesome](https://fontawesome.com/)
* [iziToast](https://izitoast.marcelodolza.com/)
* [Railway](https://railway.app/)
* [Swiper](https://swiperjs.com/)
* [WhiteNoise](https://whitenoise.evans.io/en/latest/)
