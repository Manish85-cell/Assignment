# Assignment

## Question 1

### Are Django Signals Synchronous?

### Answer:

Django signals are synchronous by default.

### Proof:

To prove this, I created two models, `People` and `Product`, and a `signals.py` file containing `post_save` signals for their creation. The People creation signal is intentionally slow, taking 5 seconds to execute, while the Product creation signal is fast.

In `views.py`, I created a People object and then a Product object and measured the total time taken.

If the signals were asynchronous, the total execution time should be equal to the time taken by the longest signal, i.e., 5 seconds. However, the observed execution time was 6.01 seconds, showing that the People creation signal (5 seconds), the Product creation signal (1 second), and the object creation time (approximately 0.01 seconds) were executed sequentially.

Hence, Django signals are executed synchronously by default.

---

## Question 2

### Do Django signals run in the same thread as the caller?

### Answer:

Django signals and the caller run on the same thread by default.

### Proof:

After running the command:

```bash
python3 manage.py runserver
```

and calling the `localhost:8000/sync` URL from the browser, the `sync` view is executed.

In the caller function, I added logs to print the name of the current thread. Similarly, in the signal functions inside `signals.py`, I added logs to print the thread name.

In the terminal, we can see:

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
June 02, 2026 - 00:21:29
Django version 6.0.5, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/6.0/howto/deployment/

[Caller] running on Thread: Thread-1 (process_request_thread)
[People] Creation Signal started on Thread: [Thread-1 (process_request_thread)]
[People] Creation Signal finished on Thread: [Thread-1 (process_request_thread)]
[Product] Creation Signal started on Thread: [Thread-1 (process_request_thread)]
[Product] Creation Signal finished on Thread: [Thread-1 (process_request_thread)]
Request completed in 6.01 seconds
[02/Jun/2026 00:21:40] "GET /sync/ HTTP/1.1" 200 33

Both signals and the caller are running on the same thread.

Hence proved.

---

## Question 3

### By default, do Django signals run in the same database transaction as the caller?

### Answer:

Yes, by default Django signals run in the same database transaction as the caller.

### Proof:

We know that if a signal runs in the same transaction as the caller using `transaction.atomic()`, and a rollback later occurs in the caller's transaction, then any database changes made inside the signal should also be rolled back.

To verify this, I created an `AuditLog` model that stores messages whenever other models are created.

In `signals.py`, I created a signal named `create_log`, which is triggered on the `post_save` event of both the Person and Product models.

In `views.py`, I created a `test_transaction` function that demonstrates the creation of a Person object inside an atomic transaction and then forces a rollback by raising an exception.

Before the rollback, a new Person object is created by the caller function, and an AuditLog object is created by the signal function.

After the rollback, the counts of Person and AuditLog objects are checked and found to be unchanged. This shows that both the caller and the signal operations were part of the same database transaction.

Hence, Django signals run in the same database transaction as the caller by default.

Hence proved.

### For Testing Purposes

Run the server and call:

```text
localhost:8000/test_transaction
```

### Server Logs:

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

4. Exception raised → Transaction rolled back

5. After transaction block
   Persons=7, AuditLogs=0

[02/Jun/2026 01:05:12] "GET /test_transaction/ HTTP/1.1" 200 4
