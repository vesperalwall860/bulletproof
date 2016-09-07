import datetime
import json
from project import app, models, forms, mail, db
from flask import render_template, flash, redirect, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message


def generate_cart_html():
    """ Generates the inner html of our cart. It is an unordable list."""
    cart_ul_inner = ''
    total = 0

    for key, value in session['cart']['products'].items():
        cart_ul_inner += \
        '<li><span class="delete" data-id="%s">X</span> %s x %d = $%d</li>' \
         % (key, value['name'], value['qty'], value['qty'] * value['price'])
        total += value['qty'] * value['price']

    session['cart']['total'] = total
    cart_ul_inner += '<li><strong>Total: $%d</strong></li>' % total

    if len(session['cart']['products']) == 0:
        return 'Empty'

    return cart_ul_inner


@app.context_processor
def inject_cart():
    if 'cart' in session:
        return dict(cart=session['cart'])
    else:
        return dict(cart=dict())

@app.route('/')
@app.route('/shop')
def shop():
    # get the first test category and all its products
    category = models.Category.query.get(1)
    products = category.products.all()

    for product in products:
        reviews = product.reviews.all()
        images = product.images.all()

        if reviews:
            rate_sum = 0
            for review in reviews:
                rate_sum += review.rate
                rate = round(rate_sum / len(reviews))
        else:
            rate = 0
        product.rate = rate

        if images:
            product.image = images[0]

    context = {
        'title': 'Shop',
        'active_menu': 'shop',
        'products': products,
    }

    # '**context' unpacks the context dictionary
    # to the function keyword arguments
    return render_template('shop.html', **context)


@app.route('/product/<int:product_id>')
def shop_inner(product_id):
    product = models.Product.query.get(product_id)

    reviews = product.reviews.all()
    images = product.images.all()

    if reviews:
        # calculate the average rate of the whole reviews' rates
        rate_sum = 0
        for review in reviews:
            rate_sum += review.rate
            rate = round(rate_sum / len(reviews))
    else:
        rate = 0
    product.rate = rate

    if images:
        product.image = images[0]

    context = {
        'title': 'Shop Inner',
        'active_menu': 'shop',
        'product': product
    }

    # '**context' unpacks the context dictionary
    # to the function keyword arguments
    return render_template('shop-inner.html', **context)


@app.route('/cart/add/<int:product_id>', methods=['GET'])
def cart_add(product_id):
    qty = request.args.get('qty')

    # if the quantity is not provided, set it to 1
    if qty is None or len(qty) == 0:
        qty = 1

    # if the quantity provided wrong, set it to 1
    try:
        qty = int(qty)
    except ValueError:
        qty = 1

    # this is the product we want to add to the cart
    product = models.Product.query.get(product_id)

    if not product:
        return 'None'

    product_info = {
        'name': product.name,
        'price': product.price,
        'qty': qty
    }

    product_id = str(product_id)

    # checks to see if the user has already started a cart
    if 'cart' in session:
        # if the product is not in the cart, then add it
        if not product_id in session['cart']['products']:
            session['cart']['products'][product_id] = product_info
        
        # if the product is already in the cart, update the quantity
        elif product_id in session['cart']['products']:
            session['cart']['products'][product_id]['qty'] += qty

    else:
        session['cart'] = {}
        session['cart']['products'] = {}
        session['cart']['products'][product_id] = product_info

    session.modified = True

    cart_ul_inner = generate_cart_html()

    return cart_ul_inner


@app.route('/cart/delete/<int:product_id>')
def cart_delete(product_id):
    product_id = str(product_id)

    # checks to see if the user has already started a cart
    if 'cart' in session:
        if product_id in session['cart']['products']:
            del session['cart']['products'][product_id]
            session.modified = True
    else:
        return 'None'

    cart_ul_inner = generate_cart_html()

    return cart_ul_inner


@app.route('/checkout', methods=['GET','POST'])
def checkout():
    form = forms.CheckoutForm()
    order_sent = False

    if form.validate_on_submit():
        msg = Message("Order received",
                      sender=("Bulletproof Shop",
                              "bulletproof.sell@gmail.com"),
                      recipients=["d1mskat@gmail.com", form.email.data])

        # create a html table which we will put into the email
        products_table = """
        <table cellpadding="0" cellspacing="0">
            <tr>
            <th style="border: 1px solid #333; padding: 5px 10px; text-align: center;">
                Name
            </th>
            <th style="border: 1px solid #333; border-left: none; border-right: none; padding: 5px 10px; text-align: center;">
                Qty
            </th>
            <th style="border: 1px solid #333; padding: 5px 10px; text-align: center;">
                Total Price
            </th>
            </tr>
        """
        for key, value in session['cart']['products'].items():
            products_table += """
            <tr>
            <td style="border: 1px solid #333; border-top: none; padding: 5px 10px; text-align: center;">
                %s
            </td>
            <td style="border: 1px solid #333; border-top: none; border-left: none; border-right: none; padding: 5px 10px; text-align: center;">
                %d
            </td>
            <td style="border: 1px solid #333; border-top: none; padding: 5px 10px; text-align: center;">
                $%d
            </td>
            </tr>
            """ % (value['name'], value['qty'], value['qty'] * value['price'])
        products_table += """
        <tr>
        <td style="border: 1px solid #333; border-top: none; padding: 5px 10px; text-align: center;"></td>
        <td style="border: 1px solid #333; border-top: none; border-left: none; border-right: none; padding: 5px 10px; text-align: center;"><b>Total:</b></td>
        <td style="border: 1px solid #333; border-top: none; padding: 5px 10px; text-align: center;"><b>$%d</b></td>
        </tr>
        """ % session['cart']['total']
        products_table += '</table>'

        # clear the cart
        session['cart']['products'] = {}
        session.modified = True

        msg.html = """
        <p>
            An order with the following data has been received:
        </p>
        <ul>
            <li>First Name: %s</li>
            <li>Last Name: %s</li>
            <li>Email: %s</li>
            <li>Address: %s</li>
        </ul>
        <p>Ordered products:</p>
        %s
        """ % (form.first_name.data, form.last_name.data, form.email.data,
            form.address.data, products_table)

        # send the email
        with app.app_context():
            mail.send(msg)

        order_sent = True

    context = {
        'title': 'Checkout',
        'active_menu': 'shop',
        'form': form,
        'order_sent': order_sent
    }

    return render_template('checkout.html', **context)


