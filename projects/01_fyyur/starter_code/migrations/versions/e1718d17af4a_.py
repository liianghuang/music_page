"""empty message

Revision ID: e1718d17af4a
Revises: aabb9da47474
Create Date: 2020-05-26 22:26:40.039109

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e1718d17af4a'
down_revision = 'aabb9da47474'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'start_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
