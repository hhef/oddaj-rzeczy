# Oddaj - Portfolio Project #2
> This application is for charity donations

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Status](#status)
* [Inspiration](#inspiration)
* [Contact](#contact)

## General info
This app is my portfolio project after programming bootcamp. I made it for additional course
Portfolio Lab. My job was to make backend with Python and some JavaScript in forms

## Technologies
* Python 3.7
* Django 2.2.6
* psycopg2-binary 2.8.3

## Setup
Create new virtualenv and install everything from requirements.txt. If you want
to use other database than this in this project, run populate_sript.py after migrate

## Code Examples
```python
def post(self, request, user_id):
    if "taken" in request.POST:
        taken_status = Donation.objects.get(id=request.POST.get("taken"))
        taken_status.is_taken = True
        taken_status.save()
    else:
        not_taken_status = Donation.objects.get(pk=request.POST.get("not-taken"))
        not_taken_status.is_taken = False
        not_taken_status.save()
    return render(request, 'user_profile.html')
```

## Features
List of features ready and TODOs for future development
* You can add charity and edit their status
* See the summary of bags given and supported organizations
* You can create user, edit profile, change password

To-do list:
* Change password with email
* Contact form

## Status
Project is _in progress_. I'm also doing other projects for my portfolio but I hope
I'll come back to this

## Inspiration
This is an app for pass Portfolio Lap course

## Contact
Created by [@hef](https://twitter.com/hef4rl) - feel free to contact me!