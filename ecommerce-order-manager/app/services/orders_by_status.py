from db.connection import Connection

class OrdersByStatus:
    def __init__(self):
        self.concur = Connection().cur

        self.concur.execute("SELECT * FROM orders_by_status;")
        self.data = self.concur.fetchall()
        self.concur.close()

    def fetching(self):
        return self.data