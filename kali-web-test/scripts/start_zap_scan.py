def run_scan(target_url):
        """
        Ejecuta una secuencia completa de escaneo en ZAP: Spider + Active Scan.
        """
        if not target_url:
            print("[-] Error: No se proporcionó una URL objetivo.", file=sys.stderr)
            sys.exit(1)
    
        print(f"[*] ========= INICIANDO ESCANEO EN ZAP PARA: {target_url} =========")
    
        try:
            # --- Paso 1: SPIDER (Descubrir el sitio) ---
            print(f"[*] Paso 1/3: Iniciando Spider en {target_url}...")
            spider_scan_id = requests.get(
                f"{ZAP_API_URL}/JSON/spider/action/scan/?url={target_url}"
            ).json()['scan']
    
            # Monitorear el progreso del Spider
            while int(requests.get(f"{ZAP_API_URL}/JSON/spider/view/status/?scanId={spider_scan_id}").json()['status']) < 100:
                progress = requests.get(f"{ZAP_API_URL}/JSON/spider/view/status/?scanId={spider_scan_id}").json()['status']
                print(f"    -> Progreso del Spider: {progress}%")
                time.sleep(5)
            print("[+] Spider completado.")
    
            # Dar tiempo a ZAP para procesar los resultados del spider
            time.sleep(5)
    
            # --- Paso 2: ACTIVE SCAN (Atacar el sitio descubierto) ---
            print(f"[*] Paso 2/3: Iniciando Active Scan en {target_url}...")
            ascan_id = requests.get(
                f"{ZAP_API_URL}/JSON/ascan/action/scan/?url={target_url}&recurse=True"
            ).json()['scan']
    
            # Monitorear el progreso del Active Scan
            while int(requests.get(f"{ZAP_API_URL}/JSON/ascan/view/status/?scanId={ascan_id}").json()['status']) < 100:
                progress = requests.get(f"{ZAP_API_URL}/JSON/ascan/view/status/?scanId={ascan_id}").json()['status']
                print(f"    -> Progreso del Active Scan: {progress}%")
                time.sleep(10)
            print("[+] Active Scan completado.")
    
            # --- Paso 3: Generar Reporte ---
            print("[*] Paso 3/3: Generando reporte...")
            report = requests.get(f"{ZAP_API_URL}/JSON/core/view/alerts/?baseurl={target_url}").json()
            num_alerts = len(report.get('alerts', []))
            print(f"[+] Reporte generado. Se encontraron {num_alerts} alertas.")
    
            print(f"\n✅ ========= ESCANEO COMPLETADO PARA: {target_url} =========\n")
    
        except requests.exceptions.RequestException as e:
            print(f"[-] Error de conexión con la API de ZAP: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyError as e:
            print(f"[-] Error inesperado en la respuesta de la API de ZAP (KeyError: {e}). ¿Está ZAP funcionando correctamente?", file=sys.stderr)
            sys.exit(1)
    
    if __name__ == "__main__":
        # El script espera un argumento desde la línea de comandos: la URL a escanear.
        if len(sys.argv) > 1:
            target = sys.argv[1]
            run_scan(target)
        else:
            print("Uso: python3 /scripts/start_zap_scan.py <URL_OBJETIVO>", file=sys.stderr)
            print("Ejemplo: python3 /scripts/start_zap_scan.py http://dvwa:80", file=sys.stderr)
            sys.exit(1)