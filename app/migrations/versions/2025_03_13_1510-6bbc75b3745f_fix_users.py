"""fix: users

Revision ID: 6bbc75b3745f
Revises: 85967aecdd6b
Create Date: 2025-03-13 15:10:07.406524

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6bbc75b3745f"
down_revision: Union[str, None] = "85967aecdd6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("user_referal_code", sa.String(), nullable=True))
    op.add_column("users", sa.Column("other_referal_code", sa.String(), nullable=True))
    op.drop_column("users", "referal_code")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("referal_code", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("users", "other_referal_code")
    op.drop_column("users", "user_referal_code")
