
from dataclasses import dataclass
from datetime import datetime
from src.utils import db

@dataclass
class Products(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(90), nullable=False)
    stock: int = db.Column(db.Integer, nullable=False)
    price: int = db.Column(db.Float, nullable=False)
    date_created: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_updated: datetime = db.Column(db.DateTime, nullable=True)
    description: str = db.Column(db.String(1000), nullable=False)
    product_images = db.relationship('ProductImages', backref=db.backref('products', lazy='joined'), lazy='select')
    product_views = db.relationship('ProductView', backref='products', lazy=True)


    def __repr__(self) -> str:
        return "name {}".format(self.name)


@dataclass
class ProductImages(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_upload: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    cover_image: int = db.Column()
    image_url: str = db.Column(db.String(200), nullable=False)
    product_id: int = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    def __repr__(self) -> str:
        return "image {}".format(self.image_url)

    

@dataclass
class ProductView(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    views: int = db.Column(db.Integer, nullable=False, default=0)
    click: int = db.Column(db.Integer, nullable=False, default=0)
    times: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    product_id: int = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)


    def __repr__(self) -> str:
        return "total view {}".format(self.views)