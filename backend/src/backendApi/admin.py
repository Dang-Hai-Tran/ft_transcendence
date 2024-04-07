from django.contrib import admin
from .models import User, Channel, Game, UserMessage, Otp

# Register your models here.
admin.site.register(User)
admin.site.register(Channel)
admin.site.register(Game)
admin.site.register(UserMessage)
admin.site.register(Otp)
