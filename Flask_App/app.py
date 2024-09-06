from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
import numpy as np
import cv2

app = Flask(__name__)

model = load_model('C:/Users/LENOVO/stage1.h5')
model2 = load_model('C:/Users/LENOVO/stage2new.h5')
model3 = load_model('C:/Users/LENOVO/stage31.h5')
parts_model = load_model('C:/Users/LENOVO/vehicle_weights.h5')

def predict_label(img_path):
    res = []
    image_ = load_img(img_path, target_size=(224, 224))
    image_ = img_to_array(image_)
    image_ = preprocess_input(image_)
    data = []
    data.append(image_)
    data = np.array(data, dtype="float32")
    p = model.predict(data)
    if p[0][0]>p[0][1]:
        res.append("damaged")
    else:
        res.append("not damaged")
        res.append("not applicable")
        res.append("not applicable")
        return res
    
    data_img = []
    image2_ = cv2.imread(img_path)
    image2_ = cv2.cvtColor(image2_, cv2.COLOR_BGR2RGB)
    image2_resized = cv2.resize(image2_, (128,128))
    data_img.append(image2_resized)
    X = np.array(data_img)
    p = model2.predict(X)
    if p[0][0]>p[0][1] and p[0][0]>p[0][2]:
        res.append("front")
    else:
        if p[0][1]>p[0][2]:
            res.append("rear")
        else:
            res.append("side")
    
    p = model3.predict(X)
    if p[0][0]>p[0][1] and p[0][0]>p[0][2]:
        res.append("minor damage")
    else:
        if p[0][1]>p[0][2]:
            res.append("moderate damage")
        else:
            res.append("severe damage")
    
    X = []
    x = cv2.imread(img_path, cv2.IMREAD_COLOR)
    x = cv2.resize(x, (224,224))
    x = np.array(x)
    x = x/255
    X.append(x)
    X = np.array(X)
    p = parts_model.predict(X)
    class_dict = {0:'unknown',
                  1:'head lamp',
                  2:'door scratch',
                  3:'glass shatter',
                  4:'tail lamp',
                  5:'bumper_dent',
                  6:'door dent',
                  7:'bumper scratch'}
    s = ""
    ind = 0
    for i in p[0]:
        if i>=0.1:
            s+=class_dict[ind]+', '
            ind = ind+1

    res.append(s)
    
    # Price estimation based on model predictions
    price = 0.0
    if res[0] == "damaged":
        if res[1] == "front":
            price += 5000
            if res[2] == "severe damage":
                price += 100000 # extra cost since damage in front means engine gone means expensive repair
        elif res[1] == "rear":
            price += 7000
            if res[2] == "severe damage":
                price += 30000  # Add cost for rear damage
        elif res[1] == "side":
            price += 3000  # Add cost for side damage
        if res[2] == "minor damage":
            price += 1000  # Add cost for minor damage
        elif res[2] == "moderate damage":
            price += 7000  # Add cost for moderate damage
        elif res[2] == "severe damage":
            price += 10000  # Add cost for severe damage

        # Add cost for each damaged part
        damaged_parts = res[3].split(', ')
        price += len(damaged_parts) * 1000
    
    res.append(price)
    
    return res
    
# Routes
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route("/submit", methods=['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['my_image']
        img2 = request.files['my_image2']
        img_path = "static/" + img.filename	
        img_path2 = "static/" + img2.filename
        img.save(img_path)
        img2.save(img_path2)
        p = predict_label(img_path)
        p2 = predict_label(img_path2)
        if len(p) >= 5 and len(p2) >= 5:
            tot = p[4] + p2[4]
        elif len(p) >= 5 and len(p2) < 5:
            tot = p[4]
        elif len(p) < 5 and len(p2) >= 5:
            tot = p[4]
        else:
            tot=0
            
    return render_template("index.html", prediction=p,prediction2=p2, img_path=img_path,img_path2=img_path2,tot=tot)


if __name__ == '__main__':
    app.run(debug=True)
