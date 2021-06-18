'''
'''

import threading
import time
import asyncio
import concurrent.futures
import requests

MAX_WORKERS = 4
_shutdown = False

def process_task(ind):
    print(f"Thread {threading.current_thread().name}: Starting task: {ind}...")
    
    resp = requests.post("https://httpbin.org/post", data={'key':'value'})
    print(f"Received response: {resp.json()}")

    if ind == 2:
        print("BOOM!")
        raise Exception("BOOM!")
    
    print(f"Thread {threading.current_thread().name}: Finished task: {ind}!")
    return ind

async def main(tasks=20):
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        loop = asyncio.get_running_loop()
        futures = [
            loop.run_in_executor(pool, process_task, task) for task in range(tasks)
        ]
        try:
            results = await asyncio.gather(*futures, return_exceptions=False)
        except Exception as ex:
            print("Caught error executing task", ex)
            _shutdown = True
            raise
    print(f"Finished processing, got results: {results}")


asyncio.run(main()) # run co-routine called "main" using event-loop
    




