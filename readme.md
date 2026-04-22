#  📚 Kaviya’s BookStore – Serverless E-Commerce App

A fully serverless bookstore web application built using AWS Cloud services.
This project demonstrates a real-world cloud architecture using API Gateway, Lambda, DynamoDB, S3, and CloudFront with a microservices approach.

---
## 🚀 Live Demo 

🔗 https://d2zskisrlfiy3d.cloudfront.net

---
## 🧩 Features

- 👤 User Signup & Login  
- 📖 View available books  
- 🛒 Add items to cart  
- ➕ Update quantity (+ / -)  
- ❌ Remove items from cart  
- ☑️ Select items using checkbox  
- 📦 Place order  
- 📜 View order history  
- 👤 User profile page  
- ⚡ Fully serverless backend

---

## 🏗️ Architecture Overview


+----------------------+
|    User (Browser)    |
+----------+-----------+
           |
           v
+----------------------+
|   CloudFront (CDN)   |
+----------+-----------+
           |
           v
+----------------------+
| S3 (Static Frontend) |
+----------+-----------+
           |
           v
+----------------------+
| API Gateway (REST)   |
+----+---------+-------+------+
     |         |              |
     |         |              |
     v         v              v
+---------+ +---------+   +---------+   +---------+
| Auth API| |Product  |   | Cart API|   |Order API|
+----+----+ |  API    |   +----+----+   +----+----+
     |      +----+----+        |              |
     v           |             v              v
+---------+      v         +---------+    +---------+
| Lambda  |  +---------+   | Lambda  |    | Lambda  |
+----+----+  | Lambda  |   +----+----+    +----+----+
     |       +----+----+        |              |
     v            |             v              v
+---------+       v         +---------+    +---------+
|DynamoDB |   +---------+   |DynamoDB |    |DynamoDB |
|(Users)  |   |DynamoDB |   | (Cart)  |    |(Orders) |
+---------+   |Products |   +---------+    +---------+
              +---------+





## ⚙️ Tech Stack

### Frontend
- HTML, CSS, JavaScript  
- Hosted on **Amazon S3**  
- Delivered via **CloudFront CDN**

### Backend
- **AWS Lambda (Python)**  
- **API Gateway (REST API)**  
- **DynamoDB (NoSQL Database)**  

### Dev Tools
- AWS CLI (SSO)  
- VS Code  
- Pytest (Unit Testing)  

---

## 🔗 API Endpoints

### 🔐 Auth
- POST https://iyueqkeyjh.execute-api.ap-southeast-1.amazonaws.com/dev/signup  
- POST https://iyueqkeyjh.execute-api.ap-southeast-1.amazonaws.com/dev/login  

---

### 📚 Products
- GET https://4vxmem30od.execute-api.ap-southeast-1.amazonaws.com/dev/products  

---

### 🛒 Cart
- GET https://u6t7qrzis6.execute-api.ap-southeast-1.amazonaws.com/dev/cart?user_id=1  
- POST https://u6t7qrzis6.execute-api.ap-southeast-1.amazonaws.com/dev/cart  
- PUT https://u6t7qrzis6.execute-api.ap-southeast-1.amazonaws.com/dev/cart  
- DELETE https://u6t7qrzis6.execute-api.ap-southeast-1.amazonaws.com/dev/cart  

---

### 📦 Orders
- POST https://e4q5pt4mri.execute-api.ap-southeast-1.amazonaws.com/dev/orders  
- GET https://e4q5pt4mri.execute-api.ap-southeast-1.amazonaws.com/dev/orders  

---

## 🗄️ Database Design

### Products Table
| Attribute | Type |
|----------|------|
| id | Number (PK) |
| title | String |
| price | Number |

### Cart Table
| Attribute | Type |
|----------|------|
| user_id | Number (PK) |
| product_id | Number (SK) |
| title | String |
| price | Number |
| qty | Number |

### Orders Table
| Attribute | Type |
|----------|------|
| orderId | String (PK) |
| user_id | Number |
| items | List |
| total | Number |

### Users Table
| Attribute | Type |
|----------|------|
| user_id | String (PK) |
| username | String |
| password | String |

---

## 🔄 Application Flow

1. User accesses the website via CloudFront  
2. Frontend loads from S3  
3. User logs in / signs up  
4. User interacts (view, cart, order)  
5. API Gateway routes requests to respective Lambda  
6. Lambda processes logic and interacts with DynamoDB  
7. Response is returned to frontend  

---

## 🧪 Unit Testing

Run tests using:

py -m pytest -v

## 🔐 Security
AWS SSO authentication (development access)
IAM roles for Lambda permissions
No hardcoded credentials

## 📦 Deployment
Frontend hosted on S3
CloudFront used as CDN
Backend deployed using Lambda + API Gateway
Cache invalidation handled after updates

## 💡 Challenges Faced
CORS configuration for PUT & DELETE
Cart quantity update issues
API Gateway routing errors
CloudFront caching old UI

## 📈 Future Enhancements
JWT Authentication
Role-based access (Admin/User)
Payment integration
Search & filtering
Order tracking

## 👩‍💻 Author

Kaviya K

## 📌 Conclusion

This project demonstrates a scalable serverless e-commerce application using AWS, implementing REST APIs, microservices architecture, and cloud-native design principles.
