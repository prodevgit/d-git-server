from django.contrib.auth.models import User
from django.core.management import BaseCommand

from access_control.models import Role

USERS = [
    {'fname':'Dev','lname':'Admin','email':'prodevonline@gmail.com','username':'dev','password':'admin'},
    {'fname':'DevD','lname':'Beinex','email':'devd.beinex@gmail.com','username':'devdbeinex','password':'admin'},
    {'fname':'Developer','lname':'DevD','email':'developerdevd@gmail.com','username':'developer','password':'admin'}
]


class Command(BaseCommand):
    help = "Add Users to database"

    def handle(self, *args, **options):
        for user in USERS:
            user_obj = User.objects.create_user(user['username'], user['email'], user['password'])
            user_obj.first_name = user['fname']
            user_obj.last_name = user['lname']
            user_obj.save()
