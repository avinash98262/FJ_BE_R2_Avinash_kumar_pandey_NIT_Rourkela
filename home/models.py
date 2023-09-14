from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Define choices for the expense_type field
TYPE = (
    ('Positive', 'Positive'),
    ('Negative', 'Negative')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    income = models.FloatField(default=20000)
    expenses = models.FloatField(default=0)
    balance = models.FloatField(blank=True, null=True,default=20000)

# Create a Profile object when a new user is registered
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, income=0, expenses=0, balance=0)

# Save the Profile object when a user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Expense(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    expense_type = models.CharField(max_length=100 , choices=TYPE)
    
    
    def __str__(self):
        return self.name
    