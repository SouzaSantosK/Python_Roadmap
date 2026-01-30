DELETE FROM articles

SELECT * FROM articles

INSERT INTO articles (article_title, article_content, article_date) VALUES 
(
    'Arquitetura MVC', 
    'Neste artigo, exploramos como é construir um sistema web sem o uso de frameworks, lidando manualmente com sockets e protocolos, como HTTP.', 
    '2025-01-15'
),
(
    'Por que o PostgreSQL?', 
    'Uma análise sobre a robustez do PostgreSQL, o uso de SQL puro e a importância de entender transações e integridade de dados.', 
    '2024-01-20'
),
(
    'A Arte do Código Limpo', 
    'Organizar o projeto seguindo o padrão Model-View-Controller ajuda na manutenção e escalabilidade.', 
    '2025-01-30'
),
(
    'Entendendo Cookies de Sessão', 
    'Como o servidor utiliza o header Set-Cookie para manter o estado do usuário entre as requisições em um ambiente originalmente stateless.', 
    '2026-01-30'
);