import threading
from time import sleep
def worker(count):
    """funcion que realiza el trabajo en el thread"""
    print("Este es el %s trabajo que hago hoy para Genbeta Dev" % count)
    sleep(count*2 + 1)
    return
threads = list()
pass
for i in range(10):
    while(len(threads)>2):
        print("Waiting") 
        sleep(1)
        for thread in threads:
            if not thread.isAlive():
                break
        if not thread.isAlive():
                threads.remove(thread)  
            
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()