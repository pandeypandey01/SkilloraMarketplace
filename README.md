# SkilloraMarketplace

## 📌 Project Overview
Skillora is a marketplace where students can offer useful skills and other users can hire them.  
Example workflow: a customer needs a logo → finds a student designer → books the service → pays → receives the work → leaves a review.  

The platform connects **customers**, **student service providers**, and **administrators** in one system.  
Designed as a **Software Engineering + Web Services project** for a 5‑member team over 2 months.

---

## 🎯 Problem Statement
- Students have skills but lack a trusted platform to advertise and monetize them.  
- Customers struggle to find reliable providers for small services.  
- Bookings, payments, and reviews are often scattered across multiple apps.  

**Skillora solves this by providing a structured, secure, and trackable service marketplace.**

---

## 👥 Users / Actors
- **Customer** → Search skills, book service, pay, review  
- **Student Provider** → Create profile, list services, accept jobs  
- **Admin** → Manage users, moderate services, generate reports  
- **Payment Service** → Handle payments, refunds, status  
- *(Future)* Notification provider / external verification service  

---

## 🧩 Main Modules
- Authentication (Register, login, JWT, roles)  
- Profiles (Student/provider profile, skills)  
- Catalogue (Services, categories, prices)  
- Booking (Create, accept, cancel, status)  
- Payment (Pay, refund, idempotency)  
- Reviews (Rating and feedback)  
- Notifications (Booking/payment updates)  
- Admin (Moderation, users, reports)  

---

## 🔄 User Workflow
1. Register / Login  
2. Browse services  
3. View provider profile  
4. Create booking  
5. Make payment  
6. Service delivery  
7. Review + notification  

Booking lifecycle: **PENDING → ACCEPTED → IN_PROGRESS → COMPLETED / CANCELLED**

---

## 🏗️ Architecture
- **Frontend** → React + HTML/CSS/JavaScript  
- **API Gateway / Server** → Node.js + Express  
- **API Styles** → REST + GraphQL + SOAP client  
- **Business Logic** → Auth, Users, Services, Booking, Payment  
- **Database & Cache** → PostgreSQL/MySQL + Redis  
- **External Services** → Payment, Email/Notification, Legacy SOAP  

---

## ⚙️ Technology Stack
- **Frontend** → React, HTML5, CSS3, JavaScript  
- **Backend** → Node.js, Express.js  
- **API** → REST API, GraphQL  
- **Legacy Integration** → SOAP + WSDL  
- **Database** → PostgreSQL / MySQL  
- **Cache** → Redis  
- **Testing** → Jest + Supertest  
- **Version Control** → Git/GitHub  

---

## 📑 Database Design
- **users** → id, name, email, password_hash, role  
- **services** → id, provider_id, category, title, price  
- **bookings** → id, customer_id, service_id, status, scheduled_at  
- **payments** → id, booking_id, amount, status, idempotency_key  
- **reviews** → id, booking_id, rating, comment  
- **notifications** → id, user_id, type, message, status  

---

## 🛡️ Security & Reliability
- JWT authentication + role‑based authorization  
- Password hashing, parameterized SQL queries  
- Input validation, CORS restrictions, rate limiting  
- Timeout, retry with backoff, circuit breaker, correlation ID  

---

## 🧪 Testing Plan
- **Unit Tests** → Business logic, utilities  
- **API Tests** → Jest + Supertest  
- **Integration** → API + DB + mocked external APIs  
- **Security** → JWT, roles, SQL injection prevention  
- **Reliability** → Timeout, retry, breaker, rate limit  
- **Acceptance** → End‑to‑end booking → payment → review  

---

## 🚀 Deployment
- Environment variables for secrets/config  
- Swagger UI for live API documentation  
- Git/GitHub for version control and collaboration  

---
