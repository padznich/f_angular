
import json

from flask import Flask,render_template, jsonify, request
from pymongo import MongoClient


application = Flask(__name__)


@application.route("/")
def show_machine_list():
    return render_template("auto_list.html")


client = MongoClient('localhost:27017')
db = client.MachineData


@application.route("/addMachine", methods=['POST'])
def add_machine():
    try:
        json_data = request.json['info']
        device_name = json_data['device']
        ip_address = json_data['ip']
        user_name = json_data['username']
        password = json_data['password']
        port_number = json_data['port']

        db.Machines.insert_one({
            'device': device_name,
            'ip': ip_address,
            'username': user_name,
            'password': password,
            'port': port_number
            })
        return jsonify(status='OK', message='inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route("/getMachineList", methods=['POST'])
def get_machine_list():
    try:
        machines = db.Machines.find()

        machine_list = []
        for machine in machines:
            print(machine)
            machine_item = {
                'device': machine['device'],
                'ip': machine['ip'],
                'username': machine['username'],
                'password': machine['password'],
                'port': machine['port'],
                'id': str(machine['_id'])
            }
            machine_list.append(machine_item)
    except Exception as e:
        return str(e)
    return json.dumps(machine_list)


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
