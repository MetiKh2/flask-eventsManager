from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin 
import json
from sqlalchemy import desc,and_
import os
from db_manager import db
from models import Event
from datetime import datetime
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')

if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')
db.init_app(app)
with app.app_context():
    db.create_all()
UPLOAD_DIR = os.path.curdir = 'static/uploads/'
app.secret_key = '1dae11441a1a2acf1cad3eca'
# cors = CORS(app, resources={r"*": {"origins": "*"}})

# app.config['CORS_HEADERS'] = 'Content-Type'

@app.get('/events')
def events_list():
    events = db.session.query(Event.Event).filter(Event.Event.published == True).order_by(
        desc(Event.Event.created_at)).all()
    return jsonify([{
        'first_name': event.first_name,
        'id': event.id,
        'last_name': event.last_name,
        'title': event.title,
        'price': event.price,
        'holding_at': event.holding_at,
        'time': event.time,
        'url': event.url,
        'image': event.image,
        'address': event.address,
        'description': event.description,
        'phone': event.phone,
        'created_at': event.created_at,
    }for event in events])
@app.get('/event/<int:id>')
def event(id):
    event = db.session.query(Event.Event).filter(and_(Event.Event.id == id,Event.Event.published==True)).first()
    if event is None:
        return jsonify({
            'error':'Event not found'
        }),404
    return jsonify([{
        'first_name': event.first_name,
        'id': event.id,
        'last_name': event.last_name,
        'title': event.title,
        'price': event.price,
        'holding_at': event.holding_at,
        'time': event.time,
        'url': event.url,
        'image': event.image,
        'address': event.address,
        'description': event.description,
        'phone': event.phone,
        'created_at': event.created_at,
    }])


@app.post('/add_event')
@cross_origin()
def add_event():
    event = request.get_json()
    print(event)
    if event['holding_at'] is '':
        event['holding_at'] ='2000-01-01'
    
    if len(event) < 10:
        return jsonify({
            'error': 'Fill All Values'
        }), 404
    
    db.session.add(Event.Event(
        first_name=event['first_name'],
        last_name=event['last_name'],
        title=event['title'],
        price=event['price'],
        holding_at=datetime.strptime(
            event['holding_at'], '%Y-%m-%d'), 
        time=event['time'],
        url=event['url'],
        image=event['image'],
        address=event['address'],
        description=event['description'],
        phone=event['phone'],
    ))
    db.session.commit()
    
    return jsonify(event)


@app.get('/events/phone/<string:phone>')
def find_by_phone(phone):
    events = db.session.query(Event.Event).filter(Event.Event.phone == phone).all()
    if events is None:
        return jsonify({
            'error':'Event not found'
        }),404
    return jsonify([{
        'first_name': event.first_name,
        'id': event.id,
        'last_name': event.last_name,
        'title': event.title,
        'published':event.published
    }for event in events])

if __name__ == '__main__':
    app.run(debug=True, port=2022)
