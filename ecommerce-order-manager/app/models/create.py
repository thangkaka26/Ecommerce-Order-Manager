from db.connection import Connection

class Add:
    def __init___(self):
        pass

    def newCustomer(self, cid: str, cname:str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL add_customer(%s, %s);", (cid, cname))
        con.commit()
        con.close()

    def newProduct(self, pid: str, pname:str, price:float):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL add_product(%s, %s, %s);", (pid, pname, price))
        con.commit()
        con.close()

    def newOrder(self, ordid: str, cid:str):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL add_order(%s, %s);", (ordid, cid))
        con.commit()
        con.close()

    def newOrderitem(self, ordid: str, pid:str, qty:int):
        con = Connection().connect_db
        cur = con.cursor()
        cur.execute("CALL add_orderitem(%s, %s, %s);", (ordid, pid, qty))
        con.commit()
        con.close()