from django.contrib import admin

from userapp.models import User


class UserViewAdmin(admin.ModelAdmin):
    list_display = ('__str__',)

    def save_model(self, request, obj, form, change):
        if change:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
            obj.save()
        else:
            obj.set_password(obj.password)
            super().save_model(request, obj, form, change)


admin.site.register(User, UserViewAdmin)
