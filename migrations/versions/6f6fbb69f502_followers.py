"""followers

Revision ID: 6f6fbb69f502
Revises: bafe7aa4f629
Create Date: 2023-03-19 17:33:21.885076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f6fbb69f502'
down_revision = 'bafe7aa4f629'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follower',
    sa.Column('follwer_id', sa.Integer(), nullable=True),
    sa.Column('follwed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['follwed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follwer_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('follower')
    # ### end Alembic commands ###
