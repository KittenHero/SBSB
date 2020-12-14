"""add prices

Revision ID: 5008728999b7
Revises: f6d1cf333d74
Create Date: 2020-12-11 19:03:53.027256

"""
from datetime import timedelta, datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5008728999b7'
down_revision = 'f6d1cf333d74'
branch_labels = None
depends_on = None

import os, sys
sys.path.append(os.getcwd())

from api.models import Price

prices = {
   'Thai Massage': {
       30: 40,
       45: 55,
       60: 65,
       90: 95,
       120: 130
   },
   'Foot Massage': {
       30: 49,
       45: 59,
       60: 69,
       90: 99,
       120: 135
   },
   'Aroma Oil Massage': {
       30: 49,
       45: 69,
       60: 79,
       90: 120,
       120: 155
   },
   'Hot Stone Massage': {
       30: 55,
       45: 70,
       60: 95,
       90: 135,
       120: 170
   },
   'Deep Tissue Massage': {
       30: 60,
       45: 75,
       60: 95,
       90: 135,
       120: 175
   },
   'Remedial Massage': {
       30: 55,
       45: 70,
       60: 85,
       90: 135,
       120: 170
   },
   'Body Scrub': {
       30: 60,
       45: 75,
       60: 95,
       90: 135
   },
   'Facial Massage': {
       30: 50,
       45: 60,
       60: 80,
       90: 100
   },
}

def upgrade():
    op.bulk_insert(
        Price.__table__,
        [
            {
                'massage_type': massage,
                'duration':
                   op.inline_literal(x)
                   if (x := (datetime(1,1,1) + timedelta(minutes=duration)).strftime('%H:%M:%S'))
                   and op.get_context().as_sql
                   else x,
                'price': price
            } for massage, pricing in prices.items()
            for duration, price in pricing.items()
        ]
    )


def downgrade():
    pass
