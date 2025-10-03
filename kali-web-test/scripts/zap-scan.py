#!/usr/bin/env python3

import requests
import time
import json
import sys

ZAP_API = "http://zap:8080"
TARGET = "http://dvwa:80"

def wait_for_zap():
    print("[*] Esperando a que ZAP esté listo...")
    for _ in range(60):
        try:
            res = requests.get(f"{ZAP_API}/JSON/core/view/version")
            if res.status_code == 200:
                print("[+] ZAP está listo")
                return True
        except:
            time.sleep(2)
    return False

def start_scan():
    print(f"[*] Iniciando escaneo en: {TARGET}")
    res = requests.post(f"{ZAP_API}/JSON/ascan/action/scan/", data={
        "url": TARGET
    })
    if res.status_code != 200:
        print("Error al iniciar escaneo")
        return None
    scan_id = res.json().get('scan')
    print(f"[+] Escaneo iniciado con ID: {scan_id}")
    return scan_id

def wait_for_completion(scan_id):
    print("[*] Esperando a que termine el escaneo...")
    while True:
        res = requests.get(f"{ZAP_API}/JSON/ascan/view/status/?scanId={scan_id}")
        status = res.json().get('status', '0')
        print(f"    Progreso: {status}%")
        if int(status) >= 100:
            break
        time.sleep(5)

def get_alerts():
    print("[*] Obteniendo vulnerabilidades...")
    res = requests.get(f"{ZAP_API}/JSON/core/view/alerts/?baseurl={TARGET}")
    alerts = res.json().get('alerts', [])
    return alerts

def save_report(alerts):
    with open("/zap-reports/latest.json", "w") as f:
        json.dump(alerts, f, indent=2)
    print(f"[+] Reporte guardado: {len(alerts)} vulnerabilidades encontradas")

if __name__ == "__main__":
    if wait_for_zap():
        scan_id = start_scan()
        if scan_id:
            wait_for_completion(scan_id)
            alerts = get_alerts()
            save_report(alerts)
            print(f"✅ Escaneo completado. {len(alerts)} vulnerabilidades encontradas.")
    else:
        print("[-] No se pudo conectar a ZAP")
