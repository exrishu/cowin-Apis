import flask, datetime, re, jwt
from flask import request, jsonify, abort, make_response
from vaccine_alert.utils.vaccine import VaccineAvailability
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from functools import wraps

app = flask.Flask(__name__)

secret_key = 'cowinApp'
app.config['SECRET_KEY'] = secret_key

db_string = 'postgresql://database_uri'

db = create_engine(db_string)
base = declarative_base()


class User(base):
    __tablename__ = 'user'

    username = Column(String(100), primary_key=True)
    tokencode = Column(String(10000))
    time_created = Column(DateTime(timezone=True), server_default=func.now())


Session = sessionmaker(db)
session = Session()


base.metadata.create_all(db)

def token_required(func):
    @wraps(func)
    def token_decorator(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"message": "Token is missing !"}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = session.query(User).filter_by(username=data['username']).first()
        except:
            return jsonify({"message": "Token is invalid!"}), 401

        return func(current_user, *args, **kwargs)

    return token_decorator


def check_request_parameters():
    if not request.json or not 'pincode' in request.json or not 'date' in request.json or not 'age' in request.json:
        error_msg = {"message": "Mandatory parameters missing"}
    else:
        req = {
            'pincode': request.json['pincode'],
            'date': request.json['date'],
            'age': request.json['age']
        }
        format = "%d-%m-%Y"
        pin_regex = re.compile(r"^[1-9]{1}[0-9]{5}$")
        age_group = ['18+', '18-44', '45+']
        try:
            datetime.datetime.strptime(req['date'], format)
            check_pin = re.match(pin_regex, req['pincode'])
            if check_pin is None:
                raise Exception("PinCodeError")
            if req['age'] not in age_group:
                raise TypeError
            return req['pincode'], req['date'], req['age']
        except ValueError:
            error_msg = {"message": "The date with the correct format is required! The correct format is DD-MM-YYYY!"}
        except TypeError:
            error_msg = {"message": "The age should be in 3 categories. '18+','18-44','45+'"}
        except Exception:
            error_msg = {"message": "The pincode should be of 6 digit and in numbers."}
    return error_msg


@app.route('/api/v1/get/vaccine/slots', methods=['GET'])
@token_required
def home(current_user):
    return jsonify({"message": "Welcome!! Here you will find vaccination details"})


@app.route('/api/v1/get/vaccine/slots/all_age', methods=['POST'])
@token_required
def get_all_age_vaccine(current_user):
    parameter_check = check_request_parameters()
    if "message" in parameter_check:
        return jsonify(parameter_check)
    else:
        vaccine_all_age = VaccineAvailability(parameter_check[0], parameter_check[1])
        if "message" in vaccine_all_age.get_data:
            return vaccine_all_age.get_data
        else:
            if parameter_check[2] == '18+':
                return jsonify({"slots": vaccine_all_age.check_availability_all_age()})
            elif parameter_check[2] == '18-44':
                return jsonify({"slots": vaccine_all_age.check_availability_youth()})
            elif parameter_check[2] == '45+':
                return jsonify({"slots": vaccine_all_age.check_availability_old()})


@app.route('/user/generate/token', methods=['POST'])
def token_auth():
    data = request.json
    if not data or not data['username']:
        return jsonify({"message": "Invalid parameters passed in request"})

    username = session.query(User).filter_by(username=data['username']).first()
    try:
        if username.username == data['username']:
            return jsonify({"message": "The username already present"})
    except AttributeError:
        token = jwt.encode(
            {'username': data['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=90)},
            app.config['SECRET_KEY'])
        user_details = User(username=data['username'], tokencode=token)
        session.add(user_details)
        session.commit()
        return jsonify({"token": token.decode('UTF-8')})


app.run()
