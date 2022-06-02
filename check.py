from bs4 import BeautifulSoup
import requests
from send import send_mail
import time
from collections import OrderedDict
import json
import re
from icecream import ic
import pandas as pd

URL = "https://telegov.njportal.com/njmvc/AppointmentWizard/12"
locs_i_care_about = {
	"Eatontown - Real ID",
	"Freehold - Real ID",
	"Elizabeth - Real ID"
}

def get_var(soup, var_name):
	pattern = re.compile(f"var {var_name} " + r"=(.*?)[;\n]")
	script_tag = soup.find("script", text=pattern)
	var_data = json.loads(pattern.search(script_tag.text).group(1))
	return var_data

def parse_status(status_text):
	return status_text != "No Appointments Available"

def check_availablility():
	webpage = requests.get(URL)
	soup = BeautifulSoup(webpage.content, "lxml")

	location_data = get_var(soup, "locationData")
	time_data = get_var(soup, "timeData")

	id_to_location = {x["LocAppointments"][0]["LocationId"]: x["Name"] for x in location_data}

	time_df = pd.DataFrame.from_dict(time_data)
	time_df["Location"] = time_df["LocationId"].map(id_to_location)
	time_df["isAvailable"] = time_df["FirstOpenSlot"].apply(parse_status)

	time_df.to_csv("locationStatus.csv", index=False)

	available = set(time_df.loc[time_df["isAvailable"] == True, "Location"]) & locs_i_care_about

	if available:
		send_mail(body=f"{available} available!\n\nSchedule here: {URL}")

	return available

if __name__ == "__main__":
	while True:
		check_availablility()
		print(f"Dormant {time.time()}")
		time.sleep(15*60)