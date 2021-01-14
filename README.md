<p align="center">
<img src="docs/img/HABITER.jpg"> 
</p>

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

habiter is a work-in-progress program that quantifies and keeps track of unwanted habits you have developed over time. It exists and is interacted with in a place where all programmers or simple travelers within the world of computing feel most comfortable in: the shell.

It essentially addresses the problem we have of ridding ourselves of bad habits by making it out in the open for us to see explicitly by essentially tracking the number of occurrences we notice with our habits per day. This data can then be viewed at any time as well manipulated by Habiter with particular math concepts (i.e Possion approximation, average percent change, etc.) to provide better insight into these habits.

## Installation
Currently, habiter can only be interacted with by __cloning the repository__. Afterwards you should be all set, assuming you are using Python v3.8.3. See below for CLI usage explanations. 
 
## Usage
Every interaction is dependent on the following shell command (assuming 'python3' is your global path variable):


`python3 hab.py`

__Note that__ this command is executed within the repo's root directory.

Everything else besides this is essentially system arguments that are parsed and interpreted thanks to the `argparse` module. Each time this command is called, no matter what else is passed into it (i.e. subcommands, options), a `Habiter` object is created to facilitate JSON R/W behavior along with a `HabiterUpdater` object that updates the JSON file depending on user activity. Now let's take a look into the following subcommands offered:
```
python3 hab.py -h
usage: hab.py [-h] {occ,add,del,reset,list} ...

Quantifies and keeps tabs on unwanted habits you have 
developed over time.

positional arguments:
  {occ,add,del,reset,list}
    occ                 increment occurrence for habit(s)
    add                 add new habit(s) into record
    del                 delete habit(s) from record
    reset               reset habit(s) to default state
    list                list all habits on record

optional arguments:
  -h, --help            show this help message and exit
  --version
  ```
This is what is printed out after the `-h` option is requested. We will analyze each subcommand found above and any of its optional arguments.

`occ` subcommand allows for the incrementation of the occurrence of one or more habits that exists within the data. It keeps track of daily and total habit occurrence day by day. It holds the following options:
* `-z, --zero` for informing habiter that you have had no occurrences for that day for some habit(s)
* `-n [1-100], --num [1-100]` for providng a particular number of occurrence for that day for some habit(s) (__please note that__ it applies to all habits that you currently inputted)

__Note that__ these two arguments are __mutually exlcusive__.

The reason why the first argument exists in the first place is because habiter has no way of telling whether a habit that has __zero occurrences__ has been recently active, has never been active before, or has been inactive for a while. `-z, --zero` simply informs habiter that this or a collection of particular habits should be considered `active` on that day. __If you add onto the occurrences__ in any way afterwards you won't find any trouble, however this argument may __no longer be used__ for that day.
#
`add` subcommand allows for the addition of one or more habits into the data. Any duplicated habit names provided is ignored and/or prints an error. It initalizes all of its corresponding genereated data to a default state.
#
`del` subcommand allows for the deletion of one or more habits from the data. Habit names that do not exist within the data prints an error but will not hinder deletion of any other inputted habit names. 
#
`reset` subcommand allows reseting one or more habits from the data to inital state. 
#
`list` subcommand allows for the printing of all existing habits within the data. Its functionality can be extended using the following option:

* `-k, --keys` for listing all habits + their attributes within the data

The following below provides an example of this optional argument in use:
```
python3 hab.py list -k
Habit + Attributes	      Value
-------------------	      -----
[mirror-writing]
  | Today's occurrences:	15
  | Total occurrences:		354
  | # of days captured:		6570
  | Last updated:		0 day(s) ago
  | Date added:			15, April, 1505 01:21AM
```


## Essential To Do's
* Implement statistical concepts that works nicely with the data under consideration
* Make implementations more 'pythonic'
* Provide explanations of math concepts that is/will be utilized
* Make the CLI globally-accessible
* Package habiter using pip
* Automate testing procedures
