"""add sessions table"""

from alembic import op
import sqlalchemy as sa
from fastapi_users_db_sqlalchemy.generics import GUID
from typing import Sequence, Union

revision: str = 'db3285631796'
down_revision: Union[str, Sequence[str], None] = 'b753a375f3e8'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        'sessions',
        sa.Column('id_sess', GUID(), primary_key=True),
        sa.Column('user_id', GUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('psychologist_id', GUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('scheduled_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column(
            'status',
            sa.Enum(
                'requested',
                'approved',
                'rejected',
                'canceled',
                'finished',
                name='sessionstatus'
            ),
            nullable=False,
            server_default='requested'
        ),
        sa.Column('jitsi_url', sa.String(length=512), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('sessions')
    op.execute("DROP TYPE IF EXISTS sessionstatus")
