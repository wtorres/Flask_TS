from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
trades = Table('trades', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('create_at', DateTime),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=35)),
    Column('email', String(length=40)),
    Column('status', String(length=1)),
    Column('valid', String(length=1)),
    Column('create_at', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['trades'].create()
    post_meta.tables['users'].columns['valid'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['trades'].drop()
    post_meta.tables['users'].columns['valid'].drop()
