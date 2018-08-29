===========================================
   Timesheet Reminder
===========================================

This module is an add-on to ``hr``.

Sends an timesheet remind email every 4th of the month when an employee forgot to complete his timesheet.

It adds a boolean remind_to_make_timesheets in hr.employee. The cron check that the employee is active
and that the boolean remind_to_make_timesheets is true before checking his timesheets.

The timesheets are checked by the date of the last month and if the state are not 'confirm' or 'done'
then an email is send.

Installation notes
==================

Credits
=======

Contributors
------------

* Bernard Delhez
* Paul Ntabuye Butera <paul.n.butera@abakusitsolutions.eu>

Maintainer
-----------

.. image:: http://www.abakusitsolutions.eu/wp-content/themes/abakus/images/logo.gif
   :alt: AbAKUS IT SOLUTIONS
   :target: http://www.abakusitsolutions.eu

This module is maintained by AbAKUS IT SOLUTIONS
