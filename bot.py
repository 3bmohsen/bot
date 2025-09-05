import requests
import time

url = "https://tms.tabadul.sa/api/appointment/tas/v2/zone/schedule/land"
params = {
    "departure": "KFC",
    "arrival": "31",
    "type": "TRANSIT",
    "economicOperator": ""
}

headers = {
    "Accept": "application/json",
    "Accept-Language": "ar",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json; charset=utf-8",
    "Origin": "https://oga.fasah.sa",
    "Pragma": "no-cache",
    "Referer": "https://oga.fasah.sa/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "token": f"Bearer {os.getenv('token')}"
}

while True:
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        print("Status:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            print("Response data:", data)

            # لو الرسالة بتقول "لا يوجد مواعيد متاحة" → كمل
            if (
                not data.get("success")
                and data.get("errors")
                and data["errors"][0].get("message") == "لا يوجد مواعيد متاحة"
            ):
                print("⚠️ مفيش مواعيد متاحة، هنجرب تاني بعد دقيقة...")
            
            else:
                # أي رد غير كده يبقى نجحنا
                print("✅ لقيت رد مختلف، وقفنا التكرار.")
                print("Final data:", data)
                break
        else:
            print("❌ Error:", response.text)

    except Exception as e:
        print("Error:", e)

    time.sleep(60)  # انتظر دقيقة

