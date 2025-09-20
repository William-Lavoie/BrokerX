from django.db import models

# The models will be accessed only through DAO, otherwise use entities
# i.e the model is only used to define the DB

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[("A", "Active"),
                                                      ("P", "Pending"),
                                                      ("R", "Rejected")
                                                    ])


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField()
