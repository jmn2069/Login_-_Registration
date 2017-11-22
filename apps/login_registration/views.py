# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

import bcrypt

from django.contrib.messages import error

from django.contrib import messages

from .models import User

def index(request):
    print "Indexing"
    return render(request, "login_registration/index.html")

def create(request):
    print "creating new user"
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    # break before hashing pw if issue with reg info
    pw_hash = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())

    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash,
    )
    user = User.objects.last()
    id = user.id
    return redirect(success, id)

def success(request, id):
    print "successful login"
    user = User.objects.get(id = id)
    return render(request, 'login_registration/success.html', {"user" : user})

def login(request):
    print "attempting login"
    try:
        user = User.objects.get(email = request.POST['email'])
    except:
        print "excepting"
        messages.add_message(request, messages.INFO, "The email address or password are incorrect")
        return redirect('/')
    if bcrypt.checkpw(request.POST['pw'].encode(), user.password.encode()):
        id = user.id
        return redirect(success, id)
    messages.add_message(request, messages.INFO, "The email address or password are incorrect")
    return redirect(index)


