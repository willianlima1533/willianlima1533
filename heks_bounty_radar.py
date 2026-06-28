#!/usr/bin/env python3
import requests
import json
import os
import time

def buscar_oportunidades_pagas():
    print("\033[1;35m[🔱] INICIALIZANDO HEKS BOUNTY RADAR... CONECTANDO À API DO GITHUB\033[0m")
    
    # Query de busca focada em issues abertas com labels de recompensa ou ajuda em projetos Python/JS
    query = 'is:issue is:open label:bounty,"help wanted","good first issue" language:python'
    url = f"https://api.github.com/search/issues?q={query}&sort=created&order=desc&per_page=10"
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            issues = data.get("items", [])
            
            os.system('clear')
            print("\033[1;32m┌────────────────────────────────────────────────────────────────────────┐\033[0m")
            print("\033[1;32m│ 💰 OPORTUNIDADES ENCONTRADAS NO RADAR DO GITHUB                         │\033[0m")
            print("\033[1;32m└────────────────────────────────────────────────────────────────────────┘\033[0m\n")
            
            if not issues:
                print("[-] Nenhuma issue com bounty encontrada neste ciclo. Refinando varredura...")
                return

            for index, issue in enumerate(issues, start=1):
                title = issue.get("title")
                repo_url = issue.get("repository_url").replace("https://api.github.com/repos/", "https://github.com/")
                html_url = issue.get("html_url")
                labels = [l.get("name") for l in issue.get("labels", [])]
                
                print(f"\033[1;33m[{index}] PROJETO:\033[0m {repo_url.split('/')[-1]}")
                print(f"    \033[1;36m▶ TÍTULO:\033[0m {title}")
                print(f"    \033[1;31m▶ LABELS:\033[0m {', '.join(labels)}")
                print(f"    \033[1;34m▶ LINK DA ISSUE:\033[0m {html_url}")
                print("-" * 74)
                
        elif response.status_code == 403:
            print("\033[1;31m[⚠️ RATE LIMIT]: Limite de requisições anônimas da API do GitHub atingido. Aguarde alguns minutos.\033[0m")
        else:
            print(f"[-] Erro de conexão com o barramento do GitHub: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"[-] Falha crítica no salto de rede: {e}")

if __name__ == "__main__":
    buscar_oportunidades_pagas()
