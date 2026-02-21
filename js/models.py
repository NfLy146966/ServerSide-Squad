"""
ServerSide Squad - Database Models
Using SQLAlchemy with SQLite
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()


class Order(db.Model):
    """
    Model untuk tabel pesanan
    """
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    telepon = db.Column(db.String(20), nullable=False)
    layanan = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    budget = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        Convert order object to dictionary
        """
        return {
            'id': self.id,
            'nama': self.nama,
            'email': self.email,
            'telepon': self.telepon,
            'layanan': self.layanan,
            'deskripsi': self.deskripsi,
            'budget': self.budget,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Order {self.id}: {self.nama} - {self.layanan}>'
