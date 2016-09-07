from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
product = Table('product', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=60)),
    Column('overview', String),
    Column('description', String),
    Column('information', String),
    Column('price', Float),
    Column('old_price', Float),
    Column('pub_date', DateTime),
    Column('category_id', Integer),
)

review = Table('review', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String),
    Column('rate', Integer),
    Column('author', String),
    Column('author_email', String),
    Column('pub_date', DateTime),
    Column('product_id', Integer),
)

order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user', Integer),
)

image = Table('image', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String),
    Column('title', String),
    Column('product_id', Integer),
)

order_line = Table('order_line', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('product', Integer),
    Column('qty', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['product'].columns['category_id'].create()
    post_meta.tables['review'].columns['product_id'].create()
    post_meta.tables['order'].columns['user'].create()
    post_meta.tables['image'].columns['product_id'].create()
    post_meta.tables['order_line'].columns['product'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['product'].columns['category_id'].drop()
    post_meta.tables['review'].columns['product_id'].drop()
    post_meta.tables['order'].columns['user'].drop()
    post_meta.tables['image'].columns['product_id'].drop()
    post_meta.tables['order_line'].columns['product'].drop()
