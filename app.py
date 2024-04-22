from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy  
from datetime import datetime

app = Flask(__name__)

# # Set up the logging for SQLALchemy to debug level
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Database connection parameters
db_params = {
    'dbname': 'HelpDesk',
    'user': 'postgres',
    'password': 'Storage321@@',
    'host': 'localhost',
    'port': '5432',
}

# Function to create a database connection
def create_db_connection():
    conn = psycopg2.connect(db_params)
    return conn

# configure the flask app for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize SQLALchemy
db = SQLAlchemy(app)

#Define the Databases
class CallDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caller_name = db.Column(db.String(100))
    operator_name = db.Column(db.String(100))
    time_of_call = db.Column(db.DateTime, default=datetime.utcnow)
    serial_number = db.Column(db.String(50))
    operating_system = db.Column(db.String(50))
    software_used = db.Column(db.String(50))
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))
    problem_description = db.Column(db.Text)
    resolved = db.Column(db.Boolean, default=False)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_type = db.Column(db.String(100))
    equipment_name = db.Column(db.String(100))
    make = db.Column(db.String(100))
    license_validity = db.Column(db.DateTime)

class Personnel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personnel_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    department = db.Column(db.String(100))

class Problems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_code = db.Column(db.String(50))
    description = db.Column(db.Text)
    resolved_status = db.Column(db.Boolean, default=False)
    problem_type_id = db.Column(db.Integer, db.ForeignKey('problem_type.id'))
    problem_type = db.relationship('ProblemType', backref=db.backref('problems', lazy=True))

class ProblemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_type_name = db.Column(db.String(100))


class Software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    software_name = db.Column(db.String(100))
    software_version = db.Column(db.String(50))
    license_type = db.Column(db.String(50))
    license_validity = db.Column(db.DateTime)

class Specialist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    specialist_name = db.Column(db.String(100))
    expert_in_problem_type = db.Column(db.Integer, db.ForeignKey('problem_type.id'))
    problems_assigned = db.Column(db.Integer, default=0)

# Route to submit call details
@app.route('/submit-call', methods=['POST'])
def submit_call():
    data = request.form  # Use request.form to get form data
    new_call = CallDetails(
        caller_name=data['caller_name'],
        operator_name=data['operator_name'],
        serial_number=data['serial_number'],
        operating_system=data['operating_system'],
        software_used=data['software_used'],
        problem_id=data['problem_id'],
        problem_description=data['problem_description']
    )
    db.session.add(new_call)
    db.session.commit()
    return 'Call details submitted successfully'


# Route to get all calls
@app.route('/get-calls', methods=['GET'])
def get_calls():
    calls = CallDetails.query.all()
    output = []
    for call in calls:
        call_data = {
            'id': call.id,
            'caller_name': call.caller_name,
            'operator_name': call.operator_name,
            'time_of_call': call.time_of_call.strftime('%Y-%m-%d %H:%M:%S'),
            'serial_number': call.serial_number,
            'operating_system': call.operating_system,
            'software_used': call.software_used,
            'problem_id': call.problem_id,
            'problem_description': call.problem_description,
            'resolved': call.resolved
        }
        output.append(call_data)
    return jsonify({'calls': output})

# Route for the html file
@app.route('/')
def index():
    # Fetch data from tables (example)
    problems_data = Problems.query.all()
    call_details_data = CallDetails.query.all()
    problem_type_data = ProblemType.query.all()
    specialist_data = Specialist.query.all()
    equipment_data = Equipment.query.all()
    software_data = Software.query.all()

    # Pass data to HTML template
    return render_template('index.html', problems=problems_data, call_details=call_details_data,
                           problem_type=problem_type_data, specialist=specialist_data,
                           equipment=equipment_data, software=software_data)



if __name__ == '__main__':
    app.run(debug=True)