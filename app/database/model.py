from db import db
from datetime import datetime
from sqlalchemy import UniqueConstraint

class CurrencyRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(3), nullable=False)
    buying_rate = db.Column(db.Float(precision=5), nullable=False)
    selling_rate = db.Column(db.Float(precision=5), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    precision = db.Column(db.Integer, default=2, nullable=False)

    __table_args__ = (
        UniqueConstraint('currency_code', 'created_at', name='uix_currency_created_at'),
    )

    def __repr__(self):
        return f'<CurrencyRate {self.currency_code}: {self.rate}>'

    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d") if self.created_at else None

    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d") if self.updated_at else None
