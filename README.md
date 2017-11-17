# AlterEgo
## A Discord Bot by 1600Horsepower

### Features

##### Direct Commands

Certain commands will be accepted by Alter Ego when written by anyone within earshot.  Currently these are:

"$reboot": Restarts Alter Ego (Assuming it is currently running)

"$shutdown": Shuts down Alter Ego

Both of these commands induce a clean exit.

##### Web Fetcher

This pulls information from various internet sources when prompted with a word of phrase bracketed in [[]]. Currently, the only implemented endpoint fetches Magic: the Gathering cards.

##### Reminders

When prompted (and tagged), Alter Ego will remind you of an event.  The syntax is relatively flexible.  Examples of prompts that work:

###### "@AlterEgo, can you remind me "that I need to buy eggs" in six hours?"
###### "Can I get a reminder in a minute that I really need to take a shower, @AlterEgo?"
###### "Please remind me in 7 hours, 6 minutes, and 10 seconds to stop being so precise, @AlterEgo."

### In Progress Features

##### Markov Chaining

Not sure what I'm gonna do with this, but it's fun to have.

##### Calendar Management

The syntax and use cases for this are very much in progress.

##### Instagram Account

Yeah.

### Requirements

Alter Ego runs on Python 3.4+.  The discord.py library is essential, for obvious reasons.  It can be found here:

https://github.com/Rapptz/discord.py
                           
