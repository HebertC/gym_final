
import random



from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic.base import View
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from django.db.models import Q

from users.forms import RegistrationForm
from users.forms import LoginForm
from users.forms import TrainerLoginForm
from users.forms import WeightForm
from users.forms import AddWorkoutForm

from users.models import Weight
from users.models import ChatMessage
from users.models import Trainer
from users.models import Client
from users.models import Workout
from users.models import User


from users.forms import RegistrationForm
from users.forms import LoginForm
from users.forms import WeightForm

from users.models import Weight
from users.models import TrainerMessage


# this constant sets the number of weight records on the page
PAGE_LIMIT = 5


class LogoutView(View):
    def get(self, request):
        """
        This handler logout user from the website
        :param request:
        :return:
        """
        logout(request)

        if request.session.get('is_user'):
            del request.session['is_user']
        if request.session.get('is_trainer'):
            del request.session['is_trainer']

        return redirect('/')


class LoginView(View):
    template = 'users/login.html'
    form = LoginForm

    def get(self, request):
        # if user already logged in

        if request.user.is_authenticated() and request.session.get('is_user'):

        if request.user.is_authenticated():

            # redirect it to dashboard
            return redirect('dashboard-view')
        # render login page
        return render(request, self.template, {'form': self.form()})

    def post(self, request):
        # if user already logged in

        if request.user.is_authenticated() and request.session.get('is_user'):

        if request.user.is_authenticated():

            # redirect it to dashboard
            return redirect('dashboard-view')
        # fill form with form data from user
        form = self.form(request.POST)
        # create context dictionary
        context = {'form': form}

        # if form contains valid data
        if form.is_valid():
            # check if user exists in the database
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            # if user exists and password is valid
            if user:
                # login user to website
                login(request, user)

                request.session['is_user'] = True

                # and redirect to dashboard
                return redirect('dashboard-view')
            # else add error message for meail
            form.add_error('email', 'Email or password is wrong.')
        # render login form with errors
        return render(request, self.template, context)


class RegistrationView(View):
    template = 'users/registration.html'
    form = RegistrationForm

    def get(self, request):
        # if user is logged in

        if request.user.is_authenticated() and request.session.get('is_user'):

        if request.user.is_authenticated():

            # redirect to dashboard
            return redirect('dashboard-view')

        # create template context
        context = {
            'form': self.form()
        }
        # render registration form
        return render(request, self.template, context)

    def post(self, request):
        # if user is logged in

        if request.user.is_authenticated() and request.session.get('is_user'):

        if request.user.is_authenticated():

            # redirect to dashboard
            return redirect('dashboard-view')

        # populate form with registration data
        form = self.form(request.POST)
        # create template context dict
        context = {
            'form': form
        }

        # if form is not valid
        if not form.is_valid():
            # render form with error messages
            return render(request, self.template, context)


        # try to save client database
        client = form.save(commit=False)
        # if not saved
        if not client:
            # render form with errors
            return render(request, self.template, context)

        # assign random trainer to user
        trainer = random.choice(list(Trainer.objects.all()))
        client.trainer = trainer
        client.save()

        # try to save user to database
        user = form.save(commit=False)
        # if not saved
        if not user:
            # render form with errors
            return render(request, self.template, context)


        # create success message
        messages.add_message(request, message='You have successfully registered.', level=messages.SUCCESS)
        # redirect to login page
        return redirect('login-view')


