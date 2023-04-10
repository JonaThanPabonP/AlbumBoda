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
    lista_fotos = []
    list_fotos = Fotos.query.all()
    for foto in list_fotos:
        storage_ref = firebase.storage.child(foto.nombre)
        url = storage_ref.get_url(None)
        lista_fotos.append({
            "url": url,
            "nombre": foto.nombre,
            "descripcion": foto.descripcion,
            "estado": foto.estado
        })
    return render_template('fotos.html', fotos=lista_fotos)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            image = Image.open(file)
            image = image.convert('RGB')
            image.thumbnail((1024,1024))
            nombre = secure_filename(file.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre), optimize=True, quality=60)
            local_file_path = app.config['UPLOAD_FOLDER'] + nombre
            firebase.upload_file(local_file_path, nombre)
            descripcion = request.form['descripcion']
            url = f"gs://albumboda-5f8d0.appspot.com/{nombre}"
            fotos = Fotos(nombre=nombre, descripcion=descripcion, url=url, estado='A')
            os.remove(local_file_path)
            mydb.session.add(fotos)
        mydb.session.commit()

        flash('Fotos cargadas exitosamente', 'success')
        return redirect(url_for('fotos'))

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)