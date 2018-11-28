import os
import sys
from flask import Flask, request, redirect, url_for, render_template
from flask import send_from_directory, flash
from werkzeug.utils import secure_filename
import face_analyzer

UPLOAD_FOLDER = './images/uploads/'
ANNOTATED_FOLDER = './images/annotated/'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ANNOTATED_FOLDER'] = ANNOTATED_FOLDER
app.config['ssl_context'] = "adhoc"
app.secret_key = "super secret key"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.data, file=sys.stdout)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text=face_analyzer.face_analyzer(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '''
            <div>
            <h1>Result</h1>
            <img height="420" src="
            '''+(os.path.join("uploads", filename))+'''
            ">
            <br><p>'''+text+"</p></div>"+'''
            <form action="/">
                <input type="submit" value="New validation" class="btn btn-dark"/>
            </form>
            '''
            
            return '''
            <!doctype html>
            <title>Result</title>
            <h1>Result</h1>
            <img height="420" src="
            '''+(os.path.join("uploads", filename))+'''
            ">
            <br>'''+text
    return render_template('index.html')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/main.css')
def maincss_file():
    return send_from_directory('static', filename='main.css')

@app.route('/bootstrap.min.css')
def bootstrap_file():
    return send_from_directory('static', filename='bootstrap.min.css')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['ANNOTATED_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run(port=80, ssl_context='adhoc')