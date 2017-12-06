# Running tests for the module

C:\Program Files (x86)\Odoo 11.0\server>

..\python\python.exe odoo-bin  \
 --test-enable \   #enable
 -u hr_expense_attachments_download \  # name the module
 --log-level=test \   # logging level
 --stop-after-init    # do not run server