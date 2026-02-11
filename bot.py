import os
import sys
import asyncio
from datetime import date
import pytz
from telegram import Bot

turkey_tz = pytz.timezone("Europe/Istanbul")
TOKEN = os.environ["TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])

TYT_TARIHI = date(2026, 6, 20)
AYT_TARIHI = date(2026, 6, 21)
YKS_TARIHI = date(2026, 6, 20)

bot = Bot(token=TOKEN)

def bugun_tipi():
    b = date.today()
    if b < TYT_TARIHI:
        return "KAMP"
    elif b == TYT_TARIHI:
        return "TYT"
    elif b == AYT_TARIHI:
        return "AYT"
    else:
        return "BITTI"

def kalan_gun():
    return (YKS_TARIHI - date.today()).days

async def main():
    tip = bugun_tipi()
    saat = sys.argv[1]

    if saat == "0700":
        if tip == "KAMP":
            await bot.send_message(chat_id=CHAT_ID, text=(
                f"📅 YKS'ye {kalan_gun()} gün kaldı\n\n"
                "⏰ 07.00\n\nAsım için kalkış zamanı.\n"
                "Bugün kütüphaneye gidebilmesi için kaldırılması gerekiyor."
            ))
        elif tip == "TYT":
            await bot.send_message(chat_id=CHAT_ID, text=(
                "📝 BUGÜN YKS (TYT) GÜNÜ\n\n"
                "• Kimlik hazır mı?\n• Sınav giriş belgesi hazır mı?\n• Su hazır mı?\n\n"
                "Sakin ol. Acele yok."
            ))
        elif tip == "AYT":
            await bot.send_message(chat_id=CHAT_ID, text=(
                "📝 BUGÜN YKS (AYT) GÜNÜ\n\n"
                "• Kimlik yanında mı?\n• Giriş belgesi yanında mı?\n• Su hazır mı?\n\n"
                "Elinden geleni yaptın."
            ))

    elif saat == "0750" and tip == "KAMP":
        await bot.send_message(chat_id=CHAT_ID, text="🚪 07.50\nAsım en geç 08.00'de evden çıkmış olmalı.")
    elif saat == "0800" and tip == "KAMP":
        await bot.send_message(chat_id=CHAT_ID, text="🚨 08.00\nHemen çıkması gerekiyor.")
    elif saat == "1930" and tip == "KAMP":
        await bot.send_message(chat_id=CHAT_ID, text="⛔ 19.30\n20.00'den önce eve gelirse ödül yok.")
    elif saat == "2000" and tip == "KAMP":
        await bot.send_message(chat_id=CHAT_ID, text="✅ 20.00\nGeldiyse: ODA KİLİTLİ / ÖDÜL YOK")
    elif saat == "2330" and tip == "KAMP":
        await bot.send_message(chat_id=CHAT_ID, text="😴 23.30\nTelefon oturma odasında.")

asyncio.run(main())
