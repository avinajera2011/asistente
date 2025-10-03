
async function startScan() {
    const btn = document.getElementById("scanBtn");
    const log = document.getElementById("scanLog");
    btn.disabled = true;
    btn.innerText = "Escaneando... (ver logs)";

    log.innerHTML = "<p>🚀 Iniciando escaneo con ZAP...</p>";

    try {
        const res = await fetch('/api/start-scan', {
            method: 'POST'
        });

        if (res.ok) {
            const reader = res.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                const text = decoder.decode(value);
                const lines = text.split('\n').filter(l => l.trim());
                lines.forEach(line => {
                    log.innerHTML += `<p>> ${line}</p>`;
                });
                log.scrollTop = log.scrollHeight;
            }
        } else {
            log.innerHTML += `<p style="color: red;">Error: ${res.status}</p>`;
        }
    } catch (e) {
        log.innerHTML += `<p style="color: red;">Error: ${e.message}</p>`;
    } finally {
        btn.disabled = false;
        btn.innerText = "Iniciar Escaneo ZAP";
    }
}
