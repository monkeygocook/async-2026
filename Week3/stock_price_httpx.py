# stock_price_httpx.py
import asyncio
import httpx
from time import ctime

async def fetch_stock_price(server_name: str):
    """
    Assignment 3 - เชื่อมต่อ Mock Server ผ่านระบบเครือข่าย
    ห้ามรับพารามิเตอร์ delay เพราะความหน่วงเกิดขึ้นจริงที่ฝั่ง API Server
    """
    url = f"http://172.16.2.117:8088/price/{server_name}"

    # ใช้ async with เพื่อดึงข้อมูลแบบไม่ Block Event Loop
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return f"[{data['server']}] Price: {data['price_usd']} USD"

async def main():
    # แปลงคอรูทีนทั้ง 3 สาขาให้เป็น asyncio.Task ส่งเข้าคิวรันพร้อมกันใน Event Loop
    tasks = [
        asyncio.create_task(fetch_stock_price("Alpha")),
        asyncio.create_task(fetch_stock_price("Beta")),
        asyncio.create_task(fetch_stock_price("Gamma")),
    ]

    # Concurrency Racing: ดีดตัวหลุดจากการรอทันทีเมื่อเซิร์ฟเวอร์ตัวแรกตอบกลับสำเร็จ
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # ดึงผลลัพธ์จากเซิร์ฟเวอร์ที่ชนะการแข่งขัน (ตัวที่เร็วที่สุด)
    for task in done:
        print(f"{ctime()} Winner Result: {task.result()}")

    # [Anti-Memory Leak] วนลูปยกเลิกงานที่ยังค้างคาในเซต pending
    # เพื่อตัดสัญญาณ Network Request ที่ยังวิ่งค้างอยู่บนเครือข่าย
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
    for task in pending:
        task.cancel()

    # รอให้การยกเลิกประมวลผลจนจบ ก่อนปิดโปรแกรม
    await asyncio.gather(*pending, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())