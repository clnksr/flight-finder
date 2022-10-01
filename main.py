from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()


sheet_data = data_manager.get_destination_data()
member_list = data_manager.get_member_list()
#
member_email_list = [member["email"] for member in member_list]
# member_email_list = ['celinekaiser5@gmail.com', 'hhhelloworld3@gmail.com', 'kgjmflb@arxxwalls.com']


# sheet_data = [
#     {"city": "Tokyo", "iataCode": "TYO", "lowestPrice": 10000, "maxStops": 1},
#     {"city": "Bali", "iataCode": "DPS", "lowestPrice": 100000, "maxStops": 1}
# ]

for row in sheet_data:
    if not row["iataCode"]:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

ORIGIN_CITY_IATA = "ZRH"

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=180)


for destination in sheet_data:
    flight = flight_search.search_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_now,
        max_stops=destination["maxStops"]
    )
    if flight:
        print(f"{flight.destination_city}: CHF {flight.price} {f'via {flight.via_city}' if flight.via_city else ''}")

        if flight.price <= destination["lowestPrice"]:
            data_manager.add_to_flight_list(flight)

        else:
            print(f"❌No flights for {flight.destination_city} below the price limit ({destination['lowestPrice']}) available.")

    else:
        print(f"❌ No flights found for {destination['iataCode']}.")


if len(data_manager.flight_list) > 0:
    notification_manager.send_emails(data_manager.flight_list, member_email_list)












