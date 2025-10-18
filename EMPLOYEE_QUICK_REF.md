# Employee Account - Quick Reference

## 🔐 Login Credentials
```
Email: employee@foodsystem.com
Password: employee123
URL: http://localhost:5000
```

---

## ✅ CAN DO (Operational Access)

### Orders
- ✅ View all active orders
- ✅ View order details
- ✅ Update status: Confirmed→Preparing→Ready→Delivered
- ❌ Cannot cancel or delete orders

### Menu
- ✅ Browse menu (read-only)
- ❌ Cannot edit menu items

### Delivery
- ✅ Track deliveries
- ❌ Cannot create/assign deliveries

### Personal
- ✅ View performance metrics
- ✅ See completed tasks
- ✅ Track personal stats

---

## ❌ CANNOT DO (Restricted)

- ❌ User management
- ❌ Financial reports
- ❌ System settings
- ❌ Feedback management
- ❌ Menu editing
- ❌ Delivery assignments

---

## 📊 Dashboard Features

### Top Stats
1. My Assigned Orders
2. Pending Tasks
3. Completed Today
4. Performance Score

### Main Table
- Active orders list
- Quick status updates
- View order details

### Sidebar
- Quick Actions
- Performance Metrics
- Recent Activity

---

## 🎯 Common Tasks

### Update Order Status
1. Find order in "My Assigned Orders"
2. Click eye icon to view
3. Update status (limited options)
4. Cannot cancel or reverse status

### View Menu
1. Click "View Menu" button
2. Browse items (read-only)
3. Search and filter available

### Track Delivery
1. Click "Delivery Tracking"
2. View delivery status
3. See estimated times

---

## 🔒 Access Restrictions

**Cannot Access:**
- /users - User management
- /reports - Financial reports
- /admin - Admin panel
- /feedback - Feedback system
- Menu editing features
- Delivery assignments
- Customer database
- System settings

**Will Be Redirected To:**
- Employee dashboard on login
- Dashboard if accessing restricted pages

---

## Server Restart
The employee account is automatically created when the server starts!
