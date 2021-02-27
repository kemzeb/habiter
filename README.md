<p align="center">
<img src="https://raw.githubusercontent.com/kemzeb/habiter/main/docs/img/HABITER.jpg" height = 350 width = 500>
</p>

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

habiter quantifies and keeps track of unwanted habits you have developed over time. It is interacted with in a place where all programmers or simple travelers within the world of computing feel are most familiar with: the shell.

It essentially addresses the problem we have of ridding ourselves of bad habits by making it out in the open for us to see explicitly by essentially tracking the number of occurrences we notice with our habits per day. This data can then be viewed at any time as well manipulated by habiter with particular math concepts (i.e Poisson approximation, average percent change, etc.) to provide better insight into these habits.


## Features
* CLI interaction using the `argparse` module
* Addition, deletion, updating of habits through the cooperation of a json file
* Persistent data storage onto your local machine; your data is yours to own and use alone
* Poisson probability utilized to act upon data (more mathematical concepts to come)
* Ability to print summary information of each habit whenever needed


## Installation

`pip install habiter`

Alternatively, you can __clone the repository__, though all interaction must take place at the root directory of the repo (usage explained below for both).

## Usage
If you installed habiter with pip, simply call `habiter` anywhere within the shell to interact with the command line interface.

If you cloned the repo, use the following (assuming 'python3' is your __global path variable__):

`python3 -m habiter.run`

Each time a command is called, no matter what else is passed into it (i.e. subcommands, options), a `Habiter` object is created to facilitate user-data interaction along with a `HabiterUpdater` object that updates the JSON file depending on user activity. Now let's take a look into the following subcommands offered:
```
habiter -h
usage: habiter [-h] [--version] {tally,add,del,reset,list} ...

Quantifies and keeps tabs on unwanted habits you have
developed over time.

positional arguments:
  {tally,add,del,reset,list}
    tally               increment tally for some habit(s)
    add                 add new habit(s) into record
    del                 delete habit(s) from record
    reset               reset habit(s) to default state
    list                list all habits on record

optional arguments:
  -h, --help            show this help message and exit
  --version
  ```
This is what is printed out after the `-h` option is requested (just typing `habiter` also does the trick). We will analyze each subcommand found above and any of its optional arguments.

`tally` subcommand allows for the incrementation of the occurrence of one or more habits that exists within the data. It keeps track of daily and total habit occurrence (aka 'tallies') day by day. It holds the following options:
* `-z, --zero` for informing habiter that you have had no occurrences for that day for some habit(s)
* `-n [1-100], --num [1-100]` for providing a particular number of occurrence for that day for some habit(s) (__please note that__ it applies to all habits that you currently inputted)

__Note that__ these two arguments are __mutually exclusive (i.e. -z/--zero | -n/--num).

The reason why the `-z, --zero` option exists in the first place is because habiter has no way of telling whether a habit that has __zero occurrences__ has been recently active, has never been active before, or has been inactive for a while. It simply informs habiter that this or a collection of particular habits should be considered `active` on that day. __If you add onto the occurrences__ in any way afterwards you won't find any trouble, however this argument may __no longer be used__ for that day.
#
`add` subcommand allows for the addition of one or more habits into the data. Any duplicated habit names provided is ignored and/or prints an error. It initializes all habits to a default state.
#
`del` subcommand allows for the deletion of one or more habits from the data. Habit names that do not exist within the data prints an error but will not hinder deletion of any other inputted habit names.
#
`reset` subcommand allows reseting one or more habits from the data to initial state. Recorded total and daily tallies, number of days captured, and other information will no longer exist, but the habit will remain in the record.
#
`list` subcommand allows for the printing of all existing habits within the data. Its functionality can be extended using the following option:

* `-k, --keys` for listing all habits + their attributes within the data

The following below provides an example of this optional argument in use:
```
habiter list -k
Habit + Attributes                    Value
-------------------                   -----
[mirror-writing]
  | P(Occurrences >= 2 today):        91.717%
  | Today's daily tally:              15
  | Total tally:                      1452
  | # of days captured:               352
  | Last updated:                     0 day(s) ago
  | Date added:                       15, Jan, 1505 1:21AM

-------------------                   -----
[habiter]  Note: More data captured = increased statistical accuracy!
```


## Essential To Do's
* Optimize by avoiding using lists for data access as much as possible 
* Improve upon CLI design (maybe even shift to community CLI packages..?)
* Shift from json R/W to sqlite3 R/W for better optimization and abstraction
* Add ability to change the "wait period" or the time it takes before some habit is updated
* Research into and implement testing procedures
* Improve upon directory organization
* Provide extended documentation within the repo
* Implement more math concepts that work nicely with the data under consideration
* Possibly consider creating a GUI variant
