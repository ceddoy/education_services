from django.contrib import admin

from trainingapp.admin import ResultAnswersInLine
from userapp.models import User


class UserViewAdmin(admin.ModelAdmin):
    fields = ('email', 'password', 'is_active', 'is_staff', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('email', 'is_active', 'is_staff', 'created_at', 'updated_at')
    search_fields = ('email',)
    inlines = (ResultAnswersInLine,)

    def save_model(self, request, obj, form, change) -> None:
        if change:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
            obj.save()
        else:
            obj.set_password(obj.password)
            super().save_model(request, obj, form, change)


admin.site.register(User, UserViewAdmin)
