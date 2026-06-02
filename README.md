# Assignment

## Question 1
### Are Django Signal Synchronous?

### Answer:
Django Signals are synchronous by default.

### Proof: 
To prove this, I have created 2 models `People` and `Product` and a `signals.py` file
containing post_save signals for their creation.
People creation signal is quite slow taking 5 sec and product creation signal is fast.

In `views.py`, I created a People object and then Product object and measured time taken.

If the signals are asynchronous, total execution time should be time taken by longest signal i.e 5 seconds but the time taken is 6.01 seconds showing signals People creation (5 second) and product creation (1 second) with object creation time 0.1 seconds (approx) are executed synchronously.
Hence proved that Django Signals are executed synchronously by default.

Question 2.
Do django signals run in the same thread as the caller? 

Answer.
Django Signals and caller thread all run on same thread.

on running command
python3 manage.py runserver 
and on browser calling localhost:8000/sync url
sync is called
and in caller function I have added logs printing name of thread
Also in signal functions in singals.py I have added similar logs
In terminal , we can see

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
June 02, 2026 - 00:21:29
Django version 6.0.5, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/6.0/howto/deployment/
[Caller] running on Thread : Thread-1 (process_request_thread)
[People] Creation Signal started on Thread: [Thread-1 (process_request_thread)]
[People] Creation Signal finished on Thread: [Thread-1 (process_request_thread)]
[Product] Creation Signal started on Thread: [Thread-1 (process_request_thread)]
[Product] Creation Signal finished on Thread: [Thread-1 (process_request_thread)]
Request completed in 6.01 seconds
[02/Jun/2026 00:21:40] "GET /sync/ HTTP/1.1" 200 33

Both signals and caller running on same thread.

Hence proved

Question 3.
By default do django signals run in the same database transaction as the caller?

Answer.
Yes by default django signals run in the same database transaction as the caller.

Proof:
We know if signal runs in same transaction as caller 
with transaction.atomic()
and later rollback occurs in caller transaction then database changes made inside signal should also rollback.

For checking this I have created a AuditLog signal which stores other models creation message
In signals.py I created a signal create_log with got called on Person and Product post_save condition
In views.py a test_transaction function is made which shows creation of Person inside a atomic transaction and then rolling back raising exception

So before rolling back a new person object by caller function and audit object by signal function is created.
After rolling back count of person and audit objects is checked and they remain same showing both django signals and caller run on same database transaction by default.
hence proved.

For testing purpose :
run the server
and in browser call localhost:8000/test_transaction

Server Logs:

Django version 6.0.5, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/6.0/howto/deployment/
1. Before entering transaction
Persons=7, AuditLogs=0
2. Inside transaction, before Person creation
[People] Creation Signal started on Thread: [Thread-1 (process_request_thread)]
[People] Creation Signal finished on Thread: [Thread-1 (process_request_thread)]
Audit log created
3. Back in caller after Person creation
Persons=8, AuditLogs=1
4. Exception raised -> Transaction rolled back
5. After transaction block
Persons=7, AuditLogs=0
[02/Jun/2026 01:05:12] "GET //test_transaction/ HTTP/1.1" 200 4