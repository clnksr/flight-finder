import requests
from pprint import pprint
from datetime import datetime, timedelta
from flight_data import FlightData
import credentials


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        location_endpoint = f"{credentials.KIWI_ENDPOINT}locations/query"
        headers = {"apikey": credentials.KIWI_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def search_flights(self, departure_city_code, arrival_city_code, from_time, to_time, max_stops, current_stops=0):
        search_endpoint = f"{credentials.KIWI_ENDPOINT}v2/search"
        headers = {"apikey": credentials.KIWI_API_KEY}
        query = {"fly_from": departure_city_code,
                 "fly_to": arrival_city_code,
                 "date_from": from_time.strftime("%d/%m/%Y"),
                 "date_to": to_time.strftime("%d/%m/%Y"),
                 "nights_in_dst_from": 7,
                 "nights_in_dst_to": 28,
                 "flight_type": "return",
                 "one_for_city": 1,
                 "curr": "CHF",
                 "max_stopovers": current_stops,
                 }
        # pprint(query)
        response = requests.get(url=search_endpoint, headers=headers, params=query)
        data = response.json()

        try:
            data = response.json()["data"][0]
        except IndexError:
            if current_stops < max_stops * 2:
                print(f"searching again for {current_stops+1} stops")
                return self.search_flights(departure_city_code, arrival_city_code, from_time, to_time, max_stops, current_stops + 1)
            else:
                return None

        via_city = ""
        for stop in data["route"]:
            if stop["cityCodeTo"] != arrival_city_code and current_stops > 0:
                via_city += stop["cityTo"]
                break

        destination_city = "n/a"
        for stop in data["route"]:
            if stop["cityCodeTo"] == arrival_city_code:
                destination_city = stop["cityTo"]
                break

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=destination_city,
            destination_airport=data["route"][current_stops]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0],
            stop_overs=current_stops,
            via_city=via_city,
            deep_link=data["deep_link"]
            )
        # pprint(data)
        return flight_data
