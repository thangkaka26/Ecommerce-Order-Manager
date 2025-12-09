from db.connection import Connection

class OrderDetails:
    def __init__(self):
        self.concur = Connection().cur

        self.concur.execute("SELECT * FROM order_details;")
        self.data = self.concur.fetchall()
        self.concur.close()

    def fetching(self):
        return self.data