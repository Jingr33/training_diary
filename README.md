# Training Diary
## Content Table
  * [Introduction](#introduction)
  * [Launch the app](#launch)
  * [Technologies](#technologies)
  * [User guide](#user_guide)
## Introdiction
The Training Diary is a Python application serving as a database of your trainings in different sports with many advanced options for managing your training plan.
## Launch the app
Open main.py file inside the repository a launch it in some development enviroment.
## Technologies
* Programming language: Python 3.11.9
* Framework: Tkinter, CustomTkinter

## User guide
### Sports
Now you can choose from 3 different sports:
* Run
* Swim
* Gym (workout)
Each sport has a specific color.
### Layout
The Training diary is divided into two sections.
* **Left column** is for adding a new training with its all behaviours or for creating a new training plan (through the "Nastavit plán" button).
* **Main section** serve to managing your training activities and data evaluation. You can choose from menu above (Přehled, Kalendář, Statistiky, Možnosti).
### Start
After start the app, you will see starting page with some last activity info. You can also add new data to a database.
### Add a new training
You can add a new training in the left column under the "Nový trénink" title. Firstly, you must choose your sport in a box called "Aktivita." Then you select a training date from a tkinter calendar and training duration in an input called "Čas". You can set also other training details if you want. Each sport has different attributes. 
If everything is setted press the "Uložit" button.
The confirmation message will appear if a training was successfully added into a database.
### Add a new training plan
 You can create your training plan in two different formats.
 * **Cycle training plan** - use it, if you want to create a complex repetitive plan with more trainings in some period.
 *  **Single training plan** - use it, if you want to add only one training, one training on specific dates or one training some day in a week.
#### Create a Cycle training plan
In the plans menu press "Vytvořit tréninkový cyklus" button.
You can see a window with a plan creator. On the bottom of a window, you must set the start date of the plan as "Začatek" and the end date as "Konec" or the number of training cycles as "Počet cyklů."
Under the "Nastavení tréninkového plánu" title there is an interactive plan creator. You can add next day if you press "Přdat den" button and remove any day through "Odstranit" button.
In each day preview you can see the number of a day in the plan and stripes of trainings. In a combobox "Nevybráno" you can set a sport and set training attributes. Then press "Přidat". If something is wrong, the button turns red for a moment, else you can see  the training stripe in the day preview. Hover over the strip to look tooltip with training attributes. You can add a free day if you want.
Press "Uložit" to save athe plan.
#### Create a Single training plan
In the plans menu press "Plán jednotlivých tréninků".
You can see a window with a plan creator. Set a date of (first) training in the plan, sport, duration and details setting of the training in the left column. You can set a day in the week (Monday, Saturday) or repetition of training (every 4 days) and set the number of weeks or repetitions. In the right column, you can set other specific dates of the training.
Press "Uložit" to save athe plan.
### Training Overview
### Calendar
### Statistics
### Options
There are two section:
#### Personal data
You can set some personal data a change it over time. (See personal data plot in Statistics.)
#### Settings
* Turn on "Cela obrazovka" mode to view the app in fullscreen.
* In "Tréninkové plány" section you can open a window of training plans and remove unnecessary plans.
* In "Sporty" section, there are all sport in the app. You can add or remove it from the sport selection menus in the app. Also you can change the colors of the sports.
* In "Položek na stránce" section you can change the number of displayed trainings on one page in the training overview.
