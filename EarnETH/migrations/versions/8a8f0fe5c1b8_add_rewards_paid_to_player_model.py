"""Add rewards_paid to Player model

Revision ID: 8a8f0fe5c1b8
Revises: 706b19af7a62
Create Date: 2024-10-11 04:57:47.120847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a8f0fe5c1b8'
down_revision = '706b19af7a62'
branch_labels = None
depends_on = None


def upgrade():
    # Add rewards_paid column to Player table
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rewards_paid', sa.Boolean(), nullable=True))

    # Update existing rows to set rewards_paid to False
    op.execute("UPDATE player SET rewards_paid = 0")

    # Make rewards_paid non-nullable
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.alter_column('rewards_paid', nullable=False, server_default=sa.text('0'))

    # Note: We're not altering the game table in this migration to avoid SQLite limitations


def downgrade():
    # Remove rewards_paid column from Player table
    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.drop_column('rewards_paid')

    # Note: We're not altering the game table in the downgrade either