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
        self.node_id = "HYPERION-QUANTUM-CORE-V5.1"
        self.groq_key = os.environ.get("GROQ_API_KEY", "")
        self.running = True
        
        self.base_dir = os.path.expanduser("~/willianlima1533")
        self.logix_file = os.path.join(self.base_dir, "totais_comandas.json")
        self._init_local_storage()
        
        # DNA Inicial Estável e Blindado
        self.alpha_logic = "return f'Psi_0 [ALPHA]: Varredura de Pullback ativa. Amplitude estável.'"
        self.logix_logic = "return f'Psi_0 [LOGIX]: Totaia de comandas processados. Estado estável.'"
        
        self.alpha_env = {}
        self.logix_env = {}
        self._compile_quantum_patch("ALPHA", self.alpha_logic)
        self._compile_quantum_patch("LOGIX", self.logix_logic)

        self.base_interval = 18  
        self.backoff_entropy = 0

    def _init_local_storage(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        if not os.path.exists(self.logix_file):
            with open(self.logix_file, "w") as f:
                json.dump({"ganhos_totais": 180.50, "km_rodado": 42.0, "consumo_estimado_l": 1.4}, f, indent=4)

    def _compile_quantum_patch(self, target, logic_body):
        """Sanitiza e valida estruturalmente o código antes do fork de execução"""
        # Se a IA esquecer o return ou quebrar a sintaxe, aborta a compilação local
        if "return" not in logic_body or "def " in logic_body:
            raise ValueError("Injeção inválida detectada pelo firewall cognitivo.")

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
        try:
            load = os.getloadavg()[0]
        except Exception:
            load = random.uniform(0.05, 0.2)
            
        entropy = round(math.sin(load) * random.uniform(0.1, 0.5), 4)
        decoherence = "CRITICAL" if load > 0.7 else "STABLE"
        
        try:
            with open(self.logix_file, "r") as f:
                real_logistics = json.load(f)
        except Exception:
            real_logistics = {"ganhos_totais": 180.5, "km_rodado": 42.0}

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
            context = f"Matriz Alpha. Preço Atual: {telemetry['market_feed']['price']}. Volatilidade: {telemetry['market_feed']['volatility']}."
            task = "Retorne uma linha de código Python pura que use return e data.get('price') para gerar um log cibernético em português."
        else:
            context = f"Matriz Logix. Dados de Comandas Reais: Ganhos={telemetry['logistics_feed']['ganhos_totais']}, KM={telemetry['logistics_feed']['km_rodado']}."
            task = "Retorne uma única linha de código Python calculando a eficiência por KM rodado diretamente, ex: return f'Otimização Cibernética de Rotas: R$ {data.get(\"ganhos_totais\") / data.get(\"km_rodado\"):.2f}/KM'."

        prompt = (
            f"Você é o Quantum Language Kernel do HEKS V5.1. {context}\n"
            f"Sua tarefa: {task}\n"
            f"REGRAS DE COMPILAÇÃO CRÍTICAS:\n"
            f"- Não use a palavra-chave 'def' para criar novas funções.\n"
            f"- Inicie a linha de código diretamente com a palavra-chave 'return'.\n"
            f"Responda estritamente no formato JSON plano: {{\"code\": \"sua linha de código aqui\"}}"
        )
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "Você é um compilador cibernético inline de expressões Python. Retorne estritamente o JSON plano, sem markdown ou explicações."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        if response.status_code == 429:
            raise Exception("QUANTUM_TUNNEL_LIMIT")
            
        res_json = response.json()
        return json.loads(res_json['choices'][0]['message']['content'].strip()).get("code")

    def quantum_evolution_loop(self):
        print(f"[🔱] Barramento Quântico Estabilizado. Monitorando mutações...")
        while self.running:
            sleep_time = self.base_interval + self.backoff_entropy + random.uniform(2, 5)
            time.sleep(sleep_time)
            
            if not self.groq_key:
                continue
                
            telemetry = self.compute_quantum_telemetry()
            target = random.choice(["ALPHA", "LOGIX"])
            
            try:
                new_logic = self.call_groq_quantum_mutation(target, telemetry)
                if new_logic:
                    new_logic = new_logic.replace('`', "'")
                    self._compile_quantum_patch(target, new_logic)
                    print(f"\n[⚛️ QUANTUM MUTATION SUCCESS]: DNA do Agente {target} colapsado com sucesso:\n--> {new_logic}\n")
                    self.backoff_entropy = max(0, self.backoff_entropy - 4)
            except Exception as e:
                if "QUANTUM_TUNNEL_LIMIT" in str(e):
                    self.backoff_entropy = min(60, self.backoff_entropy + 20)
                    print(f"[⚠️ DECOERÊNCIA DE REDE]: Ajustando frequência. Janela expandida em +{self.backoff_entropy}s.")
                else:
                    print(f"[⚠️ Quantum Bypass]: Mutação flutuante descartada pelo firewall de sintaxe.")

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
        print(f"[🔱] Inicializando Hyper-OS Cognitivo HEKS V5.1 [Estabilizado]...")
        threading.Thread(target=self.quantum_evolution_loop, daemon=True).start()
        self.run_quantum_threads()

if __name__ == "__main__":
    core = HeksQuantumCore()
    core.start()
