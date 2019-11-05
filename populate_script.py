"""This script will fill data base with a superuser, 10 users, 20 institutions and 20 donations. Superuser username
will be 'admin' and password will be 'password'. Run this script after migrations if you are using other database
than this in this project.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Oddaj.settings')
django.setup()

from django.contrib.auth.models import User
from charity.models import Category, Institution, Donation
from faker import Faker
import random


def create_superuser():
    superuser = User.objects.create_superuser('admin', 'admin@admin.com', 'password')
    superuser.save()


def create_users():
    faker = Faker()
    for _ in range(10):
        email = faker.email()
        password = 'password'
        first_name = faker.first_name()
        user = User.objects.create_user(username=email, password=password, first_name=first_name, email=email)
        user.save()


def create_categories():
    faker = Faker()
    for _ in range(10):
        name = faker.word(ext_word_list=None)
        Category.objects.create(name=name)


def create_institutions():
    faker = Faker()
    for _ in range(20):
        new_institutions = Institution.objects.create(name="Institution " + faker.word(ext_word_list=None),
                                                      description=faker.sentence(nb_words=6, variable_nb_words=True,
                                                                                 ext_word_list=None),
                                                      type=random.randint(1, 3))
        new_institutions.categories.set(random.sample(range(1, 10), 3))
        new_institutions.save()


def create_donations():
    faker = Faker()
    for _ in range(40):
        institution = Institution.objects.get(id=random.randint(1, 9))
        new_donation = Donation.objects.create(quantity=random.randint(1, 5),
                                               institution=institution,
                                               address=faker.street_name(),
                                               phone_number=random.randrange(10 ** 9),
                                               city=faker.city(),
                                               zip_code=faker.zipcode(),
                                               pick_up_date=faker.date(pattern="%Y-%m-%d", end_datetime=None),
                                               pick_up_time=faker.time(pattern="%H:%M", end_datetime=None),
                                               pick_up_comment=faker.sentence(nb_words=6, variable_nb_words=True,
                                                                              ext_word_list=None),
                                               user=User.objects.get(id=random.randint(1, 10)))
        new_donation.categories.set(institution.categories.all())
        new_donation.save()


create_superuser()
create_users()
create_categories()
create_institutions()
create_donations()
