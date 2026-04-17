# 📚 Kaviya’s BookStore – Serverless E-Commerce App

A fully serverless bookstore web application built using **AWS Cloud services**.  
This project demonstrates a real-world cloud architecture using **API Gateway, Lambda, DynamoDB, S3, and CloudFront**.

---

## 🚀 Live Demo

🔗 https://d2zskisrlfiy3d.cloudfront.net

---

## 🧩 Features

- 📖 View available books  
- 🛒 Add items to cart  
- ➕ Update quantity (+ / -)  
- ❌ Remove items from cart  
- ☑️ Select items using checkbox  
- 📦 Place order  
- 📜 View order history  
- ⚡ Fully serverless backend  

---

## 🏗️ Architecture Overview



User (Browser)
      │
      ▼
CloudFront (CDN)
      │
      ▼
S3 (Static Website)
      │
      ▼
API Gateway
  ├── Product API ── Lambda ── DynamoDB (Products)
  ├── Cart API    ── Lambda ── DynamoDB (Cart)
  └── Order API   ── Lambda ── DynamoDB (Orders)


---

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

### 📚 Products
GET https://4vxmem30od.execute-api.ap-southeast-1.amazonaws.com/dev/products

### 🛒 Cart
GET https://u6t7qrzis6.execute-api.ap-southeast-1.amazonaws.com/dev/cart?user_id=1  
POST https://u6t7qrzis6.execute-api.ap-southeast-1.amazonaws.com/dev/cart  
PUT https://u6t7qrzis6.execute-api.ap-southeast-1.amazonaws.com/dev/cart  
DELETE https://u6t7qrzis6.execute-api.ap-southeast-1.amazonaws.com/dev/cart  

### 📦 Orders
POST https://e4q5pt4mri.execute-api.ap-southeast-1.amazonaws.com/dev/orders  
GET https://e4q5pt4mri.execute-api.ap-southeast-1.amazonaws.com/dev/orders  

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

---

## 🔄 Application Flow

1. User accesses the website via CloudFront  
2. Static frontend loads from S3  
3. User performs actions (add to cart, place order)  
4. API Gateway routes requests to Lambda  
5. Lambda processes logic and interacts with DynamoDB  
6. Response is returned to frontend  

---

## 🧪 Unit Testing

Run tests using:

py -m pytest -v

## 🔐 Security

AWS SSO authentication
IAM roles for Lambda access
No hardcoded credentials

## 📦 Deployment

Frontend hosted on S3
CloudFront used for CDN
Backend deployed using Lambda + API Gateway
Cache invalidation used after updates

## 💡 Challenges Faced

CORS issues (PUT & DELETE methods)
Cart quantity update bugs
API Gateway route configuration
CloudFront caching old UI

## 📈 Future Enhancements

User authentication (Cognito)
Payment integration
Admin dashboard
Search & filtering
Order tracking

## 👩‍💻 Author
Kaviya 

## 📌 Conclusion

This project demonstrates a scalable, serverless e-commerce application using AWS, showcasing cloud-native architecture, REST APIs, and microservices design.


   
