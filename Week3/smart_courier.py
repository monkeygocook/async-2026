# Delivery System): นักศึกษาต้องเขียน try...except CancelledError ได้ถูกต้อง 
# และใช้ .get_name(), .cancel(), และ .cancelled() ได้
import asyncio
from time import ctime

async def delivery_task(package_id, duration):
    try:
        print(f"{ctime()} Courier started delivering {package_id}...")
        await asyncio.sleep(duration)
        print(f"{ctime()} Courier: Package {package_id} Delivered!")
    except asyncio.CancelledError:
        print(f"{ctime()} Delivery Canceled! Returning package to warehouse.")
        raise  # Re-raise the exception to propagate cancellation

async def main():
    # Create a list of delivery tasks with varying durations
    tasks = [
        asyncio.create_task(delivery_task("P001", 5), name="Express-Courier"),
    ]

    # Run the event loop and cancel one of the tasks after a short delay
    await asyncio.sleep(2)  # Wait for a moment before cancelling
    print(f"{ctime()} Check task '{tasks[0].get_name()}'. It is done? {tasks[0].done()}")
    tasks[0].cancel()  # Cancel the first task
    print(f"{ctime()} Taking too long! Canceling task...")
    await asyncio.gather(*tasks, return_exceptions=True)
    print(f"{ctime()} Final verify: It task officially canceled? {tasks[0].cancelled()}")

        # Wait for all tasks to complete or be cancelled
    

if __name__ == "__main__":
    asyncio.run(main())