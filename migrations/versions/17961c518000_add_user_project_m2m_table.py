"""Add user-project m2m table

Revision ID: 17961c518000
Revises: e7655e971327
Create Date: 2019-05-05 20:24:28.320047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17961c518000'
down_revision = 'e7655e971327'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accessible_projects',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('owner', 'dev', name='roles'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'project_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('accessible_projects')
    # ### end Alembic commands ###