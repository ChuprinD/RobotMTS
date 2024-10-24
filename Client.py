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
        return f"http://[{self.robot_ip}]/{action}"

    def get_sensor_data(self, request_type):
        try:
            url = self.get_url("sensor")
            response = self.client.put(url, data={"id":self.robot_id, "type":request_type})
            response.raise_for_status()

            sensor_data = json.loads(response.text)
            return sensor_data

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def make_action(self, action, len):
        try:
            url = self.get_url("move")
            response = self.client.put(url, data={"id":self.robot_id, "direction":action, "len":len})
            response.raise_for_status()

            print(f"Action '{action}' executed successfully")
            time.sleep(0.25)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during '{action}': {e}")

    def go_forward(self, len):
        self.make_action("forward", len)

    def go_back(self, len):
        self.make_action("backward", len)

    def turn_left(self, len):
        self.make_action("left", len)

    def turn_right(self, len):
        self.make_action("right", len)

    def send_matrix(self, matrix):
        try:
            url = f"http://127.0.0.1:8801/api/v1/matrix/send?token={self.token}"
            headers = {'Content-Type': 'application/json'}
            json_matrix = json.dumps(matrix)

            response = self.client.post(url, data=json_matrix, headers=headers)
            response.raise_for_status()

            print("Response status code:", response.status_code)
            print("Response body:", response.text)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while sending matrix: {e}")