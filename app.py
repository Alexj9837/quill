from flask import (Flask, jsonify, redirect, render_template, request,flash, Response,make_response)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite3'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'supersneaky'


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class ConstitutionalConvention(db.Model):
    __tablename__ = "constitutional_conventions"
    convention_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    location = db.Column(db.String(255))
    participants = db.Column(db.Text)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class ConstitutionalConventionSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = ConstitutionalConvention
        sqla_session = db.session

    convention_id = fields.Number(dump_only=True)
    date = fields.Date()
    location = fields.String()
    #participants = fields.List(fields.String())
    participants = fields.String()

@app.route('/constitutional_conventions', methods=['GET'])
def get_conventions():
    conventions = ConstitutionalConvention.query.all()
    convention_schema = ConstitutionalConventionSchema(many=True)
    result = convention_schema.dump(conventions)
    return make_response(jsonify({"constitutional_conventions": result}))

@app.route('/constitutional_conventions/<id>', methods=['GET'])
def get_convention_by_id(id):
    convention = ConstitutionalConvention.query.get(id)
    convention_schema = ConstitutionalConventionSchema()
    result = convention_schema.dump(convention)
    return make_response(jsonify({"constitutional_convention": result}))

@app.route('/constitutional_conventions/<id>', methods=['PUT'])
def update_convention_by_id(id):
    data = request.get_json()
    convention = ConstitutionalConvention.query.get(id)
    if data.get('date'):
        convention.date = data['date']
    if data.get('location'):
        convention.location = data['location']
    if data.get('participants'):
        convention.participants = data['participants']
    db.session.add(convention)
    db.session.commit()
    convention_schema = ConstitutionalConventionSchema()
    result = convention_schema.dump(convention)
    return make_response(jsonify({"constitutional_convention": result}))

@app.route('/constitutional_conventions/<id>', methods=['DELETE'])
def delete_convention_by_id(id):
    convention = ConstitutionalConvention.query.get(id)
    db.session.delete(convention)
    db.session.commit()
    return make_response("", 204)

@app.route('/constitutional_conventions', methods=['POST'])
def create_convention():
    data = request.get_json()
    convention_schema = ConstitutionalConventionSchema()
    convention = convention_schema.load(data)
    result = convention_schema.dump(convention.create())
    return make_response(jsonify({"constitutional_convention": result}), 201)


class Committees(db.Model):
    __tablename__ = "committees"
    committee_id = db.Column(db.Integer, primary_key=True)
    committee_name = db.Column(db.String(255))
    committee_members = db.Column(db.Text)
    topics_covered = db.Column(db.Text)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class CommitteesSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Committees
        sqla_session = db.session

    committee_id = fields.Number(dump_only=True)
    committee_name = fields.String()
    committee_members = fields.String()
    topics_covered = fields.String()

@app.route('/committees', methods=['GET'])
def get_committees():
    committees = Committees.query.all()
    committee_schema = CommitteesSchema(many=True)
    result = committee_schema.dump(committees)
    return make_response(jsonify({"committees": result}))

@app.route('/committees/<id>', methods=['GET'])
def get_committee_by_id(id):
    committee = Committees.query.get(id)
    committee_schema = CommitteesSchema()
    result = committee_schema.dump(committee)
    return make_response(jsonify({"committee": result}))

@app.route('/committees/<id>', methods=['PUT'])
def update_committee_by_id(id):
    data = request.get_json()
    committee = Committees.query.get(id)
    if data.get('committee_name'):
        committee.committee_name = data['committee_name']
    if data.get('committee_members'):
        committee.committee_members = ', '.join(data['committee_members'])
    if data.get('topics_covered'):
        committee.topics_covered = data['topics_covered']
    db.session.add(committee)
    db.session.commit()
    committee_schema = CommitteesSchema()
    result = committee_schema.dump(committee)
    return make_response(jsonify({"committee": result}))

@app.route('/committees/<id>', methods=['DELETE'])
def delete_committee_by_id(id):
    committee = Committees.query.get(id)
    db.session.delete(committee)
    db.session.commit()
    return make_response("", 204)

@app.route('/committees', methods=['POST'])
def create_committee():
    data = request.get_json()
    committee_schema = CommitteesSchema()
    committee = committee_schema.load(data)
    result = committee_schema.dump(committee.create())
    return make_response(jsonify({"committee": result}), 201)

