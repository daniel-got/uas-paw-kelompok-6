"""merge daniel and martino heads

Revision ID: d686fee292f3
Revises: 2a4e6ca3dfc9, d40a54c84672
Create Date: 2025-12-18 12:36:25.534090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd686fee292f3'
down_revision: Union[str, Sequence[str], None] = ('2a4e6ca3dfc9', 'd40a54c84672')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
