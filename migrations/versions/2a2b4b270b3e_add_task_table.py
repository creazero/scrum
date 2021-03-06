"""Add task table

Revision ID: 2a2b4b270b3e
Revises: 889b5185015e
Create Date: 2019-05-09 17:10:00.367915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a2b4b270b3e'
down_revision = '889b5185015e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=False),
    sa.Column('description', sa.String(length=10000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('sprint_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('assignee_id', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.Column('state', sa.Enum('todo', 'in_process', 'testing', 'done', name='taskstate'), nullable=True),
    sa.ForeignKeyConstraint(['assignee_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['sprint_id'], ['sprints.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_project_id'), 'tasks', ['project_id'], unique=False)
    op.create_index(op.f('ix_tasks_sprint_id'), 'tasks', ['sprint_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_sprint_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_project_id'), table_name='tasks')
    op.drop_table('tasks')
    # ### end Alembic commands ###
