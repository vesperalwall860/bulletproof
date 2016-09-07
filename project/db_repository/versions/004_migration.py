from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
order_line = Table('order_line', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('qty', INTEGER),
    Column('product', INTEGER),
    Column('order_id', INTEGER),
)

order_line = Table('order_line', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('product_id', Integer),
    Column('qty', Integer),
    Column('order_id', Integer),
)

order = Table('order', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user', INTEGER),
)

order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['order_line'].columns['product'].drop()
    post_meta.tables['order_line'].columns['product_id'].create()
    pre_meta.tables['order'].columns['user'].drop()
    post_meta.tables['order'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['order_line'].columns['product'].create()
    post_meta.tables['order_line'].columns['product_id'].drop()
    pre_meta.tables['order'].columns['user'].create()
    post_meta.tables['order'].columns['user_id'].drop()
