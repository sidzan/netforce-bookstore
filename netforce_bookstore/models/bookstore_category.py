from netforce.model import Model, fields

class BookstoreBook(Model):
    _name = "bookstore.category"
    _fields = {
        "name" : fields.Char("Name"),
        "description" : fields.Text("Description"),
}
BookstoreBook.register()
