// Main JavaScript file for Smart Food Ordering System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Confirm delete actions
    document.querySelectorAll('.delete-confirm').forEach(function(element) {
        element.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Quantity selectors for cart
    document.querySelectorAll('.quantity-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            var input = this.parentElement.querySelector('.quantity-input');
            var currentValue = parseInt(input.value) || 0;
            var action = this.dataset.action;
            
            if (action === 'increase') {
                input.value = currentValue + 1;
            } else if (action === 'decrease' && currentValue > 1) {
                input.value = currentValue - 1;
            }
            
            // Trigger change event
            input.dispatchEvent(new Event('change'));
        });
    });

    // Update cart totals when quantities change
    document.querySelectorAll('.quantity-input').forEach(function(input) {
        input.addEventListener('change', function() {
            updateCartTotals();
        });
    });

    // Search functionality with debouncing
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                performSearch(searchInput.value);
            }, 300);
        });
    }

    // Category filter functionality
    document.querySelectorAll('.category-filter').forEach(function(filter) {
        filter.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all filters
            document.querySelectorAll('.category-filter').forEach(f => f.classList.remove('active'));
            
            // Add active class to clicked filter
            this.classList.add('active');
            
            // Filter items
            const category = this.dataset.category;
            filterItemsByCategory(category);
        });
    });

    // Form validation
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Rating stars
    document.querySelectorAll('.rating-stars').forEach(function(ratingContainer) {
        const stars = ratingContainer.querySelectorAll('.star');
        const ratingInput = ratingContainer.querySelector('.rating-input');
        
        stars.forEach(function(star, index) {
            star.addEventListener('click', function() {
                const rating = index + 1;
                ratingInput.value = rating;
                
                // Update star display
                stars.forEach(function(s, i) {
                    if (i < rating) {
                        s.classList.remove('far');
                        s.classList.add('fas');
                    } else {
                        s.classList.remove('fas');
                        s.classList.add('far');
                    }
                });
            });
            
            star.addEventListener('mouseenter', function() {
                const rating = index + 1;
                
                // Preview star display
                stars.forEach(function(s, i) {
                    if (i < rating) {
                        s.style.color = '#ffc107';
                    } else {
                        s.style.color = '#e9ecef';
                    }
                });
            });
        });
        
        ratingContainer.addEventListener('mouseleave', function() {
            const currentRating = parseInt(ratingInput.value) || 0;
            
            // Reset to current rating
            stars.forEach(function(s, i) {
                if (i < currentRating) {
                    s.style.color = '#ffc107';
                    s.classList.remove('far');
                    s.classList.add('fas');
                } else {
                    s.style.color = '#e9ecef';
                    s.classList.remove('fas');
                    s.classList.add('far');
                }
            });
        });
    });
});

// Update cart totals
function updateCartTotals() {
    let subtotal = 0;
    const cartItems = document.querySelectorAll('.cart-item');
    
    cartItems.forEach(function(item) {
        const quantity = parseInt(item.querySelector('.quantity-input').value) || 0;
        const price = parseFloat(item.dataset.price) || 0;
        const itemTotal = quantity * price;
        
        const totalElement = item.querySelector('.item-total');
        if (totalElement) {
            totalElement.textContent = '₹' + itemTotal.toFixed(2);
        }
        
        subtotal += itemTotal;
    });
    
    // Update subtotal
    const subtotalElement = document.getElementById('cart-subtotal');
    if (subtotalElement) {
        subtotalElement.textContent = '₹' + subtotal.toFixed(2);
    }
    
    // Calculate tax (assuming 10% tax)
    const tax = subtotal * 0.1;
    const taxElement = document.getElementById('cart-tax');
    if (taxElement) {
        taxElement.textContent = '₹' + tax.toFixed(2);
    }
    
    // Calculate total
    const total = subtotal + tax;
    const totalElement = document.getElementById('cart-total');
    if (totalElement) {
        totalElement.textContent = '₹' + total.toFixed(2);
    }
}

// Search functionality
function performSearch(query) {
    const items = document.querySelectorAll('.searchable-item');
    
    items.forEach(function(item) {
        const text = item.textContent.toLowerCase();
        const searchQuery = query.toLowerCase();
        
        if (text.includes(searchQuery)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

// Filter items by category
function filterItemsByCategory(category) {
    const items = document.querySelectorAll('.filterable-item');
    
    items.forEach(function(item) {
        const itemCategory = item.dataset.category;
        
        if (category === 'all' || itemCategory === category) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

// Show loading spinner
function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="spinner"></div>';
    }
}

// Hide loading spinner
function hideLoading(element, originalContent) {
    if (element) {
        element.innerHTML = originalContent;
    }
}

// Format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// Add to cart functionality
function addToCart(menuItemId, name, price) {
    const quantity = document.getElementById('quantity-' + menuItemId)?.value || 1;
    
    // Create form data
    const formData = new FormData();
    formData.append('menu_item_id', menuItemId);
    formData.append('quantity', quantity);
    
    // Show loading
    const addButton = document.getElementById('add-to-cart-' + menuItemId);
    const originalText = addButton?.innerHTML;
    showLoading(addButton);
    
    // Send AJAX request
    fetch('/orders/add_to_cart', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        // Show success message
        showToast('Item added to cart successfully!', 'success');
        
        // Update cart counter if exists
        updateCartCounter();
        
        // Reset button
        if (addButton) {
            hideLoading(addButton, originalText);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error adding item to cart', 'error');
        
        // Reset button
        if (addButton) {
            hideLoading(addButton, originalText);
        }
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(function() {
        toast.remove();
    }, 3000);
}

// Update cart counter
function updateCartCounter() {
    // This would typically fetch the current cart count from the server
    // For now, just increment the displayed counter
    const counter = document.getElementById('cart-counter');
    if (counter) {
        let count = parseInt(counter.textContent) || 0;
        counter.textContent = count + 1;
    }
}

// Delivery tracking
function trackDelivery(trackingCode) {
    if (!trackingCode) {
        trackingCode = document.getElementById('tracking-code')?.value;
    }
    
    if (!trackingCode) {
        showToast('Please enter a tracking code', 'warning');
        return;
    }
    
    // Create form and submit
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/delivery/track_by_code';
    
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'tracking_code';
    input.value = trackingCode;
    
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

// Initialize charts (if Chart.js is loaded)
function initializeCharts() {
    if (typeof Chart !== 'undefined') {
        // Sales chart
        const salesChart = document.getElementById('salesChart');
        if (salesChart) {
            const ctx = salesChart.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [], // Will be populated from data
                    datasets: [{
                        label: 'Sales',
                        data: [],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 2,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }
}

// Export functions for global use
window.addToCart = addToCart;
window.trackDelivery = trackDelivery;
window.showToast = showToast;
window.formatCurrency = formatCurrency;