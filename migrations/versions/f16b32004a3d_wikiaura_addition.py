"""WikiAura addition

Revision ID: f16b32004a3d
Revises: 
Create Date: 2024-05-09 10:20:54.262378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f16b32004a3d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user', 'points', new_column_name = 'WikiAura')



def downgrade():
    op.alter_column('user', 'WikiAura', new_column_name = 'points')
