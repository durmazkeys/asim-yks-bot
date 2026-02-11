import os
from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import date

# === ORTAM DEĞİŞKENLERİNDEN OKU ===
TOKEN = os.environ["TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])

# === TARİHLER ===
YKS_TARIHI = date(2026, 6, 20)   # TYT günü esas
TYT_TARIHI = date(2026, 6, 20)
AYT_TARIHI = date(2026, 6, 21)

scheduler = AsyncIOScheduler()

async def gonder(bot, text):
    await bot.send_message(chat_id=CHAT_ID, text=text)

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

async def sabah_mesaji(app):
    tip = bugun_tipi()

    if tip == "KAMP":
        mesaj = (
            f"📅 YKS’ye {kalan_gun()} gün kaldı\n\n"
            "⏰ 07.00\n\n"
            "Asım için kalkış zamanı.\n"
            "Bugün kütüphaneye gidebilmesi için kaldırılması gerekiyor."
        )
    elif tip == "TYT":
        mesaj = (
            "📝 BUGÜN YKS (TYT) GÜNÜ\n\n"
            "• Kimlik hazır mı?\n"
            "• Sınav giriş belgesi hazır mı?\n"
            "• Su hazır mı?\n\n"
            "Sakin olun. Acele yok."
        )
    elif tip == "AYT":
        mesaj = (
            "📝 BUGÜN YKS (AYT) GÜNÜ\n\n"
            "• Kimlik yanında mı?\n"
            "• Giriş belgesi yanında mı?\n"
            "• Su hazır mı?\n\n"
            "Elinden geleni yaptı."
        )
    else:
        return  # sınavlardan sonra TAM SESSİZLİK

    await gonder(app.bot, mesaj)

async def start(app):

    # 07.00 – sabah mesajı
    scheduler.add_job(
        sabah_mesaji,
        "cron",
        hour=7,
        minute=0,
        args=[app]
    )

    async def kamp(text):
        if bugun_tipi() == "KAMP":
            await gonder(app.bot, text)

    scheduler.add_job(
        kamp,
        "cron",
        hour=7,
        minute=50,
        args=["🚪 07.50\nAsım en geç 08.00’de evden çıkmış olmalı."]
    )

    scheduler.add_job(
        kamp,
        "cron",
        hour=8,
        minute=0,
        args=["🚨 08.00\nHemen çıkması gerekiyor."]
    )

    scheduler.add_job(
        kamp,
        "cron",
        hour=19,
        minute=30,
        args=["⛔ 19.30\n20.00’den önce eve gelirse ödül yok."]
    )

    scheduler.add_job(
        kamp,
        "cron",
        hour=20,
        minute=0,
        args=["✅ 20.00\nGeldiyse: ODA KİLİTLİ / ÖDÜL YOK"]
    )

    scheduler.add_job(
        kamp,
        "cron",
        hour=23,
        minute=30,
        args=["😴 23.30\nTelefon oturma odasında."]
    )

    scheduler.start()

app = ApplicationBuilder().token(TOKEN).post_init(start).build()
print("Asım YKS botu aktif.")
app.run_polling()
