<p align="center">
<img src="https://raw.githubusercontent.com/kemzeb/habiter/main/docs/img/habiter.gif" height = 180 width = 450>
</p>

---

habiter quantifies and keeps track of habits within the command line.

It essentially addresses the problem of managing our habits (whether good or bad) by making it out in the open for us to see by simply tracking the number of occurrences we notice with our habits per day. This data can then be viewed at any time as well manipulated by using particular math concepts (e.g. Poisson approximation) to provide some means to visualize these habits.

## Features

- CLI interaction using the [click](https://github.com/pallets/click) library
- Addition, deletion, updating of habits through the cooperation of the `sqlite3` library
- Persistent data storage onto ***your local machine***; your data is **yours** to own and use **alone**
- Poisson probability is utilized to act upon your data (more mathematical concepts to come)
- Ability to print summary information of your habits

## Installation

`pip install habiter`

Alternatively, you can **clone the repository**, though all interaction must take place at the root directory of the repo (usage explained below for both).

## To Do's

- [ ] Provide a configuration command to allow, as one may guess, the ability to configure habiter
- [ ] "Pretty" up the list command print-outs ([rich](https://github.com/Textualize/rich) looks pretty neat!)
- [ ] Implement an "undoing" feature to restore the habit record to previous states
- [ ] Utilize a console-based GUI rather than just the CLI (something similar to [lazygit](https://github.com/jesseduffield/lazygit))
- [ ] Introduce more math concepts that work nicely with the data under consideration

## Usage

If you installed habiter with pip, simply call `habiter` anywhere to get started.

If you cloned the repo, use the following (assuming you're in the project root directory and 'python3' command is your Python intrepreter):

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

`tally` subcommand allows for incrementing the occurrence of one or more habits that exists within the record. It keeps track of daily and total habit occurrence (aka 'tallies') day by day. It holds the following options:

- `-z, --zero` for informing habiter that you have had no tallies for that day for some habit(s)
- `-n, --num` for providing a particular number of occurrences for that day for some habit(s) (**please note that** it applies to all habits that you currently inputted)

The reason why the `-z, --zero` option exists in the first place is because habiter doesn't run as a daemon, where habit data could be updated automatically based on meeting certain time constraints. You could supply `-n 0` as input and this is essentally the same thing, but since there is a good chance that you have had no tallies for a habit on that particular day and becomes too cumbersome. The zero option simply informs habiter that the habits you supplied as input should be considered `active` today. **If you tally** afterward you won't find any trouble, however, you will exit with an error if you attempt to use this option with .

#

`add` subcommand allows for the addition of one or more habits into the record. If a habit already exists in the record, it will exit with an error but will not hinder the addition of any other inputted habit names.

#

`remove` subcommand allows for the deletion of one or more habits from the record. Similar to `add`, a habit ***that does not exist*** within the record will exit with an error but will not hinder the deletion of any other inputted habit names.

#

`reset` subcommand allows resetting one or more habits from the record to the initial state. Recorded total and daily tallies, number of days captured, and other information will no longer exist, but the habit will remain in the record.

#

`list` subcommand allows for the printing of all existing habits within the record. Its functionality can be extended using the following option:

- `-v, --verbose` for listing all habits + their attributes within the record

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
