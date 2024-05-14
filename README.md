# Virtual Wallet

## Project Description
Virtual Wallet is a web application that enables users to manage their budgets. Users can send and receive money (user to user) and transfer money between their bank accounts and the Virtual Wallet (bank to app).

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
  - [Entities](#entities)
  - [Public Part](#public-part)
  - [Endpoints for Registered Users](#endpoints-for-registered-users)
  - [Administrative Part](#administrative-part)
  - [Optional Features](#optional-features)
  - [REST API - Summary](#rest-api---summary)
- [Technical Requirements](#technical-requirements)
  - [General](#general)
  - [Database](#database)
  - [Git](#git)
- [Setup and Run Instructions](#setup-and-run-instructions)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Database Relations](#database-relations)
- [Links](#links)

## Features

### Entities
#### Users
- **Must:**
  - Users can be regular users and admins.
  - Each user must have a username, password, email, and phone number. They may also have a photo.
  - Regular users must have credit/debit cards. The username for regular users cannot be amended.
  - Regular users must be able to register/login, view their credit information, transfer money between own credit/debit cards, transfer money to other users, confirm, deny, or view their transactions.
  - Admins can authorize regular users' registrations, deactivate access for users, and block accounts. Admins have predefined login details where only the password can be amended.
  
#### Credit/Debit Card
- **Must:**
  - Credit/debit card must have a number, expiration date, card holder, and a CVV number.
  - Users can register multiple credit/debit cards and transfer funds to and from their accounts.
  - Each card can have a personalized design.
  - Users can set up recurring transactions.
  - Users can create a contacts list to manage other users.
  - Users can categorize transactions and view reports for each category.

### Public Part
Accessible without authentication for anonymous users.
- **Must:**
  - Anonymous users can register and login.
  - Detailed information about Virtual Wallet and its features is available.

### Endpoints for Registered Users
Accessible only if the user is authenticated.
- **Must:**
  - Users can login/logout.
  - Users can view and update their profile (except the username).
  - Regular users can review their account and credit/debit cards, category list, contact list, and transaction history.
  - Users can register/delete credit/debit cards.
  - Users can create and manage a contacts list.
  - Users can make recurring transactions.
  - Users can categorize transactions and link them to categories.
  - Each transfer must go through a confirmation step.
  - The receiver of the money must be able to accept or decline the transaction.
  - Users can view a list of transactions with various filters and sorting options.

### Administrative Part
Accessible to users with administrative privileges.
- **Must:**
  - Admin users can approve registrations for regular users.
  - Admin users can manage users by searching and blocking/unblocking them.
  - Admin users can view and manage all user transactions.
  - Admin users can deny pending transactions.

### Optional Features
- **Should:**
  - Pagination and sorting support for search endpoints.
  - Email verification for user registration.
  - Email notifications with third-party services.
- **Could:**
  - Adding creative elements or Easter eggs.

### REST API - Summary
The REST API provides the following capabilities:
1. **Users**
   - **Must:**
     - CRUD Operations
     - Add/view/update/delete profile and credit/debit card
     - Search for users, accounts, transactions
     - Block/unblock users

2. **Transactions**
   - **Must:**
     - Add money to wallet
     - Make transactions
     - Approve/decline transactions
     - List transactions with filters and sorting
     - Withdraw

## Technical Requirements

### General
- **Must:**
  - Follow KISS, SOLID, DRY principles.
  - Use REST API design best practices.
  - Implement a tiered project structure.
  - Ensure at least 60% unit test code coverage for the service layer.
  - Implement proper exception handling and propagation.

### Database
- **Must:**
  - Use a relational database and normalize the data.
  - Include scripts to create and populate the database.

### Git
- **Must:**
  - Use meaningful commits that reflect project development and contributions.
  - Ensure contributions from all team members are evident.

## Setup and Run Instructions
1. Clone the repository.
2. Run the database scripts to create and populate the database.
3. Configure the application settings (e.g., database connection, email service).
4. Run the application.

## Project Structure
- Describe the directory structure and major components of the project.

## Technologies Used
- List the frameworks, libraries, and tools used in the project.

## Database Relations
- Include images or descriptions of the database schema and relationships.

## Links
- [Swagger Documentation](#)
- [Hosted Project](#)

---

**Note:** Replace placeholder links with actual URLs once available.
