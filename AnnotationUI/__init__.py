from flask import Flask
from Mayank.AnnotationUI.semevalidentification.routes import semevalidentification
from Mayank.AnnotationUI.semevalsequencefile.routes import semevalsequencefile



def create_app():
    app = Flask(__name__)
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.register_blueprint(semevalsequencefile)
    app.register_blueprint(semevalidentification)


    return app