from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///responses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for survey responses
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.String(80))
    position = db.Column(db.String(80))
    district_type = db.Column(db.String(80))
    ab1736_eligible = db.Column(db.String(80))

# Create the database tables
db.create_all()

# Set up Flask-Admin
admin = Admin(app, name='Survey Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Response, db.session))

# Route for the survey form
@app.route('/')
def survey():
    return render_template('survey.html')

# Route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit():
    # Get data from the form
    college_name = request.form.get('college_name')
    position = request.form.get('position')
    district_type = request.form.get('district_type')
    ab1736_eligible = request.form.get('ab1736_eligible')

    # Save the response to the database
    new_response = Response(
        college_name=college_name,
        position=position,
        district_type=district_type,
        ab1736_eligible=ab1736_eligible
    )
    db.session.add(new_response)
    db.session.commit()

    return redirect(url_for('thank_you'))

# Route to display a thank-you message
@app.route('/thank-you')
def thank_you():
    return "<h1>Thank you for your response!</h1>"

if __name__ == '__main__':
    app.run(debug=True)