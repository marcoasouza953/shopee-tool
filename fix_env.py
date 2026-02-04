import json
import re

def fix_env_file():
    """
    Lê o .env quebrado (com JSON colado) e converte para o formato correto.
    """
    try:
        with open(".env", "r") as f:
            content = f.read()
        
        # Tentar achar o bloco JSON
        # Procura por chaves { ... }
        match = re.search(r'(\{.*\})', content, re.DOTALL)
        if match:
            json_str = match.group(1)
            try:
                data = json.loads(json_str)
                # O JSON parece ter uma chave raiz "Cookies da requisição" ou pode ser direto
                cookies_dict = data.get("Cookies da requisição", data)
                
                if isinstance(cookies_dict, dict):
                    # Converter dict para string de cookie: key=value; key2=value2
                    cookie_parts = []
                    for k, v in cookies_dict.items():
                        cookie_parts.append(f"{k}={v}")
                    
                    cookie_string = "; ".join(cookie_parts)
                    
                    # Reescrever .env
                    new_content = f"SHOPEE_COOKIE={cookie_string}\n"
                    
                    with open(".env", "w") as f:
                        f.write(new_content)
                    
                    print(f"[+] .env corrigido com sucesso! Cookie recuperado.")
                else:
                    print("[!] JSON encontrado mas estrutura desconhecida.")
            except json.JSONDecodeError:
                print("[!] Bloco encontrado parece JSON mas falhou no parse.")
        else:
            print("[!] Nenhum bloco JSON encontrado no .env.")
            
    except Exception as e:
        print(f"[!] Erro ao corrigir .env: {e}")

if __name__ == "__main__":
    fix_env_file()
