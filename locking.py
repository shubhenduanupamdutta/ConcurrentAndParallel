from threading import Thread

counter = 0


def increment_counter() -> None:
    global counter  # noqa: PLW0603
    for _ in range(10**9):
        counter += 1


threads = []
for _ in range(4):
    t = Thread(target=increment_counter)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final counter value: {counter}")
