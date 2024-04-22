from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Storage321@@@localhost:5432/HelpDesk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CallDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caller_name = db.Column(db.String(100))
    operator_name = db.Column(db.String(100))
    time_of_call = db.Column(db.DateTime, default=datetime.utcnow)
    serial_number = db.Column(db.String(50))
    operating_system = db.Column(db.String(50))
    software_used = db.Column(db.String(50))
    problem_id = db.Column(db.Integer)
    problem_description = db.Column(db.Text)
    resolved = db.Column(db.Boolean, default=False)

@app.route('/submit-call', methods=['POST'])
def submit_call():
    data = request.json
    new_call = CallDetail(
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
    return jsonify({'message': 'Call details submitted successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
