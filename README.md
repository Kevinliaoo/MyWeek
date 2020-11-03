# MyWeek

MyWeek is a program that helps students with their time management, MyWeek uses Machine Learning to organize the most suitable timetable for students acording to their goals, this program can also predict the student's exam performance based on their study time.  
![img](https://github.com/Kevinliaoo/MyWeek/blob/master/assets/foto1.PNG)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

## Instructions
* Adding events:\
Click the "Add event" button to schedule a new event in the time table, a popup window will appear for user to insert the event's data.
* Editting event name:\
To edit an event's name, click the event in the time table, a popup window showing the event's information will appear, then click the "Edit event" button. 
* Deleting an event:\
To delete a single event, click the event in the time table, a popup window showing the event's information will appear, then click the "Delete event" button. 
* Delete all the schedule:\
Click the "Clear my schedule" button to clear the time table. 
* Predict exam qualifications: \
Click the "Predict qualification" button to make predictions. \
If the user has any exams scheduled, the program will show a popup window showing all the predicted grades for each exam. The prediction is based on student's study time, absences and previous failures, these last two pieces of data can be configurated by clicking the exam event in the time table. \
The Machine Learning model has an accuracy of ±2 points.
* Schedule time table: \
Click the "Predict timetable" button to make the program build a suitable time table for the student.\
A popup window asking for students target grade will appear, and once the user inserts it's desirable grade, the program will add a suitable ammount of study time for the student to reach the goal. 

## Running

```bash
python Main.py
```

## Author
Kevin Liao - @kevinliaoo