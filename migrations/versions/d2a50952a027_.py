"""empty message

Revision ID: d2a50952a027
Revises: db7eebc844de
Create Date: 2020-08-25 07:44:53.476063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2a50952a027'
down_revision = 'db7eebc844de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'about_me', ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'about_me', type_='unique')
    # ### end Alembic commands ###
