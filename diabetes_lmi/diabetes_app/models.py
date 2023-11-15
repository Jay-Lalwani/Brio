from django.db import models

class DiabetesPrediction(models.Model):
    user_input = models.JSONField()
    probability = models.FloatField()

