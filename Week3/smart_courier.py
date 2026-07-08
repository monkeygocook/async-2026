# Assignment 1: The Smart Courier System (ระบบส่งพัสดุด่วน)
import asyncio
from time import ctime

# ข้อ 1: Coroutine function จำลองการส่งพัสดุ
async def delivery_task(package_id, duration):
    try:
        print(f"{ctime()} Courier started delivering {package_id}...")
        await asyncio.sleep(duration)
        return f"Package {package_id} Delivered!"
    except asyncio.CancelledError:
        # ข้อ 5: ดักจับการยกเลิกในตัวคอรูทีนส่งของ
        print(f"{ctime()} Delivery Canceled! Returning package to warehouse.")
        raise  # ส่งต่อ exception เพื่อให้สถานะ Task เป็น cancelled จริง

async def main():
    # ข้อ 2: สร้าง Task 1 ตัว พร้อมตั้งชื่อว่า Express-Courier
    task = asyncio.create_task(
        delivery_task("P001", 5.0),
        name="Express-Courier"
    )

    # ข้อ 3: ระหว่างพัสดุกำลังเดินทาง (ผ่านไป 2 วินาที) ตรวจสอบสถานะ
    await asyncio.sleep(2)
    print(f"{ctime()} Checking task '{task.get_name()}'... Is it done? {task.done()}")

    # ข้อ 4: ผ่านไป 2 วินาทีแล้วยังไม่เสร็จ → ยกเลิกงานทันที
    if not task.done():
        print(f"{ctime()} Taking too long! Cancelling the task...")
        task.cancel()

    # รอให้การยกเลิกประมวลผลจนจบ
    try:
        await task
    except asyncio.CancelledError:
        pass  # ข้อความถูกพิมพ์ในตัวคอรูทีนแล้ว

    # ข้อ 5: ตรวจสอบสถานะจากภายนอกด้วย .cancelled()
    print(f"{ctime()} Final verify: Is task officially canceled? {task.cancelled()}")

if __name__ == "__main__":
    asyncio.run(main())