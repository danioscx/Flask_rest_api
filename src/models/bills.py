from dataclasses import dataclass
from src.utils import db


@dataclass
class Bill(db.Model):
    pass

@dataclass
class PaymentInfo(db.Model):
    pass
