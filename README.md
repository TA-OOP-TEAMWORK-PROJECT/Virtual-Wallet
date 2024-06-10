# **PayTheBills**

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
- [Documentation Link](#documentation-link)

## **Project Structure:**
The Virtual Wallet system is a comprehensive application designed to simplify financial management for users. It offers a robust set of features that allow users to manage their virtual wallets, perform various types of transactions, view transaction history, manage cards and contacts, and access the latest financial news.



### **Project Overview:**

| **Project Information** | **Diagram** |
|:---|:---:|
| <div style="text-align: left; width: 600px;">The Virtual Wallet project aims to provide an easy-to-use platform for managing personal finances. In today's fast-paced world, having a reliable and secure method for handling transactions and tracking expenses is crucial. This application caters to that need by offering a digital solution that is both powerful and user-friendly. The project was developed with the primary goal of simplifying financial management for users of all ages and technical backgrounds. By providing a comprehensive suite of tools and features, the Virtual Wallet ensures that users can stay on top of their finances with minimal effort.<br/><br/> **Importance:** <br/> - **Convenience:** Users can manage their finances from anywhere, at any time. The application's intuitive interface makes it easy for users to perform transactions, track expenses, and manage their accounts on the go. <br/> - **Security:** The application uses state-of-the-art security measures, including OAuth2 authentication and encrypted data storage, to ensure user data is protected. This commitment to security helps build trust with users and ensures their sensitive information is safe from unauthorized access. <br/> - **Efficiency:** Streamlined processes for sending and receiving money, managing cards, and organizing transactions make financial management more efficient. Users can quickly and easily handle their financial tasks, freeing up time for other important activities.<br/><br/> **Background:** <br/> This project was developed by Snezhana Petrova, Nikolay Stankov & Simeon Hristov, aiming to create a reliable and efficient financial management tool. The team focused on incorporating best practices in software development, including the use of modern frameworks and libraries, ensuring the application is maintainable and scalable. </div> | <img src="https://github.com/TA-OOP-TEAMWORK-PROJECT/Web-Project/assets/156197933/dc951363-153b-467e-a1d8-8c401acf806c" alt="Diagram" width="1400"/> |

**Key Features:**

- **User Management:** Users can register, login, and update their profiles. Admins can approve registrations and manage user accounts.
- **Card Management:** Users can add, view, update, and delete their credit/debit cards. Virtual cards can be used for online purchases.
- **Transactions:** Users can perform transactions within the app, including sending money to other users, transferring funds between their own accounts, and making bank transfers.
- **Recurring Transactions:** Users can set up and manage recurring transactions for regular payments.
- **Contact Management:** Users can maintain a list of contacts to streamline transactions with frequent recipients.
- **Financial News:** Users can stay updated with the latest financial news and top cryptocurrency prices.
- **Administrative Tools:** Admins can manage users, approve transactions, and oversee the application's operations.

**Why Use This Project:**

- **Free to Use:** The application is open-source and free for anyone to use.
- **User-Friendly:** The intuitive interface makes it easy for users of all tech-savviness levels to manage their finances.
- **Comprehensive Functionality:** From basic transactions to detailed financial news, the application covers all aspects of personal finance management.

**Interesting Functionality:**

- **Secure Authentication:** Uses OAuth2 for secure login and token-based authentication.
- **Virtual Cards for Online Purchases:** Users can create and use virtual cards specifically for online transactions, enhancing security.
- **Financial News Integration:** Provides real-time updates on financial news and cryptocurrency prices.
- **Recurring Transactions:** Automates regular payments, reducing the need for manual intervention.

**Conclusion:**

The Virtual Wallet application is a testament to the possibilities of digital financial management. With its comprehensive feature set, robust security measures, and user-friendly design, it is an invaluable tool for anyone looking to streamline their financial activities.





## **Database Schema**
![finaldatabase](https://github.com/TA-OOP-TEAMWORK-PROJECT/Virtual-Wallet/assets/156197933/082f2a84-daa1-481d-80a7-45572179cd59)

## Setup and Run Instructions
1. Clone the repository.
2. Run the database scripts to create and populate the database.
3. Configure the application settings (e.g., database connection, email service).
4. Check the [Required Packages](#required-packages) section for further instructions.
5. Run the application.

## Features

## *Public Part*

### **User Endpoints**

**Register User**
- Accepts user registration data.
- Username, email, phone number must be unique.
- Password needs to contain at least one digit, one uppercase, one lowercase, a special character and can't be less than 8 symbols long.

```http
POST /users/register HTTP/1.1
Host: 127.0.0.1:8001

JSON body:
{
    "username": "name",
    "password": "password",
    "email": "user@example.com",
    "first_name": "first_name",
    "last_name": "last_name",
    "phone_number": "123456789"
}
```

**Login User**
- Authenticates user and returns a token.

```http
POST /users/login HTTP/1.1
Host: 127.0.0.1:8001

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
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <token>

JSON response:
{
  "Username": "string",
  "Name": "string",
  "Email": "user@example.com",
  "Phone Number": "123456789"
}
```

**Get Account Details**

- Requires authentication.
- Responds with the authenticated user's account details, including wallet, cards, categories, contacts, and transactions.

```http
GET /users/details HTTP/1.1
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <token>

JSON response:
{
  "user": {
    "id": 0,
    "username": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com",
    "phone_number": "stringst",
    "role": "user",
    "hashed_password": "string",
    "is_blocked": true,
    "disabled": true
  },
  "wallet": {
    "id": 0,
    "amount": 0,
    "user_id": 0
  },
  "cards": [],
  "categories": [],
  "contacts": [],
  "transactions": []
}
```

**Update User Profile**

- Requires authentication.
- Allows the user to update their profile information. The fields of email and phone number must be unique.
- Password update has the same restrictions as when registering a new user.

```http
PUT /users/update HTTP/1.1
Host: 127.0.0.1:8001

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
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <token>

JSON response:
"Current balance = {amount} leva."
```

**Top Up Wallet**

- Requires authentication.
- Allows user to top up their wallet using a only a bank card. Can't top up using virtual card.

```http
POST /wallets/top-up HTTP/1.1
Host: 127.0.0.1:8001

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
- Allows user to withdraw money from their wallet to their bank card. Can't withdrawl money to a virtual card.

```http
POST /wallets/withdraw HTTP/1.1
Host: 127.0.0.1:8001

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
- Allows user to add a new unique bank card.
- All added bank cards must comply to the standards for VISA and MASTERCARD.

```http
POST /cards/add HTTP/1.1
Host: 127.0.0.1:8001

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
- Allows user to create a new unique virtual card, which complies with the standards for VISA and MASTERCARD.

```http
POST /cards/create HTTP/1.1
Host: 127.0.0.1:8001

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
Host: 127.0.0.1:8001

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
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <token>
```

## **Transaction Endpoints**

**View Transactions**

- Requires authentication.
- Responds with a list of transactions.

```http
GET /transactions/ HTTP/1.1
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <token>
```

**View Recurring Transactions**

- Requires authentication.
- Responds with a list of recurring transactions.

```http
GET /transactions/recurring HTTP/1.1
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <token>

JSON response:
{
  "1": {
    "Amount": 0,
    "Status": "confirmed or denied",
    "Date of next transfer": null,
    "Last transfer date": "2024-05-26",
    "Send to": "string"
  }
}
```

**Transfer to User**

- Requires authentication.
- Allows user to transfer money to another user.

```http
POST /transactions/{username} HTTP/1.1
Host: 127.0.0.1:8001

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
POST /transactions/in-app HTTP/1.1
Host: 127.0.0.1:8001

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
POST /transactions/bank-transfer HTTP/1.1
Host: 127.0.0.1:8001

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
POST /transactions/confirmation/{confirmation_id} HTTP/1.1
Host: 127.0.0.1:8001

JSON body:
{
    "is_confirmed": true
}
```

**Set In-App Recurring Transaction**

- Requires authentication.
- Allows user to set an in-app recurring transaction.

```http
POST /transactions/recurring/in-app HTTP/1.1
Host: 127.0.0.1:8001

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
POST /transactions/recurring/bank-transfer HTTP/1.1
Host: 127.0.0.1:8001

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
PUT /transactions/{transaction_id}/status HTTP/1.1
Host: 127.0.0.1:8001

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
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <token>

JSON response:
[
  {
    "id": 3,
    "contact_name": "example12",
    "email": "example12@example.com",
    "phone_or_iban": "0888445566"
  },
  {
    "id": 4,
    "contact_name": "example123",
    "email": "example123@example.com",
    "phone_or_iban": "0888445567"
  }
]
```

**Search Contacts**

- Requires authentication.
- Allows user to search for contacts.

```http
GET /contacts/search HTTP/1.1
Host: 127.0.0.1:8001

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
Host: 127.0.0.1:8001

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
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <token>

JSON body:
{
    "contact_name": "NASA",
    "contact_email": "NASA@example.com",
    "iban": "US12BUIN1234567890"
}
```

**Remove Contact**

- Requires authentication.
- Allows user to remove a contact.

```http
DELETE /contacts/remove HTTP/1.1
Host: 127.0.0.1:8001

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
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <token>
```

**Create Category**

- Requires authentication.
- Allows user to create a new category.

```http
POST /categories/ HTTP/1.1
Host: 127.0.0.1:8001

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
Host: 127.0.0.1:8001

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
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <admin_token>

JSON response:
[
  "sample",
  "sample1",
  "sample12",
  "sample123",
  "sample1234"
]
```

**Get User by Search Type**

- Requires admin authentication.
- Allows admin to search for a user by ID, username, email, or phone.

```http
GET /admin/users/{search_type}/{search_value} HTTP/1.1
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <admin_token>
```

**Get All Transactions**

- Requires admin authentication.
- Responds with a list of all transactions.

```http
GET /admin/transactions HTTP/1.1
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <admin_token>

JSON response:
[
  {
    "id": 9,
    "is_recurring": false,
    "amount": 200,
    "status": "confirmed",
    "message": null,
    "recurring_period": null,
    "recurring_date": null,
    "transaction_date": "2024-05-26",
    "wallet_id": 1,
    "receiver_id": 4,
    "contact_list_id": 1,
    "category_id": null
  },
  {
    "id": 10,
    "is_recurring": false,
    "amount": 200,
    "status": "confirmed",
    "message": null,
    "recurring_period": null,
    "recurring_date": null,
    "transaction_date": "2024-05-26",
    "wallet_id": 4,
    "receiver_id": 4,
    "contact_list_id": null,
    "category_id": null
  }
]
```

**Get Pending Transactions**

- Requires admin authentication.
- Responds with a list of all pending transactions.

```http
GET /admin/transactions/pending HTTP/1.1
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <admin_token>
```

**Approve User**

- Requires admin authentication.
- Allows admin to approve a user.

```http
POST /admin/approve/{user_id} HTTP/1.1
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <admin_token>
```

**Deny Pending Transaction**

- Requires admin authentication.
- Allows admin to deny a pending transaction.

```http
POST /admin/transactions/deny/{transaction_id} HTTP/1.1
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <admin_token>
```

**Block User**

- Requires admin authentication.
- Allows admin to block a user.

```http
PUT /admin/block/{user_id} HTTP/1.1
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <admin_token>
```

**Unblock User**

- Requires admin authentication.
- Allows admin to unblock a user.

```http
PUT /admin/unblock/{user_id} HTTP/1.1
Host: 127.0.0.1:8001

Headers:
Authorization: Bearer <admin_token>
```

## *Optional Features*

## **Financial News Endpoints**

**Get Top 10 Cryptocurrencies**

- Responds with the top 10 cryptocurrencies.

```http
GET /Finance/top10cryptos HTTP/1.1
Host: 127.0.0.1:8001
```

**Get Financial News**

- Responds with the latest financial news.

```http
GET /Finance/news HTTP/1.1
Host: 127.0.0.1:8001
```

## Required Packages
**To run this project, you need to install the following packages:**

- `fastapi`: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- `passlib`: A password hashing library for Python 2 & 3, which provides cross-platform implementations of over 30 password hashing algorithms.
- `jose`: A JavaScript Object Signing and Encryption (JOSE) library for Python, which allows you to encode and decode JSON Web Tokens (JWT).
- `mariadb`: A Python client library for MariaDB/MySQL, which allows Python programs to connect to a MariaDB or MySQL database.
- `pydantic`: Data validation and settings management using Python type annotations.
- `starlette`: A lightweight ASGI framework/toolkit, which is ideal for building high-performance asyncio services.
- `pytest`: A framework that makes it easy to write simple tests.
- `oauth2`: An implementation of OAuth 2.0 for secure authorization.

**Note:** Ensure you have Python 3.11 or later installed on your system.

**You can install these packages using pip:**

```http
pip install fastapi passlib jose mariadb pydantic starlette pytest pytest-aiohttp pytest-asyncio httpx oauth2 pytest-mocker python-multipart
```

## Links
- [Swagger Documentation](http://127.0.0.1:8001/redoc)
