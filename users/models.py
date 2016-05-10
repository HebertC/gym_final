"""
This file contains models for application
"""

from __future__ import unicode_literals

from django.db import models
# import default user model to this file
from django.contrib.auth.models import User


TRAINER_SPECIALIZATIONS = (
    ('B', 'Body Building'),
    ('F', 'Fitness'),
    ('CF', 'Cross fit')
)

# this manager returns only trainers
class TrainerManager(models.Manager):
    def get_queryset(self):
        return super(TrainerManager, self).get_queryset().filter(
            user__is_staff=True).exclude(user__username='admin')


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(choices=TRAINER_SPECIALIZATIONS, blank=False, max_length=3)

    objects = TrainerManager()

    class Meta:
        db_table = 'trainer'

    def __unicode__(self):
        return unicode('<Trainer: {} ({})>'.format(self.user.email, self.specialization))


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, default=None, null=True)

    class Meta:
        db_table = 'client'

    def __unicode__(self):
        """
        This method return string representation of this model
        :return:
        """
        return unicode('<Client {}>'.format(self.user.email))


# this is model for message to trainer
class ChatMessage(models.Model):
    _from = models.ForeignKey(User, related_name='_from')
    _to = models.ForeignKey(User, related_name='_to')
    datetime = models.DateTimeField(auto_now=True, null=False)
    message = models.CharField(max_length=4096, null=False)

    @property
    def from_user(self):
        return self._from

    class Meta:
        db_table = 'chat_message'

    def __unicode__(self):
        return unicode(self._from + ' to ' + self._to + ' ({}) '.format(self.datetime))

# this models describes workouts, which trainers assign to clients
class Workout(models.Model):
    client = models.ForeignKey(Client, null=False)
    trainer = models.ForeignKey(Trainer, null=False)
    start_date = models.DateField(null=False)
    duration = models.PositiveIntegerField(default=1, null=False)
    description = models.CharField(max_length=4096, null=False)


# this is model for message to trainer
class TrainerMessage(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now=True, null=False)
    message = models.CharField(max_length=1024, null=False)


    def __unicode__(self):
        return unicode(self.user.email + ': ' + str(self.datetime.replace(microsecond=0, tzinfo=None)))



# this is model for weight record in the database
class Weight(models.Model):

    client = models.ForeignKey(Client)

    user = models.ForeignKey(User)

    weight = models.FloatField(db_index=True)
    date = models.DateField(null=False)

    class Meta:

        db_table = 'client_weight'

        db_table = 'user_weight'


    def __unicode__(self):
        """
        This method return string representation of this model
        :return:
        """

        return unicode('Weight: ' + unicode(self.client) + '-' + str(self.weight) + '-' + str(self.datetime))

        return unicode('Weight: ' + unicode(self.user) + '-' + str(self.weight) + '-' + str(self.datetime))

