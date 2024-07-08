import time
from multiprocessing import Pool, Queue, Process, current_process, Manager

NUM_PROCESSES = 4

def target_func(tasks_to_accomplish, tasks_that_are_done):
    try:
        val = tasks_to_accomplish.get_nowait()
        print(f"Task no {val}")
        time.sleep(0.5)
        print(f"Task no {val} is done by {current_process().name}")
        tasks_that_are_done.put(f"Task no {val} is done by Process-{current_process().name[-1]}")
    except Exception as e: 
        print(e)            
    return

if __name__=="__main__":
    with Manager() as manager: # for shared queue
        tasks_to_accomplish = manager.Queue()
        tasks_that_are_done = manager.Queue()
        for i in range(10):
            tasks_to_accomplish.put(i)
            
        while not tasks_to_accomplish.empty():
        # producer process 선언
            procs=[]
            for i in range(NUM_PROCESSES):
                procs.append(Process(name=f'Process-{i+1}', target=target_func, args=(tasks_to_accomplish, tasks_that_are_done,)))

            for proc in procs:
                proc.start()
                
            for proc in procs:
                proc.join()