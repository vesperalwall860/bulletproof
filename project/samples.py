class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    file_name = db.Column(db.String)
    version = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)
    price = db.Column(db.Float)

class Purchase(db.Model):
    __tablename__ = 'purchase'
    uuid = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship(Product)
    downloads_left = db.Column(db.Integer, default=5)


@app.route('/buy', methods=['POST'])
def buy():
    stripe_token = request.form['stripeToken']
    email = request.form['stripeEmail']
    product_id = request.form['product_id']
    product = Product.query.get(product_id)
    try:
        charge = stripe.Charge.create(
                amount=int(product.price * 100),
                currency='usd',
                card=stripe_token,
                description=email)
    except stripe.CardError, e:
        return """<html><body><h1>Card Declined</h1><p>Your chard could not
        be charged. Please check the number and/or contact your credit card
        company.</p></body></html>"""
    print charge
    purchase = Purchase(uuid=str(uuid.uuid4()),
            email=email,
            product=product)
    db.session.add(purchase)
    db.session.commit()
    message = Message(
            subject='Thanks for your purchase!',
        sender="jeff@jeffknupp.com", 
        html="""<html><body><h1>Thanks for buying Writing Idiomatic Python!</h1>
<p>If you didn't already download your copy, you can visit 
<a href="http://buy.jeffknupp.com/{}">your private link</a>. You'll be able to
download the file up to five times, at which point the link will
expire.""".format(purchase.uuid),
        recipients=[email])
    with mail.connect() as conn:
        conn.send(message)
    return redirect('/{}'.format(purchase.uuid))


@app.route('/<uuid>')
def download_file(uuid):
    purchase = Purchase.query.get(uuid)
    if purchase:
        if purchase.downloads_left <= 0:
            return """<html><body><h1>No downloads left!</h1><p>You have
            exceeded the allowed number of downloads for this file. Please email
            jeff@jeffknupp.com with any questions.</p></body></html>"""
        purchase.downloads_left -= 1
        db.session.commit()
        return send_from_directory(directory='files',
                filename=purchase.product.file_name, as_attachment=True)
    else:
        abort(404)


# http://compare.platinumprioritas.com/member-dashboard-pages/html/#usa