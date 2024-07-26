"""empty message

Revision ID: e38f5e592211
Revises: c8030d2572c0
Create Date: 2024-07-25 13:33:03.628470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e38f5e592211'
down_revision = 'c8030d2572c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.drop_column('eye')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('eye', sa.VARCHAR(length=20), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
