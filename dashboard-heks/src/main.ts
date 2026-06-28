async function fetchQuantumTelemetry() {
  try {
    const response = await fetch('http://localhost:8080/');
    if (!response.ok) throw new Error('Falha no barramento.');
    
    const data = await response.json();
    
    document.getElementById('node-id')!.innerText = data.node_id;
    document.getElementById('load')!.innerText = `${data.load}%`;
    document.getElementById('thermal')!.innerText = `${data.thermal}°C`;
    document.getElementById('entropy')!.innerText = `${data.entropy} eV`;
    document.getElementById('cyber-alpha')!.innerText = data.cyber_alpha;
    document.getElementById('cyber-logix')!.innerText = data.cyber_logix;
    
    const statusEl = document.getElementById('node-id')!;
    statusEl.innerText = `${data.node_id} [CONECTADO]`;
    statusEl.style.color = '#00ff7f';
  } catch (error) {
    const statusEl = document.getElementById('node-id')!;
    statusEl.innerText = 'OFFLINE (Aguardando Python Core)';
    statusEl.style.color = '#ff7b72';
  }
}

// Inicia o loop de varredura assíncrona
setInterval(fetchQuantumTelemetry, 3000);
fetchQuantumTelemetry();
