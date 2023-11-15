from django.urls import path
from .views import predict_diabetes, result

urlpatterns = [
    path('predict/', predict_diabetes, name='predict_diabetes'),
    path('result/<str:probability>/', result, name='result'),
]
