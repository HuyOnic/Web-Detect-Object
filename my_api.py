from flask import Flask, request, flash, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
from werkzeug.middleware.shared_data import SharedDataMiddleware
import my_yolov6
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = 'static/uploads'
app.config["SECRET_KEY"] = 'fjdklsfjdsk'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
yolov6_model = my_yolov6.my_yolov6("yolov6s.pt","cpu","data/coco.yaml",640,True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST','GET'])
def upload_image():
    if request.method=="POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_to_save)
            frame = cv2.imread(path_to_save)
            frame, no_object = yolov6_model.infer(frame)
            if no_object > 0:
                cv2.imwrite(path_to_save, frame)
            del frame

            return render_template('index.html', filename='uploads/'+filename)
        
    return render_template('index.html')

@app.route('/upload/<filename>')
def send_uploaded_file(filename=""):
    return send_from_directory(app.config["UPLOAD_FOLDER"],filename)
if __name__=="__main__":
    app.run(debug=True)