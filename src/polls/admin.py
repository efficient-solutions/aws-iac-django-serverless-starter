"""Polls app admin"""

from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Choice inline forms"""
    model = Choice
    extra = 0
    max_num = 10


class QuestionAdmin(admin.ModelAdmin):
    """Question model admin"""
    list_display = ["question_text", "total_votes", "pub_date"]
    search_fields = ["question_text"]
    list_filter = ["pub_date"]
    fields = ["question_text", "pub_date"]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
