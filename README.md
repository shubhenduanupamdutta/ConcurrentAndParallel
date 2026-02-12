# Code Along and My Changes for Udemy Course `Concurrent And Parallel Programming in Python`

---

## Python Considerations

### Threads

- Share the same memory space
- Small overhead associated with thread switching and management

### Multiprocessing

- Processes don't share memory, each process has its own python interpreter and GIL
- Higher overhead because of memory duplication

### Asyncio

- Single-threaded, single-process approach to concurrency
- Uses cooperative multitasking, where tasks voluntarily yield control to allow other tasks to run
- Can be more efficient for I/O-bound tasks, but may not be suitable for CPU-bound

### Concurrency in General

- More complex to write and debug than sequential code

---

## Threading Notes

- **Daemon Threads**: Daemon threads are background threads that automatically terminate when the main program exits. They are useful for tasks that should not prevent the program from exiting, such as logging or monitoring. To create a daemon thread, you can set the `daemon` attribute to `True` when creating the thread. For example:

```python
import threading

def background_task():
    while True:
        print("Running in the background...")

daemon_thread = threading.Thread(target=background_task, daemon=True)
daemon_thread.start()
```
