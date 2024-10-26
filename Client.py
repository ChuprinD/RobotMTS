import requests
import time
import json


class Client:
    base_uri = "http://127.0.0.1:8801/api/v1/robot-cells/"
    token = "0218a97c-38a3-42e8-a97d-08c565ee7d95e80ba549-6ee3-4070-a18b-6b4bdd87aea0"

    def __init__(self, id, ip):
        self.robot_ip = ip
        self.robot_id = id
        self.client = requests.Session()
        self.request_all = "all"
        self.request_laser = "laser"
        self.request_imu = "imu"
        self.get_sensor_data(self.request_all)

    def get_url(self, action):
        return f"http://{self.robot_ip}/{action}"

    def get_sensor_data(self, request_type):
        try:
            url = self.get_url("sensor")
            time.sleep(1.4)
            print(url)
            headers = {'Content-Type': 'application/json'}
            json_matrix = json.dumps({"id": self.robot_id, "type": request_type})
            response = self.client.post(url, data=json_matrix, headers=headers)

            response.raise_for_status()

            sensor_data = json.loads(response.text)
            print(sensor_data)
            time.sleep(0.1)
            return sensor_data

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def make_action(self, direction, len):
        try:
            url = self.get_url("move")
            headers = {'Content-Type': 'application/json'}
            json_matrix = json.dumps({"id": self.robot_id, "direction": direction, "len": len})
            response = self.client.put(url, data=json_matrix, headers=headers)
            response.raise_for_status()

            print(f"Action 'move {direction}' executed successfully")
            time.sleep(0.25)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during 'move {direction}': {e}")
            return None

    def make_action_motor(self, left_pwm, right_pwm, time):
        try:
            url = self.get_url("motor")
            headers = {'Content-Type': 'application/json'}
            json_matrix = json.dumps({"id": self.robot_id, "l": left_pwm, "r": right_pwm, "l_time": time, "r_time": time})
            response = self.client.put(url, data=json_matrix, headers=headers)
            response.raise_for_status()

            print(f"Action 'move by motor' executed successfully")
            time.sleep(time / 1000)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during 'move by motor': {e}")
            return None

    def go_forward(self, len):
        self.make_action("forward", len)

    def go_back(self, len):
        self.make_action("backward", len)

    def turn_left(self, len):
        self.make_action("left", len)

    def turn_right(self, len):
        self.make_action("right", len)