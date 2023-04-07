from flask import Flask, redirect, render_template, request, url_for, flash
import os
from werkzeug.utils import secure_filename
from config import Config
from models import mydb, Fotos

app = Flask(__name__)
app.config.from_object(Config)
mydb.init_app(app)

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
        filename = secure_filename(file.filename)
        description = request.form['description']
        title = request.form['title']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        fotos = Fotos(titulo=title, archivo=filename, descripcion=description)
        mydb.session.add(fotos)
        mydb.session.commit()

        flash('Foto cargada exitosamente', 'success')
        return redirect(url_for('fotos'))

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)