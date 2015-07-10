from netforce.model import Model, fields, get_model
from netforce.utils import get_data_path
from datetime import *

class BookstoreBurrow(Model):
    _name = "bookstore.burrow"
    _key = ["number"]
    _fields = {
        "customer" : fields.Many2One("bookstore.customer","Customer"),
        "number": fields.Char("Number",required=True),
        "issuer" : fields.Many2One("bookstore.employee","Issuing staff"),        
        "date" : fields.Date("Date Issued"),
        "date_expiry" : fields.Date("Issued Upto",function="get_expiry_date"),
        "lines" : fields.One2Many("bookstore.burrow.line","burrow_id","Lines"),
        "num_of_book_burrowed" : fields.Integer("Books Burrowed",function="get_num_of_book_burrowed"),
        "total_amount" : fields.Integer("Total Amount",readonly="true",function="get_total_amount"),
        "state": fields.Selection([("draft", "Draft"), ("approv,ed", "Approved"), ("discarded", "Discarded")], "State"),
    }

    def _get_number(self, context={}):
        seq_id = get_model("sequence").find_sequence(name="BookStoreBurrow",context=context)
        if not seq_id:
            return None
        while 1:
            num = get_model("sequence").get_next_number(seq_id, context=context)
            if not num:
                return None
##            user_id = get_active_user()
##            set_active_user(1)
            res = self.search([["number", "=", num]])
##            set_active_user(user_id)
            if not res:
                return num
            get_model("sequence").increment_number(seq_id, context=context)

    _defaults = {
             "date": lambda *a: datetime.now().strftime("%Y-%m-%d"),
             "state": "draft",
             "number": _get_number,
    }


    def get_total_amount(self,ids,context={}):
        vals = {}            
        for obj in self.browse(ids):
            num = 0
            for line in obj.lines:
                num += line.unit_price *line.qty
            vals[obj.id]= num
        print("the num is ")
        print (num)
        return vals

    def onchange_book(self, context={}):
        data = context["data"]
        path = context["path"]
        line = get_data_path(data,path,parent=True)
        book_id = line["book_id"]
        book = get_model("bookstore.book").browse(book_id)
        line["unit_price"]=book.cost
        return data

    def update_cost(self,context={}):
        data =context["data"]
        path = context["path"]
        line = get_data_path(data,path,parent=True)
        line["total_cost"] = line['qty']*line['unit_price']
    
    def update_total_amount(self,context):
        data =context["data"]
        sum = 0
        for line in data["lines"]:
            quantity = line.get("unit_price")*line.get("qty")
            sum += quantity
        data["total_amount"] = sum

    def onchange_qty(self, context):
        data = self.update_num_of_book_burrowed(context)
        self.update_cost(context)
        self.update_total_amount(context)
        return data

    def update_num_of_book_burrowed(self, context):
        data = context["data"]
        sum = 0
        for line in data["lines"]:
            quantity = line.get("qty")
            sum += quantity
        data["num_of_book_burrowed"] = sum
        return data

    def approve_review(self, ids, context={}):
        self.write(ids, {"state": "approved"})

    def reset_draft(self, ids, context={}):
        self.write(ids, {"state": "draft"})

    def discard_review(self, ids, context={}):
        self.write(ids, {"state": "discarded"})

    def get_expiry_date (self, ids, context ={}):
        vals = {}
        for obj in self.browse(ids):
            date_string = obj.date
            if date_string:
                date_obj = datetime.strptime(date_string,"%Y-%m-%d")
                expiry_date = (date_obj+timedelta(days=15))#.strftime("%Y-%m-%d")
                vals[obj.id] = expiry_date.strftime("%Y-%m-%d")
            else:
                vals[obj.id]= 0
        return vals
    def get_num_of_book_burrowed(self,ids,context={}):
        books = {}            
        for obj in self.browse(ids):
            num = 0
            for line in obj.lines:
                num += line.qty
            books[obj.id]= num
        return books
BookstoreBurrow.register()
