# Employee Account Testing Checklist

## 🧪 Complete Testing Guide for Employee Role

---

## ✅ Pre-Test Setup

- [ ] Server is running (`python app.py`)
- [ ] Navigate to `http://localhost:5000`
- [ ] Employee account message displayed in console

---

## 🔐 Login Test

### Test 1: Employee Login
- [ ] Go to login page
- [ ] Enter email: `employee@foodsystem.com`
- [ ] Enter password: `employee123`
- [ ] Click "Login"
- [ ] **Expected:** Redirect to employee dashboard
- [ ] **Expected:** See "Employee Dashboard" header
- [ ] **Expected:** Welcome message shows employee name

**Result:** ✅ PASS / ❌ FAIL

---

## 📊 Dashboard Test

### Test 2: Dashboard Statistics
- [ ] Check "My Assigned Orders" card displays
- [ ] Check "Pending Tasks" card displays
- [ ] Check "Completed Today" card displays
- [ ] Check "Performance" card displays
- [ ] **Expected:** All cards show numbers/percentages

**Result:** ✅ PASS / ❌ FAIL

### Test 3: Orders Table
- [ ] Scroll to "My Assigned Orders" section
- [ ] Verify table headers visible (Order #, Customer, Status, Time, Actions)
- [ ] Check if orders are listed (if any exist)
- [ ] **Expected:** Table displays properly with dark headers

**Result:** ✅ PASS / ❌ FAIL

### Test 4: Performance Metrics
- [ ] Look at right sidebar
- [ ] Check "Completion Rate" progress bar
- [ ] Check "On-Time Delivery" progress bar
- [ ] Check "Customer Satisfaction" progress bar
- [ ] **Expected:** All show percentages

**Result:** ✅ PASS / ❌ FAIL

---

## 📋 Order Management Tests

### Test 5: View Orders
- [ ] Click "My Orders" quick action button
- [ ] **Expected:** Navigate to orders list page
- [ ] **Expected:** See list of orders
- [ ] **Expected:** Can filter by status

**Result:** ✅ PASS / ❌ FAIL

### Test 6: View Order Details
- [ ] Click eye icon on any order
- [ ] **Expected:** Navigate to order details page
- [ ] **Expected:** See customer information
- [ ] **Expected:** See order items and quantities

**Result:** ✅ PASS / ❌ FAIL

### Test 7: Update Order Status (Allowed)
- [ ] Find order with status "Confirmed"
- [ ] Try to update to "Preparing"
- [ ] **Expected:** Status updates successfully
- [ ] **Expected:** Success message appears
- [ ] Try updating "Preparing" to "Ready"
- [ ] **Expected:** Works
- [ ] Try updating "Ready" to "Delivered"
- [ ] **Expected:** Works

**Result:** ✅ PASS / ❌ FAIL

### Test 8: Update Order Status (Restricted)
- [ ] Try to cancel an order
- [ ] **Expected:** Option not available or access denied
- [ ] Try to set order to "Pending"
- [ ] **Expected:** Option not available

**Result:** ✅ PASS / ❌ FAIL

---

## 🍔 Menu Access Tests

### Test 9: View Menu (Read-Only)
- [ ] Click "View Menu" button
- [ ] **Expected:** Navigate to menu page
- [ ] **Expected:** See list of menu items
- [ ] **Expected:** Can search and filter
- [ ] **Expected:** NO "Add Item" button visible
- [ ] **Expected:** NO "Edit" or "Delete" buttons on items

**Result:** ✅ PASS / ❌ FAIL

### Test 10: Try Menu Edit (Should Fail)
- [ ] Try to access `/menu/add` directly in URL
- [ ] **Expected:** Access denied or redirect to dashboard
- [ ] Try to access `/menu/edit/1` directly
- [ ] **Expected:** Access denied or redirect to dashboard

**Result:** ✅ PASS / ❌ FAIL

---

## 🚚 Delivery Tests

### Test 11: Delivery Tracking
- [ ] Click "Delivery Tracking" button
- [ ] **Expected:** Navigate to delivery tracking page
- [ ] **Expected:** Can see delivery status
- [ ] **Expected:** NO "Create Delivery" button
- [ ] **Expected:** NO "Assign Staff" functionality

**Result:** ✅ PASS / ❌ FAIL

---

## 🚫 Restricted Access Tests

### Test 12: User Management (Should Block)
- [ ] Try to access `/users` in URL
- [ ] **Expected:** Access denied message
- [ ] **Expected:** Redirect to employee dashboard
- [ ] **Expected:** Flash message about permissions

**Result:** ✅ PASS / ❌ FAIL

### Test 13: Reports Access (Should Block)
- [ ] Try to access `/reports` in URL
- [ ] **Expected:** Access denied
- [ ] **Expected:** Redirect to dashboard

**Result:** ✅ PASS / ❌ FAIL

### Test 14: Admin Panel (Should Block)
- [ ] Try to access `/admin` in URL
- [ ] **Expected:** Access denied or 404

**Result:** ✅ PASS / ❌ FAIL

### Test 15: Feedback Management (Should Block)
- [ ] Try to access `/feedback` in URL
- [ ] **Expected:** Access denied or limited access
- [ ] **Expected:** Cannot delete or manage feedback

**Result:** ✅ PASS / ❌ FAIL

---

## 🔄 Navigation Tests

### Test 16: Quick Actions
- [ ] Click each quick action button
- [ ] "View Menu" - Should work ✅
- [ ] "My Orders" - Should work ✅
- [ ] "Delivery Tracking" - Should work ✅

**Result:** ✅ PASS / ❌ FAIL

### Test 17: Navbar
- [ ] Check navbar items
- [ ] **Expected:** NO "Users" link
- [ ] **Expected:** NO "Reports" link
- [ ] **Expected:** NO "Settings" link
- [ ] **Expected:** Has "Orders", "Menu", "Delivery"
- [ ] **Expected:** Has profile dropdown with logout

**Result:** ✅ PASS / ❌ FAIL

---

## 👤 Profile Tests

### Test 18: View Profile
- [ ] Click profile dropdown
- [ ] Click "Profile" or username
- [ ] **Expected:** Can view own profile
- [ ] **Expected:** Can edit own information

**Result:** ✅ PASS / ❌ FAIL

### Test 19: Logout
- [ ] Click profile dropdown
- [ ] Click "Logout"
- [ ] **Expected:** Logged out successfully
- [ ] **Expected:** Redirected to landing/login page
- [ ] **Expected:** Cannot access dashboard without login

**Result:** ✅ PASS / ❌ FAIL

---

## 🎯 Functionality Summary Tests

### Test 20: What Employee CAN Do
- [ ] ✅ View personal dashboard
- [ ] ✅ View assigned orders
- [ ] ✅ Update order status (limited)
- [ ] ✅ View menu (read-only)
- [ ] ✅ Track deliveries
- [ ] ✅ View performance metrics
- [ ] ✅ See customer info for active orders

**Result:** ✅ PASS / ❌ FAIL

### Test 21: What Employee CANNOT Do
- [ ] ❌ User management (verified blocked)
- [ ] ❌ Menu editing (verified blocked)
- [ ] ❌ Financial reports (verified blocked)
- [ ] ❌ Cancel orders (verified blocked)
- [ ] ❌ Assign deliveries (verified blocked)
- [ ] ❌ System settings (verified blocked)
- [ ] ❌ Feedback management (verified blocked)

**Result:** ✅ PASS / ❌ FAIL

---

## 🔒 Security Tests

### Test 22: Role Enforcement
- [ ] Logout and login as Admin
- [ ] **Expected:** See different dashboard (admin features)
- [ ] Logout and login as Supervisor
- [ ] **Expected:** See supervisor dashboard
- [ ] Logout and login as Employee
- [ ] **Expected:** Back to employee dashboard
- [ ] **Expected:** Each role sees appropriate features

**Result:** ✅ PASS / ❌ FAIL

### Test 23: Session Security
- [ ] Login as employee
- [ ] Manually change session cookie (browser dev tools)
- [ ] Refresh page
- [ ] **Expected:** Logged out or error
- [ ] **Expected:** Cannot access without valid session

**Result:** ✅ PASS / ❌ FAIL

---

## 📱 Responsive Design Tests

### Test 24: Mobile View
- [ ] Resize browser to mobile size
- [ ] **Expected:** Dashboard responsive
- [ ] **Expected:** Tables scroll horizontally
- [ ] **Expected:** Cards stack vertically
- [ ] **Expected:** Navigation collapses to hamburger

**Result:** ✅ PASS / ❌ FAIL

---

## 🎨 UI/UX Tests

### Test 25: Visual Consistency
- [ ] Check color scheme matches other dashboards
- [ ] Verify buttons have consistent styling
- [ ] Check tables have dark headers with white text
- [ ] Verify cards have shadows and hover effects
- [ ] Check fonts are consistent

**Result:** ✅ PASS / ❌ FAIL

### Test 26: User Feedback
- [ ] Perform actions and check for feedback messages
- [ ] Success messages appear (green)
- [ ] Error messages appear (red)
- [ ] Messages auto-dismiss after 3 seconds

**Result:** ✅ PASS / ❌ FAIL

---

## 📊 Final Summary

### Total Tests: 26
- **Passed:** ___ / 26
- **Failed:** ___ / 26
- **Success Rate:** ____%

### Critical Issues Found:
1. ___________________________
2. ___________________________
3. ___________________________

### Minor Issues Found:
1. ___________________________
2. ___________________________
3. ___________________________

### Notes:
_______________________________________________
_______________________________________________
_______________________________________________

---

## ✅ Sign-Off

**Tested By:** _______________
**Date:** _______________
**Status:** ✅ APPROVED / ❌ NEEDS FIXES / ⚠️ CONDITIONAL APPROVAL

---

## 🚀 Ready for Production?

- [ ] All critical tests passed
- [ ] No security issues found
- [ ] UI/UX meets requirements
- [ ] Documentation complete
- [ ] Existing functionality unaffected

**Final Verdict:** _______________
