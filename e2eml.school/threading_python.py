import queue
import threading
import time


def fold_wontons(pan):
    counter = 0
    while True:
        time.sleep(.1)
        pan.put(f"wonton_{counter}")
        counter += 1


pan = queue.Queue()
worker = threading.Thread(target=fold_wontons, args=(pan,), daemon=True)
worker.start()

for i in range(10):
    time.sleep(.4)
    print(f"cooking batch {i}")
    while True:
        try:
            next_wonton = pan.get_nowait()
            print(next_wonton)
        except queue.Empty:
            break

