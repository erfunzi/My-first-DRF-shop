# Pulse Shop Documentation

## Overview
Pulse Shop is an online store built with **Django 5.2** and **Django REST Framework**. It provides features such as user registration and login with two-factor authentication, product management, shopping cart, order processing, product reviews, and password recovery. This documentation aims to provide a comprehensive guide for developers and users to understand and interact with the system.

## Tech Stack
- **Language:** Python 3.13
- **Framework:** Django 5.2, Django REST Framework
- **Database:** PostgreSQL (with full-text search support)
- **Authentication:** Session-based with two-factor authentication via email
- **Dependencies:** Listed in `requirements.txt`

## Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd pulse_shop
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Configuration:**
   - Create a `.env` file in the project root with the following variables:
     ```
     SECRET_KEY=your-secret-key
     DEBUG=True
     EMAIL_HOST=smtp.gmail.com
     EMAIL_PORT=587
     EMAIL_USE_TLS=True
     EMAIL_HOST_USER=your-email@gmail.com
     EMAIL_HOST_PASSWORD=your-app-password
     ```
   - Replace `your-secret-key` with a secure key and configure email settings (e.g., Gmail App Password).
4. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the Server:**
   ```bash
   python manage.py runserver
   ```
   - Access the API at `http://127.0.0.1:8000/api/` and the admin panel at `http://127.0.0.1:8000/admin/`.

## Database Models
### 1. CustomUser
- **Fields:**
  - `username`, `email`, `mobile_number`, `password` (required)
  - `first_name`, `last_name`, `birth_date`, `national_code`, `profile_picture`, `job` (optional)
  - `invite_code` (unique), `wallet_balance` (default: 0.00)
- **Description:** Custom user model extending Django’s `AbstractUser`.

### 2. TwoFactorCode
- **Fields:** `user` (ForeignKey), `code` (6-digit), `created_at`, `expires_at`
- **Description:** Temporary code for two-factor authentication, valid for 10 minutes.

### 3. PasswordResetToken
- **Fields:** `user` (ForeignKey), `token` (UUID), `created_at`, `expires_at`
- **Description:** Token for password reset, valid for 1 hour.

### 4. Category
- **Fields:** `name` (unique), `parent` (self-referential), `image`, `is_active` (default: True)
- **Description:** Hierarchical structure for product categories.

### 5. Product
- **Fields:** 
  - `name`, `price`, `stock`, `discount` (default: 0.00)
  - `brand`, `size`, `color`, `is_active` (default: True)
  - `short_description`, `long_description`, `category` (ForeignKey), `main_image`
  - `search_vector` (for full-text search)
- **Description:** Product details with search capability.

### 6. ProductImage
- **Fields:** `product` (ForeignKey), `image`, `is_main` (default: False)
- **Description:** Additional images for products.

### 7. Cart
- **Fields:** `user` (ForeignKey), `product` (ForeignKey), `quantity` (default: 1), `created_at`
- **Constraints:** Unique together (`user`, `product`)
- **Description:** User’s shopping cart items.

### 8. Order
- **Fields:** 
  - `user` (ForeignKey), `created_at`, `updated_at`, `total_price`, `status`, `shipping_address`
- **Status Choices:** `pending`, `processed`, `shipped`, `delivered`, `canceled`
- **Description:** User’s orders.

### 9. OrderItem
- **Fields:** `order` (ForeignKey), `product` (ForeignKey), `quantity`, `price`
- **Description:** Items within an order, storing the price at the time of order.

### 10. Review
- **Fields:** 
  - `user` (ForeignKey), `product` (ForeignKey), `rating` (1-5), `comment`
  - `created_at`, `updated_at`, `is_approved` (default: False)
- **Constraints:** Unique together (`user`, `product`)
- **Description:** User reviews and ratings for products, only approved reviews are visible to regular users.

---

## API Endpoints
### Base URL: `http://127.0.0.1:8000/api/`

