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

class HeksQuantumCoreV6:
    def __init__(self):
        self.node_id = "HEKS-QUANTUM-CORE-V6"
        self.groq_key = os.environ.get("GROQ_API_KEY", "")
        self.running = True
        
        self.base_dir = os.path.expanduser("~/willianlima1533")
        self.logix_file = os.path.join(self.base_dir, "totais_comandas.json")
        
        # DNA Base Estável
        self.alpha_logic = "return f'ALPHA >> Frequência quântica estabilizada a 4.12 GHz.'"
        self.logix_logic = "return f'LOGIX >> Matriz de rotas sincronizada com o terminal local.'"
        
        self.alpha_env = {}
        self.logix_env = {}
        self._compile("ALPHA", self.alpha_logic)
        self._compile("LOGIX", self.logix_logic)

    def _compile(self, target, logic_body):
        if "return" not in logic_body or "def " in logic_body:
            raise ValueError("Firewall interceptou código hostil ou mal formatado.")
        indented = "\n".join([f"    {line}" for line in logic_body.splitlines()])
        func_src = f"def {target.lower()}_worker(data):\n{indented}"
        local_env = {}
        exec(func_src, globals(), local_env)
        if target == "ALPHA":
            self.alpha_env = local_env
        else:
            self.logix_env = local_env

    def render_hollywood_interface(self, telemetry, status_msg=""):
        """Renderiza uma interface gráfica diretamente no texto do terminal do Termux"""
        os.system('clear')
        print("\033[1;35m┌────────────────────────────────────────────────────────────────────────┐\033[0m")
        print(f"\033[1;35m│ \033[1;32m🔱 {self.node_id} \033[1;35m│ OPERAÇÃO: COGNITIVA MULTI-THREAD \033[1;35m│ STATUS: ATIVO   │\033[0m")
        print("\033[1;35m├────────────────────────────────────────────────────────────────────────┤\033[0m")
        print(f"\033[1;36m  ▶ ENTROPIA QUÂNTICA: {telemetry['entropy']} eV  │  DECOERÊNCIA: {telemetry['decoherence']}\033[0m")
        print(f"\033[1;31m  ▶ CORE TÉRMICO VIRTUAL: {telemetry['thermal']}°C │  CARGA ALOCADA: {telemetry['load']}%\033[0m")
        print("\033[1;35m├────────────────────────────────────────────────────────────────────────┤\033[0m")
        
        # Logs das Threads Ativas
        try:
            res_a = self.alpha_env["alpha_worker"](telemetry["market_feed"])
            print(f" \033[1;33m[🤖 CYBER-ALPHA]\033[0m -> {res_a}")
        except:
            print(" [🤖 CYBER-ALPHA] -> Estado em superposição instável.")
            
        try:
            res_b = self.logix_env["logix_worker"](telemetry["logistics_feed"])
            print(f" \033[1;32m[⚙️ CYBER-LOGIX]\033[0m -> {res_b}")
        except:
            print(" [⚙️ CYBER-LOGIX] -> Colapso de matriz pendente.")
            
        if status_msg:
            print("\033[1;35m├────────────────────────────────────────────────────────────────────────┤\033[0m")
            print(f"\033[1;34m [⚛️ IA COGNITIVA] -> {status_msg}\033[0m")
        print("\033[1;35m└────────────────────────────────────────────────────────────────────────┘\033[0m")

    def capture_telemetry(self):
        load = round(random.uniform(12.4, 45.8), 2)
        thermal = round(random.uniform(38.5, 42.1), 1)
        entropy = round(math.sin(load) * random.uniform(0.1, 0.9), 4)
        
        try:
            with open(self.logix_file, "r") as f:
                real_logistics = json.load(f)
        except:
            real_logistics = {"ganhos_totais": 180.5, "km_rodado": 42.0}

        return {
            "load": load, "thermal": thermal, "entropy": entropy, "decoherence": "ESTÁVEL",
            "market_feed": {"price": round(random.uniform(1.0850, 1.0950), 4)},
            "logistics_feed": real_logistics
        }

    def call_groq(self, target, telemetry):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
        
        prompt = (
            f"Você é o Kernel do HEKS V6. Escreva uma única linha de código Python pura que comece com 'return f...' "
            f"utilizando os dados do dict 'data'. Use jargões de inteligência robótica, quântica ou redes neurais avançadas em português. "
            f"Seja curto e direto. Exemplo: return f'Análise Quântica: Preço em {{data.get(\"price\")}}' "
            f"Responda estritamente no formato JSON: {{\"code\": \"sua linha aqui\"}}"
        )
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "temperature": 0.3
        }
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=7).json()
            return json.loads(res['choices'][0]['message']['content'].strip()).get("code")
        except:
            return None

    def mutation_loop(self):
        while self.running:
            time.sleep(16)
            if not self.groq_key: continue
            telemetry = self.capture_telemetry()
            target = random.choice(["ALPHA", "LOGIX"])
            new_code = self.call_groq(target, telemetry)
            if new_code:
                try:
                    self._compile(target, new_code)
                    self.last_msg = f"Mutação aplicada com sucesso na Thread [{target}]."
                except:
                    self.last_msg = "Firewall interceptou código com salto quântico inválido."
            else:
                self.last_msg = "Decoerência temporária na resposta da LPU Groq."

    def start(self):
        self.last_msg = "Inicializando matriz holográfica de monitoramento..."
        threading.Thread(target=self.mutation_loop, daemon=True).start()
        while self.running:
            telemetry = self.capture_telemetry()
            self.render_hollywood_interface(telemetry, self.last_msg)
            time.sleep(3)

if __name__ == "__main__":
    core = HeksQuantumCoreV6()
    core.start()
