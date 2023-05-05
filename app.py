from flask import Flask, redirect, render_template, request, url_for, flash
import os
from werkzeug.utils import secure_filename
from config import Config, Firebase
from models import mydb, Fotos
from PIL import Image, ExifTags

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
        storage_ref = firebase.storage.child(foto.name)
        url = storage_ref.get_url(None)
        lista_fotos.append({
            "url": url,
            "name": foto.name,
            "description": foto.description,
            "orientation": foto.orientation,
            "state": foto.state
        })
    return render_template('fotos.html', fotos=lista_fotos)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            image = Image.open(file)
            __rotateImage(image)
            image = image.convert('RGB')
            image.thumbnail((1024,1024))
            orientation = "Landscape" if image.width > image.height else "Portrait"
            name = secure_filename(file.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], name), optimize=True, quality=60)
            local_file_path = app.config['UPLOAD_FOLDER'] + name
            firebase.upload_file(local_file_path, name)
            description = request.form['description']
            url = f"gs://albumboda-5f8d0.appspot.com/{name}"
            fotos = Fotos(name=name, description=description, orientation=orientation, url=url, state='A')
            os.remove(local_file_path)
            mydb.session.add(fotos)
        mydb.session.commit()

        flash('Fotos cargadas exitosamente', 'success')
        return redirect(url_for('fotos'))

    return render_template('upload.html')


def __rotateImage(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS == 'Orientation':
                exif = dict(image._getexif().items())
                if exif == 3:
                    image = image.rotate(180, expand=True)
                elif exif == 6:
                    image = image.rotate(270, expand=True)
                elif exif == 8:
                    image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return image

if __name__ == '__main__':
    app.run(debug=True)