from alembic import op
import sqlalchemy as sa
from fastapi_users_db_sqlalchemy.generics import GUID

revision = 'XXXX_initial'
down_revision = None
branch_labels = None
depends_on = None
user_role_enum = sa.Enum('user', 'psychologist', 'owner', name='userrole')
user_role_enum.create(op.get_bind())


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('email', sa.String(length=320), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('role', sa.Enum('user', 'psychologist', 'owner', name='userrole'), nullable=False, server_default='user'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        'profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', GUID(), sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
        sa.Column('display_name', sa.String(length=120)),
        sa.Column('bio', sa.Text()),
        sa.Column('timezone', sa.String(length=64)),
        sa.Column('avatar_url', sa.String(length=512)),
        sa.Column('phone', sa.String(length=32)),
        sa.Column('telegram', sa.String(length=64)),
        sa.Column('birth_date', sa.Date()),
    )

    op.create_table(
        'psychologist_profile',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', GUID(), sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
        sa.Column('specialization', sa.String(length=255)),
        sa.Column('experience_years', sa.Integer()),
        sa.Column('license_number', sa.String(length=255)),
        sa.Column('price_per_hour', sa.Integer()),
        sa.Column('bio', sa.Text()),
    )


def downgrade() -> None:
    op.drop_table('psychologist_profile')
    op.drop_table('profiles')
    op.drop_table('users')
