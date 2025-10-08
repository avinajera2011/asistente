#!/usr/bin/env python3

import requests
import time
import json
import sys

ZAP_API = "http://zap:8080"
TARGET = "http://dvwa:80"

def wait_for_zap():
    """Espera un máximo de 2 minutos a que la API de ZAP esté disponible."""
    print("[*] Esperando a que ZAP esté listo...")
    for _ in range(60): # 60 intentos de 2 segundos = 120 segundos
        try:
            res = requests.get(f"{ZAP_API}/JSON/core/view/version")
            if res.status_code == 200:
                print("[+] ZAP está listo y operativo.")
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(2)
    print("[-] Error: ZAP no estuvo disponible después de 2 minutos.")
    return False

def start_scan():
    """Inicia un escaneo activo contra el objetivo definido."""
    print(f"[*] Iniciando escaneo activo en el objetivo: {TARGET}")
    try:
        res = requests.post(f"{ZAP_API}/JSON/ascan/action/scan/", data={
            "url": TARGET
        })
        res.raise_for_status() # Lanza un error si el código no es 2xx
        scan_id = res.json().get('scan')
        print(f"[+] Escaneo iniciado con éxito. ID de escaneo: {scan_id}")
        return scan_id
    except requests.exceptions.RequestException as e:
        print(f"[-] Error crítico al iniciar el escaneo: {e}")
        return None

def wait_for_completion(scan_id):
    """Verifica el progreso del escaneo y espera a que alcance el 100%."""
    print("[*] Monitoreando el progreso del escaneo...")
    while True:
        try:
            res = requests.get(f"{ZAP_API}/JSON/ascan/view/status/?scanId={scan_id}")
            res.raise_for_status()
            status = res.json().get('status', '0')
            print(f"    Progreso del escaneo: {status}%")
            if int(status) >= 100:
                break
            time.sleep(10) # Aumentamos el intervalo para no saturar la API
        except requests.exceptions.RequestException as e:
            print(f"[-] Advertencia: No se pudo obtener el estado del escaneo. Reintentando... ({e})")
            time.sleep(10)

def save_report():
    """Obtiene las alertas y las guarda en un archivo JSON."""
    print("[*] Obteniendo vulnerabilidades encontradas...")
    try:
        res = requests.get(f"{ZAP_API}/JSON/core/view/alerts/?baseurl={TARGET}")
        res.raise_for_status()
        alerts = res.json().get('alerts', [])
        
        report_path = "/zap-reports/latest_scan_report.json"
        with open(report_path, "w") as f:
            json.dump(alerts, f, indent=4)
        
        print(f"[+] Reporte guardado en {report_path}. Se encontraron {len(alerts)} vulnerabilidades.")
        return len(alerts)
    except requests.exceptions.RequestException as e:
        print(f"[-] Error crítico al generar el reporte: {e}")
        return 0

if __name__ == "__main__":
    if wait_for_zap():
        scan_id = start_scan()
        if scan_id:
            wait_for_completion(scan_id)
            num_alerts = save_report()
            print(f"✅ Escaneo completado. Total de vulnerabilidades: {num_alerts}.")
            # El contenedor terminará aquí exitosamente
    else:
        print("[-] Abortando el proceso de escaneo.")
        sys.exit(1) # Salir con código de error