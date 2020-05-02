from django.contrib import admin
from .models import Item,Order,OrderItem,BillingAddress,Payment,Copun,Refund,Category
# Register your models here.



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ordered','being_delivered','received','refund_request','refund_granted','payment','copon']
    list_filter = ['user','ordered','being_delivered','received','refund_request','refund_granted']
    list_display_links = ['user','payment','copon']
    search_fields = ['user__username','ref_code']

    actions = ['make_refund_accepted',]

    def make_refund_accepted(self,request,queryset):
        queryset.update(refund_request=False, refund_granted=True)



    make_refund_accepted.short_description = "Update orders to refund granted."


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Copun)
admin.site.register(Refund)
admin.site.register(Category)