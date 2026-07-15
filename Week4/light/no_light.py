"""
สคริปต์เปิดไฟทั้ง 4 ดวงของ Smart Lab Lighting System
ใช้ asyncio + httpx เพื่อสั่งเปิดไฟ "พร้อมกัน" (concurrent)
=> ใช้เวลารวมแค่ ~2.0 วินาที (ดวงที่ช้าที่สุด) แทนที่จะเป็น 4.5 วินาที

วิธีติดตั้ง dependency:
    pip install httpx

วิธีรัน:
    python turn_on_lights.py
"""

import asyncio
import time

import httpx

# ---------- ค่าตั้งต้น ----------
BASE_URL = "http://172.16.2.117:8088"
STUDENT_ID = "6710301031"  # แก้เป็นรหัสนักศึกษาของตัวเอง

LIGHT_IDS = ["light_1", "light_2", "light_3", "light_4"]


async def turn_on_light(client: httpx.AsyncClient, light_id: str) -> dict:
    """สั่งเปิดไฟ 1 ดวง ผ่าน POST /api/{student_id}/lights/{light_id}"""
    url = f"{BASE_URL}/api/{STUDENT_ID}/lights/{light_id}"
    start = time.perf_counter()

    resp = await client.post(url, json={"status": "ON"}, timeout=10.0)
    resp.raise_for_status()

    elapsed = time.perf_counter() - start
    data = resp.json()
    print(f"✅ {light_id} -> {data['current_status']} (ใช้เวลา {elapsed:.2f} วิ)")
    return data


async def get_all_status(client: httpx.AsyncClient) -> dict:
    """ดึงสถานะไฟทั้งหมด ผ่าน GET /api/{student_id}/lights"""
    url = f"{BASE_URL}/api/{STUDENT_ID}/lights"
    resp = await client.get(url, headers={"Accept": "application/json"})
    resp.raise_for_status()
    return resp.json()


async def main() -> None:
    async with httpx.AsyncClient() as client:
        print(f"🚀 กำลังสั่งเปิดไฟทั้ง {len(LIGHT_IDS)} ดวงพร้อมกัน...\n")
        start = time.perf_counter()

        # ยิง request ทั้ง 4 ดวงพร้อมกันด้วย asyncio.gather
        results = await asyncio.gather(
            *(turn_on_light(client, light_id) for light_id in LIGHT_IDS),
            return_exceptions=True,
        )

        total = time.perf_counter() - start
        print(f"\n⏱️ เวลารวมทั้งหมด: {total:.2f} วินาที")

        # แจ้ง error ถ้ามีดวงไหนล้มเหลว
        for light_id, result in zip(LIGHT_IDS, results):
            if isinstance(result, Exception):
                print(f"❌ {light_id} ล้มเหลว: {result}")

        # ตรวจสอบสถานะสุดท้ายของไฟทุกดวง
        print("\n📋 สถานะไฟปัจจุบัน:")
        status = await get_all_status(client)
        for light_id, info in status.items():
            icon = "💡" if info["status"] == "ON" else "⚫"
            print(f"  {icon} {info['name']}: {info['status']} (delay {info['delay']} วิ)")


if __name__ == "__main__":
    asyncio.run(main())