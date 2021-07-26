import requests


class VaccineAvailability(object):
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?'
    headers = {
        'Host': 'cdn-api.co-vin.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }

    def __init__(self, pincode, date):
        self.pincode = pincode
        self.date = date

    @property
    def generate_url(self):
        new_url = f"{self.url}pincode={self.pincode}&date={self.date}"
        return new_url

    @property
    def get_data(self):
        data_url = self.generate_url
        try:
            data = requests.get(data_url, headers=self.headers, timeout=2.0)
            return data.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            return {"message": "Unable to establish connection, timeout occurred"}

    def vaccine_final_details(self, place: str, vaccine_name: str, dose1: int, dose2: int, min_age: int,
                              max_age: int, vaccination_list_data: []) -> []:

        vaccine_details = {"place": place,
                           "vaccine": vaccine_name,
                           "dose1": dose1,
                           "dose2": dose2,
                           "min_age": min_age,
                           "max_age": max_age}
        vaccination_list_data.append(vaccine_details)
        return vaccination_list_data

    def check_vaccination_details(self, vaccine_list: []):
        if len(vaccine_list) > 0:
            return vaccine_list
        else:
            return "No vaccine available for the given date."

    def check_availability_all_age(self):
        global max_age
        vaccination_list = []
        vaccination_list_data = []
        slot_list = self.get_data
        try:
            slot_value = slot_list['sessions']
        except KeyError:
            return "No vaccine available for the given date."
        for i in range(len(slot_value)):
            try:
                if slot_value[i]['max_age_limit']:
                    max_age = slot_value[i]['max_age_limit']
            except KeyError:
                max_age = 80
            if slot_value[i]['allow_all_age']:
                if slot_value[i]['available_capacity'] > 0:
                    vaccination_list = self.vaccine_final_details(slot_value[i]['name'], slot_value[i]['vaccine'],
                                                                  slot_value[i]['available_capacity_dose1'],
                                                                  slot_value[i]['available_capacity_dose2'],
                                                                  slot_value[i]['min_age_limit'], max_age,
                                                                  vaccination_list_data)

        return self.check_vaccination_details(vaccination_list)

    def check_availability_youth(self):
        global max_age
        vaccination_list = []
        vaccination_list_data = []
        slot_list = self.get_data
        try:
            slot_value = slot_list['sessions']
        except KeyError:
            return "No vaccine available for the given date."
        for i in range(len(slot_value)):
            try:
                if slot_value[i]['max_age_limit']:
                    max_age = slot_value[i]['max_age_limit']
            except KeyError:
                max_age = 44
            if not slot_value[i]['allow_all_age'] and slot_value[i]['min_age_limit'] < 45:
                if slot_value[i]['available_capacity'] > 0:
                    vaccination_list = self.vaccine_final_details(slot_value[i]['name'], slot_value[i]['vaccine'],
                                                                  slot_value[i]['available_capacity_dose1'],
                                                                  slot_value[i]['available_capacity_dose2'],
                                                                  slot_value[i]['min_age_limit'], max_age,
                                                                  vaccination_list_data)
        return self.check_vaccination_details(vaccination_list)

    def check_availability_old(self):
        global max_age
        vaccination_list = []
        vaccination_list_data = []
        slot_list = self.get_data
        try:
            slot_value = slot_list['sessions']
        except KeyError:
            return "No vaccine available for the given date."
        for i in range(len(slot_value)):
            try:
                if slot_value[i]['max_age_limit']:
                    max_age = slot_value[i]['max_age_limit']
            except KeyError:
                max_age = 90
            if not slot_value[i]['allow_all_age'] and slot_value[i]['min_age_limit'] > 44:
                if slot_value[i]['available_capacity'] > 0:
                    vaccination_list = self.vaccine_final_details(slot_value[i]['name'], slot_value[i]['vaccine'],
                                                                  slot_value[i]['available_capacity_dose1'],
                                                                  slot_value[i]['available_capacity_dose2'],
                                                                  slot_value[i]['min_age_limit'], max_age,
                                                                  vaccination_list_data)
        return self.check_vaccination_details(vaccination_list)
