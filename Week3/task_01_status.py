# Objective: Learn how to query the lifecycle status of a task object.
import asyncio
from time import ctime

async def short_job():
    await asyncio.sleep(1)
    return "Success"

async def main():
    task = asyncio.create_task(short_job())
    
    # Query the task's status
    print(f"{ctime()} Is task done? {task.done()}")          # Check if the task is done
    print(f"{ctime()} Is task canceled? {task.cancelled()}")  # Check if the task is canceled
    
    await task # Wait for the task to complete
    
    # Inspect status again after it finishes
    print(f"{ctime()} Is task done now? {task.done()}")      # 
    print(f"{ctime()} Is task canceled now? {task.cancelled()}") # 

asyncio.run(main())