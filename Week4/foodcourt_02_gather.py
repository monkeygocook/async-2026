# foodcourt_02_gather.py
import asyncio
from asyncio import tasks
from time import ctime,time

from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "6710301031"
    print(f"{ctime()} | --- [Task 2] Practice using gather to wait for all grop orders ---")
    start_time = time()
    # 1. Create a list of tasks for ordering different dishes.
    t1 = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice"))
    t2 = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "noodle", "wonton Noodle"))
    t3 = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak"))

    # 2. Use asyncio.gather to wait for all tasks to complete and collect their results.
    results = await asyncio.gather(t1, t2, t3)
    
    # 3. Print the results of all orders.
    for result in results:
        print(f"{ctime()} | System Response: {result}")
    
    end_time = time()
    print(f"{ctime()} | Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())