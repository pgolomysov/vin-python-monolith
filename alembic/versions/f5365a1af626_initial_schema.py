"""initial schema

Revision ID: f5365a1af626
Revises: 
Create Date: 2025-05-07 18:34:20.485068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5365a1af626'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('requests',
    sa.Column('uuid', sa.UUID(), nullable=False),
        sa.Column('vin', sa.String(17), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('done', sa.BOOLEAN(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True,),
        sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('email'), 'requests', ['email'], unique=False)

    op.create_table('cars',
        sa.Column('vin', sa.String(17), nullable=False),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True,),
        sa.PrimaryKeyConstraint('vin')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('requests')
    op.drop_table('cars')
