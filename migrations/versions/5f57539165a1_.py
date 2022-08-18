"""empty message

Revision ID: 5f57539165a1
Revises: ddf3ab38634b
Create Date: 2022-08-18 07:19:31.242442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f57539165a1'
down_revision = 'ddf3ab38634b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('venues', sa.Column('created_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'created_at')
    op.drop_column('artists', 'created_at')
    # ### end Alembic commands ###