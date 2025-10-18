# Entity-Relationship (ER) Diagram
## Smart Food Ordering System

---

## 📊 ER Diagram Visual Representation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     SMART FOOD ORDERING SYSTEM - ER DIAGRAM                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐              ┌──────────────────┐              ┌──────────────────┐
│      USER        │              │    MENU_ITEM     │              │      ORDER       │
├──────────────────┤              ├──────────────────┤              ├──────────────────┤
│ PK user_id       │              │ PK menu_item_id  │              │ PK order_id      │
│    name          │              │    name          │              │ FK user_id       │
│    email (UK)    │              │    description   │              │ FK employee_id   │
│    phone         │              │    price         │              │    order_date    │
│    role          │              │    category      │              │    total_amount  │
│    password      │              │    availability  │              │    status        │
│    address       │              │    image         │              │    payment_status│
│    created_date  │              │    is_vegetarian │              │    delivery_addr │
└──────────────────┘              │    is_spicy      │              │    special_instr │
         │                        │    is_popular    │              │    completed_date│
         │ places                 │    is_new        │              └──────────────────┘
         │ 1                      │    discount      │                       │
         │                        │    created_date  │                       │
         │                        └──────────────────┘                       │
         │                                 │                                 │
         │                                 │ contains                        │
         │                                 │ M                               │
         │                        ┌──────────────────┐                       │
         │                        │   ORDER_ITEM     │                       │
         │                        ├──────────────────┤                       │
         │                        │ PK order_item_id │                       │
         │                        │ FK order_id      │◄──────────────────────┘
         │                        │ FK menu_item_id  │──────────┐
         │                        │    quantity      │          │
         │                        │    price         │          │
         │                        └──────────────────┘          │
         │                                                      │
         │ gives                                                │
         │ 1:M                                                  │
         ▼                                                      ▼
┌──────────────────┐              ┌──────────────────┐              ┌──────────────────┐
│    FEEDBACK      │              │   RECOMMENDATION │              │    DELIVERY      │
├──────────────────┤              ├──────────────────┤              ├──────────────────┤
│ PK feedback_id   │              │ PK rec_id        │              │ PK delivery_id   │
│ FK user_id       │              │ FK user_id       │              │ FK order_id      │
│ FK order_id      │              │    preference    │              │ FK employee_id   │
│    rating        │              │    created_date  │              │    assigned_date │
│    comment       │              └──────────────────┘              │    delivered_date│
│    created_date  │                                                │    status        │
└──────────────────┘                                                │    notes         │
                                                                    └──────────────────┘

