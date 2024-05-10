"""Salt and WikiAura

Revision ID: a27a73211486
Revises: 
Create Date: 2024-05-09 11:35:55.511498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a27a73211486'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user', 'points', new_column_name = 'WikiAura')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_salt', sa.Text(), nullable=False))


def downgrade():
    op.alter_column('user', 'WikiAura', new_column_name = 'points')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('password_salt')

