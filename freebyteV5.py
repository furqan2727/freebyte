import requests, json, time, hashlib, os, sys, webbrowser
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

RENK_LOGO = Fore.MAGENTA + Style.BRIGHT
RENK_YESIL = Fore.GREEN + Style.BRIGHT
RENK_KIRMIZI = Fore.RED + Style.BRIGHT
RENK_SARI = Fore.YELLOW + Style.BRIGHT
RENK_MAVI = Fore.CYAN + Style.BRIGHT
RENK_GRI = Fore.LIGHTBLACK_EX

# Global sayaç
toplam_freebyte = 0  

def input_renkli(mesaj):
    sys.stdout.write(RENK_SARI + mesaj)
    sys.stdout.flush()
    return input(RENK_MAVI).strip()

def temizle():
    os.system("cls" if os.name == "nt" else "clear")

def logo_goster():
    temizle()
    pass
    logo = pyfiglet.figlet_format("FREEBYTE", font="slant")
    print(RENK_LOGO + logo.rstrip())
    son = logo.splitlines()[-1]
    print(" " * (len(son) - len(son.lstrip())) + RENK_SARI + "@freebyteV5")
    print(RENK_MAVI + "=" * 60)
    print(RENK_MAVI + "1GB App FreeByte V5".center(60))
    print(RENK_MAVI + "=" * 60)

def generate_hash(transactionId):
    secret = "6a5de8a0a5f0ec70ee254b2046"
    return hashlib.md5((transactionId + secret).encode()).hexdigest()

def odul_al(token):
    try:
        url = "https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com/api/user/check-in"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://1gb.app"
        }
        r = requests.post(url, json={"etkAccepted": False}, headers=headers)
        if r.status_code == 200:
            print(RENK_YESIL + "[🎁] Giriş ödülü alındı!")
        else:
            print(RENK_KIRMIZI + f"[⚠️] Ödül alınamadı! ({r.status_code})")
            print(r.text)
    except Exception as e:
        print(RENK_KIRMIZI + f"[HATA] Ödül işlemi: {e}")

def reklam_gonder(token):
    global toplam_freebyte
    try:
        start_url = "https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com/api/admob/start"
        finish_url = "https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com/api/admob/finish"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "x-client-device": "ANDROID",
            "User-Agent": "okhttp/4.12.0"
        }
        r_start = requests.post(start_url, json={}, headers=headers)
        if r_start.status_code == 200 and "transactionId" in r_start.json():
            tid = r_start.json()["transactionId"]
            print(RENK_MAVI + f"[▶️] Reklam başlatıldı - ID: {tid}")
            hash_ = generate_hash(tid)
            time.sleep(2)
            r_finish = requests.post(finish_url, json={"transactionId": tid, "hash": hash_}, headers=headers)
            if r_finish.status_code == 200:
                toplam_freebyte += 10
                print(RENK_YESIL + f"[✅] Reklam tamamlandı. +10 FreeByte eklendi! (Toplam: {toplam_freebyte})")
            else:
                print(RENK_KIRMIZI + f"[❌] Finish hatası: {r_finish.status_code}")
                print(r_finish.text)
        elif r_start.status_code == 400 and "daily_limit_reached" in r_start.text:
            print(RENK_SARI + "[🚫] Günlük limit dolmuş!")
        else:
            print(RENK_KIRMIZI + f"[❌] Start hatası: {r_start.status_code}")
            print(r_start.text)
    except Exception as e:
        print(RENK_KIRMIZI + f"[HATA] Reklam gönderme: {e}")

def coklu_reklam(token, tekrar=10, bekle=1):
    for i in range(tekrar):
        print(RENK_MAVI + f"\n🔁 {i+1}. reklam başlatılıyor...")
        reklam_gonder(token)
        time.sleep(bekle)
    print(RENK_YESIL + f"\n🎉 Toplam kazanılan FreeByte: {toplam_freebyte}")

def giris_menusu(msisdn, token):
    odul_al(token)
    while True:
        secim = "2"
        if secim == "1":
            reklam_gonder(token)
        elif secim == "2":
            try:
                adet = 5
                coklu_reklam(token, tekrar=adet)
                break
            except:
                print(RENK_KIRMIZI + "[⚠️] Sayı girişi hatalı!")
        elif secim == "3":
            print(RENK_YESIL + "👋 Çıkış yapılıyor. Görüşmek üzere!")
            break
        else:
            print(RENK_KIRMIZI + "[❌] Geçersiz seçim!")

def manuel_pin_giris(msisdn):
    url = "https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com/api/auth/pin/verify"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "okhttp/4.12.0"
    }
    pin = input_renkli("[🔐] PIN kodunu girin: ")
    data = {
        "msisdn": msisdn,
        "osType": "ANDROID",
        "pin": pin
    }
    try:
        r = requests.post(url, json=data, headers=headers)
        js = r.json()
        if "token" in js:
            print(RENK_YESIL + "[✅] PIN doğrulandı, giriş başarılı!")
            giris_menusu(msisdn, js["token"])
        else:
            print(RENK_KIRMIZI + f"[❌] PIN hatalı: {js.get('message', 'Bilinmeyen hata')}")
    except Exception as e:
        print(RENK_KIRMIZI + f"[HATA] PIN doğrulama: {e}")

def otomatik_hesap_giris(dosya="accounts.txt"):
    try:
        with open(dosya, "r", encoding="utf-8") as f:
            hesaplar = [satir.strip() for satir in f if satir.strip()]
    except FileNotFoundError:
        print(RENK_KIRMIZI + f"[❌] {dosya} bulunamadı!")
        return

    for i, hesap in enumerate(hesaplar, start=1):
        try:
            msisdn, pin = hesap.split(":")
        except:
            print(RENK_KIRMIZI + f"[⚠️] Hatalı satır: {hesap}")
            continue

        print(RENK_MAVI + f"\n📱 {i}. hesap deneniyor: {msisdn}")
        url = "https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com/api/auth/pin/verify"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "okhttp/4.12.0"
        }
        data = {
            "msisdn": msisdn,
            "osType": "ANDROID",
            "pin": pin
        }

        try:
            r = requests.post(url, json=data, headers=headers)
            js = r.json()
            if "token" in js:
                print(RENK_YESIL + "[✅] Giriş başarılı!")
                giris_menusu(msisdn, js["token"])
            else:
                print(RENK_KIRMIZI + f"[❌] PIN hatalı: {js.get('message', 'Bilinmeyen hata')}")
        except Exception as e:
            print(RENK_KIRMIZI + f"[HATA] PIN doğrulama: {e}")

if __name__ == "__main__":
    logo_goster()
    otomatik_hesap_giris(".accounts.txt")
