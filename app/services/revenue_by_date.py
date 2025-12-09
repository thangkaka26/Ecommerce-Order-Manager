from db.connection import Connection

class RevenueByDate:
    def __init__(self):
        self.concur = Connection().cur

        self.concur.execute("SELECT * FROM revenue_by_date;")
        self.data = self.concur.fetchall()
        self.concur.close()

    def fetching(self):
        return self.data