// ServerSide Squad - JavaScript

// API Base URL
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const orderForm = document.getElementById('orderForm');
const ordersTableBody = document.getElementById('ordersTableBody');
const refreshBtn = document.getElementById('refreshBtn');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

// Service names mapping
const serviceNames = {
    'company_profile': 'Website Company Profile',
    'ecommerce': 'Website E-Commerce',
    'webapp': 'Web App Development',
    'responsive': 'Responsive Design',
    'seo': 'SEO Optimization',
    'hosting': 'Web Hosting & Domain',
    'lainnya': 'Lainnya'
};

// Budget mapping
const budgetNames = {
    '500k-1jt': 'Rp 500.000 - Rp 1.000.000',
    '1jt-3jt': 'Rp 1.000.000 - Rp 3.000.000',
    '3jt-5jt': 'Rp 3.000.000 - Rp 5.000.000',
    '5jt-10jt': 'Rp 5.000.000 - Rp 10.000.000',
    '10jt+': 'Rp 10.000.000+'
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadOrders();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Form submission
    if (orderForm) {
        orderForm.addEventListener('submit', handleFormSubmit);
    }

    // Refresh button
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadOrders);
    }

    // Mobile menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
                // Close mobile menu if open
                navLinks.classList.remove('active');
            }
        });
    });
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();

    // Get form data
    const formData = {
        nama: document.getElementById('nama').value,
        email: document.getElementById('email').value,
        telepon: document.getElementById('telepon').value,
        layanan: document.getElementById('layanan').value,
        deskripsi: document.getElementById('deskripsi').value,
        budget: document.getElementById('budget').value,
        status: 'pending'
    };

    try {
        const response = await fetch(`${API_BASE_URL}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            showToast('Pesanan berhasil dikirim!', 'success');
            orderForm.reset();
            loadOrders();
        } else {
            showToast(data.message || 'Gagal mengirim pesanan', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Terjadi kesalahan. Pastikan server berjalan!', 'error');
    }
}

// Load orders from API
async function loadOrders() {
    try {
        const response = await fetch(`${API_BASE_URL}/orders`);
        const orders = await response.json();

        if (response.ok) {
            renderOrders(orders);
        }
    } catch (error) {
        console.error('Error loading orders:', error);
        showToast('Gagal memuat data pesanan', 'error');
    }
}

// Render orders to table
function renderOrders(orders) {
    if (!ordersTableBody) return;

    ordersTableBody.innerHTML = '';

    if (orders.length === 0) {
        ordersTableBody.innerHTML = `
            <tr>
                <td colspan="7" style="text-align: center; padding: 40px; color: #64748b;">
                    <i class="fas fa-inbox" style="font-size: 2rem; margin-bottom: 10px;"></i><br>
                    Belum ada pesanan
                </td>
            </tr>
        `;
        return;
    }

    orders.forEach((order, index) => {
        const row = document.createElement('tr');
        const tanggal = new Date(order.created_at).toLocaleDateString('id-ID', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });

        row.innerHTML = `
            <td>${index + 1}</td>
            <td><strong>${order.nama}</strong></td>
            <td>${order.email}</td>
            <td>${serviceNames[order.layanan] || order.layanan}</td>
            <td>${budgetNames[order.budget] || order.budget}</td>
            <td><span class="status ${order.status}">${getStatusLabel(order.status)}</span></td>
            <td>${tanggal}</td>
        `;

        ordersTableBody.appendChild(row);
    });
}

// Get status label
function getStatusLabel(status) {
    const labels = {
        'pending': 'Menunggu',
        'processing': 'Diproses',
        'completed': 'Selesai',
        'cancelled': 'Dibatalkan'
    };
    return labels[status] || status;
}

// Show toast notification
function showToast(message, type = 'success') {
    toastMessage.textContent = message;
    toast.className = 'toast';

    if (type === 'error') {
        toast.classList.add('error');
    }

    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
