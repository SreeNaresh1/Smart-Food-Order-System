# System Workflow Documentation
## Smart Food Ordering System

---

## 📋 Table of Contents
1. [User Authentication Workflow](#user-authentication-workflow)
2. [Customer Order Workflow](#customer-order-workflow)
3. [Order Processing Workflow](#order-processing-workflow)
4. [Employee Assignment Workflow](#employee-assignment-workflow)
5. [Payment Processing Workflow](#payment-processing-workflow)
6. [Delivery Management Workflow](#delivery-management-workflow)
7. [Feedback Collection Workflow](#feedback-collection-workflow)
8. [Admin Management Workflow](#admin-management-workflow)

---

## 🔐 1. User Authentication Workflow

### Login Process

```
┌─────────────────────────────────────────────────────────────┐
│                     LOGIN WORKFLOW                           │
└─────────────────────────────────────────────────────────────┘

START
  │
  ▼
┌─────────────────────┐
│ User accesses       │
│ /login page         │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Enter username/email│
│ and password        │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐      YES    ┌─────────────────────┐
│ System checks if    │────────────→│ Search by email     │
│ input contains '@'  │             │ in database         │
└─────────────────────┘             └─────────────────────┘
  │                                           │
  │ NO                                        ▼
  ▼                                  ┌─────────────────────┐
┌─────────────────────┐              │ User found?         │
│ Search by username  │              └─────────────────────┘
│ (name) in database  │                       │
└─────────────────────┘                       │ YES
  │                                           ▼
  ▼                                  ┌─────────────────────┐
┌─────────────────────┐              │ Check password      │
│ User found?         │              │ using scrypt hash   │
└─────────────────────┘              └─────────────────────┘
  │                                           │
  │ YES                                       ▼
  ▼                                  ┌─────────────────────┐
┌─────────────────────┐              │ Password correct?   │
│ Check password      │              └─────────────────────┘
│ using scrypt hash   │                       │
└─────────────────────┘                       │ YES
  │                                           ▼
  │ YES                              ┌─────────────────────┐
  ▼                                  │ Create session:     │
┌─────────────────────┐              │ - user_id           │
│ Password correct?   │              │ - user_name         │
└─────────────────────┘              │ - user_role         │
  │                                  └─────────────────────┘
  │ YES                                       │
  ▼                                           ▼
┌─────────────────────┐              ┌─────────────────────┐
│ Create session:     │              │ Redirect based on   │
│ - user_id           │              │ user role:          │
│ - user_name         │              │ - Admin → Admin     │
│ - user_role         │              │ - Supervisor → Sup  │
└─────────────────────┘              │ - Employee → Emp    │
  │                                  │ - Customer → Cust   │
  ▼                                  └─────────────────────┘
┌─────────────────────┐                       │
│ Redirect to role    │                       ▼
│ specific dashboard  │              ┌─────────────────────┐
└─────────────────────┘              │ Display flash       │
  │                                  │ "Welcome back!"     │
  ▼                                  └─────────────────────┘
END                                            │
                                               ▼
┌─────────────────────┐                      END
│ Show error:         │
│ "Invalid username/  │◄────── NO (from any check)
│ email or password"  │
└─────────────────────┘
  │
  ▼
Back to login page
```

### Registration Process

```
START → Enter Details → Validate Password Match → Check Email Exists
  │                                                         │
  │                                                         ▼
  │                                                    Hash Password
  │                                                         │
  │                                                         ▼
  │                                                  Insert to Database
  │                                                         │
  └─────────────────────────────────────────────────────────┘
                                                            │
                                                            ▼
                                                    Redirect to Login
                                                            │
                                                            ▼
                                                           END
```

---

## 🛒 2. Customer Order Workflow

### Complete Order Journey

```
┌─────────────────────────────────────────────────────────────┐
│                  CUSTOMER ORDER WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

START (Customer Login)
  │
  ▼
┌─────────────────────┐
│ Browse Menu         │
│ /menu               │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Filter/Search Items:│
│ - By Category       │
│ - By Price          │
│ - Vegetarian/Spicy  │
│ - Popular/New       │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Select Item         │
│ Choose Quantity     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Add to Cart         │
│ (Session-based)     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐      Continue Shopping
│ Continue Shopping?  │──────────┐
└─────────────────────┘          │
  │ No                            │
  ▼                               │
┌─────────────────────┐          │
│ View Cart           │◄─────────┘
│ /cart               │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Update Quantities?  │
│ Remove Items?       │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Proceed to Checkout │
│ /checkout           │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Enter/Confirm:      │
│ - Delivery Address  │
│ - Phone Number      │
│ - Special Notes     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Select Payment      │
│ Method:             │
│ - Cash on Delivery  │
│ - Card              │
│ - Online            │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Review Order        │
│ Summary:            │
│ - Items             │
│ - Total Amount      │
│ - Delivery Info     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Place Order         │
│ (POST /orders/new)  │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Create Order in DB: │
│ - Status: Pending   │
│ - Payment: Pending  │
│ - Order Items       │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Clear Shopping Cart │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Show Confirmation   │
│ - Order ID          │
│ - Estimated Time    │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Redirect to:        │
│ My Orders Page      │
└─────────────────────┘
  │
  ▼
END
```

---

## ⚙️ 3. Order Processing Workflow

### Kitchen & Preparation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                ORDER PROCESSING WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

New Order Created
  │
  ▼
┌─────────────────────┐
│ Status: PENDING     │
│ Visible in:         │
│ - Kitchen Dashboard │
│ - Supervisor Panel  │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Supervisor Reviews  │
│ Order Details       │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Assign to Employee  │
│ (Kitchen Staff/     │
│ Delivery Person)    │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Employee Receives   │
│ Assignment          │
│ (Email/Dashboard)   │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Employee Views      │
│ Order Details       │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Start Preparation   │
│ Status: PREPARING   │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Customer sees:      │
│ "Order is being     │
│  prepared"          │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Food Preparation    │
│ (Kitchen)           │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Mark as READY       │
│ (Employee action)   │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Notify Delivery     │
│ Team                │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Assign Delivery     │
│ Person              │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Status: OUT FOR     │
│ DELIVERY            │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Delivery in         │
│ Progress            │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Order Delivered     │
│ Status: COMPLETED   │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Update completed_   │
│ date timestamp      │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Send Feedback       │
│ Request to Customer │
└─────────────────────┘
  │
  ▼
END
```

---

## 👥 4. Employee Assignment Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              EMPLOYEE ASSIGNMENT WORKFLOW                    │
└─────────────────────────────────────────────────────────────┘

START (Supervisor/Admin)
  │
  ▼
┌─────────────────────┐
│ View All Pending    │
│ Orders              │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Select Order to     │
│ Assign              │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ View Available      │
│ Employees:          │
│ - Kitchen Staff     │
│ - Delivery Staff    │
│ - Current Workload  │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Select Employee     │
│ based on:           │
│ - Availability      │
│ - Workload          │
│ - Specialization    │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Assign Order        │
│ (POST request)      │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Update Database:    │
│ - order.employee_id │
│ - Status updated    │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Notify Employee     │
│ (Dashboard/Email)   │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Employee sees in    │
│ "My Assignments"    │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Track Progress      │
│ (Supervisor view)   │
└─────────────────────┘
  │
  ▼
END
```

---

## 💳 5. Payment Processing Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              PAYMENT PROCESSING WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

Order Placed
  │
  ▼
┌─────────────────────┐
│ Payment Status:     │
│ PENDING             │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐      Cash on Delivery
│ Payment Method?     │──────────────────┐
└─────────────────────┘                  │
  │                                      │
  │ Online/Card                          │
  ▼                                      ▼
┌─────────────────────┐        ┌─────────────────────┐
│ Redirect to Payment │        │ Mark for COD        │
│ Gateway             │        │ Processing          │
└─────────────────────┘        └─────────────────────┘
  │                                      │
  ▼                                      ▼
┌─────────────────────┐        ┌─────────────────────┐
│ Customer Enters     │        │ Order Proceeds      │
│ Payment Details     │        │ to Kitchen          │
└─────────────────────┘        └─────────────────────┘
  │                                      │
  ▼                                      ▼
┌─────────────────────┐        ┌─────────────────────┐
│ Gateway Processes   │        │ Payment Collected   │
│ Payment             │        │ on Delivery         │
└─────────────────────┘        └─────────────────────┘
  │                                      │
  ▼                                      ▼
┌─────────────────────┐        ┌─────────────────────┐
│ Success/Failure     │        │ Update Status:      │
│ Response            │        │ PAID                │
└─────────────────────┘        └─────────────────────┘
  │                                      │
  │ Success                              │
  ▼                                      │
┌─────────────────────┐                 │
│ Create Payment      │                 │
│ Record:             │                 │
│ - transaction_id    │                 │
│ - amount            │                 │
│ - method            │                 │
│ - status: Completed │                 │
└─────────────────────┘                 │
  │                                      │
  ▼                                      │
┌─────────────────────┐                 │
│ Update Order:       │                 │
│ payment_status:PAID │◄────────────────┘
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Generate Receipt    │
│ Send to Customer    │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Record in Payment   │
│ Report              │
└─────────────────────┘
  │
  ▼
END
```

---

## 🚚 6. Delivery Management Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              DELIVERY MANAGEMENT WORKFLOW                    │
└─────────────────────────────────────────────────────────────┘

Order Ready for Delivery
  │
  ▼
┌─────────────────────┐
│ Create Delivery     │
│ Record in DB        │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Supervisor Assigns  │
│ Delivery Person     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Delivery Person     │
│ Receives:           │
│ - Order Details     │
│ - Customer Address  │
│ - Contact Info      │
│ - Special Notes     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Mark as:            │
│ IN TRANSIT          │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Customer Tracking   │
│ Shows "Out for      │
│ Delivery"           │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Delivery Person     │
│ Navigates to        │
│ Customer Location   │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Reach Destination   │
│ Contact Customer    │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐      Successful
│ Delivery Attempt    │──────────────┐
└─────────────────────┘              │
  │                                  │
  │ Failed                           ▼
  ▼                          ┌─────────────────────┐
┌─────────────────────┐      │ Hand over Order     │
│ Mark as FAILED      │      │ Collect Payment     │
│ Add Notes           │      │ (if COD)            │
│ Notify Supervisor   │      └─────────────────────┘
└─────────────────────┘                │
  │                                    ▼
  ▼                          ┌─────────────────────┐
┌─────────────────────┐      │ Confirm Delivery    │
│ Reschedule or       │      │ in App              │
│ Refund Process      │      └─────────────────────┘
└─────────────────────┘                │
  │                                    ▼
  ▼                          ┌─────────────────────┐
END                          │ Update Database:    │
                             │ - Status: DELIVERED │
                             │ - delivered_date    │
                             │ - Payment if COD    │
                             └─────────────────────┘
                                       │
                                       ▼
                             ┌─────────────────────┐
                             │ Send Feedback       │
                             │ Request             │
                             └─────────────────────┘
                                       │
                                       ▼
                                      END
```

---

## ⭐ 7. Feedback Collection Workflow

```
Order Completed
  │
  ▼
┌─────────────────────┐
│ Send Feedback       │
│ Request to Customer │
│ (Email/Dashboard)   │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Customer Opens      │
│ Feedback Form       │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Select Rating:      │
│ ⭐⭐⭐⭐⭐ (1-5)      │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Write Comment       │
│ (Optional)          │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Submit Feedback     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Save to Database:   │
│ - user_id           │
│ - order_id          │
│ - rating            │
│ - comment           │
│ - timestamp         │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Update Analytics:   │
│ - Avg Rating        │
│ - Satisfaction Rate │
│ - Menu Item Ratings │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Notify Management   │
│ (if rating < 3)     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Display in Reports  │
│ Dashboard           │
└─────────────────────┘
  │
  ▼
END
```

---

## 👨‍💼 8. Admin Management Workflow

### User Management

```
Admin Login → View Users → Select Action
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
    Add User            Edit User             Delete User
        │                     │                     │
        ▼                     ▼                     ▼
    Enter Details       Update Info           Confirm Delete
        │                     │                     │
        ▼                     ▼                     ▼
    Save to DB         Save Changes          Remove from DB
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                              ▼
                         Success Message
                              │
                              ▼
                             END
```

### Menu Management

```
Admin Login → View Menu → Select Action
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
    Add Item            Edit Item             Delete Item
        │                     │                     │
        ▼                     ▼                     ▼
    Enter Details       Update Info          Confirm Delete
    Upload Image        Change Price          Check Orders
        │                     │                     │
        ▼                     ▼                     ▼
    Save to DB         Save Changes          Soft Delete
        │                     │                (availability=FALSE)
        └─────────────────────┴─────────────────────┘
                              │
                              ▼
                         Success Message
                              │
                              ▼
                             END
```

---

## 🔄 Session Management Workflow

```
User Action
  │
  ▼
┌─────────────────────┐
│ Check Session       │
│ Exists?             │
└─────────────────────┘
  │
  │ NO
  ▼
┌─────────────────────┐
│ Redirect to Login   │
└─────────────────────┘
  │
  │ YES (Session exists)
  ▼
┌─────────────────────┐
│ Check Session       │
│ Timeout (30 min)    │
└─────────────────────┘
  │
  │ Expired
  ▼
┌─────────────────────┐
│ Clear Session       │
│ Redirect to Login   │
└─────────────────────┘
  │
  │ Valid
  ▼
┌─────────────────────┐
│ Check User Role     │
│ Permission          │
└─────────────────────┘
  │
  │ Authorized
  ▼
┌─────────────────────┐
│ Proceed with        │
│ Request             │
└─────────────────────┘
  │
  ▼
END
```

---

## 🎯 Key Workflow Features

### Concurrency Handling
- **Database Locks**: InnoDB row-level locking
- **Transaction Management**: ACID compliance
- **Session Management**: Server-side sessions
- **Race Condition Prevention**: Optimistic locking on critical operations

### Error Handling
- **Try-Catch Blocks**: All database operations
- **Rollback**: Failed transactions rolled back
- **User Notification**: Flash messages for all errors
- **Logging**: Critical errors logged for debugging

### Performance Optimization
- **Lazy Loading**: Relationships loaded on demand
- **Query Optimization**: Indexed fields used in WHERE clauses
- **Caching**: Session-based cart (not database)
- **Pagination**: Large result sets paginated

---

*Generated: October 18, 2025*
*Smart Food Ordering System - Workflow Documentation*
