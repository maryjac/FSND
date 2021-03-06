"""Initial migration

Revision ID: d3fa960ac166
Revises: 
Create Date: 2020-03-30 17:41:24.850240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3fa960ac166'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('genres', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('persons')
    op.drop_table('table2')
    op.drop_table('table1')
    op.drop_table('todos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='todos_pkey')
    )
    op.create_table('table1',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='table1_pkey')
    )
    op.create_table('table2',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('completed', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='table2_pkey')
    )
    op.create_table('persons',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='persons_pkey')
    )
    op.drop_table('Venue')
    op.drop_table('Artist')
    # ### end Alembic commands ###