class DashboardView(View):
    template = 'users/dashboard.html'
    form = WeightForm

    def get(self, request):
        # if user is not logged in

        if not request.user.is_authenticated() or not request.session.get('is_user'):

        if not request.user.is_authenticated():

            # redirect to login page
            return redirect('/')

        # get all weight records of current user

        weight_records = Weight.objects.filter(client=request.user.client).order_by('-date')

        weight_records = Weight.objects.filter(user=request.user).order_by('-date')

        # create paginator object
        paginator = Paginator(weight_records, PAGE_LIMIT)
        # get page number from request
        page = request.GET.get('page')

        try:
            # get records for specific page
            weight_records = paginator.page(page)
        except PageNotAnInteger:
            # on error - get records for first page
            weight_records = paginator.page(1)
        except EmptyPage:
            # or last page if page not exists
            weight_records = paginator.page(paginator.num_pages)

        chat_messages_filter = Q(_from=request.user) | Q(_to=request.user)
        chat_messages = ChatMessage.objects.filter(chat_messages_filter).order_by('-datetime')[:15]


        # create context
        context = {
            'form': self.form(),
            'weight_records': weight_records,
            # get number of sent messages to trainer

            'chat_messages': reversed(chat_messages),
            'workouts': Workout.objects.filter(client=request.user.client).all()

            'messages_count': len(TrainerMessage.objects.filter(user=request.user))

        }
        # render dashboard page
        return render(request, self.template, context)

    def post(self, request):
        # if user is not logged in

        if not request.user.is_authenticated() or not request.session.get('is_user'):

        if not request.user.is_authenticated():

            # redirect to login page
            return redirect('/')

        # fill form with weight data
        form = self.form(request.POST)

        # if form contains valid data
        if form.is_valid():

            # try to save it
            record = form.save()
            # if success
            if record:
                # save user to record
                record.client = request.user.client
                # update record in database
                record.save()
                # create success message
                messages.add_message(request, message='Weight record was added successfully.', level=messages.SUCCESS)
                # render dashboard page
                return redirect('dashboard-view')

        # get all weight records
        weight_records = Weight.objects.filter(client=request.user.client).order_by('-date')

            # if user has record for this date
            record = Weight.objects.filter(date=form.cleaned_data['date'], user=request.user).first()
            if not record:
                # try to save it
                record = form.save()
                # if success
                if record:
                    # save user to record
                    record.user = request.user
                    # update record in database
                    record.save()
                    # create success message
                    messages.add_message(request, message='Weight record was added successfully.', level=messages.SUCCESS)
                    # render dashboard page
                    return redirect('dashboard-view')
            # add error message for date field
            form.add_error('date', 'Record already exists for this date.')

        # get all weight records
        weight_records = Weight.objects.filter(user=request.user).order_by('-date')

        # create paginator object
        paginator = Paginator(weight_records, PAGE_LIMIT)
        # get page number
        page = request.GET.get('page')

        try:
            # get records for specific page
            weight_records = paginator.page(page)
        except PageNotAnInteger:
            # or for first page if error
            weight_records = paginator.page(1)
        except EmptyPage:
            # or last page
            weight_records = paginator.page(paginator.num_pages)


        chat_messages_filter = Q(_from=request.user) | Q(_to=request.user)
        chat_messages = ChatMessage.objects.filter(chat_messages_filter).order_by('-datetime')[:15]
        # create template context
        context = {
            'form': form,
            'chat_messages': reversed(chat_messages),
            'weight_records': weight_records,
            'workouts': Workout.objects.filter(client=request.user.client).all()

        # create template context
        context = {
            'form': form,
            'messages_count': len(TrainerMessage.objects.filter(user=request.user)),
            'weight_records': weight_records

        }

        # render dashboard
        return render(request, self.template, context)


class SendTrainerMessageView(View):
    def post(self, request):
        """
        This method saves trainer message to the database
        :param request:
        :return:
        """
        # get message from request
        message = request.POST.get('message')
        # create message

        ChatMessage.objects.create(
            message=message, _from=request.user, _to=request.user.client.trainer.user)
        # return response
        return HttpResponse('success')


# home page view
class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


# this view used to handle login for trainer user
class TrainerLoginView(View):
    template_name = 'trainers/login.html'
    form = TrainerLoginForm

    def get(self, request):
        context = {
            'form': self.form()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # if user already logged in
        if request.user.is_authenticated() and request.session.get('is_trainer'):
            # redirect it to dashboard
            return redirect('trainer-dashboard-view')
        # fill form with form data from user
        form = self.form(request.POST)
        # create context dictionary
        context = {'form': form}

        # if form contains valid data
        if form.is_valid():
            # check if user exists in the database
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            # if user exists and password is valid
            if user and user.is_staff:
                # login user to website
                login(request, user)
                request.session['is_trainer'] = True
                # and redirect to dashboard
                return redirect('trainer-dashboard-view')
            # else add error message for email
            form.add_error('username', 'Username or password is wrong.')
        # render login form with errors
        return render(request, self.template_name, context)


class TrainerDashboardView(View):
    template = 'trainers/dashboard.html'
    form = AddWorkoutForm

    def get(self, request):
        if not request.user.is_authenticated() or not request.session.get('is_trainer'):
            # redirect it to dashboard
            return redirect('/')

        context = {
            'clients': Client.objects.filter(trainer=request.user.trainer),
            'form': self.form()
        }

        return render(request, self.template, context)

    def post(self, request):
        if not request.user.is_authenticated() or not request.session.get('is_trainer'):
            # redirect it to dashboard
            return redirect('/')

        form = self.form(request.POST)

        context = {
            'clients': Client.objects.filter(trainer=request.user.trainer),
            'form': form
        }

        if form.is_valid():
            wo = form.save(commit=False)
            wo.client = Client.objects.get(pk=request.POST.get('client'))
            wo.trainer = request.user.trainer
            wo.save()

            messages.add_message(request, message='Workout was added successfully.', level=messages.SUCCESS)
            # render dashboard page
            return redirect('trainer-dashboard-view')

        return render(request, self.template, context)


class SendClientMessageView(View):
    def post(self, request):
        """
        This method saves trainer message to the database
        :param request:
        :return:
        """
        # get message from request
        message = request.POST.get('message')
        # create message
        ChatMessage.objects.create(
            message=message, _from=request.user, _to=User.objects.get(pk=request.POST.get('user_id')))
        # return response
        return HttpResponse('success')


class GetUserChatView(View):
    def get(self, request):
        user = User.objects.get(pk=request.GET.get('user_id'))

        chat_messages_filter = Q(_from=request.user) & Q(_to=user)
        chat_messages_filter |= Q(_from=user) & Q(_to=request.user)
        chat_messages = reversed(ChatMessage.objects.filter(chat_messages_filter).order_by('-datetime')[:15])

        return render(request, template_name='chat.html', context=dict(chat_messages=chat_messages))

        TrainerMessage.objects.create(message=message, user=request.user)
        # return response
        return HttpResponse('success')

