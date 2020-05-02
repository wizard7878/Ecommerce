from django.urls import path, include
from .views import HomeView,checkout,ItemDeatailView,\
    add_to_cart,delete_cart,OrderSummaryView,remove_single_item_from_cart,add_single_item_from_cart,\
    delete_cart_summary,PaymentView,add_copon,get_copon,RequestRefundView,ShowCategoury

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('product/<slug>/',ItemDeatailView.as_view(),name='product'),
    path('Checkout/',checkout.as_view(),name='checkout'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-card'),
    path('delete-from-cart/<slug>/',delete_cart,name='delete-from-card'),
    path('order-summary/',OrderSummaryView.as_view(),name='order-summary'),
    path('remove-single-from-quantity/<slug>/',remove_single_item_from_cart,name='remove-single-form-cart'),
    path('add-single-from-quantity/<slug>/',add_single_item_from_cart,name='add-single-form-cart'),
    path('delete-from-cart-summary/<slug>/',delete_cart_summary,name='delete-from-cart-summary'),
    path('payment/<payment_option>/',PaymentView.as_view(),name='payment'),
    path('add-copon/',add_copon,name='add-copon'),
    path('request-refund/',RequestRefundView.as_view(),name='request-refund'),
    path('Categouty-filter/<cate>/',ShowCategoury,name='filterCate'),
]