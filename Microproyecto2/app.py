import os
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np

from gluoncv.model_zoo import get_model
from mxnet import nd, cpu

app = Flask(__name__)

# Modelo CIFAR-10 pretrained
net = get_model('cifar_resnet20_v1', classes=10, pretrained=True)
net.collect_params().reset_ctx(cpu())  # fuerza CPU

class_names = ['airplane','automobile','bird','cat','deer','dog','frog','horse','ship','truck']

def preprocess(img: Image.Image):
    img = img.convert('RGB').resize((32, 32))
    img_nd = nd.array(np.array(img)).astype('float32')
    img_nd = img_nd.transpose((2, 0, 1)) / 255.0
    mean = nd.array([0.4914, 0.4822, 0.4465]).reshape((3,1,1))
    std  = nd.array([0.2023, 0.1994, 0.2010]).reshape((3,1,1))
    img_nd = (img_nd - mean) / std
    return img_nd.expand_dims(axis=0)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/predict', methods=['POST'])
def predict():
    if 'img' not in request.files:
        return jsonify({"error": "Use form-data con clave 'img' y un archivo de imagen"}), 400
    f = request.files['img']
    img = Image.open(f.stream)
    data = preprocess(img)

    pred = net(data)
    probs = nd.softmax(pred)[0]
    ind = int(nd.argmax(probs).asscalar())
    prob = float(probs[ind].asscalar())

    prediction = ('The input picture is classified as [%s], with probability %.3f.'
                  % (class_names[ind], prob))

    return jsonify({
        "class_index": ind,
        "class_name": class_names[ind],
        "probability": prob,
        "message": prediction
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
