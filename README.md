# Qogita Address Book
Address Book API System

## Requirements
Python 3.9+
Django 4+

## Setup

1. Create virtualenv
2. ```pip install -r requirements.txt```
3. ```python manage.py migrate```
4. ```python manage.py createsuperuser```
5. ```python manage.py runserver```
6. ```curl -X POST http://127.0.0.1:8000/api-token-auth/ -d '{"username": "$SUPERUSER_USERNAME", "password": "$SUPERUSER_PASSWORD"}'  --header 'Content-Type: application/json'```

Either browse the API at ```http://127.0.0.1:8000/address``` or use CURL and the TOKEN to interact with the API:
1. List all addresses: ```curl -X GET http://127.0.0.1:8000/api/address/ -H 'Authorization: Token $TOKEN'```
2. Create an address ```curl -X POST http://127.0.0.1:8000/api/address -d '{ "street_number": "Test", "route": "Test", "locality_name": "Test", "locality_postal_code": "Test", "state_name": "Test", "state_code": "Test", "country_name": "Test", "country_code": "Test", "latitude": 31525.343, "longitude": 14234.34 }' -H 'Authorization: Token $TOKEN```

# Features
1. Authentication using Token
2. Create an address (unique constraint)
3. Get a list of all addresses
    - Filter and search by all the address fields with request params
    - Pagination for large number of addresses
4. Update an address
5. Delete an address

# Missing features
1. Setup using Docker
2. User client can hold state (for this requirment I couldn't figure out why this was necessary so I didn't implement it. To create a stateful connections I would use django-channels but we would need to discuss more about exactly why it would be needed)