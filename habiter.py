'''
'	habiter.py
'
'	Provides essential .json file R/W and manipulation behaviors
'	
'	Note that their exists alot of boilerplate code due to the
'	way I decided to handle file R/W 
'''

# In the future I may need to create variables for CLI attributes
# just in case they're renamed

import json
import datetime
import sys
import os.path as path


class Habiter:

	def __init__(self, filePath):
		self.fp = str(filePath) # property: file path

		# Initalize JSON arrays to hold JSON objects
		habitsList = '''{"util": [], "habits": []}'''

		# If the specified file does not exist,
		# create one and store habits list
		# as a JSON array within .json file
		self.create_record(self.fp)



	def occurrence(self, *args):
		# Read up-to-date record
		with open(self.fp, 'r') as fh:
			data = json.load(fh)

		# Increment occurrence of requested habits
		for habit in data["habits"]:
			if habit["habit_name"] in args:
				habit["occ"]		+= 1
				habit["total_occ"] 	+= 1

		# Write new data to .json file		
		with open(self.fp, 'w') as fh:
			json.dump(data, fh, indent=2)



	def add_habits(self, *args:str):
		# Covert tuple to set to remove possible duplicates
		args = set(args)

		# Read up-to-date record
		with open(self.fp, 'r') as fh:
			data = json.load(fh)



		# First we need to check for duplicate habit names in the record
		for habit in data["habits"]:
			# args is empty IFF they were all removed
			if len(args) <= 0:
				break

			for arg in args:
				if arg == habit["habit_name"]:
					print(f"ERROR: ADD:\t[Habit \"{arg}\" already exists.]")
					args.remove(arg)
					break

		# Initalize unique habit dict object to default state and append to list
		for arg in args:
			newHabitObj = self.init_habit_str(arg)
			data["habits"].append(json.loads(newHabitObj) )

			print(f"[Habit \"{arg}\" has been added.]")

		# Write new data to .json file
		with open(self.fp, 'w') as fh:
			json.dump(data, fh, indent=2)

		

	def delete_habits(self, *args: str):
		# Read up-to-date record
		with open(self.fp, 'r') as fh:
			data = json.load(fh)

			if len(data["habits"]) <= 0: #! Need to provide dedicated user-friendly execption handling
				print("ERROR: DELETE:\t[Cannot delete from an empty habit list.]")
			else:
				for arg in args:
					argExists = False # Accounts for habit names that do not exist

					for i in range( len(data["habits"]) ):
						if arg == data["habits"][i]["habit_name"]:
							argExists = True
							print(1)
							data["habits"].pop(i)

							print(f"[Habit \"{arg}\" has been deleted.]")
							break # No duplicates should exist, break

					if argExists == False:
						print(f"ERROR: DELETE:\t[No habit with the name \"{arg}\".]")

		# Write new data to .json file
		with open(self.fp, 'w') as fh:
			json.dump(data, fh, indent=2)



	def reset_habits(self, *args: str):
		# Read up-to-date record
		with open(self.fp, 'r') as fh:
			data = json.load(fh)

		for arg in args:
			argExists = False # Accounts for habit names that do not exist

			for i in range( len(data["habits"]) ):
				if arg == data["habits"][i]["habit_name"]:
					argExists = True
					data["habits"][i] = json.loads( self.init_habit_str(arg) )

					print(f"[Habit \"{arg}\" has been reset.]")
					break # No duplicates should exist, break

			if argExists == False:
				print(f"ERROR: RESET:\t[No habit with the name \"{arg}\".]")

		with open(self.fp, 'w') as fh:
			json.dump(data, fh, indent=2)
	


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
		for habit in data["habits"]:
			print(habit["habit_name"])
			print("  * Today's occurrences:\t{}".format( habit["occ"]) )
			print("  * Total occurrences:\t\t{}".format( habit["total_occ"]) )
		print("-------------------")

		


	def list_habits_ks(self):
		pass

	##
	# Helper Methods


	def create_record(self, filePath):
		# Initalize JSON arrays to hold JSON objects
		fileLists = '''{"util": [], "habits": []}'''

		if not path.isfile(filePath):
			with open(filePath, 'w') as fh:
				pyObj =json.loads(fileLists) 	# Create python object

				#pyObj["util"].append(f'''{{date_acc: }} ''')
				json.dump(pyObj, fh, indent=2) 	# Convert to JSON and store into .json file



	def init_habit_str(self, habitName: str):
		return f'''{{"habit_name": \"{habitName}\", 
			"occ": 0, 
			"total_occ": 0, 
			"prev_occ": 0,
			"n_trials": 0,
			"sum": 0,
			"avg": 0.0}}'''



	def add_key(self, listName, attr):
		pass



	def del_key(self, listName, attr):
		pass

