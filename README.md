# Vendor Management System

## Overview
This is a set of REST APIs made using Django and Django Rest Framework for vendor management. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Tech Stack
- Django - Backend
- Django Rest Framework - for REST API creation
- Sqlite Database - for storing models

## Features
- Has three data models:
    1. Vendor - Details about each vendor and their performance metrics.
    2. PurchaseOrder - Captures the details of each purchase order.
    3. Performance - Stores historical data on vendor performance.
- Performance metrics are updated based on interactions recorded in the Purchase Order model in the vendor table.
- Historical performance is recorded once a week by an automatic scheduler that runs in the background using APScheduler.
- API endpoints are secured with token-based authentication.
- Utilized Django ORM for database interactions.

## Additional Features
- Logic for calculating metrics is optimized to handle large datasets.
- Django Signals are used to update metrics in real-time.
- Data integrity is maintained with the help of serializers.
- Historical Performance is auto-recorded for each vendor every week. This can be used for historical data analysis.
- Data is validated for Models.
- PEP 8 style guidelines are followed.
- Each API endpoint is documented.
- Test suite is added for all API points in tests.py.

## Important Files
<pre>
vendorMS 
|___vendorMS
|   |___ settings.py 
|   |___ urls.py
|   |___ scheduler.py
|___webapp
|   |___ models.py
|   |___ serializers.py
|   |___ urls.py
|   |___ signals.py
|   |___ tests.py
|   |___ views
|        |___ vendor_views.py
|        |___ purchase_order_views.py
|        |___ performance_views.py
|__db.sqlite3


`db.sqlite3` Database used in backend.
</pre>
#### In vendorMS directory

- `Settings.py` Has settings and configuration for this project.
- `urls.py` Contains the url configuration for the project.
- `scheduler.py` Contains a scheduler for updating vendor metrics periodically to the historical performance model.

#### In webapp directory

- `models.py` Contains the database models we used in this project.
- `serializers.py` Contains the serializers for all models which can be used to serialize and deserialize json data.
- `urls.py` Contains the url configuration for the Django app.
- `signals.py` Contains Django signals which will be triggered automatically during database operations.
- `tests.py` This is a test suit, which contains test cases for testing all API end points.

#### In views directory

- `vendor_views.py` This has views related to accessing Vendor model.
- `purchase_order_views.py` This has views related to accessing  PurchaseOrder model.
- `performance_views.py` This has views related to accessing Performance model.

## Installation
1. Clone the repository:
    ```
    git clone https://github.com/renuka010/vendorMS.git
    ```
2. Activate the virtual environment:
    ```
    python3 -m venv venv  # Create
    venv\Scripts\activate    # Activate
    ```
3. Change into the project directory:
    ```
    cd vendorMS
    ```
4. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
5. Create superuser:
    ```
    python manage.py createsuperuser
    ```
6. Run migrations:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```


## Test
To run automated tests use the following code in command line.
```
python manage.py test
```

You should see something as below in your command line after that.

```
Found 17 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.................
----------------------------------------------------------------------
Ran 17 tests in 4.247s

OK
Destroying test database for alias 'default'...
```

## Run
To run the project, use the below code in command line.
```
python manage.py runserver
```

## API end points
Use the below API code to access the data. I recommend using Postman. Copy and paste the following curl command in Postman to test the api.

To get authentication token, use the below command. `Replace the username and password` with the details of superuser created.

### Get /api/Token/

```
curl --location 'http://127.0.0.1:8000/api/token/' \
--header 'Content-Type: application/json' \
--data '{
    "username":"admin",
    "password":"adminpwd"
}'
```

For the remaining Api calls, `change the token` to your token and proceed.

### Get api/vendors -> List all vendors

```
curl --location 'http://localhost:8000/api/vendors' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74'
```

### POST /api/vendors/ -> Create a new Vendor

```
curl --location 'http://localhost:8000/api/vendors/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74' \
--data '{
    "name": "Dell",
    "contact_details": "Dell Complex, Banglore",
    "address": "Dell Complex, Banglore, 898989",
    "vendor_code": "YVU123XYZ"
}'
```

### Get api/vendors/{vendor_id}/ -> Retrieve a specific vendor's details

```
curl --location 'http://localhost:8000/api/vendors/1' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74'
```

### PUT /api/vendors/{vendor_id}/ -> Update a vendor's details

```
curl --location --request PUT 'http://localhost:8000/api/vendors/1/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74' \
--data '{
    "id": 1,
    "name": "Zeno Tech",
    "contact_details": "XYV Building, Block C,\r\nDelhi,\r\n123456",
    "address": "XYV Building, Block C,\r\nDelhi,\r\n123456",
    "vendor_code": "ABC123XYZ"
}'
```

### DELETE /api/vendors/{vendor_id}/ ->Delete a vendor

```
curl --location --request DELETE 'http://localhost:8000/api/vendors/6/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74'
```

### GET /api/purchase_orders/ -> List all purchase orders

```
curl --location 'http://localhost:8000/api/purchase_orders' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74'
```

### POST /api/purchase_orders/ ->Create a purchase order

```
curl --location 'http://localhost:8000/api/purchase_orders/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74' \
--data '{
        "po_number": "10",
        "order_date": "2024-05-01T11:30:00+05:30",
        "delivery_date": "2024-05-06T15:54:59+05:30",
        "items": {
            "Item": "Keyboards"
        },
        "quantity": 1000,
        "status": "pending",
        "quality_rating": null,
        "issue_date": "2024-05-01T11:30:00+05:30",
        "acknowledgment_date": null,
        "vendor": 1
    }'
```

### GET /api/purchase_orders/{po_id}/ -> Retrieve details of a specific purchase order

```
curl --location 'http://localhost:8000/api/purchase_orders/10/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74'
```

### PUT /api/purchase_orders/{po_id}/ ->Update a purchase order

```
curl --location --request PUT 'http://localhost:8000/api/purchase_orders/10/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74' \
--data '{
    "id": 10,
    "po_number": "10",
    "order_date": "2024-05-01T11:30:00+05:30",
    "delivery_date": "2024-05-06T15:54:59+05:30",
    "items": {
        "Item": "Wireless Keyboards"
    },
    "quantity": 1000,
    "status": "pending",
    "quality_rating": null,
    "issue_date": "2024-05-01T11:30:00+05:30",
    "acknowledgment_date": null,
    "vendor": 1
}'
```

### POST /api/purchase_orders/{po_id}/acknowledge -> Acknowledge a purchase order

```
curl --location --request POST 'http://localhost:8000/api/purchase_orders/7/acknowledge/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74'
```

### DELETE /api/purchase_orders/{po_id}/ -> Delete a purchase order

```
curl --location --request DELETE 'http://localhost:8000/api/purchase_orders/10/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74'
```

### GET /api/vendors/{vendor_id}/performance: -> Retrieve a vendor's historical performance metrics

```
curl --location 'http://localhost:8000/api/vendors/1/performance' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 794f692a64f63a949d082289414f3cc5e5061b74'
```