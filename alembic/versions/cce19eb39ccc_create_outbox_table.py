"""create outbox table

Revision ID: cce19eb39ccc
Revises: f5365a1af626
Create Date: 2025-08-30 13:33:27.713383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects as dialects


# revision identifiers, used by Alembic.
revision: str = 'cce19eb39ccc'
down_revision: Union[str, None] = 'f5365a1af626'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('outbox_relayer',
        sa.Column('id', sa.BIGINT(), nullable=False),
        sa.Column('event_type', sa.VARCHAR(255), nullable=False),
        sa.Column('payload', dialects.postgresql.JSONB, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('consumed_at', sa.TIMESTAMP(), nullable=True, ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('outbox_relayer')
    # ### end Alembic commands ###
