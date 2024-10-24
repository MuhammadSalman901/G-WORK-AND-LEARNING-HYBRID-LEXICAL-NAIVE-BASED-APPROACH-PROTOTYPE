import sys
import os
from flask import Flask, render_template, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import urllib.parse

# Determine if running in a PyInstaller bundle
if getattr(sys, 'frozen', False):
    template_dir = os.path.join(sys._MEIPASS, 'templates')
    static_dir = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
else:
    app = Flask(__name__)

# Function to load model accuracies
def load_model():
    accuracies = {
        "lexical": 0.62,
        "naive_bayes": 0.62,
        "hybrid": 0.88
    }
    return accuracies

# Route for the index page
@app.route('/')
def index():
    accuracies = load_model()
    return render_template('index.html', accuracies=accuracies)

# Route to serve the comparison graph as a base64 image
@app.route('/comparison-graph')
def comparison_graph():
    accuracies = load_model()

    # Plotting comparison graph
    fig, ax = plt.subplots()
    models = list(accuracies.keys())
    values = list(accuracies.values())

    ax.bar(models, values)
    ax.set_xlabel('Model')
    ax.set_ylabel('Accuracy')
    ax.set_title('Model Accuracy Comparison')

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Convert plot to base64 string
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    return jsonify({'comparison_graph': uri})

if __name__ == '__main__':
    app.run(debug=True)
