import peewee as pw

db = pw.SqliteDatabase(database='syndra.db')
db.connect()

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
    id : INT : PRIMARY KEY
    server : INT : FOREIGN KEY
    currency : INT : FOREIGN KEY
    balance : FLOAT
    '''
    id = pw.IntegerField(primary_key=True)
    server = pw.ForeignKeyField(Server, backref='wallet')
    currency = pw.ForeignKeyField(Currency, backref='wallet')
    balance = pw.FloatField()

class Transaction(BaseModel):
    '''
    id : INT : PRIMARY KEY
    sender : INT : FOREIGN KEY
    receiver : INT : FOREIGN KEY
    amount : FLOAT
    date : DATETIME
    description : TEXT
    '''
    id = pw.AutoField(primary_key=True)
    sender = pw.ForeignKeyField(Wallet, backref='transaction')
    receiver = pw.ForeignKeyField(Wallet, backref='transaction')
    amount = pw.FloatField()
    date = pw.DateTimeField()
    description = pw.TextField()