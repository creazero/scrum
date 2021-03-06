"""add a done_date field to the task model

Revision ID: e3c0abbbf3ef
Revises: 6c48ea066952
Create Date: 2019-05-11 20:27:43.716444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3c0abbbf3ef'
down_revision = '6c48ea066952'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('done_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'done_date')
    # ### end Alembic commands ###
