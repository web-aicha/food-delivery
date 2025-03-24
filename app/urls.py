from django.urls import path
from . import views

urlpatterns = [
    path('menu-item/all',views.getMenuItems,name="menuitems-all"),
    path('category/all',views.getCategory,name="category-all"),
    path('menu-item/get-by-category/<str:pk>',views.getMenuItemByCategory,name='menu-by-category'),
    path('cart/update', views.updateCart, name='update-cart'),
    path('cart/get-cart',views.getCart, name="get-cart"),
    path('cart/remove/<int:item_id>/',views.removeItem,name="remove-item"),
    path('delivery/information',views.placeOrder,name="place-order"),
    path('delivery/delivered/<int:id>/',views.markDelivered,name="mark-delivered"),
    
]
