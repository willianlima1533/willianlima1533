#!/usr/bin/env python3
import os
import sys
import time
import requests
import random
import threading
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HeksCore:
    def __init__(self):
        self.node_id = "HYPERION-MASTER-CORE-01"
        self.entropy_threshold = 0.70
        self.groq_key = os.environ.get("GROQ_API_KEY", "")
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "")
        self.running = True
        
        self.agent_alpha_status = "IDLE"   
        self.agent_logix_status = "IDLE"   
        self.system_resources = {}
        self.orchestration_interval = 3    

    def capture_edge_telemetry(self):
        mem_total, mem_available = 4096.0, 2048.0
        try:
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if "MemTotal" in line: mem_total = float(line.split()[1]) / 1024.0
                    if "MemAvailable" in line: mem_available = float(line.split()[1]) / 1024.0
        except Exception:
            pass
        try:
            load_avg = os.getloadavg()[0]
        except Exception:
            load_avg = random.uniform(0.1, 0.4)

        self.system_resources = {
            "node": self.node_id,
            "timestamp": time.time(),
            "system_load_avg": load_avg,
            "ram_total_mb": mem_total,
            "ram_available_mb": mem_available
        }
        return self.system_resources

    def calculate_system_entropy(self, data):
        mem_used_pct = 1.0 - (data["ram_available_mb"] / data["ram_total_mb"])
        factor = (data["system_load_avg"] / 8.0) * mem_used_pct
        return round(min(factor, 1.0), 4)

    def _run_agent_alpha(self):
        while self.running:
            time.sleep(1)

    def _run_agent_logix(self):
        while self.running:
            time.sleep(1)

    def call_groq_engine(self, prompt):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        # Atualizado para o modelo de produção estável e veloz da linha Llama 3.1
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "Você é um sistema embarcado. Responda apenas com o objeto JSON solicitado, sem texto explicativo adicional."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        response = requests.post(url, headers=headers, json=payload, timeout=7)
        result = response.json()
        if 'error' in result:
            raise Exception(f"Groq API Error: {result['error'].get('message')}")
        return result['choices'][0]['message']['content'].strip()

    def call_gemini_fallback(self, prompt):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
        response = requests.post(url, headers=headers, json=payload, timeout=7, verify=False)
        result = response.json()
        if 'error' in result:
            raise Exception(f"Gemini API Error: {result['error'].get('message')}")
        return result['candidates'][0]['content']['parts'][0]['text'].strip()

    def execute_cognitive_orchestration(self, telemetry, entropy):
        prompt = (
            f"Você é o Hyper-Kernel do HEKS. Recursos: Carga={telemetry['system_load_avg']}, Entropia={entropy}. "
            f"Agente ALPHA (Trading) está {self.agent_alpha_status}. Agente LOGIX (Logística) está {self.agent_logix_status}. "
            f"Decida as próximas ações respondendo estritamente no formato JSON plano: "
            f"{{\"alpha\": \"ACTIVE ou IDLE\", \"logix\": \"ACTIVE ou IDLE\", \"motivo\": \"frase curta\"}}"
        )
        
        err_logs = []
        
        if self.groq_key:
            try:
                raw_json = self.call_groq_engine(prompt)
                decision = json.loads(raw_json)
                self.agent_alpha_status = decision.get("alpha", "IDLE")
                self.agent_logix_status = decision.get("logix", "IDLE")
                return f"[⚡ GROQ KERNEL]: {decision.get('motivo')} -> ALPHA: {self.agent_alpha_status} | LOGIX: {self.agent_logix_status}"
            except Exception as e:
                err_logs.append(f"Groq_Fail({str(e)[:40]})")
                
        if self.gemini_key:
            try:
                raw_json = self.call_gemini_fallback(prompt)
                decision = json.loads(raw_json)
                self.agent_alpha_status = decision.get("alpha", "IDLE")
                self.agent_logix_status = decision.get("logix", "IDLE")
                return f"[🧠 GEMINI FALLBACK]: {decision.get('motivo')} -> ALPHA: {self.agent_alpha_status} | LOGIX: {self.agent_logix_status}"
            except Exception as e:
                err_logs.append(f"Gemini_Fail({str(e)[:40]})")
                
        return f"[❌ KERNEL CRITICAL ERROR]: Motores offline. Logs: {' | '.join(err_logs)}"

    def run_engine(self):
        print(f"[🔱] Inicializando Hyper-OS Cognitivo HEKS V3 [Dual-Engine Model-Patch]...")
        
        threading.Thread(target=self._run_agent_alpha, daemon=True).start()
        threading.Thread(target=self._run_agent_logix, daemon=True).start()
        
        counter = 0
        try:
            while True:
                telemetry = self.capture_edge_telemetry()
                entropy = self.calculate_system_entropy(telemetry)
                
                if entropy > self.entropy_threshold:
                    self.agent_alpha_status = "IDLE"
                    self.agent_logix_status = "IDLE"
                    print(f"[🚨 CRITICAL HARDWARE]: Entropia Elevada ({entropy}). Forçando congelamento.")
                else:
                    print(f"[NODE]: Entropia: {entropy} | Hard-Drive operando em estabilidade.")
                    counter += 1
                    if counter % self.orchestration_interval == 0:
                        insight = self.execute_cognitive_orchestration(telemetry, entropy)
                        print(insight)
                        
                time.sleep(2)
        except KeyboardInterrupt:
            self.running = False
            print("\n[⚠️] Execução do Hyper-OS HEKS abortada pelo operador.")

if __name__ == "__main__":
    engine = HeksCore()
    engine.run_engine()
