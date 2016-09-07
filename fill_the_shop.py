import datetime, random
from project import db, models

category = "T Shirts"
# test overview
overview = """
T-bone magna enim kevin qui porchetta leberkas
short loin veniam. Beef ribs rump ut t-bone chuck,
filet mignon boudin doner. Consequat meatloaf ut,
aute brisket tongue deserunt jowl prosciutto boudin.
Pariatur in elit cupim, flank ham hock minim adipisicing
aute shankle pig ut andouille ribeye rump
"""

# test product description
description = """
<p>
Lorem ipsum dolor sit amet, consectetur adipisicing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua. Ut enim ad minim veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip.
</p>
<p>
Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id
est laborum. Sed ut perspiciatis unde omnis iste
natus error sit voluptatem accusantium doloremque laudantium.
</p>
"""

# test product information
information = """
<p>
Lorem ipsum dolor sit amet, consectetur adipisicing
elit, sed do eiusmod tempor incididunt ut labore et
dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip. (THIRD)
</p>
<p>
Excepteur sint occaecat cupidatat non proident, sunt
in culpa qui officia deserunt mollit anim id est laborum.
Sed ut perspiciatis unde omnis iste natus error sit voluptatem
accusantium doloremque laudantium. (THIRD)
</p>
"""
images = [
    {
    'title': 'Product Main Image',
    'url': '/static/img/product-img-main.png'
    },
    {
    'title': 'Product Image 1',
    'url': '/static/img/product-img.png'
    },
    {
    'title': 'Product Image 2',
    'url': '/static/img/product-img.png'
    },
    {
    'title': 'Product Image 3',
    'url': '/static/img/product-img.png'
    },
    {
    'title': 'Product Image 4',
    'url': '/static/img/product-img.png'
    },
]

product = {
    'name': 'Denim Shirts',
    'price': 50,
    'images': images,
    'overview': overview,
    'description': description,
    'information': information,
    'pub_date': datetime.datetime.utcnow(),

}

category = models.Category.query.get(1)

for i in range(1,9):
    test_product = models.Product( \
        name=product['name']+' '+str(i), overview=product['overview'], \
        description=product['description'], information=product['information'], \
        price=random.randint(50,100), pub_date=datetime.datetime.utcnow(), \
        category=category
    )

    for image in images:
        test_image = models.Image(title=image['title'], url=image['url'], \
            product=test_product)
        db.session.add(test_image)

    db.session.add(test_product)
    print('%r' % test_product)

db.session.commit()