"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin


from django.views.generic import RedirectView


from users.views import LoginView
from users.views import RegistrationView
from users.views import LogoutView
from users.views import DashboardView
from users.views import SendTrainerMessageView

from users.views import IndexView
from users.views import TrainerLoginView
from users.views import TrainerDashboardView
from users.views import SendClientMessageView
from users.views import GetUserChatView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^trainers/login/$', TrainerLoginView.as_view(), name='trainer-login-view'),
    url(r'^trainers/dashboard/$', TrainerDashboardView.as_view(), name='trainer-dashboard-view'),
    url(r'^trainers/send-client-message/$', SendClientMessageView.as_view(), name="send-client-message"),
    url(r'^trainers/get-user-chat/$', GetUserChatView.as_view(), name='get-user-chat-view'),


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^users/login/$', LoginView.as_view(), name='login-view'),
    url(r'^users/logout/$', LogoutView.as_view(), name='logout-view'),
    url(r'^users/registration/$', RegistrationView.as_view(), name='registration-view'),
    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard-view"),
    url(r'^dashboard/send-trainer-message/$', SendTrainerMessageView.as_view(), name="send-trainer-message"),

    url(r'^$', IndexView.as_view(), name='index')

    url(r'^$', RedirectView.as_view(url='users/login/'))

]