┌──────────────────┐              ┌──────────────────┐
│     PAYMENT      │              │     CATEGORY     │
├──────────────────┤              ├──────────────────┤
│ PK payment_id    │              │ PK category_id   │
│ FK order_id      │              │    name          │
│    amount        │              │    description   │
│    method        │              │    created_date  │
│    status        │              └──────────────────┘
│    transaction_id│
│    payment_date  │
└──────────────────┘
```

---

## 📋 Entity Descriptions

### 1. **USER Entity**
Stores information about all system users (Admin, Supervisor, Employee, Customer)

**Attributes:**
- `user_id` (PK): Primary key, auto-increment
- `name`: Full name of the user
- `email` (UK): Unique email address
- `phone`: Contact number
- `role`: User role (Admin/Supervisor/Employee/Customer)
- `password`: Hashed password (scrypt)
- `address`: Delivery/contact address
- `created_date`: Account creation timestamp

**Relationships:**
- 1:M with ORDER (places orders)
- 1:M with FEEDBACK (gives feedback)
- 1:M with RECOMMENDATION (receives recommendations)
- 1:M with DELIVERY (assigned deliveries - for employees)

---

### 2. **MENU_ITEM Entity**
Stores food items available in the system

**Attributes:**
- `menu_item_id` (PK): Primary key, auto-increment
- `name`: Item name
- `description`: Item description
- `price`: Item price (decimal)
- `category`: Food category
- `availability`: In stock or not (boolean)
- `image`: Image file path
- `is_vegetarian`: Vegetarian flag
- `is_spicy`: Spicy flag
- `is_popular`: Popular item flag
- `is_new`: New item flag
- `discount`: Discount percentage
- `created_date`: Item creation timestamp

**Relationships:**
- M:N with ORDER (through ORDER_ITEM)
- 1:M with ORDER_ITEM

---

### 3. **ORDER Entity**
Stores customer orders

**Attributes:**
- `order_id` (PK): Primary key, auto-increment
- `user_id` (FK): Foreign key to USER
- `employee_id` (FK): Assigned employee (nullable)
- `order_date`: Order timestamp
- `total_amount`: Total order cost
- `status`: Order status (Pending/Preparing/Ready/Completed)
- `payment_status`: Payment status (Pending/Paid/Failed)
- `delivery_address`: Delivery location
- `special_instructions`: Customer notes
- `completed_date`: Completion timestamp

**Relationships:**
- M:1 with USER (customer)
- M:1 with USER (assigned employee)
- 1:M with ORDER_ITEM
- 1:1 with PAYMENT
- 1:1 with DELIVERY
- 1:M with FEEDBACK

---

### 4. **ORDER_ITEM Entity**
Junction table for Order and MenuItem (Many-to-Many relationship)

**Attributes:**
- `order_item_id` (PK): Primary key, auto-increment
- `order_id` (FK): Foreign key to ORDER
- `menu_item_id` (FK): Foreign key to MENU_ITEM
- `quantity`: Number of items ordered
- `price`: Price at time of order

**Relationships:**
- M:1 with ORDER
- M:1 with MENU_ITEM

---

### 5. **FEEDBACK Entity**
Stores customer feedback and ratings

**Attributes:**
- `feedback_id` (PK): Primary key, auto-increment
- `user_id` (FK): Foreign key to USER
- `order_id` (FK): Foreign key to ORDER
- `rating`: Rating score (1-5)
- `comment`: Customer comment
- `created_date`: Feedback timestamp

**Relationships:**
- M:1 with USER
- M:1 with ORDER

---

### 6. **DELIVERY Entity**
Tracks delivery assignments and status

**Attributes:**
- `delivery_id` (PK): Primary key, auto-increment
- `order_id` (FK): Foreign key to ORDER
- `employee_id` (FK): Assigned delivery person
- `assigned_date`: Assignment timestamp
- `delivered_date`: Delivery completion timestamp
- `status`: Delivery status
- `notes`: Delivery notes

**Relationships:**
- 1:1 with ORDER
- M:1 with USER (employee)

---

### 7. **PAYMENT Entity**
Stores payment transactions

**Attributes:**
- `payment_id` (PK): Primary key, auto-increment
- `order_id` (FK): Foreign key to ORDER
- `amount`: Payment amount
- `method`: Payment method (Cash/Card/Online)
- `status`: Payment status (Pending/Completed/Failed)
- `transaction_id`: External transaction reference
- `payment_date`: Payment timestamp

**Relationships:**
- 1:1 with ORDER

---

### 8. **RECOMMENDATION Entity**
Stores user preferences for personalized recommendations

**Attributes:**
- `rec_id` (PK): Primary key, auto-increment
- `user_id` (FK): Foreign key to USER
- `preference`: User preference data
- `created_date`: Preference timestamp

**Relationships:**
- M:1 with USER

---

### 9. **CATEGORY Entity**
Stores food categories

**Attributes:**
- `category_id` (PK): Primary key, auto-increment
- `name`: Category name
- `description`: Category description
- `created_date`: Category creation timestamp

**Relationships:**
- 1:M with MENU_ITEM (implicit through category field)

---

## 🔗 Relationship Summary

| Relationship | Cardinality | Description |
|--------------|-------------|-------------|
| USER → ORDER | 1:M | One user can place many orders |
| USER → FEEDBACK | 1:M | One user can give multiple feedbacks |
| USER → RECOMMENDATION | 1:M | One user can have multiple recommendations |
| USER → DELIVERY | 1:M | One employee can handle multiple deliveries |
| ORDER → ORDER_ITEM | 1:M | One order contains multiple items |
| ORDER → PAYMENT | 1:1 | One order has one payment |
| ORDER → DELIVERY | 1:1 | One order has one delivery |
| ORDER → FEEDBACK | 1:M | One order can have multiple feedbacks |
| MENU_ITEM → ORDER_ITEM | 1:M | One menu item can be in multiple orders |

---

## 📌 Key Constraints

### Primary Keys (PK)
- Uniquely identify each record
- Auto-increment integers
- NOT NULL

### Foreign Keys (FK)
- Maintain referential integrity
- CASCADE on delete (where appropriate)
- Some allow NULL (e.g., employee_id in ORDER)

### Unique Keys (UK)
- email in USER table
- Prevents duplicate email addresses

### Check Constraints
- `rating` in FEEDBACK: Between 1-5
- `status` fields: Enumerated values only
- `price`: Must be positive
- `quantity`: Must be positive

---

## 🎯 Design Decisions

1. **User Role in Single Table**: All user types in one table with role field (simplifies authentication)
2. **Order_Item Junction Table**: Allows many-to-many relationship between orders and menu items
3. **Separate Delivery Table**: Better tracking and assignment management
4. **Payment as Separate Entity**: Supports multiple payment methods and detailed tracking
5. **Soft Availability**: Menu items marked unavailable rather than deleted
6. **Timestamp Tracking**: All entities have created_date for audit trail

---

## 📊 Normalization Level

**Third Normal Form (3NF)**
- ✅ No repeating groups (1NF)
- ✅ All non-key attributes fully dependent on primary key (2NF)
- ✅ No transitive dependencies (3NF)

---

*Generated: October 18, 2025*
*Smart Food Ordering System Documentation*
