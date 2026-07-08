# Objective: Label task objects explicitly to simplify logging and production tracking.
import asyncio
from time import ctime

async def background_worker():
    await asyncio.sleep(0.1)

async def main():
    task = asyncio.create_task(background_worker())
    
    # defalt auto-generated name asigned by python framework
    print(f"{ctime()} Initial Name: {task.get_name()}") # Example: Task-2
    
    # Override name with custom domin 
    task.set_name("Payment-Gateway-Validator")
    print(f"{ctime()} Updated Name: {task.get_name()}") # expected: Payment-Gateway-Validator

asyncio.run(main())