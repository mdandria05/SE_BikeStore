from database.DB_connect import DBConnect
from model.product import Product as p
class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_category():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM `category` """
        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_products(start_date, end_date, category):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT
                        p.id,
                        p.product_name,
                        orders.quantity
                    FROM
                        product AS p
                    LEFT JOIN(
                        SELECT
                            oi.product_id, COUNT(oi.product_id) as quantity
                        FROM
                            `order` AS o,
                            order_item AS oi
                        WHERE
                            oi.order_id = o.id AND o.order_date BETWEEN %s AND %s
                        GROUP BY
                            oi.product_id
                    ) AS orders
                    ON
                        p.id = orders.product_id
                    WHERE
                        p.category_id = %s 
                    ORDER BY `orders`.`quantity` ASC"""
        cursor.execute(query, (start_date, end_date, category))

        for row in cursor:
            results.append(p(**row))

        cursor.close()
        conn.close()
        return results

