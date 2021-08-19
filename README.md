<p align="center">
<img src="https://raw.githubusercontent.com/kemzeb/habiter/main/docs/img/habiter.gif" height = 180 width = 450>
</p>

---

habiter quantifies and keeps track of unwanted habits you have developed over time. It is interacted within a place where all programmers or simple travelers within the world of computing feel are most familiar with: the shell.

It essentially addresses the problem we have of ridding ourselves of bad habits by making it out in the open for us to see explicitly by tracking the number of occurrences we notice with our habits per day. This data can then be viewed at any time as well manipulated by habiter with particular math concepts (i.e Poisson approximation, average percent change, etc.) to provide better insight into these habits.

## Features

- CLI interaction using the `click` library
- Addition, deletion, updating of habits through the cooperation of the `sqlite3` library
- Persistent data storage onto your local machine; your data is **yours** to own and use **alone**
- Poisson probability utilized to act upon data (more mathematical concepts to come)
- Ability to print summary information of your habits

## Installation

`pip install habiter`

Alternatively, you can **clone the repository**, though all interaction must take place at the root directory of the repo (usage explained below for both).

## Usage

If you installed habiter with pip, simply call `habiter` anywhere within the shell to interact with the command-line interface.

If you cloned the repo, use the following (assuming 'python3' is your **global path variable** and you're in the project root directory):

`python3 -m habiter.internal.run`

```
➜  habiter -h
[habiter]  Last accessed: 15 Jan, 1505 1:21AM

Usage: habiter [OPTIONS] COMMAND [ARGS]...

  Quantifies and keeps tabs on unwanted habits you have developed over time.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  add     add new habit(s) into record
  list    list all habits on record
  remove  delete habit(s) from record
  reset   reset some habit(s) from record
  tally   increment the number of occurrences for some habit(s)

  For more information, visit the code repository at
  https://github.com/kemzeb/habiter.
```

This is what is printed out after the `-h` option is requested (just typing `habiter` also does the trick). We will analyze each subcommand found above and any of its optional arguments.

#

`tally` subcommand allows for the incrementation of the occurrence of one or more habits that exists within the data. It keeps track of daily and total habit occurrence (aka 'tallies') day by day. It holds the following options:

- `-z, --zero` for informing habiter that you have had no occurrences for that day for some habit(s)
- `-n, --num` for providing a particular number of occurrences for that day for some habit(s) (**please note that** it applies to all habits that you currently inputted)

The reason why the `-z, --zero` option exists in the first place is because habiter has no way of telling whether a habit that has **zero occurrences** has been recently active, has never been active before, or has been inactive for a while. It simply informs habiter that this or a collection of particular habits should be considered `active` on that day. **If you add onto the occurrences** in any way afterward you won't find any trouble, however, this argument may **no longer be used** for that day.

#

`add` subcommand allows for the addition of one or more habits into the data. Any duplicated habit names provided are ignored and/or prints an error. It initializes all habits to a default state.

#

`remove` subcommand allows for the deletion of one or more habits from the data. Habit names that do not exist within the data prints an error but will not hinder the deletion of any other inputted habit names.

#

`reset` subcommand allows resetting one or more habits from the data to the initial state. Recorded total and daily tallies, number of days captured, and other information will no longer exist, but the habit will remain in the record.

#

`list` subcommand allows for the printing of all existing habits within the data. Its functionality can be extended using the following option:

- `-v, --verbose` for listing all habits + their attributes within the data

The following provides an example of this optional argument in use:

```
➜  habiter list -v
Habit + Attributes                    Value
-------------------                   -----
[mirror-writing]
  | P(Occurrences >= 2 today):        91.717%
  | Today's daily tally:              15
  | Total tally:                      1452
  | # of days captured:               352
  | Last updated:                     0 day(s) ago
  | Date added:                       15 Jan, 1505 1:21AM

-------------------                   -----
[habiter]  Note: More data captured = increased statistical accuracy!
```

## Essential To Do's

- Add ability to change the "wait period" or the time it takes before some habit is updated
- Research into and implement testing procedures
- Implement an undo manager class that accounts for alterations made to the database
- Provide extended documentation within the repo
- Implement more math concepts that work nicely with the data under consideration
