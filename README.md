# Smart Inventory Manager (Backend)

A backend system for managing restaurant inventory with real-time stock tracking, recipe-based deductions, purchase flow, low-stock alerts, and POS-ready APIs.

This project focuses on building a **correct, auditable, and extensible inventory engine**, following industry-standard backend architecture.

---

## 🚀 Features

### Core Inventory Management

- Manage inventory items (ingredients, packaged items)
- Track current stock and reorder levels
- Support stock-in (purchase) and stock-out (sales)

### Menu & Recipe Management

- Define menu items (what customers order)
- Map each menu item to ingredients via recipes
- Automatically deduct inventory based on recipes when sales occur

### Sales (POS Integration Ready)

- Record sales via API
- Prevent sales if inventory is insufficient
- Ensure accurate stock deduction per recipe

### Purchase Flow

- Increase inventory when stock is purchased
- Log every purchase as a transaction
- Maintain a complete audit trail

### Inventory Transactions (Audit Log)

- Every inventory change is recorded
- Supports reasons like `sale`, `purchase`, `waste`
- Enables traceability and reporting

### Low-Stock Alerts

- Identify items below reorder level
- Expose alerts via API
- Ready for future notifications (email / dashboard)

---

## 🧠 Why This System Is “Smart”

- Inventory is **recipe-aware**, not just quantity-based
- Sales automatically translate into ingredient usage
- Stock never goes negative
- Alerts are generated proactively
- Data is structured for forecasting and AI extensions

---

## 🏗 Architecture

The backend follows a clean layered architecture:
API Routers (FastAPI)
↓
Service Layer (Business Logic)
↓
Data Models (SQLAlchemy ORM)
↓
PostgreSQL Database

This separation ensures:

- Maintainability
- Testability
- Scalability

---

## 🗄 Database Models

- `InventoryItem` – Ingredients / packaged items
- `MenuItem` – Sellable dishes/items
- `Recipe` – Mapping between menu items and inventory
- `Sale` – POS sales records
- `InventoryTransaction` – Audit log of stock changes

---

## 📡 API Endpoints (Highlights)

- `POST /inventory` – Create inventory item
- `GET /inventory` – List inventory
- `POST /menu` – Create menu item
- `POST /recipes` – Define recipe
- `POST /sales` – Record a sale
- `POST /purchase` – Add purchased stock
- `GET /alerts/low-stock` – View low-stock items

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Version Control:** Git

---

## 🔮 Future Enhancements

- Authentication (Admin / Staff roles)
- Reporting (daily usage, waste analysis)
- Demand forecasting
- Supplier management
- AI-based optimization

---

## 📌 Status

✅ Core backend complete  
✅ Production-style architecture  
🚧 Ready for extensions (AI, frontend, analytics)
