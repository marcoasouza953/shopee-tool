import json
import os

def generate_report(input_file=".tmp/products_with_videos.json", output_file="relatorio_produtos.html"):
    """
    Gera um relatório HTML estilizado com os produtos e vídeos encontrados.
    """
    try:
        with open(input_file, "r") as f:
            products = json.load(f)
    except FileNotFoundError:
        print(f"[!] Arquivo {input_file} não encontrado.")
        return

    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Radar de Produtos Shopee + Vídeos</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css">
        <style>
            body { font-family: 'Inter', sans-serif; background: #f4f6f8; margin: 0; padding: 20px; color: #333; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            h1 { color: #ee4d2d; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
            .badge { background: #ee4d2d; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { text-align: left; padding: 12px; border-bottom: 1px solid #eee; vertical-align: middle; }
            th { background: #fafafa; font-weight: 600; color: #555; }
            .product-cell { display: flex; align-items: center; gap: 15px; }
            .product-img { width: 60px; height: 60px; object-fit: cover; border-radius: 6px; border: 1px solid #eee; }
            .product-info a { color: #333; text-decoration: none; font-weight: 600; display: block; margin-bottom: 4px; }
            .product-info a:hover { color: #ee4d2d; }
            .video-links a { display: inline-block; margin-right: 8px; text-decoration: none; color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.85em; margin-bottom: 4px; }
            .tiktok-btn { background: #000; }
            .kwai-btn { background: #ff7e05; }
            .metrics { font-size: 0.9em; color: #666; }
            .metrics strong { color: #333; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛍️ Radar Afiliado Shopee <span class="badge">Top """ + str(len(products)) + """</span></h1>
            <p>Lista dos produtos mais promissores gerada automaticamente. Use os links para criar seus conteúdos.</p>
            
            <table id="productsTable">
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Métricas (Vendas/Nota)</th>
                        <th>Score</th>
                        <th>Vídeos Sugeridos</th>
                    </tr>
                </thead>
                <tbody>
    """

    for p in products:
        tiktok_html = ""
        for link in p.get("tiktok_links", [])[:2]:
            tiktok_html += f'<a href="{link}" target="_blank" class="tiktok-btn">TikTok</a>'
            
        kwai_html = ""
        for link in p.get("kwai_links", [])[:2]:
            kwai_html += f'<a href="{link}" target="_blank" class="kwai-btn">Kwai</a>'
            
        videos_html = tiktok_html + kwai_html
        if not videos_html:
            videos_html = "<span style='color:#999; font-size:0.9em'>Sem vídeos encontrados</span>"

        html_content += f"""
        <tr>
            <td>
                <div class="product-cell">
                    <img src="{p['image_url']}" class="product-img" onerror="this.src='https://via.placeholder.com/60'">
                    <div class="product-info">
                        <a href="{p['url']}" target="_blank">{p['name'][:60]}...</a>
                    </div>
                </div>
            </td>
            <td>
                <div class="metrics">
                    📦 Vendidos: <strong>{p['sold']}</strong><br>
                    ⭐ Nota: <strong>{p['rating']:.1f}</strong><br>
                    💰 Preço: <strong>R$ {p['price']:.2f}</strong>
                </div>
            </td>
            <td><strong>{p['score']:.0f}</strong></td>
            <td class="video-links">{videos_html}</td>
        </tr>
        """

    html_content += """
                </tbody>
            </table>
        </div>

        <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
        <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready(function() {
                $('#productsTable').DataTable({
                    "order": [[ 2, "desc" ]], // Ordenar por Score decrescente
                    "pageLength": 25,
                    "language": {
                        "search": "🔍 Filtrar:",
                        "lengthMenu": "Mostrar _MENU_ produtos",
                        "info": "Mostrando _START_ a _END_ de _TOTAL_",
                        "paginate": { "first": "Inicio", "last": "Fim", "next": "Próximo", "previous": "Anterior" }
                    }
                });
            });
        </script>
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"[+] Relatório gerado com sucesso: {output_file}")

if __name__ == "__main__":
    generate_report()