class Debates(db.Model):
    __tablename__ = "debates"
    debate_id = db.Column(db.Integer, primary_key=True)
    debate_date = db.Column(db.Date)
    debate_location = db.Column(db.String(255))
    participants = db.Column(db.Text)
    debate_content = db.Column(db.Text)
    committee_id = db.Column(db.Integer, db.ForeignKey('committees.committee_id'))
    document_id = db.Column(db.Integer, db.ForeignKey('documents.document_id'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class DebatesSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Debates
        sqla_session = db.session

    debate_id = fields.Number(dump_only=True)
    debate_date = fields.Date()
    debate_location = fields.String()
    participants = fields.String()
    debate_content = fields.String()
    committee_id = fields.Number()
    document_id = fields.Number()

@app.route('/debates', methods=['GET'])
def get_debates():
    debates = Debates.query.all()
    debates_schema = DebatesSchema(many=True)
    result = debates_schema.dump(debates)
    return make_response(jsonify({"debates": result}))

@app.route('/debates/<id>', methods=['GET'])
def get_debate_by_id(id):
    debate = Debates.query.get(id)
    debate_schema = DebatesSchema()
    result = debate_schema.dump(debate)
    return make_response(jsonify({"debate": result}))

@app.route('/debates/<id>', methods=['PUT'])
def update_debate_by_id(id):
    data = request.get_json()
    debate = Debates.query.get(id)
    if data.get('debate_date'):
        debate.debate_date = data['debate_date']
    if data.get('debate_location'):
        debate.debate_location = data['debate_location']
    if data.get('committee_members'):
        debate.participants = ', '.join(data['participants'])       
    if data.get('debate_content'):
        debate.debate_content = data['debate_content']
    if data.get('committee_id'):
        debate.committee_id = data['committee_id']
    if data.get('document_id'):
        debate.document_id = data['document_id']
    db.session.add(debate)
    db.session.commit()
    debate_schema = DebatesSchema()
    result = debate_schema.dump(debate)
    return make_response(jsonify({"debate": result}))

@app.route('/debates/<id>', methods=['DELETE'])
def delete_debate_by_id(id):
    debate = Debates.query.get(id)
    db.session.delete(debate)
    db.session.commit()
    return make_response("", 204)

@app.route('/debates', methods=['POST'])
def create_debate():
    data = request.get_json()
    debate_schema = DebatesSchema()
    debate = debate_schema.load(data)
    result = debate_schema.dump(debate.create())
    return make_response(jsonify({"debate": result}), 201)

class Documents(db.Model):
    __tablename__ = "documents"
    document_id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(255))
    author = db.Column(db.String(255))
    document_content = db.Column(db.Text)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class DocumentsSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Documents
        sqla_session = db.session

    document_id = fields.Number(dump_only=True)
    document_type = fields.String()
    author = fields.String()
    document_content = fields.String()

@app.route('/documents', methods=['GET'])
def get_documents():
    documents = Documents.query.all()
    documents_schema = DocumentsSchema(many=True)
    result = documents_schema.dump(documents)
    return make_response(jsonify({"documents": result}))

@app.route('/documents/<id>', methods=['GET'])
def get_document_by_id(id):
    document = Documents.query.get(id)
    document_schema = DocumentsSchema()
    result = document_schema.dump(document)
    return make_response(jsonify({"document": result}))

@app.route('/documents/<id>', methods=['PUT'])
def update_document_by_id(id):
    data = request.get_json()
    document = Documents.query.get(id)
    if data.get('document_type'):
        document.document_type = data['document_type']
    if data.get('author'):
        document.author = data['author']
    if data.get('document_content'):
        document.document_content = data['document_content']
    db.session.add(document)
    db.session.commit()
    document_schema = DocumentsSchema()
    result = document_schema.dump(document)
    return make_response(jsonify({"document": result}))

@app.route('/documents/<id>', methods=['DELETE'])
def delete_document_by_id(id):
    document = Documents.query.get(id)
    db.session.delete(document)
    db.session.commit()
    return make_response("", 204)

@app.route('/documents', methods=['POST'])
def create_document():
    data = request.get_json()
    document_schema = DocumentsSchema()
    document = document_schema.load(data)
    result = document_schema.dump(document.create())
    return make_response(jsonify({"document": result}), 201)

class Commentaries(db.Model):
    __tablename__ = "commentaries"
    commentary_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    commentary_text = db.Column(db.Text)
    debate_id = db.Column(db.Integer, db.ForeignKey('debates.debate_id'))
    document_id = db.Column(db.Integer, db.ForeignKey('documents.document_id'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class CommentariesSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Commentaries
        sqla_session = db.session

    commentary_id = fields.Number(dump_only=True)
    author = fields.String()
    timestamp = fields.DateTime()
    commentary_text = fields.String()
    debate_id = fields.Number()
    document_id = fields.Number()

@app.route('/commentaries', methods=['GET'])
def get_commentaries():
    commentaries = Commentaries.query.all()
    commentaries_schema = CommentariesSchema(many=True)
    result = commentaries_schema.dump(commentaries)
    return make_response(jsonify({"commentaries": result}))

@app.route('/commentaries/<id>', methods=['GET'])
def get_commentary_by_id(id):
    commentary = Commentaries.query.get(id)
    commentary_schema = CommentariesSchema()
    result = commentary_schema.dump(commentary)
    return make_response(jsonify({"commentary": result}))

@app.route('/commentaries/<id>', methods=['PUT'])
def update_commentary_by_id(id):
    data = request.get_json()
    commentary = Commentaries.query.get(id)
    if data.get('author'):
        commentary.author = data['author']
    if data.get('timestamp'):
        commentary.timestamp = data['timestamp']
    if data.get('commentary_text'):
        commentary.commentary_text = data['commentary_text']
    if data.get('debate_id'):
        commentary.debate_id = data['debate_id']
    if data.get('document_id'):
        commentary.document_id = data['document_id']
    db.session.add(commentary)
    db.session.commit()
    commentary_schema = CommentariesSchema()
    result = commentary_schema.dump(commentary)
    return make_response(jsonify({"commentary": result}))

@app.route('/commentaries/<id>', methods=['DELETE'])
def delete_commentary_by_id(id):
    commentary = Commentaries.query.get(id)
    db.session.delete(commentary)
    db.session.commit()
    return make_response("", 204)

@app.route('/commentaries', methods=['POST'])
def create_commentary():
    data = request.get_json()
    commentary_schema = CommentariesSchema()
    commentary = commentary_schema.load(data)
    result = commentary_schema.dump(commentary.create())
    return make_response(jsonify({"commentary": result}), 201)