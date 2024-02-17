import peewee as pw

db = pw.SqliteDatabase(database='syndra.db')
db.connect()

class BaseModel(pw.Model):
    class Meta:
        database = db

class Server(BaseModel):
    id = pw.TextField(primary_key=True)
