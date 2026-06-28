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

class HeksPolyCore:
    def __init__(self):
        self.node_id = "HYPERION-POLY-CORE-V4.3"
        self.groq_key = os.environ.get("GROQ_API_KEY", "")
        self.running = True
        
        self.base_dir = os.path.expanduser("~/willianlima1533")
        self.logix_file = os.path.join(self.base_dir, "totais_comandas.json")
        
        self._init_local_storage()
        
        self.alpha_logic = "return f'ALPHA: Scanner ativo. Preço base: {data.get(\"price\")}'"
        self.logix_logic = "return f'LOGIX: Processando Base Real. Ganhos: R$ {data.get(\"ganhos_totais\")}'"
        
        self.alpha_env = {}
        self.logix_env = {}
        self._compile_agent("ALPHA", self.alpha_logic)
        self._compile_agent("LOGIX", self.logix_logic)

        # Gerenciamento adaptativo de janelas de chamada
        self.base_mutation_interval = 20  
        self.current_backoff = 0

    def _init_local_storage(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        if not os.path.exists(self.logix_file):
            default_data = {
                "ganhos_totais": 180.50,
                "km_rodado": 42.0,
                "consumo_estimado_l": 1.4
            }
            with open(self.logix_file, "w") as f:
                json.dump(default_data, f, indent=4)

    def _compile_agent(self, target, logic_body):
        indented_body = "\n".join([f"    {line}" for line in logic_body.splitlines()])
        func_src = f"def {target.lower()}_worker(data):\n{indented_body}"
        local_env = {}
        exec(func_src, globals(), local_env)
        if target == "ALPHA":
            self.alpha_env = local_env
            self.alpha_logic = logic_body
        else:
            self.logix_env = local_env
            self.logix_logic = logic_body

    def load_real_logistics_data(self):
        try:
            with open(self.logix_file, "r") as f:
                return json.load(f)
        except Exception:
            return {"ganhos_totais": 0.0, "km_rodado": 1.0, "consumo_estimado_l": 1.0}

    def capture_telemetry_and_data(self):
        try:
            load = os.getloadavg()[0]
        except Exception:
            load = random.uniform(0.1, 0.3)
        return {
            "load": load,
            "market_feed": {"price": round(random.uniform(1.0850, 1.0950), 4), "volatility": random.choice(["ALTA", "BAIXA"])},
            "logistics_feed": self.load_real_logistics_data()
        }

    def call_groq_mutation(self, target_agent, data_pack):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
        
        if target_agent == "ALPHA":
            context = f"Dados de Mercado no dict 'data': {data_pack['market_feed']}."
            task = "Crie uma lógica em Python de uma linha usando 'data.get(\"price\")' para monitoramento e retorne uma string analítica."
        else:
            context = f"DADOS REAIS extraídos de totais_comandas.json no dict 'data': {data_pack['logistics_feed']}."
            task = "Crie uma lógica matemática em Python que processe esses dados de logística reais (ex: ganhos_totais / km_rodado) e retorne o resultado formatado em uma string curta de faturamento por quilômetro."

        prompt = (
            f"Você é o Hyper-Kernel do HEKS V4.3. {context}\n"
            f"Sua tarefa: {task}\n"
            f"Importante: Responda estritamente no formato JSON plano: {{\"code\": \"sua linha de código baseada em 'data' aqui\"}}"
        )
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "Você é um gerador de código analítico bruto para strings Python. Responda apenas o JSON estruturado plano, sem markdown."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        
        # Proteção ativa de barramento contra Rate Limit (HTTP 429)
        if response.status_code == 429:
            raise Exception("RATE_LIMIT_HIT")
            
        res_json = response.json()
        if 'choices' not in res_json:
            raise Exception("INVALID_API_RESPONSE")
            
        raw_content = res_json['choices'][0]['message']['content'].strip()
        return json.loads(raw_content).get("code")

    def mutation_engine_loop(self):
        print(f"[🔱] Ciclo Mutagênico Antigargalo Conectado ao Termux...")
        while self.running:
            # Janela de sono dinâmica calculada com Jitter aleatório para quebrar detecção de robô
            sleep_time = self.base_mutation_interval + self.current_backoff + random.uniform(1, 5)
            time.sleep(sleep_time)
            
            if not self.groq_key:
                continue
                
            data_pack = self.capture_telemetry_and_data()
            target = random.choice(["ALPHA", "LOGIX"])
            
            try:
                new_logic = self.call_groq_mutation(target, data_pack)
                if new_logic and "return" in new_logic:
                    new_logic = new_logic.replace('`', "'")
                    self._compile_agent(target, new_logic)
                    print(f"\n[⚡ DATA MUTATION SUCCESS]: Algoritmo {target} adaptado para dados reais:\n--> {new_logic}\n")
                    self.current_backoff = max(0, self.current_backoff - 5) # Reduz o backoff se teve sucesso
            except Exception as e:
                err_msg = str(e)
                if "RATE_LIMIT_HIT" in err_msg:
                    self.current_backoff = min(60, self.current_backoff + 15) # Aumenta a janela de espera em 15s
                    print(f"[⚠️ QUOTA PROTECTION]: Limite atingido. Expandindo backoff para +{self.current_backoff}s.")
                else:
                    print(f"[⚠️ Mutation Bypass]: Ajuste retido: {err_msg[:40]}")

    def run_threads(self):
        while self.running:
            data_pack = self.capture_telemetry_and_data()
            try:
                if "alpha_worker" in self.alpha_env:
                    res_a = self.alpha_env["alpha_worker"](data_pack["market_feed"])
                    print(f"[Run ALPHA]: {res_a}")
                if "logix_worker" in self.logix_env:
                    res_b = self.logix_env["logix_worker"](data_pack["logistics_feed"])
                    print(f"[Run LOGIX]: {res_b}")
            except Exception as e:
                print(f"[Execution Error]: Falha sintática em tempo de execução: {e}")
            time.sleep(4)

    def start(self):
        print(f"[⚙️] Inicializando Core Polimórfico Real-Data V4.3 Antigargalo...")
        threading.Thread(target=self.mutation_engine_loop, daemon=True).start()
        self.run_threads()

if __name__ == "__main__":
    core = HeksPolyCore()
    core.start()
