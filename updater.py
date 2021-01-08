'''
'	updater.py
'
'	Handles updating the JSON file data and
'	also detects and will eventually be able to
'	update outdated versions of Habiter to maintain
'	compatibility
'''

# NOTE: ensure standard datetime format

import json
import sys
import datetime as date
import os.path as path

import habiter_math as habmath

# Constants
HABITER_VERSION = "1.1.0"
HAB_DATE_FORMAT = "%d, %b, %Y %H:%M%p"
HAB_JSON_FPATH	= "records.json"
HAB_JSON_IND	= 2


class HabiterUpdater:
	def __init__(self, filePath):
		self.fp = filePath
		self.date = date.datetime.now()

		self.update_habiter()


	# Note that this method simply ignores inactivity of Habiter and updates where it left off
	def update_habiter(self):
		# Read up-to-date record

		try:
			with open(self.fp, 'r') as fh:
				data = json.load(fh)
		except json.JSONDecodeError:
			print(f"[ERROR: UPDATE_HABITER:\t JSON decoding error; \"{HAB_JSON_FPATH}\" may have been tampered with.]")
		else:
			# Update last accessed datetime to current time
			data["util"]["last_logged"] = self.date.strftime(HAB_DATE_FORMAT)
			loggedDate = date.datetime.strptime( data["util"]["last_logged"], HAB_DATE_FORMAT ).date()

			# Compare last logged date to each last updated habit 
			for habit in data["habits"]:
				# Has the habit been recently active
				if habit["date_info"]["active"] == True:
					habitDate = date.datetime.strptime( habit["date_info"]["last_updated"], HAB_DATE_FORMAT ).date()

					# Has the date stored in this habit object already passed
					if habitDate < loggedDate:
						# If so, that means we need to update its information
						habit["prev_occ"]				= None
						habit["n_trials"]				+= 1
						habit["date_info"]["active"]	= False
						habit["avg"] = habmath.running_avg( habit["avg"],
															habit["occ"],
															habit["n_trials"])
						habit["occ"] = 0

			# Write new data to .json file
			with open(self.fp, 'w') as fh:
				json.dump(data, fh, indent=HAB_JSON_IND)


	def check_version(self):
		raise NotImplementedError


	##
	# Helper Methods
	##


	def add_key_into_list_objs(self, listName:str, key:str, initVal=None):
		count = 0

		with open(self.fp, 'r') as fh:
			data = json.load(fh)

		# Does the list exist
		if listName not in data:
			print(f"ERROR: ADD_KEY FROM LIST:\t[The list \"{listName}\" does not exist within the record.]")
			return

		# Add keys if they don't already exist
		for obj in data[listName]:
			if key not in obj:
				obj[key] = initVal
				count += 1
			else:
				print(f"ERROR: ADD_KEY INTO LIST:\t[Key with the name \"{key}\" already exists.]")

		with open(self.fp, 'w') as fh:
			json.dump(data, fh, indent=HAB_JSON_IND)

		print(f"[Added {count} \"{key}\" keys into the list \"{listName}\".]")


	def del_key_from_list_objs(self, listName:str, key:str):
		count = 0

		with open(self.fp, 'r') as fh:
			data = json.load(fh)

		# Does the list exist
		if listName not in data:
			print(f"ERROR: DEL_KEY FROM LIST:\t[The list \"{listName}\" does not exist within the record.]")
			return

		# Delete keys if they haven't already been deleted
		for obj in data[listName]:
			if key in obj:
				obj.pop(key)
				count += 1
			else:
				print(f"ERROR: DEL_KEY FROM LIST:\t[No key with the name \"{key}\".]")

		# Write new data to .json file
		with open(self.fp, 'w') as fh:
			json.dump(data, fh, indent=HAB_JSON_IND)
		print(f"[Deleted {count} \"{key}\" keys from the list \"{listName}\".]")
