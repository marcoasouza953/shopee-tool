# Diretiva: Análise de Produtos Shopee e Buscador de Vídeos

## Objetivo
Identificar produtos com alto potencial de vendas na Shopee Brasil e encontrar vídeos correlatos no TikTok e Kwai para criação de conteúdo de afiliado.

## Inputs
- Termo de busca (opcional, padrão: "ofertas do dia" ou categorias populares)
- Limite de produtos: 50

## Tools & Scripts
1. `execution/shopee_scanner.py`
   - **Função**: Coleta dados de produtos da API da Shopee.
   - **Output**: `.tmp/products_raw.json`
2. `execution/video_finder.py`
   - **Função**: Busca vídeos no TikTok e Kwai usando Google Dorking para os produtos listados.
   - **Input**: `.tmp/products_raw.json`
   - **Output**: `.tmp/products_with_videos.json`
3. `execution/report_generator.py`
   - **Função**: Gera um relatório HTML amigável p/ o usuário.
   - **Input**: `.tmp/products_with_videos.json`
   - **Output**: `relatorio_produtos.html`

## Fluxo de Execução
1. Executar `execution/shopee_scanner.py` para gerar a lista base.
2. Validar se `products_raw.json` foi criado e não está vazio.
3. Executar `execution/video_finder.py` para enriquecer os dados com links de vídeos.
4. Executar `execution/report_generator.py` para criar a visualização final.
5. Avisar o usuário que o relatório está pronto em `relatorio_produtos.html`.

## Edge Cases & Tratamento de Erros
- **Falha na API Shopee**: Se a API mudar ou bloquear, o script deve falhar graciosamente e avisar. Tentar usar User-Agent rotativo se necessário.
- **Google Rate Limit**: A busca de vídeos usa queries do Google. Se houver erro 429, o script deve esperar ou alertar o usuário para tentar mais tarde. Implementar delay entre buscas.
- **Produtos sem vídeos**: O relatório deve indicar "Nenhum vídeo encontrado" em vez de quebrar.
