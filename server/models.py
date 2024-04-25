from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    vendor_sweets = relationship("VendorSweet", back_populates="sweet")

    def __repr__(self):
        return f'<Sweet {self.name}>'

class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    vendor_sweets = relationship("VendorSweet", back_populates="vendor")

    def __repr__(self):
        return f'<Vendor {self.name}>'

class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    vendor_id = db.Column(db.Integer, ForeignKey('vendors.id'), nullable=False)
    sweet_id = db.Column(db.Integer, ForeignKey('sweets.id'), nullable=False)

    vendor = relationship("Vendor", back_populates="vendor_sweets")
    sweet = relationship("Sweet", back_populates="vendor_sweets")

    def __repr__(self):
        return f'<VendorSweet {self.price}>'

