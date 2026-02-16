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

---

## Docker to Run PostgreSQL

---

- Use `docker-compose` to manage the PostgreSQL container

```sh
docker compose -f compose.yaml up -d --build
```

Command to stop the container:

```sh
docker compose -f compose.yaml down
```

`-d` flag runs the container in detached mode, allowing you to continue using the terminal for other commands while the container is running. The `--build` flag forces a rebuild of the Docker image, ensuring that any changes to the Dockerfile or dependencies are included in the new image.

---

## Difference between Asyncio and Threading/Multiprocessing

---

- **Threading/Multiprocessing**: These approaches involve creating multiple threads or processes that can run concurrently. They are suitable for CPU-bound tasks (multiprocessing) and I/O-bound tasks (threading). However, they can be more complex to manage due to issues like race conditions and deadlocks.

- **Asyncio**: This is a single-threaded, single-process approach to concurrency that uses cooperative multitasking. It is particularly efficient for I/O-bound tasks, as it allows tasks to yield control when they are waiting for I/O operations to complete. However, it may not be suitable for CPU-bound tasks, as it does not take advantage of multiple CPU cores.
