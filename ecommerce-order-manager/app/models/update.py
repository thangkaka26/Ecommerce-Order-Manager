from db.connection import Connection

class Update:
    def __init___(self):
        pass

    def product_price(self, pid: str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL update_price(%s);", (pid))
        con.commit()
        con.close()

    def order_status(self, ordid: str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL update_status(%s);", (ordid))
        con.commit()
        con.close()