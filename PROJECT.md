# Project Management


## Epic: Interface de administração para curar fontes.

Funcionalidades:
  - Autenticação Segura
    - [ ] Administradores Humanos na interface adicionando fontes
    - [ ] Outras componentes do sistema autenticando com system accounts para consultar informações
  - Gestão de fontes
  - Expor modelagem para as fontes para outras componentes do sistema

Tipos de conteúdo:  
  - [ ] Canais de vídeo
    - [ ] Youtube
    - [ ] Tiktok
    - [ ] Reels
  - [ ] RSS de Podcasts
  - [ ] RSS de Blogs
  - [ ] Plataformas Blog-like fechadas
    - [ ] Substack
  - [ ] Perfis de redes sociais
    - [ ] Bluesky

Prioridade:
  - Cadastrar canais de Youtube

### User Stories - Epic: Interface de administração

**US-001: Autenticação de Administrador**
- **Como** administrador humano
- **Eu quero** fazer login de forma segura na interface de administração
- **Para que** eu possa gerenciar fontes de conteúdo com segurança
- **Critérios de Aceitação:**
  - Sistema deve validar credenciais do administrador
  - Sessão deve ser segura e ter timeout apropriado
  - Deve haver proteção contra ataques de força bruta

**US-002: Cadastro de Canal do YouTube**
- **Como** administrador
- **Eu quero** cadastrar um canal do YouTube como fonte de conteúdo
- **Para que** o sistema possa coletar e indexar vídeos desse canal
- **Critérios de Aceitação:**
  - Deve aceitar URL ou ID do canal do YouTube
  - Deve validar se o canal existe e é acessível
  - Deve armazenar metadados básicos do canal (nome, descrição, etc.)
  - Deve permitir ativar/desativar a coleta de dados do canal

**US-003: Listagem de Fontes Cadastradas**
- **Como** administrador
- **Eu quero** visualizar todas as fontes cadastradas
- **Para que** eu possa gerenciar e monitorar o status das fontes
- **Critérios de Aceitação:**
  - Deve mostrar lista de todas as fontes com status
  - Deve permitir filtrar por tipo de fonte (YouTube, RSS, etc.)
  - Deve mostrar última atualização de cada fonte
  - Deve permitir editar ou remover fontes existentes


## Epic: Indexação Inicial

Cada fonte tem que ter uma funcionalidade para
    1. coletar metadados dos conteúdos da fonte
    2. indexar os metadados para serem buscados
  
Prioridade:
  - Coletar metadados de vídeos do youtube:
    - título
    - descrição
    - transcrição
    - comentários (será que a API permite?)
  - Esses dados devem ser processados e indexados em um servidor de busca

### User Stories - Epic: Indexação Inicial

**US-004: Coleta de Metadados Básicos do YouTube**
- **Como** sistema de indexação
- **Eu quero** coletar título e descrição dos vídeos de um canal do YouTube
- **Para que** os usuários possam encontrar conteúdo relevante através de busca
- **Critérios de Aceitação:**
  - Deve usar a API do YouTube para coletar dados
  - Deve coletar título, descrição, data de publicação, duração
  - Deve lidar com rate limits da API adequadamente
  - Deve armazenar dados de forma estruturada no banco de dados
  - Deve processar vídeos novos automaticamente

**US-005: Coleta de Transcrições de Vídeos**
- **Como** sistema de indexação
- **Eu quero** coletar transcrições automáticas dos vídeos do YouTube
- **Para que** o conteúdo falado possa ser pesquisado textualmente
- **Critérios de Aceitação:**
  - Deve tentar obter legendas automáticas quando disponíveis
  - Deve suportar múltiplos idiomas
  - Deve armazenar transcrições com timestamps
  - Deve lidar graciosamente com vídeos sem transcrição disponível

**US-006: Indexação para Busca**
- **Como** sistema de busca
- **Eu quero** indexar os metadados coletados em um servidor de busca
- **Para que** os usuários possam fazer consultas rápidas e relevantes
- **Critérios de Aceitação:**
  - Deve indexar título, descrição e transcrição em servidor de busca (ex: Elasticsearch)
  - Deve suportar busca por texto completo
  - Deve permitir filtros por data, canal, duração
  - Deve atualizar índices quando novos vídeos são adicionados
  - Deve ter performance adequada para consultas em tempo real

**US-007: Coleta de Comentários (Investigação)**
- **Como** sistema de indexação
- **Eu quero** investigar a viabilidade de coletar comentários dos vídeos
- **Para que** possamos decidir se incluir comentários na indexação
- **Critérios de Aceitação:**
  - Deve verificar limitações da API do YouTube para comentários
  - Deve avaliar volume de dados e impacto na performance
  - Deve considerar questões de privacidade e moderação
  - Deve documentar recomendações para implementação futura