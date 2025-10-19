"""
Payment Gateway Configuration
Supports: Stripe, PayPal, Razorpay, and other payment methods
"""
import os
from decimal import Decimal

class PaymentConfig:
    """Base Payment Configuration"""
    
    # Supported Payment Gateways
    SUPPORTED_GATEWAYS = {
        'stripe': 'Stripe',
        'paypal': 'PayPal',
        'razorpay': 'Razorpay',
        'cash': 'Cash on Delivery',
        'card': 'Card Payment',
        'upi': 'UPI'
    }
    
    # Currency Settings
    DEFAULT_CURRENCY = 'INR'
    SUPPORTED_CURRENCIES = ['INR', 'USD', 'EUR', 'GBP']
    
    # Payment Status
    PAYMENT_STATUS = {
        'pending': 'Pending',
        'processing': 'Processing',
        'completed': 'Completed',
        'failed': 'Failed',
        'refunded': 'Refunded',
        'cancelled': 'Cancelled'
    }
    
    # Minimum and Maximum amounts
    MIN_PAYMENT_AMOUNT = Decimal('10.00')
    MAX_PAYMENT_AMOUNT = Decimal('100000.00')
    
    # Test Mode
    TEST_MODE = os.environ.get('PAYMENT_TEST_MODE', 'True') == 'True'
    
    # Webhook URLs (to be set in production)
    WEBHOOK_BASE_URL = os.environ.get('WEBHOOK_BASE_URL', 'http://localhost:5000')


class StripeConfig(PaymentConfig):
    """Stripe Payment Gateway Configuration"""
    
    # API Keys (use environment variables in production)
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', 'pk_test_your_key_here')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_your_key_here')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_your_webhook_secret')
    
    # Stripe Settings
    STRIPE_API_VERSION = '2023-10-16'
    STRIPE_PAYMENT_METHODS = ['card', 'upi']
    
    # Success and Cancel URLs
    STRIPE_SUCCESS_URL = '/payments/success'
    STRIPE_CANCEL_URL = '/payments/cancel'


class PayPalConfig(PaymentConfig):
    """PayPal Payment Gateway Configuration"""
    
    # API Credentials
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', 'your_client_id')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET', 'your_client_secret')
    
    # PayPal Mode
    PAYPAL_MODE = 'sandbox' if PaymentConfig.TEST_MODE else 'live'
    
    # PayPal API URLs
    PAYPAL_API_BASE_URL = (
        'https://api-m.sandbox.paypal.com' if PAYPAL_MODE == 'sandbox'
        else 'https://api-m.paypal.com'
    )
    
    # Success and Cancel URLs
    PAYPAL_RETURN_URL = '/payments/paypal/success'
    PAYPAL_CANCEL_URL = '/payments/paypal/cancel'


class RazorpayConfig(PaymentConfig):
    """Razorpay Payment Gateway Configuration (Popular in India)"""
    
    # API Keys
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_your_key_id')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'your_key_secret')
    
    # Razorpay Settings
    RAZORPAY_CURRENCY = 'INR'
    RAZORPAY_PAYMENT_CAPTURE = 1  # Auto capture
    
    # Webhook Secret
    RAZORPAY_WEBHOOK_SECRET = os.environ.get('RAZORPAY_WEBHOOK_SECRET', 'your_webhook_secret')
    
    # Success and Cancel URLs
    RAZORPAY_CALLBACK_URL = '/payments/razorpay/callback'


class CashPaymentConfig(PaymentConfig):
    """Cash on Delivery Configuration"""
    
    COD_ENABLED = True
    COD_MAX_AMOUNT = Decimal('5000.00')
    COD_CHARGE = Decimal('50.00')  # Extra charge for COD
    COD_CHARGE_PERCENT = Decimal('0.00')  # Or percentage


# Gateway Selection Helper
def get_gateway_config(gateway_name):
    """Get configuration for specific gateway"""
    configs = {
        'stripe': StripeConfig,
        'paypal': PayPalConfig,
        'razorpay': RazorpayConfig,
        'cash': CashPaymentConfig
    }
    return configs.get(gateway_name.lower(), PaymentConfig)


# Payment Method Icons and Display Names
PAYMENT_METHOD_INFO = {
    'stripe': {
        'name': 'Credit/Debit Card (Stripe)',
        'icon': 'fa-credit-card',
        'color': '#6772E5',
        'description': 'Pay securely with your card'
    },
    'paypal': {
        'name': 'PayPal',
        'icon': 'fa-paypal',
        'color': '#0070BA',
        'description': 'Pay with your PayPal account'
    },
    'razorpay': {
        'name': 'Razorpay (UPI/Card/Wallet)',
        'icon': 'fa-mobile-alt',
        'color': '#3395FF',
        'description': 'Pay with UPI, Cards, or Wallets'
    },
    'upi': {
        'name': 'UPI Payment',
        'icon': 'fa-qrcode',
        'color': '#097969',
        'description': 'Pay using UPI apps'
    },
    'card': {
        'name': 'Debit/Credit Card',
        'icon': 'fa-credit-card',
        'color': '#2C3E50',
        'description': 'Pay with card on delivery'
    },
    'cash': {
        'name': 'Cash on Delivery',
        'icon': 'fa-money-bill-wave',
        'color': '#27AE60',
        'description': 'Pay cash when order arrives'
    }
}
