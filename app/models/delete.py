from db.connection import Connection

class Delete:
    def __init___(self):
        pass

    def aCustomer(self, cid: str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL delete_customer(%s);", (cid))
        con.commit()
        con.close()

    def aProduct(self, pid: str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL delete_product(%s);", (pid))
        con.commit()
        con.close()

    def anOrder(self, ordid: str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL delete_order(%s);", (ordid))
        con.commit()
        con.close()

    def anOrderitem(self, ordid: str, pid:str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL delete_orderitem(%s, %s);", (ordid, pid))
        con.commit()
        con.close()