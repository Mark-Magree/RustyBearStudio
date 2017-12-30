from flask import render_template
from os import listdir

from rbs import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

#TODO add for loop to route to all "img_" galleries from static
#TODO build matrix of galleries by "/" dir & sub dirs where "/" = [0][:]
@app.route('/gallery')
def gallery():
    img_dir = "static/img_poly_jewelry/"
    images = [i for i in listdir("rbs/%s" % img_dir) if i.endswith('.jpg')]
    return render_template('gallery.html',
                            img_dir=img_dir,
                            images=images)

