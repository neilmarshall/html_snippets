"""empty message

Revision ID: 3fbe37f9b019
Revises: 
Create Date: 2019-04-17 22:09:22.702051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fbe37f9b019'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news_sources',
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('source_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('source_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('token', sa.String(length=64), nullable=True),
    sa.Column('token_expiry', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news_requests',
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('news_source', sa.Integer(), nullable=False),
    sa.Column('request_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['news_source'], ['news_sources.source_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('request_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news_requests')
    op.drop_table('users')
    op.drop_table('news_sources')
    # ### end Alembic commands ###