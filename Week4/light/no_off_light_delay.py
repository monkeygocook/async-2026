"""
สคริปต์ควบคุมไฟ Smart Lab Lighting System
  กด 1 = เปิดไฟทั้ง 4 ดวง (พร้อมกันแบบ async)
  กด 0 = ปิดไฟทั้ง 4 ดวง (พร้อมกันแบบ async)

วิธีติดตั้ง dependency:
    pip install httpx

วิธีรัน:
    python light_control.py
"""

import asyncio
import time

import httpx

# ---------- ค่าตั้งต้น ----------
BASE_URL = "http://172.16.2.117:8088"
STUDENT_ID = "6710301031"  # แก้เป็นรหัสนักศึกษาของตัวเอง

LIGHT_IDS = ["light_1", "light_2", "light_3", "light_4"]


async def set_light(client: httpx.AsyncClient, light_id: str, status: str) -> dict:
    """สั่งเปิด/ปิดไฟ 1 ดวง ผ่าน POST /api/{student_id}/lights/{light_id}"""
    url = f"{BASE_URL}/api/{STUDENT_ID}/lights/{light_id}"
    start = time.perf_counter()

    resp = await client.post(url, json={"status": status}, timeout=10.0)
    resp.raise_for_status()

    elapsed = time.perf_counter() - start
    data = resp.json()
    print(f"✅ {light_id} -> {data['current_status']} (ใช้เวลา {elapsed:.2f} วิ)")
    return data


async def set_all_lights(client: httpx.AsyncClient, status: str) -> None:
    """สั่งไฟทั้ง 4 ดวงพร้อมกันด้วย asyncio.gather"""
    action = "เปิด" if status == "ON" else "ปิด"
    print(f"\n🚀 กำลังสั่ง{action}ไฟทั้ง {len(LIGHT_IDS)} ดวงพร้อมกัน...\n")
    start = time.perf_counter()

    results = await asyncio.gather(
        *(set_light(client, light_id, status) for light_id in LIGHT_IDS),
        return_exceptions=True,
    )

    total = time.perf_counter() - start
    print(f"\n⏱️ เวลารวมทั้งหมด: {total:.2f} วินาที")

    # แจ้ง error ถ้ามีดวงไหนล้มเหลว
    for light_id, result in zip(LIGHT_IDS, results):
        if isinstance(result, Exception):
            print(f"❌ {light_id} ล้มเหลว: {result}")


async def main() -> None:
    async with httpx.AsyncClient() as client:
        print("=" * 50)
        print("💡 Smart Lab Lighting System")
        print(f"   Student ID: {STUDENT_ID}")
        print("=" * 50)

        while True:
            print("\n[1] เปิดไฟทั้งหมด  [0] ปิดไฟทั้งหมด")
            choice = input("เลือกคำสั่ง: ").strip()

            try:
                if choice == "1":
                    await set_all_lights(client, "ON")
                elif choice == "0":
                    await set_all_lights(client, "OFF")
                else:
                    print("⚠️ กรุณากด 1 หรือ 0 เท่านั้น")
            except httpx.ConnectError:
                print(f"❌ ต่อเซิร์ฟเวอร์ {BASE_URL} ไม่ได้ ตรวจสอบว่าเซิร์ฟเวอร์รันอยู่")
            except httpx.HTTPStatusError as e:
                print(f"❌ เซิร์ฟเวอร์ตอบกลับ error: {e.response.status_code} - {e.response.text}")


if __name__ == "__main__":
    asyncio.run(main())