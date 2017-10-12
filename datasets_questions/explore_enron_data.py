#!/usr/bin/python

"""
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000

"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl",
                              "r"))

print("people in the data:", len(enron_data))
print("features in the data:", len(enron_data[enron_data.keys()[0]]))
print("number of poi:", sum(enron_data[key]["poi"] for key in enron_data))
print("emails from Wesley Colwell to poi:",
      enron_data["COLWELL WESLEY"]["from_this_person_to_poi"])
print("stock options from Skilling:",
      enron_data['SKILLING JEFFREY K']['exercised_stock_options'])
poi_keys = ['SKILLING JEFFREY K', 'FASTOW ANDREW S', 'LAY KENNETH L']
for key in poi_keys:
    print(key, enron_data[key]["total_payments"])
print("people with salary info:",
      sum(enron_data[key]['salary'] != 'NaN' for key in enron_data))
print("people with email address:",
      sum(enron_data[key]['email_address'] != 'NaN' for key in enron_data))
print("POIs with missing payment info:",
      sum(enron_data[key]['total_payments'] == 'NaN' for key in poi_keys))
print("Number of people with total_payments:",
      sum(enron_data[key]['total_payments'] != 'NaN' for key in enron_data))
