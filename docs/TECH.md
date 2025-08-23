# Technical Choices


A aplicação consistirá de uma série de microserviços com as seguintes escolhas:

- Frontends em React + TypeScript (Vite)
- Backends em Python
- Backends em Rust quando fizer sentido


## Escolhas globais:


| Camada / Domínio         | Escolha principal                                            | Justificativa pragmática                                                                                  |
| ------------------------ | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **Banco de Dados**       | **EdgeDB (Gel)** em cima do PostgreSQL                       | Schema declarativo único (`.esdl`), migrações automáticas, geração de clientes tipados para Python/Rust.  |
| **ORM / Modelagem**      | **EdgeQL + codegen**                                         | Evita duplicar modelos entre linguagens; mantém um único “fonte da verdade” para o schema.                |
| **Tarefas assíncronas**  | **Hatchet** (com Postgres backend)                           | Jobs duráveis, retries e rate limiting; mais simples que Kafka/Temporal para um dev solo.                 |
| **Comunicação síncrona** | **HTTP/REST**                                                | Menos complexidade; contratos via OpenAPI; fácil de consumir no frontend.                                 |
| **Observabilidade**      | **OpenTelemetry + Prometheus + Grafana**                     | EdgeDB já exporta métricas OTLP; fácil integração com stack de métricas/logs.                             |
| **Deploy / Ops**         | **Docker Compose (dev)** + **Fly.io/Railway (prod inicial)** | Simplicidade para um dev; upgrades fáceis; pode evoluir para Kubernetes se necessário.                    |
| **CI/CD**                | **GitHub Actions**                                           | Roda `edgedb migrate` + `edgedb generate` em cada commit; builds/testes automatizados.                    |

## Backends Python:

| Camada / Domínio         | Escolha principal                                            | Justificativa pragmática                                                                                  |
| ------------------------ | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **Backend Python**       | **FastAPI + Uvicorn**                                        | Simples, tipado, documentação automática; alta produtividade.                                             |
| **DI em Python**         | **Antidote**                                                 | Leve, tipagem estática, funciona também em workers (Hatchet); substitui `Depends` quando necessário.      |

## Backends Rust:

| Camada / Domínio         | Escolha principal                                            | Justificativa pragmática                                                                                  |
| ------------------------ | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **Backend Rust**         | **Axum** (REST)                                              | Idiomático, baseado em Tower; integração fácil com `State`; comunidade crescente.                         |
| **DI em Rust**           | **Traits + construtores + Arc + axum::State**                | Injecção via composição explícita; testabilidade via `mockall`; container (shaku) só se precisar runtime. |

# Frontend

| Camada / Domínio         | Escolha principal                                            | Justificativa pragmática                                                                                  |
| ------------------------ | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **Frontend**             | **React + TypeScript (Vite)**                                | Rápido para dev, ecossistema maduro; consumo via OpenAPI SDK.                                             |
