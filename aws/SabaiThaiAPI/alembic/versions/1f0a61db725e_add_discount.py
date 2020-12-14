"""add discount

Revision ID: 1f0a61db725e
Revises: 5008728999b7
Create Date: 2020-12-14 17:31:57.493843

"""
from datetime import datetime
from decimal import Decimal

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f0a61db725e'
down_revision = '5008728999b7'
branch_labels = None
depends_on = None


import os, sys
sys.path.append(os.getcwd())

from api.models import Discount

CODE = 'dec 2020'
PER_ITEM = 0
PERCENT = 10
END_DATE = datetime(2020, 12, 24, 13).isoformat() # 25 dec AEDT

def upgrade():
    op.execute(sa.insert(Discount).values({
        'code': CODE,
        'per_item': PER_ITEM,
        'percent': PERCENT,
        'end_date': op.inline_literal(END_DATE)
        if op.get_context().as_sql
        else END_DATE
    }))

def downgrade():
    op.execute(sa.delete(Discount).where(sa.and_(
        Discount.code == CODE,
        Discount.end_date == END_DATE
    )))
