from db.connection import Connection

class Search:
    def __init___(self):
        pass

    def customers_by_name(self, cname:str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL search_customer(%s);", (cname))
        cuss = cur.fetchall()
        con.close()
        return cuss

    def products_by_name(self, pname: str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL search_product(%s);", (pname))
        prods = cur.fetchall()
        con.close()
        return prods

    def order_details_by_id(self, ordid: str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL search_orderdetail(%s);", (ordid))
        ordts = cur.fetchall()
        con.close()
        return ordts

    def customer_orders_by_id(self, cid:str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL search_customer_orders(%s);", (cid))
        cords = cur.fetchall()
        con.close()
        return cords