@app.route('/review/add/<int:product_id>', methods=['GET','POST'])
def review_add(product_id):
    # this is the product we want to add the review to
    product = models.Product.query.get(product_id)

    if not product:
        return 'None'

    # if it was sent from our js script
    if request.method == 'POST':
        author = request.form.get('author')
        author_email = request.form.get('author_email')
        text = request.form.get('text')
        rate = request.form.get('rate')

        # add the new review to a database
        review = models.Review(author=author, author_email=author_email,
            text=text, rate=int(rate), pub_date=datetime.datetime.utcnow(),
            product=product)
        db.session.add(review)
        db.session.commit()

        # generate the output html with the all product's reviews
        product = models.Product.query.get(product_id)
        reviews = product.reviews.all()

        html_output = ""

        for review in reviews:
            html_output += """
            <p>
            Author: <strong>%s</strong>
            </p>
            <p>
            Rate: <strong>%s</strong>
            </p>
            <p style="border-bottom: 1px solid #707070;">
            Text:<br>%s
            <br><br>
            </p>
            """ % (review.author, review.rate, review.text)

        return html_output

    # if it was not sent by our js script
    else:
        return 'None'


@app.route('/member-page')
def member_page():
    context = {
        'title': 'Member Page',
        'active_menu': 'home',
    }

    # '**context' unpacks the context dictionary
    # to the function keyword arguments
    return render_template('member-page.html', **context)


@app.route('/member-account')
def member_account():
    # all the variables below are created for test purposes
    # and will be replaced with the objects from a database
    context = {
        'title': 'Member Account',
        'active_menu': 'member_account',
        'email': 'test@test.com',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'profile_image': {
            'title': 'Profile Image',
            'url': '/static/img/profile-photo.png'
        }
    }

    # '**context' unpacks the context dictionary
    # to the function keyword arguments
    return render_template('member-account.html', **context)


@app.route('/live-bulletproof')
def live_bulletproof():
    # all the variables below are created for test purposes
    # and will be replaced with the objects from a database

    # test live items
    live_sample_text = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    """
    live_sample = {
        'title': 'Lorem Ipsum',
        'text': live_sample_text
    }
    lives = [live_sample, live_sample]

    context = {
        'title': 'Live Bulletproof',
        'active_menu': 'live_bulletproof',
        'lives': lives
    }

    # '**context' unpacks the context dictionary
    # to the function keyword arguments
    return render_template('live-bulletproof.html', **context)


@app.route('/live-bulletproof-details')
def live_bulletproof_details():
    # all the variables below are created for test purposes
    # and will be replaced with the objects from a database

    # test bulletproof text
    post_text = """
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem
    ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua.</p>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem
    ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua.</p>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
    eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem
    ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua.</p>
    """

    context = {
        'title': 'Live Bulletproof Details',
        'active_menu': 'live_bulletproof',
        'post_title': 'Lorem Ipsum Dolor Sit Amet',
        'post_date': '25 July 2016',
        'post_text': post_text,
        'post_images': [
        {
            'title': 'Live Bulletproof Details Image 1',
            'url': '/static/img/bulletproof-details-img1.png'
        },
        {
            'title': 'Live Bulletproof Details Image 2',
            'url': '/static/img/bulletproof-details-img2.png'
        }
        ]
    }

    # '**context' unpacks the context dictionary
    # to the function keyword arguments
    return render_template('live-bulletproof-details.html', **context) 


@app.route('/limited-time-offer')
def limited_time_offer():
    # all the variables below are created for test purposes
    # and will be replaced with the objects from a database

    # test offers
    offers = [
    {
        'title': 'Health Protection',
        'description': 'lorem ipsum dolor',
        'old_price': 2500000.00,
        'price': 2000000.00,
        'image': {'title': 'Health Protection', 
                  'url': '/static/img/limited-offer-img.png'},
        'discount': 20
    },
    {
        'title': 'Travel Protection',
        'description': 'lorem ipsum dolor',
        'old_price': 2500000.00,
        'price': 2000000.00,
        'image': {'title': 'Health Protection', 
                  'url': '/static/img/limited-offer-img.png'},
        'discount': 20
    },
    {
        'title': 'Accident Protection',
        'description': 'lorem ipsum dolor',
        'old_price': 2500000.00,
        'price': 2000000.00,
        'image': {'title': 'Health Protection', 
                  'url': '/static/img/limited-offer-img.png'},
        'discount': 20
    },
    {
        'title': 'Gear Protection',
        'description': 'lorem ipsum dolor',
        'old_price': 2500000.00,
        'price': 2000000.00,
        'image': {'title': 'Health Protection', 
                  'url': '/static/img/limited-offer-img.png'},
        'discount': 20
    },
    ]

    context = {
        'title': 'Limited Time Offers',
        'active_menu': 'limited_time_offer',
        'offers': offers
    }

    # '**context' unpacks the context dictionary
    # to the function keyword arguments
    return render_template('limited-time-offer.html', **context)