from netforce.model import Model, fields

class BookstoreEmployee(Model):
    _name = "bookstore.employee"
    _fields = {
        "name" : fields.Char("Name"),
        "age" : fields.Integer("Age"),
    }
BookstoreEmployee.register()
