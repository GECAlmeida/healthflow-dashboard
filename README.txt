========================================
CÓDIGO-FONTE - HEALTHFLOW
========================================

Esta pasta contém todo o código-fonte do projeto HealthFlow.

========================================
ESTRUTURA DO PROJETO
========================================

healthflow_dashboard_mockup/
├── client/                    # Frontend (React)
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.tsx      # Dashboard principal
│   │   │   └── NotFound.tsx  # Página 404
│   │   ├── components/       # Componentes React
│   │   ├── data/
│   │   │   └── patients.json # Dados dos pacientes
│   │   ├── App.tsx           # Componente raiz
│   │   ├── main.tsx          # Entry point
│   │   └── index.css         # Estilos globais
│   ├── public/               # Arquivos estáticos
│   └── index.html            # HTML principal
│
├── server/                    # Backend (Node.js/Express)
│   └── index.ts              # Servidor Express
│
├── shared/                    # Código compartilhado
│   └── const.ts              # Constantes
│
├── package.json              # Dependências do projeto
├── tsconfig.json             # Configuração TypeScript
├── vite.config.ts            # Configuração Vite
└── README.md                 # Documentação

========================================
TECNOLOGIAS UTILIZADAS
========================================

Frontend:
- React 19.2.1
- TypeScript 5.6.3
- Tailwind CSS 4.1.14
- shadcn/ui (componentes)
- Lucide React (ícones)
- Wouter (roteamento)

Backend:
- Node.js 22.13.0
- Express 4.21.2
- TypeScript

Build & Deploy:
- Vite 7.1.7
- pnpm 10.15.1
- ESBuild

========================================
COMO EXECUTAR LOCALMENTE
========================================

1. INSTALAR DEPENDÊNCIAS
   pnpm install

2. INICIAR SERVIDOR DE DESENVOLVIMENTO
   pnpm dev
   
   Acesse: http://localhost:3000

3. BUILD PARA PRODUÇÃO
   pnpm build
   
   Cria pasta 'dist' com arquivos otimizados

4. INICIAR SERVIDOR DE PRODUÇÃO
   pnpm start

========================================
COMPONENTES PRINCIPAIS
========================================

HOME.TSX
- Dashboard principal
- Lista de pacientes com scores
- Filtros por risco, busca, ordenação
- Estatísticas em tempo real

COMPONENTS/UI/
- Button, Card, Badge, Input, Select
- Table, Dialog, Dropdown, etc.
- Todos os componentes shadcn/ui

DATA/PATIENTS.JSON
- 50 pacientes com scores de risco
- Utilizado para popular o dashboard

========================================
FLUXO DE DADOS
========================================

1. Dados carregados de: data/patients.json
2. Estado gerenciado com React Hooks (useState, useEffect)
3. Filtros e busca aplicados em tempo real
4. Componentes renderizados com Tailwind CSS
5. Interface responsiva e acessível

========================================
VARIÁVEIS DE AMBIENTE
========================================

Não há variáveis de ambiente obrigatórias para o dashboard.

Opcionais (para futuras integrações):
- VITE_API_URL: URL da API backend
- VITE_ANALYTICS_ID: ID do Google Analytics
- VITE_APP_TITLE: Título da aplicação

========================================
COMO FAZER DEPLOY
========================================

Opção 1: VERCEL (Recomendado)
1. Fazer push do código para GitHub
2. Conectar repositório ao Vercel
3. Vercel faz build e deploy automaticamente
4. URL: https://seu-projeto.vercel.app

Opção 2: NETLIFY
1. Fazer push do código para GitHub
2. Conectar repositório ao Netlify
3. Configurar: Build command: "pnpm build"
4. Publish directory: "dist"

Opção 3: GITHUB PAGES
1. Fazer push do código para GitHub
2. Configurar GitHub Actions para deploy
3. URL: https://seu-usuario.github.io/healthflow

========================================
ESTRUTURA DE PASTAS EXPLICADA
========================================

client/src/pages/
- Componentes de página (Home, NotFound)
- Cada página é uma rota

client/src/components/
- Componentes reutilizáveis
- Componentes UI do shadcn/ui

client/src/data/
- Dados estáticos (JSON)
- Dados de exemplo para o dashboard

client/src/lib/
- Funções utilitárias
- Helpers e utilities

client/public/
- Arquivos estáticos (favicon, robots.txt)
- Servidos na raiz do site

server/
- Código backend (Node.js/Express)
- Atualmente é um placeholder
- Pode ser expandido para API futura

========================================
PRINCIPAIS ARQUIVOS
========================================

Home.tsx
- 300+ linhas
- Lógica do dashboard
- Filtros, busca, ordenação
- Estatísticas em tempo real

App.tsx
- Configuração de rotas
- Theme Provider
- Layout global

index.css
- Estilos globais
- Variáveis CSS
- Tema (light/dark)

package.json
- Dependências do projeto
- Scripts de build e deploy

========================================
COMO CONTRIBUIR
========================================

1. Clonar o repositório
   git clone https://github.com/seu-usuario/healthflow-dashboard.git

2. Criar branch para feature
   git checkout -b feature/sua-feature

3. Fazer alterações e commits
   git add .
   git commit -m "Descrição da mudança"

4. Push para GitHub
   git push origin feature/sua-feature

5. Criar Pull Request

========================================
TROUBLESHOOTING
========================================

Erro: "pnpm: comando não encontrado"
Solução: npm install -g pnpm

Erro: "Port 3000 already in use"
Solução: pnpm dev -- --port 3001

Erro: "Module not found"
Solução: pnpm install

Erro: "TypeScript errors"
Solução: pnpm check

========================================
PRÓXIMAS ETAPAS
========================================

1. Implementar backend API
2. Conectar com banco de dados
3. Integrar com sistema de agendamento
4. Adicionar autenticação
5. Implementar notificações em tempo real
6. Expandir para mobile app

========================================
DOCUMENTAÇÃO ADICIONAL
========================================

- ../04_Documentacao/Fluxo_Operacional.md
- ../04_Documentacao/Arquitetura_Solucao.md
- ../04_Documentacao/Validacao_Modelo.md

========================================
CONTATO & SUPORTE
========================================

GitHub: https://github.com/seu-usuario/healthflow-dashboard
Email: seu-email@example.com
Issues: https://github.com/seu-usuario/healthflow-dashboard/issues

========================================
