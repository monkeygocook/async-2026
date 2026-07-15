# Objective: Stop an ongoing execution prematurely by triggering a cancellation exception.
import asyncio
from time import ctime

async def background_loop():
    try:
        print(f"{ctime()} Worker: Starting long infinite process...")
        while True:
            await asyncio.sleep(1)
            print(f"{ctime()} Worker: Still ticking...")
    except asyncio.CancelledError:
        # act as a signal to perform any necessary clean-up before the task is fully canceled
        print(f"{ctime()} Worker: Interrupted! Executing clean-up logic before exit...")

async def main():
    task = asyncio.create_task(background_loop())
    await asyncio.sleep(2.5) # await for a while before canceling the task
    
    print(f"{ctime()} Main: Changing plans, canceling the worker task now!")
    task.cancel() # 
    await asyncio.sleep(0.1) # await for a moment to let the cancellation propagate

asyncio.run(main())