from django.shortcuts import render
from .models import Item
from django.views.generic import DetailView,ListView
# Create your views here.


def home(request):

    context = {
        'items' : Item.objects.all()
    }
    return render(request,'home-page.html',context)


def product(request):

    context = {
        'items' : Item.objects.all()
    }
    return render(request,'product-page.html',context)


def checkout(request):

    context = {
        'items' : Item.objects.all()
    }
    return render(request,'checkout-page.html',context)

class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'
    context_object_name = 'items'



class ItemDeatailView(DetailView):
    model = Item
    template_name = 'product-page.html'
    
    
