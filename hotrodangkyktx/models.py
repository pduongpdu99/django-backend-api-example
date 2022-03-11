import uuid
from django.db import models


# Create your models here.
class Room(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(null=True, max_length=50)
	status = models.IntegerField(null=True)
	createdat = models.DateTimeField(auto_now_add=True)
	updatedat = models.DateTimeField(auto_now=True)

class User(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	role = models.IntegerField(null=False)
	name = models.CharField(null=False, max_length=50)
	phonenumber = models.CharField(null=False, max_length=50)
	address = models.CharField(null=False, max_length=50)
	nationality = models.CharField(null=False, max_length=50)
	idcard = models.CharField(null=False, max_length=50)
	birth = models.DateTimeField(null=True)
	sex = models.IntegerField(null=False)
	roomid = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)
	createdat = models.DateTimeField(auto_now_add=True)
	updatedat = models.DateTimeField(auto_now=True)

class History(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	eventname = models.CharField(null=True, max_length=50)
	createdat = models.DateTimeField(auto_now_add=True)
	updatedat = models.DateTimeField(auto_now=True)
