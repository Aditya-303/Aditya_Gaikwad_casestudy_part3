# Aditya_Gaikwad_casestudy_part3
# Low Stock Alert API

A REST API endpoint that returns low-stock alerts for a company's inventory across multiple warehouses — built with **Python** and **Flask**.

---

## Endpoint

```
GET /api/companies/{company_id}/alerts/low-stock
```

### Query Parameters

| Parameter           | Type    | Default | Description                                   |
|---------------------|---------|---------|-----------------------------------------------|
| `warehouse_id`      | int     | null    | Filter to a specific warehouse (omit = all)   |
| `days_of_sales`     | int     | 30      | Lookback window in days for recent sales      |
| `include_zero_stock`| bool    | true    | Whether to include fully out-of-stock items   |

### Sample Request

```bash
curl -H "Authorization: Bearer <token>" \
  "http://localhost:5000/api/companies/1/alerts/low-stock?days_of_sales=30"
```

### Sample Response

```json
{
  "alerts": [
    {
      "product_id": 123,
      "product_name": "Widget A",
      "sku": "WID-001",
      "warehouse_id": 456,
      "warehouse_name": "Main Warehouse",
      "current_stock": 5,
      "threshold": 20,
      "days_until_stockout": 12,
      "supplier": {
        "id": 789,
        "name": "Supplier Corp",
        "contact_email": "orders@supplier.com"
      }
    }
  ],
  "total_alerts": 1
}
```

---

## Business Rules

| Rule | Detail |
|------|--------|
| **Threshold by product type** | `raw_material` = 100, `finished_good` = 20, `consumable` = 50 |
| **Recent sales activity only** | Products with no sales in the lookback window are excluded |
| **Multi-warehouse support** | Each (product, warehouse) pair generates a separate alert |
| **Days until stockout** | `current_stock / avg_daily_sales` — sorted ascending (most urgent first) |
| **Supplier info included** | For immediate reorder action; null if no supplier is linked |

---

## Tech Stack

- **Python 3.11+**
- **Flask 3.0**
- **MySQL**
- **PyJWT** for authentication

---

## Project Structure

```
low-stock-alert-api/
├── app.py                        # Flask app entry point
├── db.py                         # Database connection manager
├── requirements.txt
├── .env.example                  # Environment variable template
├── .gitignore
├── routes/
│   └── alerts.py                 # GET /api/companies/{id}/alerts/low-stock
├── services/
│   └── low_stock_service.py      # Business logic + SQL query
├── middleware/
│   └── auth.py                   # JWT auth decorator
└── utils/
    ├── validators.py              # Company access check
    └── exceptions.py             # Custom exception classes
```

---

## Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/low-stock-alert-api.git
cd low-stock-alert-api
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Mac / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
# Open .env and fill in your DB credentials and SECRET_KEY
```

**5. Run the server**
```bash
python app.py
```

Server starts at `http://localhost:5000`

---

## Database Schema (Assumed)

```sql
-- Core tables this API relies on
products        (id, name, sku, product_type, company_id, supplier_id, is_active)
warehouses      (id, name, company_id)
warehouse_stock (id, product_id, warehouse_id, quantity)
order_items     (id, product_id, quantity, created_at)
suppliers       (id, name, contact_email)
companies       (id, name)
```

---

## Edge Cases Handled

| Scenario | Behaviour |
|----------|-----------|
| Company does not exist | `404 Not Found` |
| User accessing another company | `403 Forbidden` |
| No warehouses / no stock data | `200` with `"alerts": []` |
| Product has no supplier | Alert returned with `null` supplier fields |
| Zero average daily sales | Product skipped — no urgency to compute |
| Expired / invalid JWT | `401 Unauthorized` |
| `days_of_sales` out of range | `400 Bad Request` |
| Unexpected DB error | `500` logged internally, no details leaked |

---

## Authentication

All requests require a valid JWT in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

JWT payload expected:
```json
{
  "sub": 1,
  "company_id": 42,
  "role": "user",
  "exp": 1234567890
}
```

---

## Author

Built as part of a backend engineering selection round.
