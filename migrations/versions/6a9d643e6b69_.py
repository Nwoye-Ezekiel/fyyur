"""empty message

Revision ID: 6a9d643e6b69
Revises: 5f57539165a1
Create Date: 2022-08-18 08:29:15.103499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a9d643e6b69'
down_revision = '5f57539165a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('artists', 'website',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('venues', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('venues', 'website',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'website',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('venues', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('venues', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'website',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('artists', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('artists', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###
