# SecurityScore Simplificado

Projeto inspirado no SecurityScorecard para monitoramento contínuo da postura de segurança cibernética.

## Funcionalidades

- Enumeração de subdomínios
- Busca por vazamentos no GitHub
- Escaneamento de vulnerabilidades web
- Geração de score (0–100)
- Notificações automáticas por e-mail, Slack e Google Chat
- Automatizado via GitHub Actions
- Painel web estático via GitHub Pages

## Como usar

1. Configure os segredos no GitHub (SMTP, Slack, etc.)
2. Ative o GitHub Pages
3. Projeto roda toda segunda-feira automaticamente

Para mais detalhes, veja o workflow `.github/workflows/automate.yml`.
