# E-Commerce Application API Documentation

This repository contains the backend APIs for a full-featured E-Commerce application.  
The APIs are built using Django and Django REST Framework (DRF) and follow **RESTful principles**.

---

## **Base URL**

/api/v1/

---

## **1. User / Authentication APIs**

Handles user accounts, login, registration, and profile management.

| API                       | Method    | Description                        | Status    |
|---------------------------|-----------|------------------------------------|-----------|
| `/users/register/`        | POST      | Register a new user                | Completed |
| `/users/login/`           | POST      | User login (returns token/session) | Completed |
| `/users/logout/`          | POST      | Logout user                        |           |
| `/users/profile/`         | GET       | Fetch user profile                 | Completed |
| `/users/profile/`         | PUT/PATCH | Update user profile                | Completed |
| `/users/password/change/` | POST      | Change password                    |           |
| `/users/password/reset/`  | POST      | Reset password via email           |           |

---

## **2. Product APIs**

Handles product listings, details, categories, and search.

| API                                                            | Method    | Description                                                       | Status    |
|----------------------------------------------------------------|-----------|-------------------------------------------------------------------|-----------|
| `/products/`                                                   | GET       | List all products (with filters, pagination, search) (Admin only) | Completed |
| `/products/`                                                   | POST      | Add new product (Admin only)                                      | Completed |
| `/products/search?name={name}`                                 | GET       | Get details of a products with that name                          | Completed |
| `/products/search?category={category}`                         | GET       | Get details of a products in that category                        | Completed |
| `/products/search?max_price={max_price}&min_price={min_price}` | GET       | Get details of a products with in price range                     | Completed |
| `/products/search?is_wishlist={is_wishlist}`                   | GET       | Get details of a products in wish list                            | Completed |
| `/products/`                                                   | PUT/PATCH | Update product (Admin only)                                       | Completed |
| `/products/`                                                   | DELETE    | Delete product (Admin only)                                       | Completed |
| `/categories/`                                                 | GET       | List all categories                                               | Completed |

---

## **3. Cart APIs**

Manage user carts and items in it.

| API                      | Method    | Description                       | Status    |
|--------------------------|-----------|-----------------------------------|-----------|
| `/cart/items/`           | GET       | View all items in the user’s cart | Completed |
| `/cart/items/`           | POST      | Add item to cart                  | Completed |
| `/cart/items/{item_id}/` | PUT/PATCH | Update quantity of an item        | Completed |
| `/cart/items/{item_id}/` | DELETE    | Remove an item from cart          | Completed |
| `/cart/clear/`           | POST      | Clear all items in the cart       | Completed |

---

## **4. Wishlist APIs**

Optional, allows users to maintain a wishlist.

| API                    | Method | Description               | Status    |
|------------------------|--------|---------------------------|-----------|
| `/wishlist/`           | GET    | View wishlist items       | Completed |
| `/wishlist/`           | POST   | Add item to wishlist      | Completed |
| `/wishlist/{item_id}/` | DELETE | Remove item from wishlist | Completed |

---

## **5. Order / Checkout APIs**

Handles checkout, orders, and order history.

| API                    | Method | Description                         | Status |
|------------------------|--------|-------------------------------------|--------|
| `/orders/`             | GET    | View all orders of a user           |        |
| `/orders/{id}/`        | GET    | Get details of a specific order     |        |
| `/orders/`             | POST   | Place a new order                   |        |
| `/orders/{id}/cancel/` | POST   | Cancel an order (before processing) |        |
| `/orders/{id}/status/` | GET    | Track order status                  |        |

---

## **6. Payment APIs**

Handles payment processing.

| API                   | Method | Description               |
|-----------------------|--------|---------------------------|
| `/payments/initiate/` | POST   | Initiate a payment        |
| `/payments/confirm/`  | POST   | Confirm payment status    |
| `/payments/history/`  | GET    | View user payment history |

---

## **7. Reviews & Ratings APIs**

Allows users to review and rate products.

| API                              | Method    | Description                        | Status |
|----------------------------------|-----------|------------------------------------|--------|
| `/products/{id}/reviews/`        | GET       | Get all reviews for a product      |        |
| `/products/{id}/reviews/`        | POST      | Add a review (Authenticated users) |        |
| `/products/reviews/{review_id}/` | PUT/PATCH | Update review (Author only)        |        |
| `/products/reviews/{review_id}/` | DELETE    | Delete review (Author or Admin)    |        |

---

## **8. Admin / Management APIs**

Admin-only APIs for managing products, categories, orders, and users.

| API                          | Method          | Description                                        | Status |
|------------------------------|-----------------|----------------------------------------------------|--------|
| `/admin/products/`           | POST/PUT/DELETE | Manage products                                    |        |
| `/admin/orders/`             | GET             | View all orders                                    |        |
| `/admin/orders/{id}/status/` | PUT/PATCH       | Update order status (shipped, delivered, canceled) |        |
| `/admin/users/`              | GET             | View all users                                     |        |
| `/admin/users/{id}/`         | PATCH/DELETE    | Manage user account (ban, delete, etc.)            |        |

---

## **9. Optional Features**

- **Notifications:** `/notifications/` (GET, POST)
- **Coupons / Discounts:** `/coupons/` (GET, POST)
- **Shipping / Address Management:** `/addresses/` (GET, POST, PUT, DELETE)
- **Analytics (Admin):** `/admin/reports/` (GET)

---

## **API Best Practices**

1. Use **HTTP methods** to indicate action (`GET`, `POST`, `PUT/PATCH`, `DELETE`).
2. API URLs are **resource-based**, not action-based.
3. Implement **authentication & permissions** (JWT / Token / Session).
4. Use **pagination, filtering, and search** for product and order listings.
5. Standardize **response structure**:

```json
{
    "success": true,
    "data": {},
    "message": "Operation completed successfully."
}
