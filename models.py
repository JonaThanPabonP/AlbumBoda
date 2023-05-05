from flask_sqlalchemy import SQLAlchemy

mydb = SQLAlchemy()

class Fotos(mydb.Model):
    __tablename__ = 'Fotos'
    id = mydb.Column(mydb.Integer, primary_key=True)
    name = mydb.Column(mydb.String(30), nullable=False)
    description = mydb.Column(mydb.String(100), nullable=True)
    orientation = mydb.Column(mydb.String(100), nullable=False)
    url = mydb.Column(mydb.String(200), nullable=False)
    state = mydb.Column(mydb.String(1), nullable=False)

    def __repr__(self):
        return f'{self.nombre}'