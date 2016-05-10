from django.contrib import admin

from users.models import Trainer
from users.models import User
from users.models import Workout
from users.models import Client

class TrainerAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(TrainerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].queryset = User.objects.filter(
            is_staff=True).exclude(username='admin')
        return form


admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Workout)
admin.site.register(Client)

from users.models import TrainerMessage


admin.site.register(TrainerMessage)

