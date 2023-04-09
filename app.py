from flask import Flask, redirect, render_template, request, url_for, flash
import os
from werkzeug.utils import secure_filename
from config import Config, Firebase
from models import mydb, Fotos
from PIL import Image

app = Flask(__name__)
app.config.from_object(Config)
mydb.init_app(app)

firebase = Firebase()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fotos')
def fotos():
    fotos = Fotos.query.all()
    return render_template('fotos.html', fotos=fotos)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('Debe seleccionar una foto', 'error')
            return redirect(url_for('upload'))
        image = Image.open(file)
        image = image.convert('RGB')
        image.thumbnail((1024,1024))
        nombre = secure_filename(file.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre), optimize=True, quality=60)
        local_file_path = app.config['UPLOAD_FOLDER'] + nombre
        firebase.upload_file(local_file_path, nombre)
        descripcion = request.form['descripcion']
        fotos = Fotos(nombre=nombre, descripcion=descripcion, estado='A')
        mydb.session.add(fotos)
        mydb.session.commit()

        flash('Foto cargada exitosamente', 'success')
        return redirect(url_for('fotos'))

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)