import threading
import queue
pan = queue.Queue()

def fold_wontons(pan, wrappers, filling):
    while wrappers > 0 and filling > 0:
        # It takes about 10 seconds for a 13 year old to fold a wonton.
        time.sleep(10)
        pan.put("wonton")

worker_1 = threading.Thread(
    target=fold_wontons, args=(pan, wrappers, filling))
worker_2 = threading.Thread(
    target=fold_wontons, args=(pan, wrappers, filling))

worker_1.start()
worker_2.start()

