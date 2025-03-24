from rest_framework import serializers
from .models import MenuItem,Category,CartItem,Cart,Delivery

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','image']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
        fields = ['id','name','category','price','description','rating','image']
        
class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only = True)
    menu_item_id = serializers.PrimaryKeyRelatedField(
        queryset = MenuItem.objects.all(), write_only = True, source ="menu_item"
    )
    
    class Meta:
        model = CartItem
        fields = ['id','menu_item','menu_item_id','quantity']
        
class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    
    class Meta :
        model = Cart
        fields = ['id','subtotal','delivery_fee','total','cart_items']
        
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"
        
        
