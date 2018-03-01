from flask import render_template, Flask
from flask_bootstrap import Bootstrap
from os import listdir, path

app = Flask(__name__)
bootstrap = Bootstrap(app)

gal_dir = "static"
gallery_list = []
for f in listdir(gal_dir):
    if path.isdir(f"{gal_dir}/{f}"):
        gallery_list.append(f)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                            gallery_list=gallery_list)

@app.route('/about')
def about():
    return render_template('about.html',
                            gallery_list=gallery_list)

@app.route('/gallery')
def galleries():
    #TODO display image from each gallery
    return render_template('galleries.html',
                            gallery_list=gallery_list)

@app.route('/<gallery>')
def gallery(gallery):
    '''open specific gallery or return page with list of galleries'''
    img_dir = f"{gal_dir}/{gallery}/"
    if path.isdir(img_dir):
        images = [i for i in listdir(img_dir) if i.endswith('.jpg')]
        return render_template('gallery.html',
                                img_dir=img_dir,
                                images=images,
                                gallery_list=gallery_list)
    else:
        return render_template('galleries.html',
                                gallery_list=gallery_list)

if __name__ == "__main__":
    app.run(debug=True)
