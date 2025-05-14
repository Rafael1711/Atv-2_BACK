from django.urls import path
from . import views

urlpatterns = [
    path('instruments/', views.instrument_list),
    path('instruments/<int:id>/', views.instrument_detail),
]
