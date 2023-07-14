from typing import Any,Dict
from django.contrib import admin
from .models import DKBFile
from django.core.exceptions import ValidationError
from django import forms
from django.db.models import FileField
from .scripts.dkb import parser

class BadgeRuleForm(forms.ModelForm):
    class Meta:
        model = DKBFile
        fields = "__all__"

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        try:

            file:FileField = cleaned_data["file"]
        except:
            raise ValidationError("A file must be chosen!")

        if(not file.name.endswith(".dkb")):
            raise ValidationError("File extension should be 'dkb'")

        try:
            print(parser.parse(file.read().decode("utf-8")).pretty())
        except Exception as e:
            raise ValidationError("Syntax Error: "+str(e))

        return cleaned_data

class DkbFileAdmin(admin.ModelAdmin):
    form = BadgeRuleForm
    readonly_fields = ("id","created_by","created_at","updated_at")
    search_fields = ['pk', "title__icontains"]
    list_display = ['pk', "title","file"]
    save_as = True

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.created_by = request.user
        if obj.title == None:
            obj.title = obj.file.name.split('.')[0]
        
        return super().save_model(request, obj, form, change)

admin.site.register(DKBFile,DkbFileAdmin)

