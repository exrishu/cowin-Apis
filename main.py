import flask, datetime, re
from flask import request, jsonify, abort, make_response
from vaccine_alert.utils.vaccine import VaccineAvailability

app = flask.Flask(__name__)


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
def home():
    return jsonify({"message": "Welcome!! Here you will find vaccination details"})


@app.route('/api/v1/get/vaccine/slots/all_age', methods=['POST'])
def get_all_age_vaccine():
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


app.run()
