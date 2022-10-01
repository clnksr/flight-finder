import requests
import credentials


class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.member_data = {}
        self.flight_list = []

    def get_destination_data(self):
        response = requests.get(url=credentials.SHEETY_ENDPOINT, headers=credentials.BEARER_HEADER)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{credentials.SHEETY_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=credentials.BEARER_HEADER
            )

    def get_member_list(self):
        response = requests.get(url=credentials.SHEETY_MEMBER_ENDPOINT, headers=credentials.BEARER_HEADER)
        data = response.json()

        self.member_data = data["users"]
        return self.member_data

    def add_to_flight_list(self, flight):
        self.flight_list.append(flight)
        return self.flight_list
