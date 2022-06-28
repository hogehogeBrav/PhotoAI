import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, ORJSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_302_FOUND
import shutil
import uvicorn
import csv
import numpy as np

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("value_list.csv") as f:
  for row in csv.reader(f):
    value_list = row

@app.post('/predict')
# async def predict_image(file: UploadFile = File(...)):
    # extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    # if not extension:
    #     return "Image must be jpg or png format!"
    # path = f'tmp/{file.filename}'
    # with open(path, 'w+b') as buffer:
    #     shutil.copyfileobj(file.file, buffer)

async def fileupload_post(request: Request):
    new_path = "tmp" #フォルダ名
    if not os.path.exists(new_path): #ディレクトリがない場合、作成
        os.mkdir(new_path)

    # アップロードされたファイルを保存する
    form = await request.form()
    uploadedpath = "./tmp"
    files = os.listdir(uploadedpath)
    for formdata in form:
        uploadfile = form[formdata]
        path = os.path.join("./tmp", uploadfile.filename)
        fout = open(path, 'wb')
        while 1:
            chunk = await uploadfile.read(100000)
            if not chunk: break
            fout.write (chunk)
        fout.close()

    # label_image.py
    import argparse
    from fileinput import filename

    import numpy as np
    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()

    def load_graph(model_file):
      graph = tf.Graph()
      graph_def = tf.GraphDef()

      with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
      with graph.as_default():
        tf.import_graph_def(graph_def)

      return graph

    def read_tensor_from_image_file(file_name,
                                    input_height=299,
                                    input_width=299,
                                    input_mean=0,
                                    input_std=255):
      input_name = "file_reader"
      output_name = "normalized"
      file_reader = tf.read_file(file_name, input_name)
      if file_name.endswith(".png"):
        image_reader = tf.io.decode_png(file_reader, channels=3, name="png_reader")
      elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(tf.io.decode_gif(file_reader, name="gif_reader"))
      elif file_name.endswith(".bmp"):
        image_reader = tf.io.decode_bmp(file_reader, name="bmp_reader")
      else:
        image_reader = tf.io.decode_jpeg(
            file_reader, channels=3, name="jpeg_reader")
      float_caster = tf.cast(image_reader, tf.float32)
      dims_expander = tf.expand_dims(float_caster, 0)
      resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
      normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
      sess = tf.Session()
      return sess.run(normalized)


    def load_labels(label_file):
      proto_as_ascii_lines = tf.io.gfile.GFile(label_file).readlines()
      return [l.rstrip() for l in proto_as_ascii_lines]


    # if __name__ == "__main__":
    #   file_name = "tensorflow/examples/label_image/data/grace_hopper.jpg"
    #   model_file = \
    #     "tensorflow/examples/label_image/data/inception_v3_2016_08_28_frozen.pb"
    #   label_file = "tensorflow/examples/label_image/data/imagenet_slim_labels.txt"
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255
    input_layer = "Placeholder"
    output_layer = "final_result"

    #   parser = argparse.ArgumentParser()
    #   parser.add_argument("--image", help="image to be processed")
    #   parser.add_argument("--graph", help="graph/model to be executed")
    #   parser.add_argument("--labels", help="name of file containing labels")
    #   parser.add_argument("--input_height", type=int, help="input height")
    #   parser.add_argument("--input_width", type=int, help="input width")
    #   parser.add_argument("--input_mean", type=int, help="input mean")
    #   parser.add_argument("--input_std", type=int, help="input std")
    #   parser.add_argument("--input_layer", help="name of input layer")
    #   parser.add_argument("--output_layer", help="name of output layer")
    #   args = parser.parse_args()

    # if args.graph:
    #   model_file = args.graph
    # if args.image:
    #   file_name = args.image
    # if args.labels:
    #   label_file = args.labels
    # if args.input_height:
    #   input_height = args.input_height
    # if args.input_width:
    #   input_width = args.input_width
    # if args.input_mean:
    #   input_mean = args.input_mean
    # if args.input_std:
    #   input_std = args.input_std
    # if args.input_layer:
    #   input_layer = args.input_layer
    # if args.output_layer:
    #   output_layer = args.output_layer

    model_file = './model/output_graph.pb'
    # file_name = path
    label_file = './model/output_labels.txt'

    graph = load_graph(model_file)
    t = read_tensor_from_image_file(
        f'tmp/{uploadfile.filename}',
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
      results = sess.run(output_operation.outputs[0], {
          input_operation.outputs[0]: t
      })
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    main = []
    for i in top_k:
      index = value_list.index(labels[i])
      index = index + 1
      main.append({
                  "labels": str(labels[i]),
                  "index":str(index),
                  "results": str(results[i])
                  })

    return main

if __name__ == "__main__":
    uvicorn.run(app, port=8081, host='0.0.0.0')