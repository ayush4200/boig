from ninja import ModelSchema


# a User Schema

from django.contrib.auth.models import User
from ninja.orm import create_schema

UserOutSchema = create_schema(User, fields=['id', 'username', 'first_name', 'last_name', 'email'])
