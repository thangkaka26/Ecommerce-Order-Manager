from db.connection import Connection

class ProductsRevenueSummary:
    def __init__(self):
        self.concur = Connection().cur

        self.concur.execute("SELECT * FROM products_revenue_summary;")
        self.data = self.concur.fetchall()
        self.concur.close()

    def fetching(self):
        return self.data