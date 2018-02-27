"""empty message

Revision ID: 75fc46b14493
Revises: 
Create Date: 2018-02-26 21:03:14.378656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75fc46b14493'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tipo_usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('correo', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=80), nullable=True),
    sa.Column('live', sa.Boolean(), nullable=True),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.Column('id_tipo_usuario', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_tipo_usuario'], ['tipo_usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo')
    )
    op.create_table('aspirante',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=True),
    sa.Column('documento', sa.String(length=80), nullable=True),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('documento'),
    sa.UniqueConstraint('id_usuario')
    )
    op.create_table('colegio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=True),
    sa.Column('documento', sa.String(length=80), nullable=True),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('documento'),
    sa.UniqueConstraint('id_usuario')
    )
    op.create_table('aspirante_colegio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_colegio', sa.Integer(), nullable=True),
    sa.Column('id_aspirante', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_aspirante'], ['aspirante.id'], ),
    sa.ForeignKeyConstraint(['id_colegio'], ['colegio.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_aspirante')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('aspirante_colegio')
    op.drop_table('colegio')
    op.drop_table('aspirante')
    op.drop_table('usuario')
    op.drop_table('tipo_usuario')
    # ### end Alembic commands ###
