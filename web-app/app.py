from flask import Flask, request, jsonify, abort
import urllib3
import control
import action
import sensor
import actuator
import log
from dotenv import load_dotenv
from functools import wraps

# Define used objects for our APIs
dht_thread = control.dht_worker()
adc_thread = control.adc_worker()
action_thread = action.action_worker()
http = urllib3.PoolManager()
app = Flask(__name__)


# Run our sensors threads and action thread to perform action
dht_thread.start()
adc_thread.start()
action_thread.start()

# Load environment variables used in our server
load_dotenv()


# The actual decorator function used to check APIs requests
def require_appkey(view_function):
    @wraps(view_function)
    # The new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        with open('api.key', 'r') as apikey:
            key = apikey.read().replace('\n', '')

        if request.headers.get('server-api-key') and request.headers.get('server-api-key') == key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


# Extract Header Data From APIs Requests
def get_header_info():
    response = {}
    response['method'] = request.__dict__['environ']['REQUEST_METHOD']
    response['path'] = request.__dict__['environ']['PATH_INFO']
    response['remote_addr'] = request.__dict__['environ']['REMOTE_ADDR']
    response['host_server'] = request.__dict__['environ']['HTTP_HOST']
    header_msg = response['remote_addr'] + " " + response['method'] + \
        " " + response['host_server'] + response['path']
    return header_msg

#--------------------------------------------------------------------#
#   API         :  <ip>:<port>/sensors                               #
#   Discription :  Get all information about sensors in the field    #
#                  And add a new sensor                              #
#   Methods     :  GET , POST [name, number, discription,isDigitsl]  #
#--------------------------------------------------------------------#


@app.route('/sensors', methods=['GET'])
def handle_get():
    header_log = log.log()
    header_log.add(get_header_info(), "HEADER_INFO")

    sensor_obj = sensor.sensor()
    return jsonify(sensor_obj.get_all())


@app.route('/sensors', methods=['POST'])
@require_appkey
def handle_post():
    header_log = log.log()
    header_log.add(get_header_info(), "HEADER_INFO")

    sensor_obj = sensor.sensor()
    sensor_name = request.form['name']
    sensor_number = request.form['number']
    sensor_discription = request.form['discription']
    sensor_isDigital = request.form['isDigital']
    return jsonify(sensor_obj.add(sensor_name, sensor_number, sensor_discription, sensor_isDigital))

#--------------------------------------------------------------------#
#   API         :  <ip>:<port>/sensors/<id>                          #
#   Description :  Get and delete a sensor with the ID               #
#   Methods     :  GET , DELETE [name, number, discription,isDigitsl]#
#--------------------------------------------------------------------#


@app.route('/sensors/<int:id>', methods=['GET', 'DELETE'])
def get_sensor(id):
    header_log = log.log()
    header_log.add(get_header_info(), "HEADER_INFO")
    if request.method == 'GET':
        sensor_obj = sensor.sensor()
        return jsonify(sensor_obj.get_id(id))
    elif request.method == 'DELETE':
        sensor_obj = sensor.sensor()
        action_msg = "the sensor with id " + str(id) + " is deleted"
        return jsonify(sensor_obj.remove(id))

#--------------------------------------------------------------------#
#   API         :  <ip>:<port>/actuators                             #
#   Discription :  Get all information about actuators in the field  #
#                  And add a new actuator                            #
#   Methods     :  GET , POST [name, number, discription,isDigitsl]  #
#--------------------------------------------------------------------#


@app.route('/actuators', methods=['GET'])
def handle_actuator_get():
    header_log = log.log()
    header_log.add(get_header_info(), "HEADER_INFO")

    actuator_obj = actuator.actuator()
    return jsonify(actuator_obj.get_all())


@app.route('/actuators', methods=['POST'])
@require_appkey
def handle_actuator_post():
    header_log = log.log()
    header_log.add(get_header_info(), "HEADER_INFO")

    actuator_obj = actuator.actuator()
    sensor_name = request.form['name']
    sensor_number = request.form['number']
    sensor_discription = request.form['discription']
    sensor_isDigital = request.form['isDigital']
    return jsonify(actuator_obj.add(sensor_name, sensor_number, sensor_discription, sensor_isDigital))

#--------------------------------------------------------------------#
#   API         :  <ip>:<port>/actuators/<id>                        #
#   Description :  Get and delete a actuator with the ID             #
#   Methods     :  GET , DELETE [name, number, discription,isDigitsl]#
#--------------------------------------------------------------------#


@app.route('/actuators/<int:id>', methods=['GET', 'DELETE'])
def get_actuator(id):
    header_log = log.log()
    header_log.add(get_header_info(), "HEADER_INFO")
    if request.method == 'GET':
        actuator_obj = actuator.actuator()
        return jsonify(actuator_obj.get_id(id))
    elif request.method == 'DELETE':
        actuator_obj = sensor.sensor()
        return jsonify(actuator_obj.remove(id))

#--------------------------------------------------------------------#
#   API         :  <ip>:<port>/actuators/set_action/<id>             #
#   Description :  Set action to specific actuator with ID           #
#   Methods     :  POST[value, action_type]                          #
#--------------------------------------------------------------------#


@app.route('/actuators/set_action/<int:id>', methods=['POST'])
@require_appkey
def control_servo(id):

    header_log = log.log()
    header_log.add(get_header_info(), "HEADER_INFO")

    actuator_obj = actuator.actuator()
    #value = int(request.form['value'])
    action_type = request.form['action_type']
    # return jsonify(actuator_obj.set_action(id, value, action_type))
    return jsonify(actuator_obj.set_action(id, action_type))

#--------------------------------------------------------------------#
#   API         :  <ip>:<port>/system_log                            #
#   Discription :  Get all records related in log database           #
#   Methods     :  GET                                               #
#--------------------------------------------------------------------#


@app.route('/system_log', methods=['GET'])
def get_sensor_log():
    header_log = log.log()
    header_log.add(get_header_info(), "HEADER_INFO")
    if request.method == 'GET':
        system_log = log.log()
        return jsonify(system_log.get_all())


if __name__ == '__main__':
    app.run()
