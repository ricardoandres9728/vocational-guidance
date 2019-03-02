"""empty message

Revision ID: 6cf10ba97a49
Revises: 
Create Date: 2019-02-24 13:38:35.188560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cf10ba97a49'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('perfil',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=True),
    sa.Column('live', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tipo_usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('encuesta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_perfil', sa.Integer(), nullable=True),
    sa.Column('preguntas', sa.JSON(), nullable=True),
    sa.Column('live', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_perfil'], ['perfil.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('correo', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('live', sa.Boolean(), nullable=True),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
    sa.Column('id_tipo_usuario', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_tipo_usuario'], ['tipo_usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo')
    )
    op.create_table('aspirante',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombres', sa.String(length=80), nullable=True),
    sa.Column('apellidos', sa.String(length=80), nullable=True),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.Column('newsletter', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_usuario')
    )
    op.create_table('colegio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=True),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_usuario')
    )
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comentario', sa.String(length=500), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
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
    op.drop_table('feedback')
    op.drop_table('colegio')
    op.drop_table('aspirante')
    op.drop_table('usuario')
    op.drop_table('encuesta')
    op.drop_table('tipo_usuario')
    op.drop_table('perfil')
    # ### end Alembic commands ###