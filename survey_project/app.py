from flask import Flask, request, render_template, redirect, url_for
import csv

app = Flask(__name__)

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

    # Save the response to a CSV file
    with open('responses.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([college_name, position, district_type, ab1736_eligible])

    return redirect(url_for('thank_you'))

# Route to display a thank-you message
@app.route('/thank-you')
def thank_you():
    return "<h1>Thank you for your response!</h1>"

if __name__ == '__main__':
    app.run(debug=True)