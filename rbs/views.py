from flask import render_template, Flask, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Email
from os import listdir, path, environ
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Event, Image, Base

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

gal_dir = "static"
gallery_list = []
for f in listdir(gal_dir):
    if path.isdir(f"{gal_dir}/{f}/thumbs"):
        gallery_list.append(f)

def send_query(name,email,query):
    msg = Message("Customer inquery")
    msg.sender="yesyesyesprobably@gmail.com"
    msg.recipients=["yesyesyesprobably@gmail.com"]
    msg.body = f"{name} - {query} \n {email}"
    msg.html = f"<b>{name}</b> - {query} <br> {email}"
    with app.app_context():
        mail.send(msg)

class QueryForm(Form):
    name = StringField('Name:')
    email = StringField('Email:', validators=[Required(),Email()])
    query = TextAreaField('Type your question here:', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/')
@app.route('/index')
def index():
    engine = create_engine('sqlite:///rbs.db')
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

@app.route('/contact', methods=['GET','POST'])
def contact():
    '''Contact form for questions or orders (for now)'''
    form = QueryForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        send_query(name=form.name.data,email=form.email.data,
                query=form.query.data)
        flash('Your message has been sent. Thank you!')
        return redirect(url_for('contact'))
    return render_template('contact.html',
                            form=form,
                            gallery_list=gallery_list)

@app.route('/policy')
def policy():
    return render_template('policy.html',
                            gallery_list=gallery_list)

@app.route('/<gallery>')
def gallery(gallery):
    '''open specific gallery'''
    img_dir = f"{gal_dir}/{gallery}"
    if path.isdir(f"{img_dir}/thumbs"):
        engine = create_engine('sqlite:///rbs.db')
        Session = sessionmaker(bind=engine)
        s = Session()
        images = [i for i in listdir(img_dir) if i.endswith('.jpg')]
        db_image_info = s.query(Image).filter_by(file_loc=img_dir).all()
        image_info = {}
        for i in db_image_info:
            image_info[i.file_name] = {"image_name": i.image_name,
                                        "description": i.description,
                                        "price": i.price,
                                        "sold": i.sold}
        return render_template('gallery.html',
                                images=images,
                                image_info=image_info,
                                img_dir=img_dir,
                                gallery_name=gallery,
                                gallery_list=gallery_list)
    else:
        #TODO Redirect instead?
        return render_template('index.html',
                                gallery_list=gallery_list)

if __name__ == "__main__":
    app.run(debug=True)
