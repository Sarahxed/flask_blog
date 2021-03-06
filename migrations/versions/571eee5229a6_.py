"""empty message

Revision ID: 571eee5229a6
Revises: d2a50952a027
Create Date: 2020-08-25 08:07:04.918091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '571eee5229a6'
down_revision = 'd2a50952a027'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message_board',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.String(length=300), nullable=False),
    sa.Column('mdatetime', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message_board')
    # ### end Alembic commands ###
