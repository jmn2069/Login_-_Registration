# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 3:
            errors['first_name'] = "First name must be longer than 2 characters"
        elif not 'first_name' in errors and not re.match(NAME_REGEX, post_data['first_name']):
            errors['first_name'] = "First name must only contain letters"
        if len(post_data['last_name']) < 3:
            errors['last_name'] = "Last name must be longer than 2 characters"
        elif not 'last_name' in errors and not re.match(NAME_REGEX, post_data['last_name']):
            errors['last_name'] = "Last name must only contain letters"
        if len(post_data['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters"
        if post_data['pw'] != post_data['pw_confirm']:
            errors['pw'] = "Passwords do not match"
        if not 'email' in errors and not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = "Email is invalid"
        else:
            if len(self.filter(email = post_data['email'])) > 1:
                errors['email'] = 'Email address is already in use'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()