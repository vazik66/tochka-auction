"""init 2

Revision ID: 86830c1a98ca
Revises: cfc14b6074bb
Create Date: 2022-05-26 14:01:37.146767

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '86830c1a98ca'
down_revision = 'cfc14b6074bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bid',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bid_id'), 'bid', ['id'], unique=False)
    op.create_table('order',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_id'), 'order', ['id'], unique=False)
    op.add_column('item', sa.Column('min_bid', sa.Integer(), nullable=False))
    op.add_column('item', sa.Column('min_bid_step', sa.Integer(), server_default='1', nullable=True))
    op.add_column('item', sa.Column('is_ended', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('item', sa.Column('end_date', sa.DateTime(timezone=True), nullable=False))
    op.add_column('item', sa.Column('images', sa.ARRAY(sa.String()), server_default='{}', nullable=True))
    op.add_column('item', sa.Column('winner', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'item', 'user', ['winner'], ['id'])
    op.drop_column('item', 'is_moderating')
    op.drop_column('item', 'price')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('item', sa.Column('is_moderating', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.drop_column('item', 'winner')
    op.drop_column('item', 'images')
    op.drop_column('item', 'end_date')
    op.drop_column('item', 'is_ended')
    op.drop_column('item', 'min_bid_step')
    op.drop_column('item', 'min_bid')
    op.drop_index(op.f('ix_order_id'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_bid_id'), table_name='bid')
    op.drop_table('bid')
    # ### end Alembic commands ###
