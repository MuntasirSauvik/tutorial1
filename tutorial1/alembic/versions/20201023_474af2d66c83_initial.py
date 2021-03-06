"""initial

Revision ID: 474af2d66c83
Revises: 
Create Date: 2020-10-23 13:29:39.728320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '474af2d66c83'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chatrooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('roomDescription', sa.String(length=64), nullable=False),
    sa.Column('door', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_chatrooms')),
    sa.UniqueConstraint('roomDescription', name=op.f('uq_chatrooms_roomDescription'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('role', sa.Text(), nullable=False),
    sa.Column('loggedIn', sa.Boolean(), nullable=True),
    sa.Column('password_hash', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('name', name=op.f('uq_users_name'))
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message_text', sa.Text(), nullable=True),
    sa.Column('dateTime', sa.DateTime(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], name=op.f('fk_messages_creator_id_users')),
    sa.ForeignKeyConstraint(['room_id'], ['chatrooms.id'], name=op.f('fk_messages_room_id_chatrooms')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_messages'))
    )
    op.create_table('pages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('data', sa.Text(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], name=op.f('fk_pages_creator_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_pages')),
    sa.UniqueConstraint('name', name=op.f('uq_pages_name'))
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pages')
    op.drop_table('messages')
    op.drop_table('users')
    op.drop_table('chatrooms')
    # ### end Alembic commands ###
