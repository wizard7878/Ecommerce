from django.shortcuts import render,get_object_or_404,redirect
from .models import Item,OrderItem,Order
from django.views.generic import DetailView,ListView,View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django_countries.fields import CountryField
from .forms import CheckoutForm,CoponForm,RefundForm
from .models import BillingAddress,Payment,Copun,Refund,Category
# Create your views here.

import random
import string

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits,k=20))


class PaymentView(View):
    def get(self,*args,**kwargs):
        order_item = OrderItem.objects.filter(ordered=False,user=self.request.user).all()
        order = Order.objects.get(ordered=False,user=self.request.user)
        context = {
            'order':order,
            'orderitem':order_item,
            'ShowCoponForm': False
        }
        return render(self.request,'payment.html',context=context)

    def post(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)
        amount = order.get_total_item_all_price()

        payment = Payment()
        payment.Stripe_id = ''
        payment.user = self.request.user
        payment.amount = amount
        payment.save()

        order.ref_code = create_ref_code()
        order.ordered = True
        order.payment = payment
        order.save()

        messages.info(self.request,'Payment Successfully Done.')
        return redirect('/')

class checkout(View):

    def get(self,*args,**kwargs):
        orderItems = OrderItem.objects.filter(user=self.request.user,ordered=False).all()
        form = CheckoutForm()
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {
                'order':order,
                'orderitem':orderItems,
                'form': form,
                'coponForm':CoponForm(),
                'ShowCoponForm':True
            }
            return render(self.request,'checkout-page.html',context)
        except ObjectDoesNotExist:
            messages.info(self.request,'There is no active order!')
            context = {
 
                'form': form
            }
            return render(self.request, 'checkout-page.html', context)

    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)

            if form.is_valid():
                street_address = form.cleaned_data['street_address']
                apartment_address = form.cleaned_data['apartment_address']
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data['zip']
                payment_option = self.request.POST['payment_option']
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                print(self.request.POST)
                if self.request.POST['payment_option'] == 'S':
                    return redirect('payment',payment_option='stripe')
                else:
                    messages.info(self.request, 'Faild Checkout!')
                    return redirect('checkout')


        except ObjectDoesNotExist:
            messages.error(self.request,'You do not have an active order')
            return redirect('checkout')

class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'
    context_object_name = 'items'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Category'] = Category.objects.all()

        return context

def ShowCategoury(request,cate):

    item = Item.objects.filter(category__title=cate)

    context = {
        'items': item,
        'Category': Category.objects.all()
    }
    return render(request,'Filter_product_home_page.html',context)

class ItemDeatailView(DetailView):
    model = Item
    template_name = 'product-page.html'


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        item = OrderItem.objects.filter(user=self.request.user,ordered=False).all()
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {'items':item,
                   'order':order
                   }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You don't have an active order")
            return redirect('/')

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item,create = OrderItem.objects.get_or_create(user=request.user,item=item,ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'Item has been added to your cart')
        else:
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)

    return redirect('product',slug=slug)

@login_required
def delete_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)

    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(OrderItem.objects.get(user=request.user,item=item,ordered=False))
            try:
                OrderItem.objects.get(user=request.user,item=item,ordered=False).delete()
                messages.error(request, 'Your item has been removed from cart')

                return redirect('product',slug=slug)
            except ObjectDoesNotExist:
                messages.error(request, 'This item is not in your cart')
                return redirect('product',slug=slug)
        else:
            messages.error(request,'This item is not in your cart')
            return redirect('product',slug=slug)
    else:
        return redirect('product',slug=slug)



@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item = OrderItem.objects.filter(user=request.user,item=item,ordered=False)[0]
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(user=request.user,ordered=False,item__slug=item.slug).exists():

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, 'This item quantity was updated')
            else:
                order.items.remove(order_item)
                order_item.delete()



            return redirect('order-summary')
        else:

            return redirect('order-summary',slug=slug)
    else:
        messages.info(request,'You do not have this item')
        return redirect(
            'order-summary',slug=slug
        )



@login_required
def add_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item = OrderItem.objects.filter(user=request.user,ordered=False,item=item)[0]
    order_qs = Order.objects.filter(ordered=False,user=request.user)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=slug,user=request.user,ordered=False).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f'This item quantity was updated')
            return redirect('order-summary')
        else:
            messages.info(request, 'Item not found!')
            return redirect('order-summary',slug=slug)
    else:
        messages.info(request, 'You do not have this item')
        return redirect('order-summary',slug=slug)




@login_required
def delete_cart_summary(request,slug):
    item = get_object_or_404(Item,slug=slug)

    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(OrderItem.objects.get(user=request.user,item=item,ordered=False))
            try:
                OrderItem.objects.get(user=request.user,item=item,ordered=False).delete()
                messages.error(request, 'Your item has been removed from cart')
                return redirect('order-summary')
            except ObjectDoesNotExist:
                messages.error(request, 'This item is not in your cart')
                return redirect('order-summary')
        else:
            messages.error(request,'This item is not in your cart')
            return redirect('order-summary',slug=slug)
    else:
        return redirect('order-summary',slug=slug)


def get_copon(request,code):
    try:
        copon = Copun.objects.get(code=code)
        return copon
    except ObjectDoesNotExist:
        return redirect('checkout')


def add_copon(request):

    if request.method == 'POST':
        form = CoponForm(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data['code']
                order = Order.objects.get(user=request.user,ordered=False)
                order.copon = get_copon(request,code)
                order.save()
                messages.success(request, "Code Confirmed!")
                return redirect('checkout')

            except:
                messages.error(request, "This code has been expired.")
                return redirect('checkout')



class RequestRefundView(View):

    def get(self,*args,**kwargs):
        form = RefundForm()
        context = {
            'form':form
        }

        return render(self.request,'request_refund.html',context)

    def post(self,*args,**kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data['ref_code']
            message = form.cleaned_data.get('message')

            email = form.cleaned_data['email']
            try:
                order  = Order.objects.get(ref_code=ref_code)
                order.refund_request = True
                order.save()


                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.success(self.request, "Your request recevied.")
                return redirect('request-refund')

            except ObjectDoesNotExist:
                messages.success(self.request,"This Orderd dose not exist.")
                return redirect('request-refund')



