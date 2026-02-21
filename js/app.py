"""
ServerSide Squad - Flask REST API
Jasa Pembuatan Website
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from models import db, Order
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'serversidesquad-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serverside_squad.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Initialize database
db.init_app(app)


# Create database tables
def create_tables():
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")


# API Routes

@app.route('/')
def index():
    """Home page - Serve the frontend"""
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', filename)


@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [order.to_dict() for order in orders]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order by ID"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404

        return jsonify({
            'success': True,
            'data': order.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['nama', 'email', 'telepon', 'layanan', 'deskripsi', 'budget']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'Field {field} is required'
                }), 400

        # Create new order
        new_order = Order(
            nama=data['nama'],
            email=data['email'],
            telepon=data['telepon'],
            layanan=data['layanan'],
            deskripsi=data['deskripsi'],
            budget=data['budget'],
            status='pending'
        )

        # Save to database
        db.session.add(new_order)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'data': new_order.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update order status"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404

        data = request.get_json()

        # Update fields if provided
        if 'status' in data:
            valid_statuses = ['pending', 'processing', 'completed', 'cancelled']
            if data['status'] not in valid_statuses:
                return jsonify({
                    'success': False,
                    'message': 'Invalid status'
                }), 400
            order.status = data['status']

        if 'nama' in data:
            order.nama = data['nama']
        if 'email' in data:
            order.email = data['email']
        if 'telepon' in data:
            order.telepon = data['telepon']
        if 'layanan' in data:
            order.layanan = data['layanan']
        if 'deskripsi' in data:
            order.deskripsi = data['deskripsi']
        if 'budget' in data:
            order.budget = data['budget']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order updated successfully',
            'data': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete order"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404

        db.session.delete(order)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/orders/<int:order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    """Update order status specifically"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404

        data = request.get_json()
        new_status = data.get('status')

        valid_statuses = ['pending', 'processing', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({
                'success': False,
                'message': 'Invalid status'
            }), 400

        order.status = new_status
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Status updated successfully',
            'data': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500


# Main entry point
if __name__ == '__main__':
    # Create database tables
    create_tables()

    # Run the app
    print("\n" + "="*50)
    print("🚀 ServerSide Squad API Server")
    print("="*50)
    print("🌐 URL: http://localhost:5000")
    print("📚 API: http://localhost:5000/api")
    print("="*50 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
