# Database Schema Documentation
## Smart Food Ordering System

---

## 📋 Database Information

- **Database Type**: MySQL / MariaDB
- **Database Name**: food_ordering_system
- **Character Set**: utf8mb4
- **Collation**: utf8mb4_unicode_ci
- **Engine**: InnoDB
- **Normalization**: 3NF (Third Normal Form)

---

## 📊 Complete Schema Definition

### 1. USER Table

```sql
CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    role VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    address TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_role (role),
    
    CHECK (role IN ('Admin', 'Supervisor', 'Employee', 'Customer'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `email`: UNIQUE constraint
- `role`: CHECK constraint for valid roles
- Password stored using scrypt hashing

**Indexes:**
- Primary Key: `user_id`
- Unique Index: `email`
- Index: `role` (for role-based queries)

---

### 2. MENU_ITEM Table

```sql
CREATE TABLE menuitem (
    menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    availability BOOLEAN NOT NULL DEFAULT TRUE,
    image VARCHAR(255),
    is_vegetarian BOOLEAN NOT NULL DEFAULT FALSE,
    is_spicy BOOLEAN NOT NULL DEFAULT FALSE,
    is_popular BOOLEAN NOT NULL DEFAULT FALSE,
    is_new BOOLEAN NOT NULL DEFAULT FALSE,
    discount DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_category (category),
    INDEX idx_availability (availability),
    INDEX idx_price (price),
    
    CHECK (price > 0),
    CHECK (discount >= 0 AND discount <= 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `price`: CHECK constraint (must be positive)
- `discount`: CHECK constraint (0-100%)

**Indexes:**
- Primary Key: `menu_item_id`
- Index: `category` (for filtering)
- Index: `availability` (for filtering)
- Index: `price` (for sorting)

---

### 3. ORDER Table

```sql
CREATE TABLE `order` (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    employee_id INT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    payment_status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    delivery_address TEXT,
    special_instructions TEXT,
    completed_date DATETIME,
    
    FOREIGN KEY (user_id) REFERENCES user(user_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES user(user_id) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_employee_id (employee_id),
    INDEX idx_status (status),
    INDEX idx_order_date (order_date),
    
    CHECK (status IN ('Pending', 'Preparing', 'Ready', 'Completed', 'Cancelled')),
    CHECK (payment_status IN ('Pending', 'Paid', 'Failed', 'Refunded')),
    CHECK (total_amount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `status`: CHECK constraint for valid statuses
- `payment_status`: CHECK constraint
- `total_amount`: CHECK constraint (non-negative)

**Foreign Keys:**
- `user_id`: References USER (CASCADE delete)
- `employee_id`: References USER (SET NULL on delete)

**Indexes:**
- Primary Key: `order_id`
- Index: `user_id`, `employee_id`, `status`, `order_date`

---

### 4. ORDER_ITEM Table

```sql
CREATE TABLE order_item (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menuitem(menu_item_id) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    INDEX idx_order_id (order_id),
    INDEX idx_menu_item_id (menu_item_id),
    
    CHECK (quantity > 0),
    CHECK (price >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `quantity`: CHECK constraint (must be positive)
- `price`: CHECK constraint (non-negative)

**Foreign Keys:**
- `order_id`: References ORDER (CASCADE delete)
- `menu_item_id`: References MENU_ITEM (RESTRICT delete)

---

### 5. FEEDBACK Table

```sql
CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_id INT,
    rating INT NOT NULL,
    comment TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES user(user_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_order_id (order_id),
    INDEX idx_rating (rating),
    INDEX idx_created_date (created_date),
    
    CHECK (rating >= 1 AND rating <= 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `rating`: CHECK constraint (1-5)

**Foreign Keys:**
- `user_id`: References USER (CASCADE delete)
- `order_id`: References ORDER (SET NULL on delete)

---

### 6. DELIVERY Table

```sql
CREATE TABLE delivery (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL UNIQUE,
    employee_id INT,
    assigned_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    delivered_date DATETIME,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    notes TEXT,
    
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES user(user_id) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    
    INDEX idx_order_id (order_id),
    INDEX idx_employee_id (employee_id),
    INDEX idx_status (status),
    
    CHECK (status IN ('Pending', 'In Transit', 'Delivered', 'Failed'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `order_id`: UNIQUE constraint (one delivery per order)
- `status`: CHECK constraint

**Foreign Keys:**
- `order_id`: References ORDER (CASCADE delete)
- `employee_id`: References USER (SET NULL on delete)

---

### 7. PAYMENT Table

```sql
CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL UNIQUE,
    amount DECIMAL(10, 2) NOT NULL,
    method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    transaction_id VARCHAR(100),
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    
    INDEX idx_order_id (order_id),
    INDEX idx_status (status),
    INDEX idx_method (method),
    INDEX idx_payment_date (payment_date),
    
    CHECK (method IN ('Cash', 'Card', 'Online', 'Wallet')),
    CHECK (status IN ('Pending', 'Completed', 'Failed', 'Refunded')),
    CHECK (amount > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `order_id`: UNIQUE constraint (one payment per order)
- `method`: CHECK constraint
- `status`: CHECK constraint
- `amount`: CHECK constraint (must be positive)

---

### 8. RECOMMENDATION Table

```sql
CREATE TABLE recommendation (
    rec_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    preference TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES user(user_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_created_date (created_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Foreign Keys:**
- `user_id`: References USER (CASCADE delete)

---

### 9. CATEGORY Table

```sql
CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Constraints:**
- `name`: UNIQUE constraint

---

## 🔑 Index Strategy

### B+Tree Indexes Created:

1. **Primary Keys** (Clustered Index):
   - Automatically created on all `_id` columns
   - Provides fast lookup by ID

2. **Foreign Keys**:
   - `user_id`, `order_id`, `menu_item_id`, `employee_id`
   - Speeds up JOIN operations

3. **Search Fields**:
   - `email` (UNIQUE) - Fast user lookup
   - `category` - Menu filtering
   - `status` fields - Order/delivery filtering
   - `order_date`, `payment_date` - Date range queries

4. **Composite Indexes** (Optional for optimization):
   ```sql
   CREATE INDEX idx_order_user_status ON `order`(user_id, status);
   CREATE INDEX idx_menu_category_availability ON menuitem(category, availability);
   ```

---

## 📊 Query Performance Benchmarks

### Simple Queries (Target: < 10ms)

```sql
-- User lookup by email
SELECT * FROM user WHERE email = 'admin@example.com';
-- Expected: 0.001 - 0.005 seconds

-- Menu items by category
SELECT * FROM menuitem WHERE category = 'Main Course' AND availability = TRUE;
-- Expected: 0.002 - 0.008 seconds

-- Order by ID
SELECT * FROM `order` WHERE order_id = 123;
-- Expected: 0.001 - 0.003 seconds
```

### Complex Queries (Target: < 100ms)

```sql
-- Order with all details (JOINS)
SELECT 
    o.order_id,
    u.name AS customer_name,
    u.email,
    o.order_date,
    o.total_amount,
    o.status,
    oi.quantity,
    m.name AS item_name,
    m.price
FROM `order` o
JOIN user u ON o.user_id = u.user_id
JOIN order_item oi ON o.order_id = oi.order_id
JOIN menuitem m ON oi.menu_item_id = m.menu_item_id
WHERE o.order_id = 123;
-- Expected: 0.010 - 0.050 seconds

-- Sales report with aggregations
SELECT 
    DATE(order_date) AS date,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS daily_revenue,
    AVG(total_amount) AS avg_order_value
FROM `order`
WHERE order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
    AND status = 'Completed'
GROUP BY DATE(order_date)
ORDER BY date DESC;
-- Expected: 0.020 - 0.080 seconds
```

---

## 🔒 Security Measures

### 1. Password Security
- **Algorithm**: scrypt (via Werkzeug)
- **Storage**: Hashed string (255 characters)
- **Format**: `scrypt:32768:8:1$salt$hash`

### 2. SQL Injection Prevention
- **Method**: SQLAlchemy ORM with parameterized queries
- **Example**:
  ```python
  # SECURE - Using ORM
  user = User.query.filter_by(email=email).first()
  
  # SECURE - Using parameters
  db.session.execute("SELECT * FROM user WHERE email = :email", {"email": email})
  ```

### 3. Data Integrity
- Foreign key constraints with CASCADE/RESTRICT
- CHECK constraints on critical fields
- NOT NULL constraints on required fields

---

## 📈 Scalability Considerations

### Current Capacity:
- **Users**: Up to 4.2 billion (INT AUTO_INCREMENT)
- **Orders**: Up to 4.2 billion
- **Concurrent Users**: 5-10 (tested)
- **Database Size**: Optimized for < 10GB

### Optimization Strategies:
1. **Indexing**: All foreign keys and search fields indexed
2. **Partitioning**: Can partition ORDER table by date if needed
3. **Caching**: Application-level caching for menu items
4. **Connection Pooling**: SQLAlchemy connection pool
5. **Query Optimization**: SELECT only needed columns

---

## 🔄 Backup Strategy

### Recommended Backup Schedule:
```bash
# Daily full backup
mysqldump -u root -p food_ordering_system > backup_$(date +%Y%m%d).sql

# Weekly incremental backup
mysqlbinlog --start-datetime="YYYY-MM-DD 00:00:00" > incremental_backup.sql
```

---

## 📝 Migration Scripts

### Initial Database Setup:
```sql
-- Create database
CREATE DATABASE IF NOT EXISTS food_ordering_system
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE food_ordering_system;

-- Import all tables (in order to respect foreign keys)
-- 1. user
-- 2. menuitem, category
-- 3. order
-- 4. order_item, payment, delivery, feedback, recommendation
```

---

*Generated: October 18, 2025*
*Smart Food Ordering System - Database Schema Documentation*
