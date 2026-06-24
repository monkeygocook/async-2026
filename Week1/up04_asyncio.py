import asyncio
from time import sleep, ctime, time

async def update_cup_number(customer_name):
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    await asyncio.sleep(1) # บล็อกการทำงานของ Thread นี้ไว้ 5 วินาทีเต็มๆ
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

async def make_coffee(customer_name):
    print(f"{ctime()} | Making coffee for {customer_name}...")
    await asyncio.sleep(1) # บล็อกการทำงานของ Thread นี้ไว้ 5 วินาทีเต็มๆ
    print(f"{ctime()} | Coffee ready for {customer_name}!")
    await update_cup_number(customer_name)

async def main():
    queue = ['A', 'B', 'C']

    
    print(f"{ctime()} | === asyncio Coffee Machine === ")
    start_time = time()
    
    tasks = []
    for customer in queue:
        # สร้าง Coroutine
        coro = make_coffee(customer)
        # แปลง Coroutine ให้เป็น Task เพื่อให้ Event Loop บริหาร และตั้งชื่อได้
        task = asyncio.create_task(coro, name=f"Task-{customer}")
        tasks.append(task)
        
    # สั่งให้ทำพร้อมกัน
    await asyncio.gather(*tasks)
    
    duration = time() - start_time
    print(f"{ctime()} | total time: {duration:0.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())