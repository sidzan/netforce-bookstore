from netforce.model import Model, fields, get_model
from datetime import *

class BookstoreCustomer(Model):
    _name = "bookstore.customer"
    _fields = {
        "name" : fields.Char("Name",required=True,size=256,search=True),
        "age" : fields.Integer("Age",function="get_age"),
        "gender" : fields.Selection([("male","Male"),("female","Female")], "Gender" , required= True),
        "job" : fields.Char("Job"),
        "birth_date" : fields.Date("Birth Date"),
        "num_of_book_burrowed" : fields.Integer("Books Burrowed",function="get_num_of_book_burrowed"),
        "myfield": fields.Char("blabla"),
    }

    _defaults = {
        "birth_date": lambda *a: datetime.now().strftime("%Y-%m-%d"),
        }

    def get_age (self ,ids ,context={}):
        vals = {}
        for obj in self.browse(ids):
           
            date_string = obj.birth_date
            if date_string:
                date_obj = datetime.strptime(date_string,"%Y-%m-%d")
                today_obj = datetime.now()
                age=today_obj.year- date_obj.year
                vals[obj.id]= age 
            else:
                vals[obj.id]= 0
        return vals

    def get_num_of_book_burrowed(self,ids,context={}):
        books = {}            
        for obj in self.browse(ids):
            num = 0
            burrow_ids =get_model("bookstore.burrow").search([["customer","=",obj.id]])
            for j in burrow_ids:
                burrow = get_model("bookstore.burrow").browse(j)
                for line in burrow.lines:
                    num += line.qty
            books[obj.id]= num
        return books


BookstoreCustomer.register()
