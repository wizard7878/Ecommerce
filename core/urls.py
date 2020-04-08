from django.urls import path, include
from .views import HomeView,checkout,ItemDeatailView

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('product/<slug>/',ItemDeatailView.as_view(),name='product'),
    path('Checkout/',checkout,name='checkout')
]