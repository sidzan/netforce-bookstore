from netforce.model import Model,fields

class BookstoreBurrowLine(Model):
    _name = "bookstore.burrow.line"
    _fields = {
        "burrow_id" : fields.Many2One("bookstore.burrow","Burrow",required=True,on_delete="cascade"),
        "book_id" : fields.Many2One("bookstore.book","Book",required=True),
        "unit_price" : fields.Integer("Unit Price",readonly=True),
        "qty" : fields.Integer("Qty",required=True),
        "total_cost" : fields.Integer("Total Cost",readonly=True)
    }
    _defaults = {
        "unit_price" : 0,
        "total_cost" :0
    }
    
BookstoreBurrowLine.register()
