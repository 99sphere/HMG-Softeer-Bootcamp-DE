import time
from multiprocessing import Pool, Queue, Process, current_process, Manager

NUM_TASK = 10
NUM_PROCESSORS = 4

def target_func(tasks_to_accomplish, tasks_that_are_done):
    try:
        while True:
            c_proc = current_process()
            print("Running on Process", c_proc.name, "PID", c_proc.pid)
            val = tasks_to_accomplish.get_nowait()
            print(f"Task no {val}")
            time.sleep(0.5)
            tasks_that_are_done.put(f"Task no {val} is done by {current_process().name}")
    except Exception as e: 
        pass          
    return

def main():
    manager = Manager()
    tasks_to_accomplish = manager.Queue()
    tasks_that_are_done = manager.Queue()

    for i in range(NUM_TASK):
        tasks_to_accomplish.put(i)
    
    p = Pool(NUM_PROCESSORS)
    p.map(target_func, tasks_to_accomplish, tasks_that_are_done)
    p.close()
    p.join()
    

    for i in range(NUM_TASK):
        msg = tasks_that_are_done.get()
        print(msg)
        

if __name__=="__main__":
    main()