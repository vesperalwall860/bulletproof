from project import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    overview = db.Column(db.String)
    description = db.Column(db.String)
    information = db.Column(db.String)
    price = db.Column(db.Float)
    old_price = db.Column(db.Float)
    pub_date = db.Column(db.DateTime)
    reviews = db.relationship('Review', backref='product', lazy='dynamic')
    images = db.relationship('Image', backref='product', lazy='dynamic')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    rate = db.Column(db.Integer)
    author = db.Column(db.String)
    author_email = db.Column(db.String)
    pub_date = db.Column(db.DateTime)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String)
    description = db.column(db.String)
    products = db.relationship('Product', backref='category', lazy='dynamic')


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_lines = db.relationship('OrderLine', backref='order', lazy='dynamic')


class OrderLine(db.Model):
    __tablename__ = 'order_line'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    qty = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    address = db.Column(db.String)
    password = db.Column(db.String)
    orders = db.relationship('Order', backref='user', lazy='dynamic')
