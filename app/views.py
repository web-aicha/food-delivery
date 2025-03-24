from django.shortcuts import render
from .models import MenuItem,Category,Cart,CartItem,Delivery
from .serializers import MenuItemSerializer,CategorySerializer,DeliverySerializer,CartSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.decorators import permission_classes
import json
from rest_framework import status
# Create your views here.



@api_view(["GET"])
@permission_classes([AllowAny])
def getMenuItems(request):
    data = MenuItem.objects.all()
    serialized_data = MenuItemSerializer(data, many=True)
    return Response(serialized_data.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def getCategory(request):
    data = Category.objects.all()
    serialized_data = CategorySerializer(data, many=True)
    return Response(serialized_data.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def getMenuItemByCategory(request, pk):
    category = Category.objects.get(id=pk)
    data = MenuItem.objects.filter(category=category)
    serialized_data = MenuItemSerializer(data, many=True)
    return Response(serialized_data.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateCart(request):
    user = request.user
    data = request.data

    try:
        cart = Cart.get_or_create_cart(user)
        menu_item = MenuItem.objects.get(id=data['menu_item_id'])
        cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)

        if data['quantity'] > 0:
            cart_item.quantity = data['quantity']
            cart_item.save()
        else:
            cart_item.delete()

        # Refresh cart details
        cart_items = CartItem.objects.filter(cart=cart)
        cart_data = [
            {
                "menu_item_id": item.menu_item.id,
                "name": item.menu_item.name,
                "price": item.menu_item.price,
                "quantity": item.quantity,
                "image": item.menu_item.image.url if item.menu_item.image else "",
            }
            for item in cart_items
        ]

        return Response({
            "success": True,
            "message": "Cart updated successfully",
            "cart_items": cart_data,
            "cart_subtotal": cart.subtotal,
            "cart_delivery_fee": cart.delivery_fee,
            "cart_total": cart.total,
        })
    except MenuItem.DoesNotExist:
        return Response({"success": False, "error": "Item not found"}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"success": False, "error": str(e)}, status=500)
    
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def removeItem(request, item_id):
    user = request.user
    try:
        cart = Cart.objects.filter(user=user, is_ordered=False).first()
        if not cart:
            return Response({"success": False, "error": "No active cart found."}, status=404)

        # Search using menu_item_id instead of CartItem ID
        cart_item = CartItem.objects.filter(cart=cart, menu_item_id=item_id).first()
        if not cart_item:
            return Response({"success": False, "error": "Item not found in the cart."}, status=404)

        cart_item.delete()
        cart.update_totals()

        return Response({"success": True, "message": "Item removed from cart."})
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCart(request):
    try:
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        cart_data = [
            {
                "menu_item_id": item.menu_item.id,
                "name": item.menu_item.name,
                "price": item.menu_item.price,
                "quantity": item.quantity,
                "image": item.menu_item.image.url if item.menu_item.image else "",
            }
            for item in cart_items
        ]

        return Response({
            "success": True,
            "cart_items": cart_data,
            "cart_subtotal": cart.subtotal,
            "cart_delivery_fee": cart.delivery_fee,
            "cart_total": cart.total,
        })

    except Cart.DoesNotExist:
        return Response({"success": False, "error": "Cart not found"}, status=404)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)
    
    
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def placeOrder(request):
    user = request.user

    # Get the cart for the user
    cart = Cart.objects.filter(user=user, is_ordered=False).first()
    if not cart:
        return Response({"success": False, "error": "No active cart found"}, status=status.HTTP_400_BAD_REQUEST)

    # If GET request, return cart information
    if request.method == "GET":
        cart_data = CartSerializer(cart).data
        return Response({"success": True, "cart": cart_data})

    # If POST request, place order
    data = request.data
    delivery_data = {
        "cart": cart.id,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "email": data.get("email"),
        "street": data.get("street"),
        "city": data.get("city"),
        "state": data.get("state"),
        "zip_code": data.get("zip_code"),
        "country": data.get("country"),
        "phone": data.get("phone"),
    }

    serializer = DeliverySerializer(data=delivery_data)
    if serializer.is_valid():
        serializer.save()
        cart.is_ordered = True
        cart.save()
        cart.delete()

        return Response({"success": True, "message": "Order placed successfully.", "delivery_id": serializer.data["id"]}, status=status.HTTP_201_CREATED)
    else:
        return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
@permission_classes([IsAdminUser])
def markDelivered(request, id):
    try :
        delivery = Delivery.objects.get(id=id)
    except Delivery.DoesNotExist:
        return Response({"success":False,"error":"Delivery not found "},status=status.HTTP_404_NOT_FOUND)
    
    delivery.is_delivered = True
    delivery.save()
    delivery.delete()
    delivery.cart.delete()
    
    return Response({"success":True,"message":"delivery mark as delivered and delevery and cart deleted "})
        
        
    