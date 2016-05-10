"""
This file contains forms for this application
"""

from django.forms import ValidationError, ModelForm, Form

from django.forms.fields import EmailField, CharField, FloatField, DateField, IntegerField
from django.core.validators import MinLengthValidator, EmailValidator

from users.models import Client
from users.models import User
from users.models import Weight
from users.models import Workout

from django.forms.fields import EmailField, CharField, FloatField, DateField
from django.core.validators import MinLengthValidator, EmailValidator

from users.models import User
from users.models import Weight



class WeightForm(ModelForm):
    """
    This form accepts weight and date from the user
    and creates new record in database if weight and date are valid
    """
    weight = FloatField(required=True)
    date = DateField(required=True)

    class Meta:
        model = Weight
        fields = ('date', 'weight')

    def clean_weight(self):
        """
        This method checks if weight is a positive value
        :return:
        """
        weight = self.cleaned_data['weight']
        if not weight or weight < 0.0:
            raise ValidationError('Only positive value.')
        return weight

    def save(self, commit=False):
        """

        This method save checks if record for submitted date exists. If exists,
        method throws validation error. Else, it creates records, but not saves
        it to database
        :param commit:
        :return:
        """
        record = Weight.objects.filter(date=self.cleaned_data['date']).first()
        if record:
            self.add_error('date', 'Record already exists for this date.')
            return None

        This method saves record to database
        :param commit:
        :return:
        """


        record = super(WeightForm, self).save(commit)
        return record




class LoginForm(Form):
    """
    This form validates login credentials
    """
    email = EmailField(required=True, max_length=255, validators=[EmailValidator()])
    password = CharField(required=True, max_length=255)



class TrainerLoginForm(Form):
    """
    This form validates trainer login credentials
    """
    username = CharField(required=True, max_length=255)
    password = CharField(required=True, max_length=255)




class RegistrationForm(ModelForm):
    """
    This form validates registration data and creates user in database
    """
    class Meta:
        model = User
        exclude = ('is_active', 'username', 'date_joined')

    email = EmailField(required=True, max_length=255, validators=[EmailValidator()])
    password = CharField(required=True, max_length=255, validators=[MinLengthValidator(limit_value=5)])
    password2 = CharField(required=True, max_length=255)

    def clean_password2(self):
        """
        This method checks if both passwords are equal
        :return:
        """
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise ValidationError("You must confirm your password.")
        if password != password2:
            raise ValidationError("Your passwords do not match.")
        return password2

    def save(self, commit=False):
        """
        This method checks if user with submitted email not exists. Is exists,
        method will add error message. In other case, method will create user
        in the database
        :param commit:
        :return:
        """
        user = User.objects.filter(email=self.cleaned_data['email']).first()
        if user:
            self.add_error('email', 'Email already registered.')
            return None

        user = super(RegistrationForm, self).save(commit)
        user.username = user.email
        user.set_password(user.password)
        user.save()

        client = Client()
        client.user = user
        client.save()
        return client

class AddWorkoutForm(ModelForm):
    start_date = DateField(required=True)
    duration = IntegerField(required=True)
    description = CharField(required=True, min_length=1)

    class Meta:
        model = Workout
        exclude = ('trainer',)

        return user

