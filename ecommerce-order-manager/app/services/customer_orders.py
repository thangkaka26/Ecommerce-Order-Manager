from db.connection import Connection

class CustomerOrder:
    def __init__(self):
        self.concur = Connection().cur

        self.concur.execute("SELECT * FROM customer_orders;")
        self.data = self.concur.fetchall()
        self.concur.close()

    def fetching(self):
        return self.data