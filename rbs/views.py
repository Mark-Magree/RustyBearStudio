from flask import render_template, Flask
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from flask_mail import Mail, Message
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from os import listdir, path, environ
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Event, Base

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = environ.get("EMAIL_ADDR")
app.config['MAIL_PASSWORD'] = environ.get("EMAIL_PASS")
app.config['MAIL_DEFAULT_SENDER'] = environ.get("EMAIL_ADDR")

#init mail after config or variables won't be set
mail = Mail(app)

msg = Message("Hello",
                sender="yesyesyesprobably@gmail.com",
                recipients=["yesyesyesprobably@gmail.com"])
msg.body = "testing"
msg.html = "<b>testing</b>"
with app.app_context():
    mail.send(msg)

gal_dir = "static"
gallery_list = []
for f in listdir(gal_dir):
    if path.isdir(f"{gal_dir}/{f}/thumbs"):
        gallery_list.append(f)

@app.route('/')
@app.route('/index')
def index():
    engine = create_engine('sqlite:///event_info.db')
    Session = sessionmaker(bind=engine)
    s = Session()
    name_query = s.query(Event)
    show_list = name_query.all()
    return render_template('index.html',
                            show_list=show_list,
                            gallery_list=gallery_list)

@app.route('/about')
def about():
    return render_template('about.html',
                            gallery_list=gallery_list)

@app.route('/contact')
def contact():
    return render_template('contact.html',
                            gallery_list=gallery_list)

@app.route('/policy')
def policy():
    return render_template('policy.html',
                            gallery_list=gallery_list)

@app.route('/<gallery>')
def gallery(gallery):
    '''open specific gallery'''
    img_dir = f"{gal_dir}/{gallery}/"
    if path.isdir(f"{img_dir}thumbs"):
        images = [i for i in listdir(img_dir) if i.endswith('.jpg')]
        return render_template('gallery.html',
                                img_dir=img_dir,
                                images=images,
                                gallery_name=gallery,
                                gallery_list=gallery_list)
    else:
        return render_template('index.html',
                                gallery_list=gallery_list)

if __name__ == "__main__":
    app.run(debug=True)
