import asyncio
from time import time, ctime
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "6710301049"
    print(f"{ctime()} | --- [Task 2] Practice using gather to wait for all group orders ---")
    start_time = time()

    # 1. Create a list of tasks for ordering different food items.
    t1 = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice"))
    t2 = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles"))
    t3 = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak"))

    # 2. Use asyncio.gather to run all tasks concurrently and wait for their completion.
    results = await asyncio.gather(t1, t2, t3)

    # 3. Print the results of all orders once they are completed.
    for dish in results:
        print(f"{ctime()} | [Pickup] Shop: {dish['shop']} | Menu: {dish['menu']} is ready!")

    print(f"{ctime()} | Total elapsed time: {time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())