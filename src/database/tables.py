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

class Product(BaseModel):
    '''
    id : INT : PRIMARY KEY
    name : TEXT
    description : TEXT
    price : FLOAT
    '''
    id = pw.AutoField(primary_key=True)
    owner = pw.ForeignKeyField(Wallet, backref='product')
    name = pw.TextField()
    description = pw.TextField()
    price = pw.FloatField()
    is_active = pw.BooleanField()
    stock = pw.IntegerField() # -1 for infinite stock

class Transaction(BaseModel):
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
    date = pw.DateTimeField()

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

class Mail(BaseModel):
    '''
    id : INT : PRIMARY KEY
    wallet : INT : FOREIGN KEY
    transaction : INT : FOREIGN KEY
    read : BOOLEAN
    '''
    id = pw.AutoField(primary_key=True)
    recipient = pw.IntegerField()
    wallet = pw.ForeignKeyField(Wallet, backref='mail')
    transaction = pw.ForeignKeyField(Transaction, backref='mail')
    read = pw.BooleanField()

class MailChannel(BaseModel):
    '''
    id : INT : PRIMARY KEY
    recipient : INT : FOREIGN KEY
    server : INT : FOREIGN KEY
    channel : INT : FOREIGN KEY
    '''
    id = pw.AutoField(primary_key=True)
    recipient = pw.IntegerField()
    server = pw.ForeignKeyField(Server, backref='mailchannel')
    channel = pw.IntegerField()