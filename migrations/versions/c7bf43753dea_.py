"""empty message

Revision ID: c7bf43753dea
Revises: a10efe2aa38b
Create Date: 2016-01-23 10:43:57.454240

"""

# revision identifiers, used by Alembic.
revision = 'c7bf43753dea'
down_revision = 'a10efe2aa38b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fridges', sa.Column('quantity', sa.Float(), nullable=True))
    op.drop_column('fridges', 'quality')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fridges', sa.Column('quality', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_column('fridges', 'quantity')
    ### end Alembic commands ###