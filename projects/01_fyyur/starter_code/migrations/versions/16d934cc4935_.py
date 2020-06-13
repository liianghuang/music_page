"""empty message

Revision ID: 16d934cc4935
Revises: b30c0ad91e7d
Create Date: 2020-05-26 21:43:40.022268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16d934cc4935'
down_revision = 'b30c0ad91e7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    op.drop_column('Artist', 'genres') 
    op.add_column('Artist', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###