import torch
from PIL import Image
import flask
from flask_cors import CORS
import io
import utils
from net import Net, Vgg16
# from base64 import encodebytes
from torch.autograd import Variable
from flask import send_file,jsonify
from azure.storage.blob import BlockBlobService
import string, random, requests
import random
from flask_cors import CORS
import os

app = flask.Flask(__name__)
# global account, key, container,blob_service, model

def loadModel():
    global style_model
    model_dict = torch.load("21styles.model")
    model_dict_clone = model_dict.copy() # We can't mutate while iterating

    for key, value in model_dict_clone.items():
        if key.endswith(('running_mean', 'running_var')):
            del model_dict[key]

    style_model = Net(ngf=128)
    style_model.load_state_dict(model_dict, False)



def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def evaluate(contentImage):    

    print("Evaluating")

    contentImage = utils.tensor_load_rgbimage(contentImage,size=512 ,keep_asp=True)
    content_image = contentImage.unsqueeze(0)

    styleimg = random.choice(styles)
    style = utils.tensor_load_rgbimage("images/21styles/"+styleimg,size=512).unsqueeze(0) 
    style = utils.preprocess_batch(style)

    style_v = Variable(style)
    content_image = Variable(utils.preprocess_batch(content_image))
    style_model.setTarget(style_v)

    output = style_model(content_image).data[0]
    Randomfilename = id_generator() + ".jpg"
    utils.tensor_save_bgrimage(output, Randomfilename, 0)
    print("Done")
    return Randomfilename

@app.route("/",methods=["GET"])
def home():
    return "<h1>Hello, World!</h1>"

styles = [
"candy.jpg","composition_vii.jpg","feathers.jpg","la_muse.jpg","mosaic.jpg","starry_night.jpg","the_scream.jpg","udnie.jpg","wave.jpg"]


@app.route("/predict", methods=['GET',"POST"])  
def predict():
    if flask.request.method == "POST":
        image = flask.request.files['file'].read()
        image = Image.open(io.BytesIO(image)).convert('RGB')
        Randomfilename = evaluate(image)

        # blob_service.create_blob_from_path(container, Randomfilename, Randomfilename)
        # ref =  'https://'+ account + '.blob.core.windows.net/' + container + '/' + Randomfilename
        return send_file(Randomfilename,mimetype='image/gif')
        # return jsonify({'url':ref})

@app.route('/health')
def health():
    return '', 200

@app.route('/ready')
def ready():
    return '', 200




loadModel()
# account = "dcluster"
# key="HP0jQjf8+w8mGK3L9hhjshZajfrx1tMx3zysBF3dWke8mDaQ5jnH2qxQYeqkEEzuZr6UWentCEOtLT+XrX9r1w=="
# container = "images"
# blob_service = BlockBlobService(account_name=account, account_key=key)
CORS(app,expose_headers='Authorization')
# app.run(host='0.0.0.0', port=5000)