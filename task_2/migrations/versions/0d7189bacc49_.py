"""empty message

Revision ID: 0d7189bacc49
Revises: d192bee1b162
Create Date: 2021-01-16 12:57:03.797068

"""
import random

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import orm
from app import Cats

revision = '0d7189bacc49'
down_revision = 'd192bee1b162'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'cats', ['id'])
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    names = ['bamby', 'loly', 'karol', 'schrödinger', 'snowbubble', 'corny', 'jack', 'barsik', 'kitty', 'wanda',
             'marcus', 'tilda', 'becky', 'mini', 'mike', 'daisy', 'iron man', 'cap', 'snowball', 'backy']
    for idx, name in enumerate(names):
        session.add(Cats(
            name=name,
            image=f"images/{idx + 1 if idx < 15 else 'no_image'}.jpg",
            breed="unknown",
            description="no description",
            age=random.randint(1, 9),
        ))
    session.commit()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.query(Cats).delete()
    session.commit()
    # ### end Alembic commands ###