from django.urls import path, include
from .views import HomeView,checkout,ItemDeatailView,add_to_cart

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('product/<slug>/',ItemDeatailView.as_view(),name='product'),
    path('Checkout/',checkout,name='checkout'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-card')

]