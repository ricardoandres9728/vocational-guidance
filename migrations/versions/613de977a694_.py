"""empty message

Revision ID: 613de977a694
Revises: 
Create Date: 2019-10-22 14:51:12.032687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '613de977a694'
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
    sa.Column('live', sa.Boolean(), nullable=True),
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
    op.create_table('muestra',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_encuesta', sa.Integer(), nullable=True),
    sa.Column('id_perfil', sa.Integer(), nullable=True),
    sa.Column('live', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_encuesta'], ['encuesta.id'], ),
    sa.ForeignKeyConstraint(['id_perfil'], ['perfil.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pregunta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pregunta', sa.String(), nullable=True),
    sa.Column('id_encuesta', sa.Integer(), nullable=True),
    sa.Column('live', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_encuesta'], ['encuesta.id'], ),
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
    op.create_table('muestra_respuesta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_muestra', sa.Integer(), nullable=True),
    sa.Column('id_pregunta', sa.Integer(), nullable=True),
    sa.Column('valor', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_muestra'], ['muestra.id'], ),
    sa.ForeignKeyConstraint(['id_pregunta'], ['pregunta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recomendacion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recomendacion', sa.String(), nullable=True),
    sa.Column('id_pregunta', sa.Integer(), nullable=True),
    sa.Column('live', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_pregunta'], ['pregunta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('respuesta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_pregunta', sa.Integer(), nullable=True),
    sa.Column('respuesta', sa.String(), nullable=True),
    sa.Column('valor', sa.Integer(), nullable=True),
    sa.Column('live', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_pregunta'], ['pregunta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('aspirante_respuesta',
    sa.Column('aspirante_id', sa.Integer(), nullable=False),
    sa.Column('respuesta_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['aspirante_id'], ['aspirante.id'], ),
    sa.ForeignKeyConstraint(['respuesta_id'], ['respuesta.id'], ),
    sa.PrimaryKeyConstraint('aspirante_id', 'respuesta_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('aspirante_respuesta')
    op.drop_table('respuesta')
    op.drop_table('recomendacion')
    op.drop_table('muestra_respuesta')
    op.drop_table('aspirante_colegio')
    op.drop_table('pregunta')
    op.drop_table('muestra')
    op.drop_table('feedback')
    op.drop_table('colegio')
    op.drop_table('aspirante')
    op.drop_table('usuario')
    op.drop_table('encuesta')
    op.drop_table('tipo_usuario')
    op.drop_table('perfil')
    # ### end Alembic commands ###