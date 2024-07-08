"""Polls app models"""

from django.db import models
from django.contrib import admin


class Question(models.Model):
    """Question model"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    @admin.display
    def total_votes(self):
        """Return the total number of votes for the question"""
        return self.choice_set.aggregate(models.Sum('votes'))['votes__sum'] or 0


class Choice(models.Model):
    """Choice model"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
