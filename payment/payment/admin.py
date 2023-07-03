from django.contrib import admin
from .models import Item, Orders, Discount, Tax

admin.site.register(Item)
admin.site.register(Orders)
admin.site.register(Discount)
admin.site.register(Tax)
