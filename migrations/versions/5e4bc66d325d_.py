"""empty message

Revision ID: 5e4bc66d325d
Revises: 613de977a694
Create Date: 2019-11-04 17:31:45.016254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e4bc66d325d'
down_revision = '613de977a694'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('aspirante', sa.Column('perfil', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('aspirante', 'perfil')
    # ### end Alembic commands ###
