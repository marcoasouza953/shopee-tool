import json
import time
import random
from googlesearch import search

def find_videos(input_file=".tmp/products_raw.json", output_file=".tmp/products_with_videos.json"):
    """
    Lê a lista de produtos e busca vídeos correspondentes no TikTok e Kwai usando Google Dorking.
    """
    try:
        with open(input_file, "r") as f:
            products = json.load(f)
    except FileNotFoundError:
        print(f"[!] Arquivo {input_file} não encontrado. Execute o shopee_scanner.py primeiro.")
        return

    print(f"[*] Buscando vídeos para {len(products)} produtos...")
    
    for i, product in enumerate(products):
        name = product.get("name")
        print(f"[{i+1}/{len(products)}] Processando: {name[:30]}...")
        
        # Estratégia de busca simples e efetiva
        # "nome do produto" site:tiktok.com
        tiktok_query = f'"{name}" site:tiktok.com'
        kwai_query = f'"{name}" site:kwai.com'
        
        tiktok_links = []
        kwai_links = []
        
        try:
            # Buscar TikTok (limitado a 3 resultados para ser rápido)
            for url in search(tiktok_query, num_results=3, lang="pt"):
                if "video" in url: # Filtrar apenas links de vídeo
                    tiktok_links.append(url)
            
            # Pequeno delay aleatório para evitar 429
            time.sleep(random.uniform(1.5, 3.0))
            
            # Buscar Kwai (limitado a 3 resultados)
            for url in search(kwai_query, num_results=3, lang="pt"):
                if "video" in url or "kwai" in url:
                    kwai_links.append(url)
                    
            time.sleep(random.uniform(1.5, 3.0))
            
        except Exception as e:
            print(f"[!] Erro na busca Google para '{name}': {e}")
            # Se der erro (ex: 429 Too Many Requests), espera mais tempo
            time.sleep(10)
            
        product["tiktok_links"] = tiktok_links
        product["kwai_links"] = kwai_links
        
        # Salvar progresso incrementalmente (opcional, mas seguro)
        if i % 5 == 0:
             with open(output_file, "w", encoding="utf-8") as f:
                json.dump(products, f, indent=2, ensure_ascii=False)

    # Salva resultado final
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Busca de vídeos concluída! Dados salvos em {output_file}")

if __name__ == "__main__":
    find_videos()
