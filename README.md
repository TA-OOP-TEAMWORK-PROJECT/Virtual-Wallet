# **Virtual Wallet Backend with FastAPI**

## Project Description:
This project aims to create a secure and efficient Virtual Wallet System backend using FastAPI, offering a modern RESTful API for various client applications.

## Table of Contents
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Setup and Run Instructions](#setup-and-run-instructions)
- [Features](#features)
  - [Public Part](#public-part)
  - [Registered Users](#registered-users)
  - [Administrative Part](#administrative-part)
  - [Optional Features](#optional-features)
- [Required Packages](#required-packages)
- [Links](#links)

## **Project Structure:**
The system allows users to manage their virtual wallet, perform transactions, view transaction history, manage cards and contacts, and access financial news.

## **Database Schema**
![finaldatabase](https://github.com/TA-OOP-TEAMWORK-PROJECT/Virtual-Wallet/assets/156197933/082f2a84-daa1-481d-80a7-45572179cd59)

## Setup and Run Instructions
1. Clone the repository.
2. Run the database scripts to create and populate the database.
3. Configure the application settings (e.g., database connection, email service).
4. Check the [Required Packages](#required-packages) section for further instructions.
5. Run the application.

## **Rest assured, the API meets modern standards and offers a comprehensive set of functionalities, including:**

## Features

## *Public Part*

### **User Endpoints**

**Register User**
- Accepts user registration data.
- Ensures that at least one user property is unique for login purposes.

```http
POST /users/register HTTP/1.1
Host: 127.0.0.1:8000

JSON body:
{
    "username": "name",
    "password": "password",
    "email": "samplemail@someting.com",
    "first_name": "first_name",
    "last_name": "last_name",
    "phone_number": "123456789"
}
```

**Login User**
- Authenticates user and returns a token.
```http
POST /users/login HTTP/1.1
Host: 127.0.0.1:8000

Form data:
{
    "username": "name",
    "password": "password"
}
```

## *Registered Users*

**View User Profile**
- Requires authentication.
- Responds with the authenticated user's profile details.

```http
GET /users/ HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>
```

**Get Account Details**

- Requires authentication.
- Responds with the authenticated user's account details, including wallet, cards, categories, contacts, and transactions.

```http
GET /users/details HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>
```

**Update User Profile**

- Requires authentication.
- Allows the user to update their profile information.

```http
PUT /users/update HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "email": "newemail@example.com",
    "phone_number": "987654321",
    "password": "newpassword"
}
```

### **Wallet Endpoints**

**Get Wallet Balance**

- Requires authentication.
- Responds with the authenticated user's wallet balance.

```http
GET /wallets/balance HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>
```

**Top Up Wallet**

- Requires authentication.
- Allows user to top up their wallet using a card.

```http
POST /wallets/top-up HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "card_id": 1,
    "amount": 100.0
}
```

**Withdraw Money from Wallet**

- Requires authentication.
- Allows user to withdraw money from their wallet to a card.

```http
POST /wallets/withdraw HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "card_id": 1,
    "amount": 50.0
}
```

## **Card Endpoints**

**Add Card**

- Requires authentication.
- Allows user to add a new card.

```http
POST /cards/add HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "number": "4242424242424242",
    "expiration_date": "2026-12-31",
    "cvv": 123
}
```

**Create Virtual Card**

- Requires authentication.
- Allows user to create a new virtual card.

```http
POST /cards/create HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "number": "4242424242424242",
    "expiration_date": "2026-12-31",
    "cvv": 123
}
```

**Online Purchase with Virtual Card**

- Requires authentication.
- Allows user to make an online purchase using a virtual card.

```http
POST /cards/virtual/online-purchases HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "card_id": 1,
    "amount": 100.0
}
```

**Delete Card**

- Requires authentication.
- Allows user to delete a card.

```http
DELETE /cards/delete/{card_id} HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>
```

## **Transaction Endpoints**

**View Transactions**

- Requires authentication.
- Responds with a list of transactions.

```http
GET /transactions/ HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>
```

**View Recurring Transactions**

- Requires authentication.
- Responds with a list of recurring transactions.

```http
GET /transactions/recurring HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>
```

**Transfer to User**

- Requires authentication.
- Allows user to transfer money to another user.

```http
POST /transactions/{username} HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "amount": 100.0
}
```

**New In-App Transaction**

- Requires authentication.
- Allows user to create a new in-app transaction.

 ```http
POST /transactions/new_transaction/in_app HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "amount": 100.0,
    "search": "username_or_email"
}
```

**New Bank Transfer**

- Requires authentication.
- Allows user to create a new bank transfer.

```http
POST /transactions/new_transaction/bank_transfer HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "contact_name": "John Doe",
    "contact_email": "john.doe@example.com",
    "iban": "BG12BUIN1234567890",
    "amount": 100.0
}
```

**Confirm Transfer**

- Confirms a pending transaction.

```http
POST /transactions/transfer-confirmation/{confirmation_id} HTTP/1.1
Host: 127.0.0.1:8000

JSON body:
{
    "is_confirmed": true
}
```

**Set In-App Recurring Transaction**

- Requires authentication.
- Allows user to set an in-app recurring transaction.

```http
POST /transactions/recurring/new-in-app HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "username": "receiver_username",
    "amount": 100.0,
    "recurring_period": 30,
    "recurring_date": "2024-06-01"
}
```

**Set External Recurring Transaction**

- Requires authentication.
- Allows user to set an external recurring transaction.

```http
POST /transactions/recurring/new-external HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "contact_name": "John Doe",
    "contact_email": "john.doe@example.com",
    "iban": "BG12BUIN1234567890",
    "amount": 100.0,
    "recurring_period": 30,
    "recurring_date": "2024-06-01"
}
```

**Update Transaction Status**

- Requires authentication.
- Allows user to update the status of a transaction.

```http
PUT /transactions/{transaction_id}/amount/status HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "new_status": "confirmed"
}

or

JSON body:
{
    "new_status": "denied"
}
```

## **Contact Endpoints**

**View Contacts**

- Requires authentication.
- Responds with a list of user contacts.

```http
GET /contacts/ HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>
```

**Search Contacts**

- Requires authentication.
- Allows user to search for contacts.

```http
GET /contacts/search HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

Query Parameters:
search: "search_term"
contact_list: true
```

**Add Contact From App**

- Requires authentication.
- Allows user to add a new contact.

```http
POST /contacts/add HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "contact_request": "contact_username"
}
```

**Add External Contact**

- Requires authentication.
- Allows user to add a new external contact.

 ```http
POST /contacts/add/external HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "contact_name": "John Doe",
    "contact_email": "john.doe@example.com",
    "iban": "BG12BUIN1234567890"
}
```

**Remove Contact**

- Requires authentication.
- Allows user to remove a contact.

```http
DELETE /contacts/remove HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "removed_user_id": 2
}
```

## **Category Endpoints**

**View Categories**

- Requires authentication.
- Responds with a list of categories.

```http
GET /categories/ HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>
```

**Create Category**

- Requires authentication.
- Allows user to create a new category.

```http
POST /categories/ HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>

JSON body:
{
    "title": "New Category"
}
```

**Link Transaction to Category**

- Requires authentication.
- Allows user to link a transaction to a category.

```http
POST /categories/{category_id}/transactions/{transaction_id} HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <token>
```

## *Administrative Part*

## **Admin Endpoints**

**Get All Users**

- Requires admin authentication.
- Responds with a list of all users.

```http
GET /admin/users HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <admin_token>
```

**Get User by Search Type**

- Requires admin authentication.
- Allows admin to search for a user by ID, username, email, or phone.

```http
GET /admin/users/{search_type}/{search_value} HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <admin_token>
```

**Get All Transactions**

- Requires admin authentication.
- Responds with a list of all transactions.

```http
GET /admin/transactions HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <admin_token>
```

**Get Pending Transactions**

- Requires admin authentication.
- Responds with a list of all pending transactions.

```http
GET /admin/transactions/pending HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <admin_token>
```

**Approve User**

- Requires admin authentication.
- Allows admin to approve a user.

```http
POST /admin/approve/{user_id} HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <admin_token>
```

**Deny Pending Transaction**

- Requires admin authentication.
- Allows admin to deny a pending transaction.

```http
POST /admin/transactions/deny/{transaction_id} HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <admin_token>
```

**Block User**

- Requires admin authentication.
- Allows admin to block a user.

```http
PUT /admin/block/{user_id} HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <admin_token>
```

**Unblock User**

- Requires admin authentication.
- Allows admin to unblock a user.

```http
PUT /admin/unblock/{user_id} HTTP/1.1
Host: 127.0.0.1:8000

Headers:
Authorization: Bearer <admin_token>
```

## *Optional Features*

## **Financial News Endpoints**

**Get Top 10 Cryptocurrencies**

- Responds with the top 10 cryptocurrencies.

```http
GET /Finance/top10cryptos HTTP/1.1
Host: 127.0.0.1:8000
```

**Get Financial News**

- Responds with the latest financial news.

```http
GET /Finance/news HTTP/1.1
Host: 127.0.0.1:8000
```

## Required Packages
**To run this project, you need to install the following packages:**

- fastapi: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- passlib: A password hashing library for Python 2 & 3, which provides cross-platform implementations of over 30 password hashing algorithms.
- jose: A JavaScript Object Signing and Encryption (JOSE) library for Python, which allows you to encode and decode JSON Web Tokens (JWT).
- mariadb: A Python client library for MariaDB/MySQL, which allows Python programs to connect to a MariaDB or MySQL database.
- pydantic: Data validation and settings management using Python type annotations.
- starlette: A lightweight ASGI framework/toolkit, which is ideal for building high-performance asyncio services.
- pytest: A framework that makes it easy to write simple tests.

**You can install these packages using pip:**

```http
pip install fastapi passlib jose mariadb pydantic starlette pytest pytest-aiohttp pytest-asyncio httpx
```

## Links
- [Swagger Documentation](#http://127.0.0.1:8001/redoc)
