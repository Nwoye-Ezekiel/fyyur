"""empty message

Revision ID: 1afdf8f19f39
Revises: 58c0aff4a636
Create Date: 2022-08-17 14:10:14.736077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1afdf8f19f39'
down_revision = '58c0aff4a636'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.drop_column('artists', 'venue_search')
    op.add_column('venues', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.drop_column('venues', 'talent_search')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('talent_search', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('venues', 'seeking_talent')
    op.add_column('artists', sa.Column('venue_search', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('artists', 'seeking_venue')
    # ### end Alembic commands ###
