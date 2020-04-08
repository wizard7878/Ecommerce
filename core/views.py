from django.shortcuts import render,get_object_or_404,redirect
from .models import Item,OrderItem,Order
from django.views.generic import DetailView,ListView
from django.utils import timezone
# Create your views here.

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
    
    
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    oreder_item,created = OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            oreder_item.quantity += 1
            oreder_item.save()
        else:
            order.items.add(oreder_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(oreder_item)

    return redirect('product',slug=slug)


