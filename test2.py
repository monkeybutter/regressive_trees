from multiprocessing import Process, Manager
import time


def long_process(queue, id):
    time.sleep(10)
    queue.put((id, [13,6], {}))
    return


processes = []
#queue = Queue()
manager = Manager()
queue = manager.Queue()

for id in range(8):
    p = Process(target=long_process, args=(queue, id))
    processes.append(p)
    p.start()

# Wait for all processes to finish
for p in processes:
    p.join()

for p in processes:
    id, de, di = queue.get()
    #ida = queue.get()
    print(id)
    print(de)
    print(di)
    #print(ida)