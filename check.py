from bs4 import BeautifulSoup
import requests
from send import send_mail
import time

URL = "https://telegov.njportal.com/njmvc/AppointmentWizard/12/135" # freehold DMV

def check_availablility():
	webpage = requests.get(URL)
	soup = BeautifulSoup(webpage.content, "lxml")

	text = soup.get_text()

	appt_available = "Currently, there are no appointments available at this location. Please try later in the case of a cancellation or try again over the next few days as more appointment times become available." not in text

	print(appt_available)

	if appt_available:
		send_mail(body=f"Schedule here:\n\n{URL}")

if __name__ == "__main__":
	while True:
		check_availablility()
		print(f"Dormant {time.time()}")
		time.sleep(15*60)