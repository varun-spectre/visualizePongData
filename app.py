from flask import Flask, request, render_template
from visualize import visualize
# from temp import visualize
import logging


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    print('index() called')  # Add this line
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        graph = visualize(file.stream)
        # Render the result template if graph is True
        if graph:
            return render_template('results.html')
        else:
            print("Error in Visualize.py")
            return render_template('index.html')
    else:
        logging.info('I told you so')
        return render_template('index.html')


app.run()
