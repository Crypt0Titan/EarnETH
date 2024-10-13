"""Add score to WordlePlayer

Revision ID: a3730d5fa461
Revises: 8a8f0fe5c1b8
Create Date: 2024-10-12 06:52:50.792847
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a3730d5fa461'
down_revision = '8a8f0fe5c1b8'
branch_labels = None
depends_on = None

def upgrade():
    # Add score column to wordle_players
    op.add_column('wordle_players', sa.Column('score', sa.Integer(), nullable=True))

    # Copy data from high_score to score if high_score exists
    connection = op.get_bind()
    if 'high_score' in [column['name'] for column in connection.execute('PRAGMA table_info(wordle_players)').fetchall()]:
        op.execute('UPDATE wordle_players SET score = high_score')
        # Drop high_score column from wordle_players
        op.drop_column('wordle_players', 'high_score')

def downgrade():
    # Add high_score column back to wordle_players
    op.add_column('wordle_players', sa.Column('high_score', sa.INTEGER(), nullable=True))

    # Copy data from score to high_score
    op.execute('UPDATE wordle_players SET high_score = score')

    # Drop score column from wordle_players
    op.drop_column('wordle_players', 'score')