#### Accounts (`/accounts/`)
1. **Register (`POST /accounts/register/`)**
   - **Request:**
     ```json
     {
         "username": "testuser",
         "email": "test@example.com",
         "mobile_number": "09123456789",
         "password": "test1234",
         "first_name": "Ali",
         "last_name": "Rezaei"
     }
     ```
   - **Response:** `201 Created` - `"Registration successful"`

2. **Login (`POST /accounts/login/`)**
   - **Request:**
     ```json
     {
         "username": "testuser",
         "password": "test1234"
     }
     ```
   - **Response:** `200 OK` - `"Verification code sent to your email"`

3. **Verify Two-Factor Code (`POST /accounts/two-factor-verify/`)**
   - **Request:**
     ```json
     {
         "code": "483920"
     }
     ```
   - **Response:** `200 OK` - `"Login successful"`

4. **Logout (`POST /accounts/logout/`)**
   - **Authentication:** Required
   - **Response:** `200 OK` - `"Logout successful"`

5. **Profile (`GET/PUT /accounts/profile/`)**
   - **Authentication:** Required
   - **GET Response:** User profile data
   - **PUT Request:** 
     ```json
     {
         "first_name": "New Name"
     }
     ```
   - **PUT Response:** `200 OK` - `"Profile updated"`

6. **Password Reset Request (`POST /accounts/password-reset/`)**
   - **Request:**
     ```json
     {
         "email": "test@example.com"
     }
     ```
   - **Response:** `200 OK` - `"Reset link sent to your email"`

7. **Password Reset Confirm (`POST /accounts/password-reset-confirm/`)**
   - **Request:**
     ```json
     {
         "token": "550e8400-e29b-41d4-a716-446655440000",
         "new_password": "newpass123"
     }
     ```
   - **Response:** `200 OK` - `"Password changed successfully"`

#### Products and Orders (`/products/`)
1. **List Products (`GET /products/products/`)**
   - **Parameters:** `search` (optional, full-text search)
   - **Response:** List of products with approved reviews only (for non-staff users).

2. **Add to Cart (`POST /products/cart/`)**
   - **Authentication:** Required
   - **Request:**
     ```json
     {
         "product_id": 1,
         "quantity": 2
     }
     ```
   - **Response:** `201 Created`

3. **View Cart (`GET /products/cart/`)**
   - **Authentication:** Required
   - **Response:** List of cart items for the authenticated user.

4. **Create Order (`POST /products/orders/`)**
   - **Authentication:** Required
   - **Request:**
     ```json
     {
         "shipping_address": "Tehran, Test Street"
     }
     ```
   - **Response:** `201 Created` - Cart is cleared, and product stock is reduced.
   - **Error:** `400 Bad Request` - If cart is empty or stock is insufficient.

5. **List Orders (`GET /products/orders/`)**
   - **Authentication:** Required
   - **Response:** List of orders for the authenticated user.

6. **Add Review (`POST /products/reviews/`)**
   - **Authentication:** Required
   - **Request:**
     ```json
     {
         "product_id": 1,
         "rating": 4,
         "comment": "Good product!"
     }
     ```
   - **Response:** `201 Created`

7. **List User Reviews (`GET /products/reviews/`)**
   - **Authentication:** Required
   - **Response:** List of reviews by the authenticated user (approved and unapproved).

---

## Key Features
- **Authentication:** Session-based with two-factor authentication via email.
- **Reviews:** Regular users see only approved reviews (`is_approved=True`) in product details. Staff users see all reviews.
- **Stock Management:** Order creation reduces product stock, with checks for sufficient stock.
- **Email Integration:** Used for two-factor authentication and password reset (SMTP configuration required).

## Admin Panel
- **URL:** `http://127.0.0.1:8000/admin/`
- **Features:**
  - Manage users, products, orders, and reviews.
  - Approve or reject reviews (`is_approved` toggle).

## Notes
- **Permissions:** Most endpoints require authentication except registration and password reset requests.
- **Error Handling:** Returns meaningful error messages (e.g., insufficient stock, invalid code).
- **Scalability:** Uses PostgreSQL’s full-text search and atomic transactions for order processing.
