from flask import Flask

app = Flask(__name__)
app.config.from_object('rbs.config')

from rbs import views
