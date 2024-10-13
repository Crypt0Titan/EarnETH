"""Add total_score and games_played to WordlePlayer

Revision ID: 09d2c5067ab2
Revises: a3730d5fa461
Create Date: 2024-10-12 07:21:07.345729
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '09d2c5067ab2'
down_revision = 'a3730d5fa461'
branch_labels = None
depends_on = None

def upgrade():
    # Check if total_score column exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = inspector.get_columns('wordle_players')
    column_names = [c['name'] for c in columns]

    if 'total_score' not in column_names:
        op.add_column('wordle_players', sa.Column('total_score', sa.Integer(), nullable=True))

    if 'games_played' not in column_names:
        op.add_column('wordle_players', sa.Column('games_played', sa.Integer(), nullable=True))

    # Update wordle_players to set default values
    op.execute('UPDATE wordle_players SET total_score = 0, games_played = 0 WHERE total_score IS NULL OR games_played IS NULL')

    # For game table, create a new table with the desired schema
    op.create_table('new_game',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('has_started', sa.Boolean(), nullable=True),
        sa.Column('player_id', sa.Integer(), nullable=True),
        sa.Column('level', sa.Integer(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('contract_address', sa.String(length=42), nullable=True),
        sa.Column('token_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from the old game table to the new one
    op.execute('INSERT INTO new_game SELECT * FROM game')

    # Drop the old game table
    op.drop_table('game')

    # Rename the new game table to the original name
    op.rename_table('new_game', 'game')

    # For player table, create a new table with the desired schema
    op.create_table('new_player',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ethereum_address', sa.String(length=42), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('password_hash', sa.String(length=128), nullable=True),
        sa.Column('rewards_paid', sa.Boolean(), nullable=True, server_default=sa.text('0')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ethereum_address')
    )

    # Copy data from the old player table to the new one
    op.execute('INSERT INTO new_player SELECT * FROM player')

    # Drop the old player table
    op.drop_table('player')

    # Rename the new player table to the original name
    op.rename_table('new_player', 'player')

def downgrade():
    # Remove total_score and games_played from wordle_players if they exist
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = inspector.get_columns('wordle_players')
    column_names = [c['name'] for c in columns]

    if 'total_score' in column_names:
        op.drop_column('wordle_players', 'total_score')

    if 'games_played' in column_names:
        op.drop_column('wordle_players', 'games_played')

    # For game table, revert to the original schema
    op.create_table('old_game',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('has_started', sa.Boolean(), nullable=True),
        sa.Column('player_id', sa.Integer(), nullable=True),
        sa.Column('level', sa.Integer(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('contract_address', sa.String(length=42), nullable=True),
        sa.Column('token_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.execute('INSERT INTO old_game SELECT * FROM game')
    op.drop_table('game')
    op.rename_table('old_game', 'game')

    # For player table, revert to the original schema
    op.create_table('old_player',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ethereum_address', sa.String(length=42), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('password_hash', sa.String(length=128), nullable=True),
        sa.Column('rewards_paid', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ethereum_address')
    )
    op.execute('INSERT INTO old_player SELECT * FROM player')
    op.drop_table('player')
    op.rename_table('old_player', 'player')