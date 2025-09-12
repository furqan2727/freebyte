import os
import time
from colorama import Fore, Style, init

# Colorama başlat
init(autoreset=True)

def banner():
    print(Fore.CYAN + Style.BRIGHT + "="*40)
    print(Fore.GREEN + Style.BRIGHT + "   🚀  FreeByteTool Başlatıcıya Hoşgeldin 🚀")
    print(Fore.CYAN + Style.BRIGHT + "="*40)

def menu():
    print(Fore.YELLOW + Style.BRIGHT + "\nLütfen bir versiyon seç:")
    print(Fore.MAGENTA + Style.BRIGHT + "1) MANUEL")
    print(Fore.MAGENTA + Style.BRIGHT +  "2) OTOMATİK")
    print(Fore.RED + Style.BRIGHT +  "0) Çıkış\n")

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        banner()
        menu()
        secim = input(Fore.CYAN + Style.BRIGHT +  "👉 Seçiminizi yapın (1/2/0): ")

        if secim == "1":
            print(Fore.GREEN + "\n[+] FreeByteTool v3 başlatılıyor...\n")
            time.sleep(1)
            os.system("python freebyteV3.py")
            break
        elif secim == "2":
            print(Fore.GREEN + "\n[+] FreeByteTool v5 başlatılıyor...\n")
            time.sleep(1)
            os.system("python freebyteV5.py")
            break
        elif secim == "0":
            print(Fore.RED + "\n[-] Çıkış yapılıyor...")
            break
        else:
            print(Fore.RED + "\n[!] Geçersiz seçim, tekrar dene!")
            time.sleep(1.5)

if __name__ == "__main__":
    main()
