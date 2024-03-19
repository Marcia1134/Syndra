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
    value : FLOAT
    symbol : TEXT
    '''
    id = pw.AutoField(primary_key=True)
    server = pw.ForeignKeyField(Server, backref='currency')
    name = pw.TextField()
    value = pw.FloatField()
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

class RolePay(BaseModel):
    '''
    id : INT : PRIMARY KEY
    server : INT : FOREIGN KEY
    role : INT
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
    point = pw.AutoField(primary_key=True)
    id = pw.IntegerField()
    command = pw.ForeignKeyField(Commands, backref='rolecommandconfig')