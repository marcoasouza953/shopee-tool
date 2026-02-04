import json
import os

def create_mock_data():
    """
    Cria um arquivo products_raw.json com dados reais de exemplo
    para permitir que o fluxo continue mesmo com bloqueio da API Shopee.
    """
    print("[*] API Shopee instável. Gerando lista de produtos populares para demonstração...")
    
    mock_products = [
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
    
    os.makedirs(".tmp", exist_ok=True)
    with open(".tmp/products_raw.json", "w", encoding="utf-8") as f:
        json.dump(mock_products, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Dados de exemplo gerados ({len(mock_products)} produtos) em .tmp/products_raw.json")

if __name__ == "__main__":
    create_mock_data()
