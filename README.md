# 📚 Kaviya's Bookstore

A serverless e-commerce web application built using AWS services.
This project demonstrates a microservices architecture with separate services for Products, Cart, and Orders, deployed using AWS Lambda, API Gateway, DynamoDB, S3, and CloudFront.

## 🚀 Features
📖 View available books (Product Service)
🛒 Add / update / delete items in cart (Cart Service)
📦 Place orders and view order history (Order Service)
🌐 Static frontend hosted on S3 + CloudFront
⚡ Serverless backend using AWS Lambda
🔄 Fully RESTful API design
✅ Unit testing using pytest

## 🏗️ Architecture

Frontend (HTML/CSS/JS)
        ↓
CloudFront (CDN)
        ↓
S3 (Static Hosting)
        ↓
API Gateway (REST APIs)
        ↓
AWS Lambda (Microservices)
        ↓
DynamoDB (Database)

## 🧰 Tech Stack

Frontend: HTML, CSS, JavaScript
Backend: Python (AWS Lambda)
API: API Gateway (REST)
Database: DynamoDB
Infrastructure: Terraform
Hosting: S3 + CloudFront
Testing: pytest + unittest.mock

## 📂 Project Structure

bookstore-frontend-tf/
│
├── frontend/
│   ├── index.html
│   ├── products.html
│   ├── cart.html
│   └── orders.html
│
├── lambda/
│   └── src/
│       ├── product-service/
│       ├── cart-service/
│       └── order-service/
│
├── tests/
│   ├── test_cart_lambda.py
│   ├── test_order_lambda.py
│   └── test_product_lambda.py
│
├── main.tf
├── provider.tf
├── outputs.tf

🧪 Running Tests

Install pytest:

py -m pip install pytest

Run tests:

py -m pytest -v

✔ Covers:

Cart Service (GET, POST, PUT, DELETE)
Order Service (GET, POST)
Product Service (GET)

## 📌 API Endpoints

Product Service
GET /products → Get all products
Cart Service
GET /cart → Get cart items
POST /cart → Add item
PUT /cart → Update quantity
DELETE /cart → Remove item
Order Service
POST /orders → Place order
GET /orders → View orders
