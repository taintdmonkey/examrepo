from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import date, time, datetime


passwordRegex = re.compile(r'^(?=.{8,16}$)(?=.*[A-Z])(?=.*[0-9]).*$')
emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
nameRegex = re.compile(r'^(?=.{2,})([a-zA-z]*)$')
bdayRegex = re.compile(r'^[0-3]?[0-9].[0-3]?[0-9].(?:[0-9]{2})?[0-9]{2}$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) <  3:
            errors['first_name'] = "Your name must be 3 letters or more!"

        if len(postData['last_name']) < 3:
            errors['last_name'] = "Your last name must be 3 letters or more!"

        if not nameRegex.match(postData['first_name']):
            errors['last_name'] = "Your name can only contain letters!"
            
        if not nameRegex.match(postData['last_name']):
            errors['last_name'] = "Your name can only contain letters!"

        if str(date.today()) < str(postData['birthdate']):
            errors['birthdate'] = "Please input a valid date. Your birthdate needs to be before today's date."

        if not emailRegex.match(postData['email']):
            errors['email'] = "Your email is not a valid address!"

        if not passwordRegex.match(postData['pw']):
            errors['pw'] = "Your password must be between 8 and 16 characters in length and can only be comprised of letters and numbers!"

        if not postData['pw'] == postData['confpw']:
            errors['confpw'] = "Your passwords don't match!"
        return errors
        
        if len(errors) == 0:
            hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print "This is the hashed pw: ", hash1
            newUser = User.userMgr.create(first_name=first_name, last_name=last_name, birthdate=birthdate, email=email, password=hash1)
            return True, newUser

        else:
            return False, errors

    def log_validator(self, postData):
        user = self.filter(email=postData['email'])
        errors = {}
        password = postData['pw']
        if user:
            if not bcrypt.hashpw(postData['pw'].encode(), user[0].password.encode()) == user[0].password.encode():
                errors['pw'] = "Your email/password combo doesn't match!!"
                return errors
        else: 
            errors['email'] = "Your email does not exist in the database!"
            return errors

            # if destination AND start date match 

class TripManager(models.Manager):
    def trip_validator(self, postData):
        print str(date.today())
        print str(postData['start_date'])
        todays_date = datetime.strptime(str(date.today()), '%Y-%m-%d').strftime('%m/%d/%Y')
        print todays_date
        # if datetime.strptime(str(date.today()), '%Y-%m-%d').strftime('%m/%d/%Y')
        
        errors = {}
        if len(postData['start_date']) < 1:
            errors['start_date'] = 'Your trip needs a start date.'
        if len(postData['end_date']) < 1:
            errors['end_date'] = 'Your trip needs an end date. When you make millions you can have open-ended vacations.. Just not yet.'
        if todays_date > postData['start_date']:
            errors['trip'] = 'Please input a valid start date. The start date can\'t be in the past.'
        if datetime.strptime(str(date.today()), '%Y-%m-%d').strftime('%m/%d/%Y') > postData['end_date']:
            errors['trip'] = 'Please input a valid end date. No time travel here...'
        if postData['start_date'] > postData['end_date']:
                    errors['trip'] = 'No time travel here... your trip end date needs to be after your trip start date.'
        
        if len(postData['destination']) <  1:
            errors['destination'] = "Your name must be at least one letter!"
        if len(postData['itinerary_goal']) < 1:
            errors['itinerary_goal'] = "Your itinerary goal must be at least one letter!"
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    birthdate = models.DateTimeField(default=datetime.now)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __unicode__(self):
        return self.first_name

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    itinerary_goal = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    trip_creator = models.ForeignKey(User, related_name="trip_planner")
    users = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()