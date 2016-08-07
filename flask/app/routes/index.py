from flask import jsonify, render_template, request

from app import app

from src import pipeline_global as Pipeline
Pipeline.init_model()

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/tmp', methods=['GET'])
def tmp():
  return render_template('tmp.html')

@app.route('/api/charts', methods=['GET'])
def charts():
  result = dict(Pipeline.extrapolate(Pipeline.PREPROCESSED_GUINEA_DATA_EXTRA, request.json))
  for key in result:
    for i, elem in enumerate(result[key]):
      # result[key] is a tuple of lists and elem is one such list
      result[key][i] = [str(n) for n in result[key][i]]
  return jsonify(result)