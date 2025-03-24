from django.contrib import admin
from .models import MenuItem,Category,Cart,CartItem,Delivery
# Register your models here.


admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)