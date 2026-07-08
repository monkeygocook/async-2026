# นักเรียนต้องเลือกใช้ asyncio.wait() พร้อมออปชัน return_when=asyncio.FIRST_COMPLETED เท่านั้น (หากใครใช้ gather หรือ wait_for จะไม่ตรงสเปกเงื่อนไขการแข่งส่งข้อมูล)
# Assignment 2: The Stock Price Race (ระบบแข่งดึงข้อมูลราคาหุ้น)
import asyncio
from time import ctime

# Coroutine function สำหรับดึงราคาหุ้นจากเซิร์ฟเวอร์
async def fetch_stock_price(server_name, delay):
    await asyncio.sleep(delay)  # จำลองความหน่วงของอินเทอร์เน็ต
    return f"[{server_name}] Price: 150 USD"

async def main():
    # แตก Task 3 ตัวพร้อมกันใน Event Loop
    tasks = [
        asyncio.create_task(fetch_stock_price("Alpha", 3.0)),
        asyncio.create_task(fetch_stock_price("Beta", 0.8)),
        asyncio.create_task(fetch_stock_price("Gamma", 1.5)),
    ]

    # ใช้ asyncio.wait() แบบ FIRST_COMPLETED
    # ระบบจะตัดตัวหลุดจากการรอทันทีเมื่อเซิร์ฟเวอร์ตัวแรกส่งข้อมูลสำเร็จ
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # แสดงผลลัพธ์ของเซิร์ฟเวอร์ที่ชนะ (ตัวที่เร็วที่สุด)
    for task in done:
        print(f"{ctime()} Winner Result: {task.result()}")

    # วนลูปเคลียร์ระบบ: สั่งยกเลิก Task ที่ยังค้างอยู่ทั้งหมด
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
    for task in pending:
        task.cancel()

    # รอให้การ cancel เสร็จสมบูรณ์ ป้องกัน Memory Leak / warning ค้าง
    await asyncio.gather(*pending, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())