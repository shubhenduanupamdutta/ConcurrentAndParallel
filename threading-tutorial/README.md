# Threading Tutorial Notes

---

Cleaning up example code in `main.py` and creating worker classes inherited from `threading.Thread` to demonstrate the use of threads in Python. This is part of the Udemy course `Concurrent And Parallel Programming in Python`.

---

## `threading.Thread` class

- `run` method is the entry point for the thread's activity. You can override this method in a subclass to define the thread's behavior. - `start` method is used to start the thread's activity. It calls the `run` method in a separate thread of control.
- `daemon` parameter in subclass must be set before `start` call to be effective.
