import json
import os
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_mock_products():
    """Retorna produtos de exemplo para fallback."""
    print("[*] Usando dados de fallback (MOCK) devido a erro no Selenium...")
    return [
        {
            "id": 11111,
            "name": "Fone de Ouvido Bluetooth Sem Fio TWS i12 Touch",
            "price": 29.99,
            "sold": 15000,
            "rating": 4.8,
            "score": 72000,
            "url": "https://shopee.com.br/search?keyword=fone+bluetooth",
            "image_url": "https://down-br.img.susercontent.com/file/br-11134207-7r98o-lm42p5q3k5qf38" 
        },
        {
            "id": 22222,
            "name": "Mini Processador de Alimentos Manual Triturador Alho",
            "price": 12.50,
            "sold": 45000,
            "rating": 4.9,
            "score": 220500,
            "url": "https://shopee.com.br/search?keyword=processador+alimentos",
            "image_url": "https://down-br.img.susercontent.com/file/br-11134207-7r98o-ll1p6q3k5qf38"
        },
        {
            "id": 33333,
            "name": "Garrafa De Água Squeeze 2 Litros Motivacional Academia",
            "price": 19.90,
            "sold": 22000,
            "rating": 4.7,
            "score": 103400,
            "url": "https://shopee.com.br/search?keyword=garrafa+motivacional",
            "image_url": "https://down-br.img.susercontent.com/file/br-11134207-7qukw-ljz6p5q3k5qf38"
        },
        {
            "id": 44444,
            "name": "Kit 10 Pares Meia Soquete Unissex Algodão",
            "price": 25.00,
            "sold": 8500,
            "rating": 4.6,
            "score": 39100,
            "url": "https://shopee.com.br/search?keyword=kit+meias",
            "image_url": "https://down-br.img.susercontent.com/file/br-11134207-7qukw-ljz6p5q3k5qf39"
        },
        {
            "id": 55555,
            "name": "Luz De Led Rgb Colorida Com Controle Remoto Bivolt",
            "price": 15.99,
            "sold": 12000,
            "rating": 4.5,
            "score": 54000,
            "url": "https://shopee.com.br/search?keyword=luz+led+rgb",
            "image_url": "https://down-br.img.susercontent.com/file/br-11134207-7qukw-ljz6p5q3k5qf40"
        }
    ]

def scan_shopee_products(limit=50):
    """
    Busca produtos populares na Shopee Brasil usando Selenium (undetected-chromedriver).
    """
    print("[*] Iniciando Chrome Driver (Headless)...", flush=True)
    
    # Configurar opções do Chrome
    options = uc.ChromeOptions()
    options.add_argument('--headless=new') # Headless moderno
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = uc.Chrome(options=options, version_main=None) # version_main=None deixa ele auto-detectar
    except Exception as e:
        print(f"[!] Erro ao iniciar Chrome: {e}", flush=True)
             
        # Tentar mock direto se falhar driver
        mock = get_mock_products()
        os.makedirs(".tmp", exist_ok=True)
        with open(".tmp/products_raw.json", "w", encoding="utf-8") as f:
            json.dump(mock, f, indent=2, ensure_ascii=False)
        return mock

    try:
        # URL da API direta
        api_url = "https://shopee.com.br/api/v4/search/search_items?by=sales&keyword=achadinhos&limit=50&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
        
        print(f"[*] Navegando para API Shopee...", flush=True)
        driver.get(api_url)
        
        # Esperar carregar (JSON raw na tela)
        time.sleep(5) 
        
        # Extrair texto do body
        content = driver.find_element(By.TAG_NAME, "body").text
        
        try:
            data = json.loads(content)
        except:
            # As vezes o navegador envolve em tag <pre>
            try:
                content = driver.find_element(By.TAG_NAME, "pre").text
                data = json.loads(content)
            except:
                print("[!] Não foi possível parsear JSON da resposta do browser.")
                print(f"Conteúdo parcial: {content[:200]}")
                raise Exception("JSON Parse Error")

        # Processar dados (Mesma lógica de antes)
        items = data.get("items", [])
        if not items:
            print("[!] JSON válido mas sem itens. Shopee pode ter pedido CAPTCHA.")
            # Fallback
            final_items = get_mock_products()
        else:
            processed_items = []
            for item_wrapper in items:
                item = item_wrapper.get("item_basic", {})
                if not item: continue
                    
                itemid = item.get("itemid")
                shopid = item.get("shopid")
                name = item.get("name")
                sold = item.get("historical_sold", 0)
                price = item.get("price", 0) / 100000
                rating = item.get("item_rating", {}).get("rating_star", 0)
                image = item.get("image")
                
                clean_name = name.replace(" ", "-").replace("/", "-")
                url = f"https://shopee.com.br/{clean_name}-i.{shopid}.{itemid}"
                image_url = f"https://down-br.img.susercontent.com/file/{image}"
                score = sold * rating
                
                processed_items.append({
                    "id": itemid,
                    "name": name,
                    "price": price,
                    "sold": sold,
                    "rating": rating,
                    "score": score,
                    "url": url,
                    "image_url": image_url
                })
            
            processed_items.sort(key=lambda x: x["score"], reverse=True)
            final_items = processed_items[:limit]
            print(f"[+] Scan Selenium Sucesso! {len(final_items)} itens.")

        os.makedirs(".tmp", exist_ok=True)
        with open(".tmp/products_raw.json", "w", encoding="utf-8") as f:
            json.dump(final_items, f, indent=2, ensure_ascii=False)
            
        return final_items

    except Exception as e:
        print(f"[!] Erro durante navegação: {e}")
        mock = get_mock_products()
        os.makedirs(".tmp", exist_ok=True)
        with open(".tmp/products_raw.json", "w", encoding="utf-8") as f:
            json.dump(mock, f, indent=2, ensure_ascii=False)
        return mock
        
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    scan_shopee_products()
