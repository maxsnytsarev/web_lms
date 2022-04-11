"""добавили признак публикации

Revision ID: 59de5986df44
Revises: 
Create Date: 2022-03-27 16:49:37.199435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59de5986df44'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('is_published', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('news', 'is_published')
    # ### end Alembic commands ###
