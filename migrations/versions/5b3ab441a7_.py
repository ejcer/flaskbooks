"""empty message

Revision ID: 5b3ab441a7
Revises: None
Create Date: 2016-01-07 01:22:40.033406

"""

# revision identifiers, used by Alembic.
revision = '5b3ab441a7'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_posts_author_id', 'posts', ['author_id'], unique=False)
    op.create_index('ix_posts_timestamp', 'posts', ['timestamp'], unique=False)
    op.create_table('subscribers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_subscribers_email', 'subscribers', ['email'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_subscribers_email', 'subscribers')
    op.drop_table('subscribers')
    op.drop_index('ix_posts_timestamp', 'posts')
    op.drop_index('ix_posts_author_id', 'posts')
    op.drop_table('posts')
    ### end Alembic commands ###