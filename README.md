# Django E-commerce Platform

An e-commerce platform built with **Django** and **Django REST Framework**, integrated with **ZarinPal Payment Gateway** for secure online payments.  
This platform allows admins to manage products, and customers can browse products, add items to their cart, and make purchases safely.




## Features

- Product catalog
- Shopping cart
- Order management
- Secure payment processing via ZarinPal
- User registration and login using JWT authentication




## Usage

- Customers can browse products, add items to the cart, adjust quantities, and make purchases securely via ZarinPal.
- Admins can manage products and monitor orders.

---

## Technologies Used

- Django
- Django REST Framework
- JWT Authentication
- ZarinPal Payment Gateway
- SQLite (or any preferred database)



## API Endpoints

### User & Authentication
| Endpoint | Method | Description |
|----------|--------|------------|
| `/api/register` | POST | Register a new user |
| `/api/token` | POST | Obtain JWT token for login |
| `/api/refresh` | POST | Refresh JWT token |

### Orders
| Endpoint | Method | Description |
|----------|--------|------------|
| `/api/order` | GET | List all orders of the logged-in user |
| `/api/order` | POST | Manage items: add, remove, update quantity, or mark as paid |
| `/api/order/<int:pk>` | GET | Get details of a specific order |

### Products
| Endpoint | Method | Description |
|----------|--------|------------|
| `/api/product/` | GET | List all products |
| `/api/product/` | POST | Add a new product (Admin only) |
| `/api/product/<int:pk>/` | GET | Retrieve a specific product |
| `/api/product/<int:pk>/` | PUT/PATCH | Update a product (Admin only) |
| `/api/product/<int:pk>/` | DELETE | Delete a product (Admin only) |

---

https://roadmap.sh/projects/ecommerce-api
