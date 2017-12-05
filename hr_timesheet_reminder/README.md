#Timesheet Reminder

Sends an timesheet remind email every 4th of the month when an employee forgot to complete his timesheet.
It adds a boolean remind_to_make_timesheets in hr.employee. The cron check that the employee is active and that the boolean remind_to_make_timesheets is true before checking his timesheets.
The timesheets are checked by the date of the last month and if the state are not 'confirm' or 'done' then an email is send.
    
This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions under the control of Valentin THIRION.
