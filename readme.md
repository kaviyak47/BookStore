<div align="center">

# 📚 BookStore — Serverless E-Commerce Platform

**A cloud-native, microservices-based bookstore application built on AWS**

[![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-purple?logo=terraform)](https://www.terraform.io/)

🌐 **Live Demo:** [https://d2zskisrlfiy3d.cloudfront.net](https://d2zskisrlfiy3d.cloudfront.net)  
📁 **Repository:** [https://github.com/kaviyak47/BookStore](https://github.com/kaviyak47/BookStore)

</div>

---

## 📌 Overview

BookStore is a fully serverless e-commerce application designed and deployed on AWS. Built as part of an internship project, it demonstrates real-world cloud engineering including microservices architecture, JWT-based authentication, role-based access control, and Infrastructure as Code using Terraform.

The application allows customers to browse books, manage a cart, and place orders while admins can manage the product catalog through protected APIs.

---

## 🏗️ Architecture

```
User
 │
 ▼
Amazon CloudFront (CDN)
 │
 ▼
Amazon S3 (Static Website Hosting)
 │
 ▼
Amazon API Gateway
 │
 ├── /auth      → Authentication Service
 ├── /products  → Product Service
 ├── /cart      → Cart Service
 └── /orders    → Order Service
                      │
                      ▼
                 AWS Lambda (Business Logic)
                      │
                      ▼
               Amazon DynamoDB (Data Layer)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python (AWS Lambda) |
| **API** | Amazon API Gateway |
| **Database** | Amazon DynamoDB |
| **Storage & CDN** | Amazon S3 + CloudFront |
| **Authentication** | JWT (JSON Web Tokens) |
| **Infrastructure** | Terraform |
| **CI / Dev Tools** | AWS CLI, Git, VS Code, Pytest |

---

## ✨ Features

### 👤 Customer
- User signup and login with JWT authentication
- Browse and search the full book catalog
- Add, update, and remove items from cart
- Place orders and view order history
- Manage personal profile

### 🔐 Admin
- JWT-based secure login
- Role-based access control (Admin / Customer)
- Add and manage products via protected APIs

---

## 🗂️ Project Structure

```
BookStore/
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── products.html
│   ├── cart.html
│   ├── orders.html
│   ├── profile.html
│   └── images/
│
├── lambda/
│   ├── auth-service/
│   ├── product-service/
│   ├── cart-service/
│   └── order-service/
│
├── tests/
└── terraform/
```

---

## 🗄️ Database Schema

### Users Table
| Attribute | Type | Key |
|-----------|------|-----|
| `email` | String | Primary Key |
| `name` | String | — |
| `password` | String | — |
| `role` | String | — |

### Products Table
| Attribute | Type | Key |
|-----------|------|-----|
| `id` | Number | Primary Key |
| `title` | String | — |
| `author` | String | — |
| `price` | Number | — |
| `image` | String | — |

### Cart Table
| Attribute | Type | Key |
|-----------|------|-----|
| `user_id` | Number | — |
| `product_id` | Number | — |
| `title` | String | — |
| `price` | Number | — |
| `quantity` | Number | — |

### Orders Table
| Attribute | Type | Key |
|-----------|------|-----|
| `orderId` | String | Primary Key |
| `user_id` | Number | — |
| `items` | List | — |
| `total` | Number | — |

---

## 🔄 Application Workflow

1. User visits the app — CloudFront serves assets from **S3**
2. User signs up or logs in — **Auth Service** validates and returns a **JWT token**
3. Frontend attaches the JWT to subsequent requests
4. **API Gateway** routes requests to the correct **Lambda microservice**
5. Lambda functions execute business logic and read/write from **DynamoDB**
6. Responses are returned to the frontend
7. Admin users access protected product management APIs via role-based authorization

---

## 🚀 Deployment

### Infrastructure (Terraform)
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Backend (AWS Lambda + API Gateway + DynamoDB)
Deployed automatically via Terraform. Lambda functions are packaged and deployed per microservice.

### Frontend (S3 + CloudFront)
Static assets are uploaded to S3 and served globally through CloudFront CDN.

---

## 🧪 Testing

Unit tests are written using **Pytest**.

```bash
py -m pytest -v
```

---

## 🛠️ Key Technical Challenges Solved

| Challenge | Solution |
|-----------|----------|
| API Gateway Routing | Configured path-based routing to Lambda microservices |
| DynamoDB Data Modeling | Designed partition keys and attribute structures per table |
| CORS Configuration | Enabled cross-origin headers on API Gateway and Lambda responses |
| CloudFront Cache Invalidation | Managed invalidations on frontend deployments |
| JWT Authentication | Implemented token generation, signing, and validation in auth service |
| Role-Based Authorization | Decoded JWT claims to enforce admin vs. customer access |

---

## 🔭 Future Enhancements

- [ ] Payment gateway integration
- [ ] Real-time order tracking
- [ ] Email notifications (SES)
- [ ] Analytics dashboard

---

## ☁️ AWS Services Used

`Amazon S3` · `Amazon CloudFront` · `Amazon API Gateway` · `AWS Lambda` · `Amazon DynamoDB` · `AWS IAM` · `Terraform`

---

## 👩‍💻 Author

**Kaviya K**  

## Project Summary

This project demonstrates a scalable serverless e-commerce platform built using AWS cloud services. It implements microservices architecture, JWT authentication, role-based authorization, Infrastructure as Code (Terraform), and cloud-native deployment practices.

---

