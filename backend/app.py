import torch
from PIL import Image
import numpy as np
import flask
import io
import utils
from net import Net, Vgg16

from torch.autograd import Variable
from flask import send_file

app = flask.Flask(__name__)
model = None

def loadModel():
    global style_model
    model_dict = torch.load("21styles.model")
    model_dict_clone = model_dict.copy() # We can't mutate while iterating

    for key, value in model_dict_clone.items():
        if key.endswith(('running_mean', 'running_var')):
            del model_dict[key]

    style_model = Net(ngf=128)
    style_model.load_state_dict(model_dict, False)


def evaluate(contentImage):    
    contentImage = utils.tensor_load_rgbimage(contentImage,size=512 ,keep_asp=True)
    content_image = contentImage.unsqueeze(0)
    style = utils.tensor_load_rgbimage("images/21styles/candy.jpg",size=512).unsqueeze(0) 
    style = utils.preprocess_batch(style)

    style_v = Variable(style)
    content_image = Variable(utils.preprocess_batch(content_image))
    style_model.setTarget(style_v)

    output = style_model(content_image)
    utils.tensor_save_bgrimage(output.data[0], "output.jpg", 0)

@app.route("/",methods=["GET"])
def home():
    print("Here")
    return "<h1>Hello, World!</h1>"

styles = ["Robert_Delaunay,_1906,_Portrait.jpg",
"candy.jpg",
"composition_vii.jpg",
"escher_sphere.jpg",
"feathers.jpg",
"frida_kahlo.jpg",
"la_muse.jpg",
"mosaic.jpg",
"mosaic_ducks_massimo.jpg",
"pencil.jpg",
"picasso_selfport1907.jpg",
"rain_princess.jpg",
"seated-nude.jpg",
"shipwreck.jpg",
"starry_night.jpg",
"stars2.jpg",
"strip.jpg",
"the_scream.jpg",
"udnie.jpg",
"wave.jpg",
"woman-with-hat-matisse.jpg"]

@app.route("/predict", methods=["POST"])
def predict():
    data = {"success": False}
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image)).convert('RGB')
            # preprocess the image and prepare it for classification
            evaluate(image)
            return send_file("output.jpg",mimetype='image/gif')

if __name__ == "__main__":
    loadModel()
    print(("* Loading PyTorch model and Flask starting server..."
        "please wait until server has fully started"))
    app.run(host='0.0.0.0')