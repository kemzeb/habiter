'''
'	habiter.py
'
'	Provides essential .json file R/W and manipulation behaviors
'	as well as the shell display of its results
'''

# In the future I may need to create variables for CLI attributes
# just in case they're renamed

import json
import datetime as date
import os
from os import path

import habiter_math as habmath
import updater as upt


class Habiter:
	def __init__(self, filePath:str):
		self.fp = filePath

		# Create a JSON record IFF it does not exist OR contents are empty
		self.create_record()

		# Update record each time habiter is executed
		upt.HabiterUpdater(upt.HAB_JSON_FPATH)


	def occurrence(self, args, numOfOcc = 1):
		# Covert tuple to set to remove possible duplicates
		args = set(args)

		# Read up-to-date record
		with open(self.fp, 'r') as fh:
			data = json.load(fh)

		for arg in args:
			index = self.search_record_for_habit(arg, data) # search for index matching current habit name

			if index != None:
				# Check it the zero CLI flag has been used
				if numOfOcc == 0:
					if data["habits"][index]["occ"] > 0: # Has there already been occ's captured
						print(f"[ERROR: OCCURRENCE:\tHabit \"{arg}\" contains occurrences.]")
						continue

				# Update habit data
				data["habits"][index]["prev_occ"]		= data["habits"][index]["occ"] # Capture previous occurrence
				data["habits"][index]["occ"]			+= numOfOcc 
				data["habits"][index]["total_occ"] 		+= numOfOcc

				# Update date information
				data["habits"][index]["date_info"]["last_updated"]	= f"{date.datetime.now().strftime(upt.HAB_DATE_FORMAT)}"
				data["habits"][index]["date_info"]["active"] 		= True
			
				print("[Habit \"{}\" occurrence updated from {} to {}.]".format(arg, 
																		data["habits"][index]["prev_occ"], 
																		data["habits"][index]["occ"]))
			else:
				print(f"[ERROR: OCCURRENCE:\tHabit \"{arg}\" does not exist.]")

		# Write new data to .json file		
		with open(self.fp, 'w') as fh:
			json.dump(data, fh, indent=upt.HAB_JSON_IND)


	def add_habits(self, *args):
		# Covert tuple to set to remove possible duplicates
		args = set(args)

		# Read up-to-date record
		with open(self.fp, 'r') as fh:
			data = json.load(fh)

		# Check for already existing habit names in the record
		for habit in data["habits"]:
			# args is empty IFF they were all removed
			if len(args) <= 0:
				break

			for arg in args:
				if arg == habit["habit_name"]:
					print(f"ERROR: ADD:\t[Habit \"{arg}\" already exists.]")
					args.remove(arg)
					break

		# Initalize unique habit dict to default state and append to list
		for arg in args:
			newHabitObj = self.init_habit_str(arg)
			data["habits"].append( json.loads(newHabitObj) )

			print(f"[Habit \"{arg}\" has been added.]")

		# Write new data to .json file
		with open(self.fp, 'w') as fh:
			json.dump(data, fh, indent=upt.HAB_JSON_IND)


	def delete_habits(self, *args: str):
		# Read up-to-date record
		with open(self.fp, 'r') as fh:
			data = json.load(fh)

			if len(data["habits"]) <= 0: #! Need to provide dedicated user-friendly execption handling
				print("ERROR: DELETE:\t[Cannot delete from an empty habit list.]")
			else:
				for arg in args:
					index = self.search_record_for_habit(arg, data)

					if index != None:
						data["habits"].pop(index) # Remove dict from "habits" list
						print(f"[Habit \"{arg}\" has been deleted.]")
					else:
						print(f"ERROR: DELETE:\t[No habit with the name \"{arg}\".]")

		# Write new data to .json file
		with open(self.fp, 'w') as fh:
			json.dump(data, fh, indent=upt.HAB_JSON_IND)


	def reset_habits(self, *args: str):
		# Read up-to-date record
		with open(self.fp, 'r') as fh:
			data = json.load(fh)

		for arg in args:
			index = self.search_record_for_habit(arg, data)
			
			if index != None:
				data["habits"][index] = json.loads( self.init_habit_str(arg) ) 
				print(f"[Habit \"{arg}\" has been reset.]")
			else:
				print(f"ERROR: RESET:\t[No habit with the name \"{arg}\".]")

		with open(self.fp, 'w') as fh:
			json.dump(data, fh, indent=upt.HAB_JSON_IND)
	

	def list_habits(self):
		# Read up-to-date record
		with open(self.fp, 'r') as fh:
			data = json.load(fh)

		print("Habit\n-------------------")
		for habit in data["habits"]:
			print(habit["habit_name"])
		print("-------------------")

		
	def list_habits_k(self):
		# Read up-to-date record
		with open(self.fp, 'r') as fh:
			data = json.load(fh)

		print("Habit + Attributes\t\t\b\bValue")
		print("-------------------\t\t\b\b-----")

		currDay =  date.datetime.strptime(data["util"]["last_logged"], upt.HAB_DATE_FORMAT).day
		for habit in data["habits"]:
			deltaDay = None
			if habit["date_info"]["last_updated"] != None:
				habitDay = date.datetime.strptime(habit["date_info"]["last_updated"], upt.HAB_DATE_FORMAT).day
				deltaDay = currDay - habitDay

			print("[{}]".format( habit["habit_name"]) )
			print("  | Today's occurrences:\t{}".format( habit["occ"]) )
			print("  | Total occurrences:\t\t{}".format( habit["total_occ"]) )
			print("  | # of days captured:\t\t{}".format( habit["n_trials"]) )
			print(f"  | Last updated:\t\t{deltaDay} day(s) ago")
			print("  | Date added:\t\t\t{}".format( habit["date_info"]["date_added"]) )
		print("-------------------\t\t\b\b-----")

		
	def list_habits_ks(self):
		raise NotImplementedError


	##
	# Helper Methods
	##

	# Returns an index of the first found dict, else None
	def search_record_for_habit(self, key, data):
		return next( (i for i, habit in enumerate(data["habits"]) if habit["habit_name"] == key), None)


	def create_record(self):
		# If the file does not exist or is empty
		if not path.isfile(self.fp) or os.stat(self.fp).st_size <= 0:
			# Initalize JSON arrays to hold JSON objects
			fileLists = f'''{{"util": {{
							"version": \"{upt.HABITER_VERSION}\",
							"last_logged": \"{date.datetime.now().strftime(upt.HAB_DATE_FORMAT)}\"
							}}, 
							"habits": []}}'''

			with open(self.fp, 'w') as fh:
				pyObj =json.loads(fileLists) 	# Create python object
				json.dump(pyObj, fh, indent=upt.HAB_JSON_IND) 	# Convert to JSON and store into .json file


	# Note: "active" key represents if the habit saw new occurrences,
	# not if the habit data has been modified
	def init_habit_str(self, habitName: str):
		return f'''{{"habit_name": \"{habitName}\",
			"occ": 0, 
			"total_occ": 0, 
			"prev_occ": null,
			"n_trials": 0,
			"avg": 0.0,
			"date_info":
			{{
				"date_added": \"{date.datetime.now().strftime(upt.HAB_DATE_FORMAT)}\",
				"last_updated": null,
				"active": false	
			}}
			}}''' 
