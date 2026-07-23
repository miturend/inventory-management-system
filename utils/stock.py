from database import get_connection
from flask import session


def add_stock_movement(
    product_id,
    movement_type,
    quantity,
    description
):

    connection = get_connection()
    cursor = connection.cursor()

    user_id = session.get("user_id")


    cursor.execute("""
        INSERT INTO stockmovements
        (
            ProductID,
            UserID,
            MovementType,
            Quantity,
            Description
        )
        VALUES
        (%s,%s,%s,%s,%s)
    """, (
        product_id,
        user_id,
        movement_type,
        quantity,
        description
    ))


    connection.commit()

    cursor.close()
    connection.close()