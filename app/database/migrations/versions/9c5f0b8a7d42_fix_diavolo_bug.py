"""fix diavolo bug

Revision ID: 9c5f0b8a7d42
Revises: 5f8bda508cfd
Create Date: 2026-06-19 12:00:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '9c5f0b8a7d42'
down_revision = '5f8bda508cfd'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        UPDATE dough
        SET stock = 1
        WHERE id IN (
            SELECT dough_id
            FROM pizza_type
            WHERE lower(name) LIKE '%diavolo%'
        )
        AND stock < 1
    """)

    op.execute("""
        UPDATE topping
        SET stock = pizza_type_topping_quantity.quantity
        FROM pizza_type_topping_quantity
        JOIN pizza_type
          ON pizza_type.id = pizza_type_topping_quantity.pizza_type_id
        WHERE topping.id = pizza_type_topping_quantity.topping_id
          AND lower(pizza_type.name) LIKE '%diavolo%'
          AND topping.stock < pizza_type_topping_quantity.quantity
    """)


def downgrade():
    pass
