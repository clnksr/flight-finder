from twilio.rest import Client
from flight_data import FlightData
import credentials
import smtplib
from pprint import pprint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



class NotificationManager:
    #client: Client
    def __init__(self):
        self.client = Client(credentials.account_sid, credentials.auth_token)

    def send_price_alert(self, flight_data: FlightData, desired_price):
        body = f"Low price alert!📢 Only CHF {flight_data.price} to fly from " \
                f"{flight_data.origin_city}-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport} " \
                f"from {flight_data.out_date} to {flight_data.return_date} "\
                f"Book here: {flight_data.deep_link}"
        if flight_data.via_city:
            body += f"Stop-over in {flight_data.via_city}. "
        body += f"FYI: your price limit for this route is CHF {desired_price}"
        body.encode("utf-8")
        print(f"✅Text message sent: {body}")

        self.client.messages \
            .create(
                body=body,
                from_=credentials.twilio_number,
                to=credentials.personal_phone_number
            )

    def send_emails(self, flight_list: list[FlightData], email_list):
        msg = MIMEMultipart("alternative")
        msg['Subject'] = f"Subject: Low price alert from {flight_list[0].origin_city}-{flight_list[0].origin_airport}! ✈️"
        msg['From'] = credentials.sender
        msg['To'] = credentials.my_email
        html_email_body = "<img src='https://i.imgur.com/zw0UdkD.png' width='100%'/>"
        html_email_body += "<h1>Hey there!</h1>"
        html_email_body += "Here are the newest deals I found for you:"
        html_email_body += "<ul>"
        for flight_data in flight_list:
            html_email_body += "<li style='margin-bottom: 20px'>"
            html_email_body += f"Only <strong>CHF {flight_data.price}</strong> to fly to " \
                f"<strong>{flight_data.destination_city}-{flight_data.destination_airport} </strong>  " \
                "<br>" \
                f"from {flight_data.out_date} to {flight_data.return_date}"
            if flight_data.via_city:
                html_email_body += "<br>"
                html_email_body += f"stop-over in {flight_data.via_city} "
            html_email_body += "<br>"
            html_email_body += f"<a href='{flight_data.deep_link}' target='_blank'>Book here! </a>"

            html_email_body += "</li>"
        html_email_body += "</ul>"
        part1 = MIMEText("", 'plain')
        part2 = MIMEText(html_email_body, 'html')
        msg.attach(part1)
        msg.attach(part2)
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(credentials.sender, credentials.gmail_pw)
            for email in email_list:
                connection.sendmail(from_addr=credentials.sender, to_addrs=email, msg=msg.as_string())
        print(f"✅Email is sent: {html_email_body}.")




