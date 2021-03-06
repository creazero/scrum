"""Make project_id field in Sprint's model not nullable

Revision ID: 889b5185015e
Revises: 84bcfe5dbe74
Create Date: 2019-05-09 15:32:16.298650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '889b5185015e'
down_revision = '84bcfe5dbe74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sprints', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sprints', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
