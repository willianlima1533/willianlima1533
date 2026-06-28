#!/usr/bin/env python3
import os
import sys
import time
import requests
import random
import threading
import json
import math
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HeksQuantumCore:
    def __init__(self):
        self.node_id = "HYPERION-QUANTUM-CORE-V5"
        self.groq_key = os.environ.get("GROQ_API_KEY", "")
        self.running = True
        
        # Diretórios locais do Termux
        self.base_dir = os.path.expanduser("~/willianlima1533")
        self.logix_file = os.path.join(self.base_dir, "totais_comandas.json")
        self._init_local_storage()
        
        # Estados de Matriz Quântica Inicial (DNA das Threads)
        self.alpha_logic = "return f'Psi_0 [ALPHA]: Varredura de Pullback ativa. Amplitude estável.'"
        self.logix_logic = "return f'Psi_0 [LOGIX]: Matriz Logística real carregada. Colapso de dados ok.'"
        
        self.alpha_env = {}
        self.logix_env = {}
        self._compile_quantum_patch("ALPHA", self.alpha_logic)
        self._compile_quantum_patch("LOGIX", self.logix_logic)

        # Controle de Entrelaçamento e Backoff
        self.base_interval = 18  
        self.backoff_entropy = 0

    def _init_local_storage(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        if not os.path.exists(self.logix_file):
            with open(self.logix_file, "w") as f:
                json.dump({"ganhos_totais": 180.50, "km_rodado": 42.0, "consumo_estimado_l": 1.4}, f, indent=4)

    def _compile_quantum_patch(self, target, logic_body):
        """Injeta código gerado pela IA no escopo molecular do interpretador"""
        indented = "\n".join([f"    {line}" for line in logic_body.splitlines()])
        func_src = f"def {target.lower()}_worker(data):\n{indented}"
        local_env = {}
        exec(func_src, globals(), local_env)
        if target == "ALPHA":
            self.alpha_env = local_env
            self.alpha_logic = logic_body
        else:
            self.logix_env = local_env
            self.logix_logic = logic_body

    def compute_quantum_telemetry(self):
        """Simula flutuações quânticas baseadas na carga de hardware do dispositivo"""
        try:
            load = os.getloadavg()[0]
        except Exception:
            load = random.uniform(0.05, 0.2)
            
        # Cálculos de matriz quântica decorativa/estética
        entropy = round(math.sin(load) * random.uniform(0.1, 0.5), 4)
        decoherence = "CRITICAL" if load > 0.7 else "STABLE"
        
        try:
            with open(self.logix_file, "r") as f:
                real_logistics = json.load(f)
        except Exception:
            real_logistics = {"ganhos_totais": 0.0, "km_rodado": 1.0}

        return {
            "entropy": entropy,
            "decoherence": decoherence,
            "market_feed": {"price": round(random.uniform(1.0850, 1.0950), 4), "volatility": random.choice(["HIGH", "LOW"])},
            "logistics_feed": real_logistics
        }

    def call_groq_quantum_mutation(self, target_agent, telemetry):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
        
        if target_agent == "ALPHA":
            context = f"Matriz Alpha. Preço: {telemetry['market_feed']}. Entropia de Hardware: {telemetry['entropy']}."
            task = "Crie uma expressão de uma linha em Python que valide 'data.get(\"price\")' ou volatilidade e retorne um relatório quântico-robótico futurista curto em português."
        else:
            context = f"Matriz Logix. Base Real Termux: {telemetry['logistics_feed']}. Estado: {telemetry['decoherence']}."
            task = "Crie uma expressão matemática analítica em Python que calcule faturamento por KM rodado com base em 'data' e retorne formatado com termos como 'Otimização Cibernética de Rotas'."

        prompt = (
            f"Você é o Quantum Language Kernel do HEKS V5. {context}\n"
            f"Tarefa: {task}\n"
            f"Responda estritamente no formato JSON plano, contendo apenas a chave 'code' com a linha de comando Python que use return: {{\"code\": \"sua linha aqui\"}}"
        )
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "Você é um gerador de strings de código quântico-futurista para Python. Sem markdown."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.25
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        if response.status_code == 429:
            raise Exception("QUANTUM_TUNNEL_LIMIT")
            
        res_json = response.json()
        return json.loads(res_json['choices'][0]['message']['content'].strip()).get("code")

    def quantum_evolution_loop(self):
        print(f"[🔱] Barramento Quântico Ativo. Orquestrando superposição de IA...")
        while self.running:
            sleep_time = self.base_interval + self.backoff_entropy + random.uniform(2, 6)
            time.sleep(sleep_time)
            
            if not self.groq_key:
                continue
                
            telemetry = self.compute_quantum_telemetry()
            target = random.choice(["ALPHA", "LOGIX"])
            
            try:
                new_logic = self.call_groq_quantum_mutation(target, telemetry)
                if new_logic and "return" in new_logic:
                    new_logic = new_logic.replace('`', "'")
                    self._compile_quantum_patch(target, new_logic)
                    print(f"\n[⚛️ QUANTUM MUTATION SUCCESS]: DNA do Agente {target} colapsado para nova função:\n--> {new_logic}\n")
                    self.backoff_entropy = max(0, self.backoff_entropy - 4)
            except Exception as e:
                if "QUANTUM_TUNNEL_LIMIT" in str(e):
                    self.backoff_entropy = min(60, self.backoff_entropy + 20)
                    print(f"[⚠️ DECOERÊNCIA DE REDE]: Limite de requisições atingido. Backoff Quântico expandido para +{self.backoff_entropy}s.")
                else:
                    print(f"[⚠️ Quantum Bypass]: Mutação flutuante retida.")

    def run_quantum_threads(self):
        while self.running:
            telemetry = self.compute_quantum_telemetry()
            try:
                if "alpha_worker" in self.alpha_env:
                    res_a = self.alpha_env["alpha_worker"](telemetry["market_feed"])
                    print(f"[🤖 CYBER-ALPHA]: {res_a}")
                if "logix_worker" in self.logix_env:
                    res_b = self.logix_env["logix_worker"](telemetry["logistics_feed"])
                    print(f"[⚙️ CYBER-LOGIX]: {res_b}")
            except Exception as e:
                print(f"[Quantum Execution Error]: Salto de estado inválido: {e}")
            time.sleep(4)

    def start(self):
        print(f"[🔱] Inicializando Hyper-OS Cognitivo HEKS V5 [Quantum-Inspired Mode]...")
        threading.Thread(target=self.quantum_evolution_loop, daemon=True).start()
        self.run_quantum_threads()

if __name__ == "__main__":
    core = HeksQuantumCore()
    core.start()
