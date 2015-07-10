from netforce.model import Model, fields,get_model

class BookstoreBook(Model):
    _name = "bookstore.book"
    _fields = {
        "name" : fields.Char("Name",required="True"),
        "author" : fields.Char("Author",required="True"),
        "description" : fields.Text("Description"),
        "cost" : fields.Integer("Cost"),
        "category" : fields.Many2One("bookstore.category","Category"),
        "number_of_books" : fields.Integer("Number of Books",required="True"),
        "number_of_book_left" : fields.Integer("Book Left",function="get_number_of_book_left"),
}

    def get_number_of_book_left(self,ids,context={}):
        vals = {}
        for obj in self.browse(ids):
            num_issued = 0
            total = 0
            for line in get_model("bookstore.burrow.line").search_browse([["book_id","=",obj.id]]):
                num_issued += line.qty
        
            
            total = obj.number_of_books
            vals[obj.id] = total-num_issued
        return vals

BookstoreBook.register()

