"""upload resume

Revision ID: b2963d885c86
Revises: 2604cf85f223
Create Date: 2025-04-02 12:28:20.834991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2963d885c86'
down_revision = '2604cf85f223'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.add_column(sa.Column('upload_resume', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('other_documents', sa.String(length=255), nullable=True))
        batch_op.alter_column('cover_letter',
               existing_type=sa.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.alter_column('cover_letter',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.drop_column('other_documents')
        batch_op.drop_column('upload_resume')

    # ### end Alembic commands ###
