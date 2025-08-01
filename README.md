# ExchangeAppDjango

**ExchangeAppDjango** is a web application built with Django that provides a platform for users to exchange items. Users can create offers for their items and propose exchanges with other users, making trading easy and efficient.

## Features

- User registration and authentication  
- Create, view, edit, and delete personal items  
- Browse available items and filter by category  
- Create and manage exchange offers  
- Accept, reject, or delete exchange requests  
- Admin panel to manage users and items  
- Password recovery via phone number  
- Responsive and user-friendly interface  

## System Structure

The application is built on a client-server architecture with Django handling backend logic and a PostgreSQL/MySQL database for data storage. Users interact with the app via a clean web interface.

## Data Model

- **Users**: Stores user information including username, hashed password, and phone number.  
- **Items**: Contains details of items listed for exchange with fields like name, description, category, owner, and image.  
- **ExchangeOffers**: Tracks offers made between users, including offered item, requested item, sender, receiver, and status (new, accepted, rejected).

## Requirements

- Python 3.8+  
- Django 4.x  
- Database: PostgreSQL/MySQL (configured in settings.py)  
