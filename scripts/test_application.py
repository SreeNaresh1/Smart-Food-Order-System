"""
Application Testing Script - Smart Food Ordering System
Tests all major components and features
"""

import requests
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TIMEOUT = 5

# ANSI color codes for better output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'=' * 80}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(80)}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 80}{RESET}\n")

def print_section(text):
    print(f"\n{BOLD}{YELLOW}{text}{RESET}")
    print(f"{YELLOW}{'-' * len(text)}{RESET}")

def test_result(test_name, passed, message=""):
    status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
    print(f"{status:20} {test_name}")
    if message:
        print(f"            → {message}")
    return passed

def test_flask_server():
    """Test if Flask server is running"""
    print_section("1. Flask Server Status")
    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        return test_result("Flask Server Running", True, f"Status Code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        return test_result("Flask Server Running", False, "Cannot connect to server")
    except Exception as e:
        return test_result("Flask Server Running", False, str(e))

def test_main_routes():
    """Test main application routes"""
    print_section("2. Main Routes")
    
    routes = {
        "Home Page": "/",
        "Login Page": "/auth/login",
        "Register Page": "/auth/register",
        "Menu Page": "/menu",
        "Dashboard": "/dashboard",
    }
    
    results = []
    for name, route in routes.items():
        try:
            response = requests.get(BASE_URL + route, timeout=TIMEOUT, allow_redirects=False)
            # Accept 200 (OK) or 302 (Redirect to login)
            passed = response.status_code in [200, 302]
            results.append(test_result(name, passed, f"Status: {response.status_code}"))
        except Exception as e:
            results.append(test_result(name, False, str(e)))
    
    return all(results)

def test_customer_dashboard():
    """Test customer dashboard file"""
    print_section("3. Customer Dashboard")
    
    import os
    dashboard_path = "templates/dashboards/customer.html"
    
    if not os.path.exists(dashboard_path):
        return test_result("Dashboard File Exists", False, "File not found")
    
    test_result("Dashboard File Exists", True, dashboard_path)
    
    # Check file size
    file_size = os.path.getsize(dashboard_path)
    is_simple = file_size < 20000  # Less than 20KB means simple version
    test_result("Simple Dashboard Active", is_simple, f"Size: {file_size:,} bytes")
    
    # Check content
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple dashboard checks
    checks = {
        "Has base template": "extends" in content,
        "Has header section": "dashboard-header" in content,
        "Has quick actions": "quick-action-card" in content,
        "Has stats section": "stat-card" in content,
        "No ultra-vibrant code": "gradientFlow" not in content and "createParticles" not in content,
    }
    
    results = []
    for check_name, passed in checks.items():
        results.append(test_result(check_name, passed))
    
    return all(results)

def test_database():
    """Test database connection"""
    print_section("4. Database")
    
    import os
    import sqlite3
    
    db_path = "database.db"
    
    if not os.path.exists(db_path):
        return test_result("Database File Exists", False, "database.db not found")
    
    test_result("Database File Exists", True, db_path)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['user', 'menu_item', 'order', 'order_details', 'payment', 'feedback', 'delivery']
        
        results = []
        for table in required_tables:
            exists = table in tables
            results.append(test_result(f"Table: {table}", exists))
        
        # Check user count
        cursor.execute("SELECT COUNT(*) FROM user")
        user_count = cursor.fetchone()[0]
        test_result("Users in Database", user_count > 0, f"Count: {user_count}")
        
        # Check menu items
        cursor.execute("SELECT COUNT(*) FROM menu_item")
        menu_count = cursor.fetchone()[0]
        test_result("Menu Items", menu_count > 0, f"Count: {menu_count}")
        
        conn.close()
        return all(results)
        
    except Exception as e:
        return test_result("Database Connection", False, str(e))

def test_static_files():
    """Test static files"""
    print_section("5. Static Files")
    
    import os
    
    files = {
        "Base Template": "templates/base.html",
        "Login Template": "templates/login.html",
        "Register Template": "templates/register.html",
    }
    
    results = []
    for name, path in files.items():
        exists = os.path.exists(path)
        results.append(test_result(name, exists, path if exists else "Not found"))
    
    return all(results)

def test_blueprints():
    """Test blueprint imports"""
    print_section("6. Blueprint Configuration")
    
    try:
        import sys
        import os
        sys.path.insert(0, os.getcwd())
        
        # Import app to check blueprints
        from app import app as flask_app
        
        blueprints = [
            'auth',
            'menu',
            'orders',
            'users',
            'payments',
            'feedback',
            'delivery',
            'kitchen',
            'recommendations',
            'reports'
        ]
        
        results = []
        for bp_name in blueprints:
            has_bp = bp_name in [bp.name for bp in flask_app.blueprints.values()]
            results.append(test_result(f"Blueprint: {bp_name}", has_bp))
        
        return all(results)
        
    except Exception as e:
        return test_result("Blueprint Import", False, str(e))

def test_cache_busting():
    """Test cache-busting headers"""
    print_section("7. Cache-Busting Headers")
    
    import os
    
    app_path = "app.py"
    if not os.path.exists(app_path):
        return test_result("app.py exists", False)
    
    with open(app_path, 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    checks = {
        "Has after_request": "@app.after_request" in app_content,
        "Has Cache-Control": "Cache-Control" in app_content,
        "Has Pragma": "Pragma" in app_content,
        "Has Expires": "Expires" in app_content,
    }
    
    results = []
    for check_name, passed in checks.items():
        results.append(test_result(check_name, passed))
    
    return all(results)

def test_file_structure():
    """Test project file structure"""
    print_section("8. Project File Structure")
    
    import os
    
    required = {
        "Files": [
            "app.py",
            "models.py",
            "database.db",
            "requirements.txt",
        ],
        "Directories": [
            "templates",
            "templates/dashboards",
            "routes",
            "static",
        ]
    }
    
    results = []
    
    for file_path in required["Files"]:
        exists = os.path.exists(file_path)
        results.append(test_result(f"File: {file_path}", exists))
    
    for dir_path in required["Directories"]:
        exists = os.path.isdir(dir_path)
        results.append(test_result(f"Directory: {dir_path}", exists))
    
    return all(results)

def generate_summary(results):
    """Generate test summary"""
    print_header("TEST SUMMARY")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"{BOLD}Total Tests:{RESET}     {total}")
    print(f"{GREEN}{BOLD}Passed:{RESET}         {passed}")
    print(f"{RED}{BOLD}Failed:{RESET}         {failed}")
    print(f"{BOLD}Success Rate:{RESET}   {percentage:.1f}%")
    
    if percentage == 100:
        print(f"\n{GREEN}{BOLD}🎉 ALL TESTS PASSED! Application is ready to use!{RESET}")
    elif percentage >= 80:
        print(f"\n{YELLOW}{BOLD}⚠️  Most tests passed. Some issues need attention.{RESET}")
    else:
        print(f"\n{RED}{BOLD}❌ Multiple tests failed. Please review errors above.{RESET}")
    
    print(f"\n{BOLD}Tested on:{RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Run all tests"""
    print_header("SMART FOOD ORDERING SYSTEM - APPLICATION TESTS")
    print(f"{BOLD}Testing Date:{RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{BOLD}Base URL:{RESET}     {BASE_URL}")
    
    results = {
        "Flask Server": test_flask_server(),
        "Main Routes": test_main_routes(),
        "Customer Dashboard": test_customer_dashboard(),
        "Database": test_database(),
        "Static Files": test_static_files(),
        "Blueprints": test_blueprints(),
        "Cache-Busting": test_cache_busting(),
        "File Structure": test_file_structure(),
    }
    
    generate_summary(results)
    
    # Access instructions
    print(f"\n{BOLD}{BLUE}{'=' * 80}{RESET}")
    print(f"{BOLD}🚀 HOW TO ACCESS THE APPLICATION:{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 80}{RESET}")
    print(f"\n1. Make sure Flask is running (should be running now)")
    print(f"2. Open browser and go to: {BOLD}{BASE_URL}{RESET}")
    print(f"3. Login as customer:")
    print(f"   - Username: {BOLD}Eriz{RESET}")
    print(f"   - Password: {BOLD}password{RESET}")
    print(f"4. Or login as admin:")
    print(f"   - Email: {BOLD}admin@foodsystem.com{RESET}")
    print(f"   - Password: {BOLD}admin123{RESET}")
    print(f"\n{YELLOW}💡 TIP: Clear browser cache (Ctrl+Shift+Delete) if you see old design{RESET}")
    print(f"{YELLOW}💡 TIP: Use Incognito mode (Ctrl+Shift+N) for fresh view{RESET}")
    print(f"\n{BOLD}{BLUE}{'=' * 80}{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Test interrupted by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{RED}Fatal error: {e}{RESET}")
        sys.exit(1)
