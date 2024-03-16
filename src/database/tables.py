import peewee as pw

db = pw.SqliteDatabase(database='syndra.db')

class BaseModel(pw.Model):
    class Meta:
        database = db

class Server(BaseModel):
    '''
    id : INT : PRIMARY KEY
    '''
    id = pw.IntegerField(primary_key=True)

class Currency(BaseModel):
    '''
    id : INT : PRIMARY KEY
    server : INT : FOREIGN KEY
    name : TEXT
    symbol : TEXT
    '''
    id = pw.AutoField(primary_key=True)
    server = pw.ForeignKeyField(Server, backref='currency')
    name = pw.TextField()
    symbol = pw.TextField()

class Wallet(BaseModel):
    '''
    wallet_ref_num : INT : PRIMARY KEY
    id : INT
    server : INT : FOREIGN KEY
    currency : INT : FOREIGN KEY
    balance : FLOAT
    '''
    wallet_ref_num = pw.AutoField(primary_key=True)
    id = pw.IntegerField(primary_key=False)
    server = pw.ForeignKeyField(Server, backref='wallet')
    currency = pw.ForeignKeyField(Currency, backref='wallet')
    balance = pw.FloatField()

"""class Product(BaseModel):
    '''
    id : INT : PRIMARY KEY
    emoji : TEXT
    owner : INT : FOREIGN KEY
    name : TEXT
    description : TEXT
    price : FLOAT
    currency : INT : FOREIGN KEY
    is_active : BOOLEAN
    stock : INT
    '''
    id = pw.AutoField(primary_key=True)
    emoji = pw.TextField()
    owner = pw.ForeignKeyField(Wallet, backref='product')
    name = pw.TextField()
    description = pw.TextField()
    price = pw.FloatField()
    currency = pw.ForeignKeyField(Currency, backref='product')
    is_active = pw.BooleanField()
    stock = pw.IntegerField() # -1 for infinite stock"""

"""class Transaction(BaseModel):
    '''
    id : INT : PRIMARY KEY
    sender : INT : FOREIGN KEY
    receiver : INT : FOREIGN KEY
    currency : INT : FOREIGN KEY
    product_id : INT : FOREIGN KEY
    date : DATETIME
    '''
    id = pw.AutoField(primary_key=True)
    sender = pw.ForeignKeyField(Wallet, backref='transaction')
    receiver = pw.ForeignKeyField(Wallet, backref='transaction')
    currency = pw.ForeignKeyField(Currency, backref='transaction')
    product_id = pw.ForeignKeyField(Product, backref='transaction')
    date = pw.DateTimeField()"""

class RolePay(BaseModel):
    '''
    id : INT : PRIMARY KEY
    server : INT : FOREIGN KEY
    role : INT : FOREIGN KEY
    amount : FLOAT
    '''
    id = pw.AutoField(primary_key=True)
    server = pw.ForeignKeyField(Server, backref='rolepay')
    role = pw.IntegerField()
    amount = pw.FloatField()

class Commands(BaseModel):
    '''
    id : INT : PRIMARY KEY
    command_name : TEXT : UNIQUE
    '''
    id = pw.AutoField(primary_key=True)
    command_name = pw.TextField(unique=True)

class CommandConfig(BaseModel):
    '''
    id : INT : PRIMARY KEY
    server : INT : FOREIGN KEY
    command : TEXT : FOREIGN KEY
    enabled : BOOLEAN
    '''
    id = pw.AutoField(primary_key=True)
    server = pw.ForeignKeyField(Server, backref='commandconfig')
    command = pw.ForeignKeyField(Commands, backref='commandconfig')
    enabled = pw.BooleanField()

class RoleCommandConfig(BaseModel):
    '''
    id : INT : PRIMARY KEY // Role ID
    command : TEXT : FOREIGN KEY
    '''