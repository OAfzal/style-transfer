import torch
from PIL import Image
import numpy as np
import flask
from flask_cors import CORS
import io
import utils
from net import Net, Vgg16
from base64 import encodebytes
from torch.autograd import Variable
from flask import send_file,jsonify
from azure.storage.blob import BlockBlobService
import string, random, requests
import random

model = None
app = flask.Flask(__name__)

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
    print(styleimg)
    style = utils.tensor_load_rgbimage("images/21styles/"+styleimg,size=512).unsqueeze(0) 
    style = utils.preprocess_batch(style)

    style_v = Variable(style)
    content_image = Variable(utils.preprocess_batch(content_image))
    style_model.setTarget(style_v)

    output = style_model(content_image).data[0]
    img = utils.tensor_save_bgrimage(output, "output.jpg", 0)
    return img

@app.route("/",methods=["GET"])
def home():
    print("Here")
    return "<h1>Hello, World!</h1>"

styles = [
"candy.jpg",
"composition_vii.jpg",
"feathers.jpg",
"la_muse.jpg",
"mosaic.jpg",
"starry_night.jpg",
"the_scream.jpg",
"udnie.jpg",
"wave.jpg"
]

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format="jpg")
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


@app.route("/predict", methods=['GET',"POST"])  
def predict():
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        image = flask.request.files['file'].read()
        # read the image in PIL format
        image = Image.open(io.BytesIO(image)).convert('RGB')
        # preprocess the image and prepare it for classification
        
        output = evaluate(image)

        # img_io = io.BytesIO()
        # output.save(img_io, 'JPEG', quality=70)
        # img_io.seek(0)
        # encoded_img = encodebytes(img_io.getvalue()).decode('ascii') # encode as base64
        # # return send_file(img_io, mimetype='image/jpeg')
        # response =  { 'Status' : 'Success',  'ImageBytes': encoded_img}
        # return jsonify(response)

        Randomfilename = id_generator() + ".jpg"
        blob_service.create_blob_from_path(container, Randomfilename, "output.jpg")
        ref =  'https://'+ account + '.blob.core.windows.net/' + container + '/' + Randomfilename

        return jsonify({'url':ref})
        # return send_file("output.jpg",mimetype='image/gif')

# if __name__ == "__main__":
#     loadModel()
#     print(("* Loading PyTorch model and Flask starting server..."
#         "please wait until server has fully started"))
#     app.run(host='0.0.0.0')



CORS(app,expose_headers='Authorization')
loadModel()
account = "dcstore1"
key="W/K4v+3w79iFfD9dx/a8DqUNsTkrjaEhJyr9creDToR/XsvySVumhy4WHYVvoC2DjKlU71WW+HKN+fRkYAh2rw=="
container = "images"
blob_service = BlockBlobService(account_name=account, account_key=key)
app.run(host='0.0.0.0', port=80)