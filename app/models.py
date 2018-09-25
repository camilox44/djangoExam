from django.db import models
import re, bcrypt
from datetime import datetime
# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+.-_]+@[a-zA-Z0-9+.-_]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, PostData):
        print('in our models', PostData)
        errors = {}

        #username validation
        if len(PostData['username']) < 1:
            errors['username'] = 'Username is required'
        elif len(PostData['username']) < 3:
            errors['username'] = 'Username must have 3 or more characters'
        #email validation
        if len(PostData['email']) < 1:
            errors['email'] = "Email is required"
        elif not EMAIL_REGEX.match(PostData['email']):
            errors['email'] = "Invalid Email"
        else:
            users = User.objects.filter(email=PostData['email'])
            if len(users) > 0:
                errors['email'] = "Email is already in use!"

        #age validation
        if len(PostData['datehired']) < 8:
            errors['datehired'] = "Please Enter Your Birthday"
        else:
            d = PostData['datehired']
            day = datetime.strptime(d, "%Y-%m-%d")
            if day > datetime.now():
                errors['datehired'] = "Invalid Hire Date"
        
        #password validation
        if len(PostData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if PostData['password'] != PostData['confirmpassword']:
            errors['confirmpassword'] = "Passwords don't match!"
        
        if len(errors) == 0:
            return User.objects.create(
                username=PostData['username'],
                email=PostData['email'],
                datehired=PostData['datehired'],
                password=bcrypt.hashpw(PostData['password'].encode(), bcrypt.gensalt()).decode()
            )
        else: 
            return errors
    def login(self, PostData):

        print("in our models", PostData)
        errors = {}
        #email validation
        if len(PostData['email']) < 1:
            errors['email'] ="Email is required to login"
        elif not EMAIL_REGEX.match(PostData['email']):
            errors['email'] = "Invalid Email"
        else:
            list_of_users_with_email = User.objects.filter(email=PostData['email'])
            if len(list_of_users_with_email) < 1:
                errors['email'] = "Email Not in use"

        #password validation
        if len(PostData['password']) < 8:
            errors['password'] = "Password must be 8 characters or longer"
        
        if len(errors) == 0:
            stored_password = list_of_users_with_email[0].password
            if not bcrypt.checkpw(PostData['password'].encode(),stored_password.encode()):
                errors['password'] = "Incorrect Password"
                return errors
            else:
                return list_of_users_with_email[0]
        else:
            return errors


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    datehired = models.DateTimeField()
    password = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add = True)
    # updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()


class ItemManager(models.Manager):
    def add_item(self, PostData, user_id):
        errors = {}
        print(PostData)
        if len(PostData['name']) < 0:
            errors['name'] = "Item Name Cannot Be Blank"
        elif len(PostData['name']) < 3:
            errors['name'] = "Item Name Needs At Least 3 Characters"
        if len(errors) == 0:
            return Item.objects.create(
                name = PostData['name'],
                user_id = user_id
            )
        else:
            return errors


class Item(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    addwish = models.ManyToManyField(User, related_name="addwish_items")

    objects = ItemManager()

