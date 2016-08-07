from flask import render_template

from app import app

from src import pipeline_global as Pipeline
Pipeline.init_model()

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/tmp', methods=['GET'])
def tmp():
  return render_template('tmp.html')
