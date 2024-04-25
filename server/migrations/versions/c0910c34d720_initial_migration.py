"""Initial migration

Revision ID: c0910c34d720
Revises: b1db92b90945
Create Date: 2024-04-25 10:47:44.965814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0910c34d720'
down_revision = 'b1db92b90945'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sweets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vendors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vendor_sweets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('vendor_id', sa.Integer(), nullable=False),
    sa.Column('sweet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sweet_id'], ['sweets.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('vendor')
    op.drop_table('sweet')
    op.drop_table('vendor_sweet')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vendor_sweet',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('price', sa.INTEGER(), nullable=False),
    sa.Column('vendor_id', sa.INTEGER(), nullable=False),
    sa.Column('sweet_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['sweet_id'], ['sweet.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['vendor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sweet',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vendor',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('vendor_sweets')
    op.drop_table('vendors')
    op.drop_table('sweets')
    # ### end Alembic commands ###