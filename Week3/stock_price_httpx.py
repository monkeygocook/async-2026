# stock_price_httpx.py
import asyncio
import httpx
from time import ctime

BASE_URL = "http://127.0.0.1:8088"       # ทดสอบที่บ้านกับ mock server
# BASE_URL = "http://172.16.2.117:8088"  # สลับมาใช้อันนี้ตอนอยู่ในแลป/ส่งงาน


async def fetch_stock_price(server_name: str):
    """เชื่อมต่อ Mock Server ผ่าน httpx.AsyncClient เพื่อไม่ Block Event Loop"""
    url = f"{BASE_URL}/price/{server_name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        data = response.json()
        return f"[{data['server']}] Price: {data['price_usd']} USD"


async def main():
    tasks = [
        asyncio.create_task(fetch_stock_price("Alpha")),
        asyncio.create_task(fetch_stock_price("Beta")),
        asyncio.create_task(fetch_stock_price("Gamma")),
    ]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    winner = done.pop()
    print(f"{ctime()} Winner Result: {winner.result()}")

    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())