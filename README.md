# Vendor-Management
Develop a Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

This Django-based Vendor Management System allows users to manage vendor profiles, track purchase orders, and evaluate vendor performance metrics. The system exposes RESTful API endpoints for seamless integration into various applications.

Table of Contents

1.Setup Instructions
->Requirements
->Installation
->Database Setup
->Run the Application

2.API Endpoints
->Vendor Profile Management
->Purchase Order Tracking
->Vendor Performance Evaluation
->Additional Technical Considerations

3.Testing
->Running Tests


-----------------------------------------------


1. Setup Instructions

Requirements
Python 3.11
Django 5.0
Django REST Framework 3.14.0

--Installation

Navigate to the project directory:
cd Vendor management

Create a virtual environment:
$virtualenv VendorManagement

Activate the virtual environment:
VendorManagement\Scripts\activate

Install dependencies:

Install django in ENV:
$ pip install django

Install restframework in env:
$ pip install djangorestframework

Database Setup
Apply database migrations:
python manage.py migrate

Create a superuser (for admin access):
python manage.py createsuperuser
Follow the prompts to set a username, email, and password.

Run the Application

Start the development server:
python manage.py runserver
The application will be accessible at http://127.0.0.1:8000/.



2. API Endpoints
1. Vendor Profile Management
Create a new vendor:
POST /api/vendors/
Create a new vendor profile with the provided information.

List all vendors:
GET /api/vendors/
Retrieve a list of all vendors.

Retrieve a specific vendor's details:
GET /api/vendors/{vendor_id}/
Retrieve details of a specific vendor using their unique id.

Update a vendor's details:
PUT /api/vendors/{vendor_id}/
Update details of a specific vendor using their unique id.

Delete a vendor:
DELETE /api/vendors/{vendor_id}/
Delete a specific vendor using their unique id.

2. Purchase Order Tracking

Create a purchase order:
POST /api/purchase_orders/
Create a new purchase order with the provided information.

List all purchase orders:
GET /api/purchase_orders/
Retrieve a list of all purchase orders.

Retrieve details of a specific purchase order:
GET /api/purchase_orders/{po_id}/
Retrieve details of a specific purchase order using its unique id.

Update a purchase order:
PUT /api/purchase_orders/{po_id}/
Update details of a specific purchase order using its unique id.

Delete a purchase order:
DELETE /api/purchase_orders/{po_id}/
Delete a specific purchase order using its unique id.

Acknowledge a purchase order:
PATCH /api/purchase_orders/{po_id}/acknowledge/
Acknowledge a purchase order, updating the acknowledgment_date.

3. Vendor Performance Evaluation

Retrieve a vendor's performance metrics:
GET /api/vendors/{vendor_id}/performance/
Retrieve performance metrics for a specific vendor.

3. Testing

Running Tests
Run the test suite to ensure the functionality and reliability of the endpoints:
python manage.py test
Add more testcases as you needed to test in test.py file.

To run the test suite in POSTMAN for your Django application, you can follow these steps:

Install POSTMAN:
If you haven't installed POSTMAN, download and install it from the official website.

Run Your Django Development Server:
Ensure that your Django development server is running. You can start it using the following command in your terminal:

python manage.py runserver

Open POSTMAN:
Open POSTMAN on your computer.

Create a New Request:

Click on the "New" button in POSTMAN to create a new request.
Choose the HTTP method (GET, POST, PUT, DELETE, etc.) based on the view you want to test.
Set the Request URL:

Set the request URL based on your Django development server and the API endpoint you want to test. For example:
For vendor list: http://localhost:8000/api/vendors/
For a specific vendor: http://localhost:8000/api/vendors/{vendor_id}/
For vendor performance: http://localhost:8000/api/vendors/{vendor_id}/performance/
For purchase orders list: http://localhost:8000/api/purchase_orders/
For a specific purchase order: http://localhost:8000/api/purchase_orders/{po_id}/
For acknowledging a purchase order: http://localhost:8000/api/purchase_orders/{po_id}/acknowledge/

Set Headers:

If your views require authentication, you may need to set the Authorization header with the token.

To get the Authorization Token use the API endpoint as below:
For a Token: http://localhost:8000/api-token-auth/

For example:
Key: Authorization
Value: Token YOUR_TOKEN_HERE
Set Request Body:

For POST or PUT requests, you might need to set the request body. Ensure that the request body matches the expected format and structure.
Send the Request:

Click the "Send" button to send the request to your Django server.
Check the Response:

Check the response received from the server. Ensure that it matches your expectations.
Repeat for Other Endpoints:

Repeat the process for other API endpoints and methods.
Remember that this is a basic guide, and you may need to adapt it based on your specific API endpoints and authentication requirements. Also, make sure your application is properly configured to handle the authentication token for protected views.
