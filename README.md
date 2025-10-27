# Restaurant API - Backend System
A Django REST API for managing restaurant operations including menu items, categories, shopping cart, and order delivery tracking.

## 🚀 Features
- Menu Management: Browse all menu items and categories

- Category Filtering: Get menu items by specific categories

- Shopping Cart: Full cart functionality (add, update, remove, view)

- Order System: Place orders and track delivery status

- Delivery Tracking: Mark orders as delivered


## 📸 Screens :

- Dashboard :
  * Header :
    ![Header](docs/screenshots/header.png)
  * Menu items :
    ![Menu Items](docs/screenshots/MenuItems.png)
  * Footer
    ![Footer](docs/screenshots/footer.png)
- Login Popup:
  ![Login](docs/screenshots/login.png)
- Cart :
  ![Cart](docs/screenshots/cart.png)
- Delivery Page :
  ![del](docs/screenshots/del.png)




## 📚 API Endpoints
- Menu Endpoints
  * GET /menu-item/all - Retrieve all menu items

  * GET /category/all - Get all menu categories

  * GET /menu-item/get-by-category/<str:pk> - Get menu items by category ID

- Cart Endpoints
  * POST /cart/update - Add or update items in cart

  * GET /cart/get-cart - Retrieve current cart contents

  * DELETE /cart/remove/<int:item_id>/ - Remove item from cart

- Order & Delivery Endpoints
  * POST /delivery/information - Place a new order

  * PATCH /delivery/delivered/<int:id>/ - Mark order as delivered

