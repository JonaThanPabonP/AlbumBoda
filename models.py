from flask_sqlalchemy import SQLAlchemy

mydb = SQLAlchemy()

class Fotos(mydb.Model):
    __tablename__ = 'Fotos'
    id = mydb.Column(mydb.Integer, primary_key=True)
    nombre = mydb.Column(mydb.String(30), nullable=False)
    descripcion = mydb.Column(mydb.String(100), nullable=True)
    estado = mydb.Column(mydb.String(1), nullable=False)

    def __repr__(self):
        return f'{self.nombre}'