"""update_accountactivation_status

Revision ID: d61b8eda995b
Revises: 219c014c39c1
Create Date: 2024-10-07 19:05:31.668126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd61b8eda995b'
down_revision: Union[str, None] = '219c014c39c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.execute("ALTER TABLE account_activations ALTER COLUMN status TYPE tokenstatus USING status::text::tokenstatus")



def downgrade() -> None:
        op.execute("ALTER TABLE account_activations ALTER COLUMN status TYPE accountstatus USING status::text::accountstatus")

