from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Storage321@@@localhost:5432/HelpDesk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_code = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    resolved_status = db.Column(db.Boolean, default=False)

@app.route('/add-problem', methods=['POST'])
def add_problem():
    data = request.json
    new_problem = Problem(
        problem_code=data['problem_code'],
        description=data['description'],
        resolved_status=data['resolved_status']
    )
    db.session.add(new_problem)
    db.session.commit()
    return jsonify({'message': 'Problem added successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
