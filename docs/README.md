# AutoMedia AI — Documentação Oficial

Bem-vindo ao índice documental da plataforma AutoMedia AI. 
Esta pasta contém a base de conhecimento estrutural e de engenharia do projeto.

## Hierarquia Completa de Autoridade

1. **Documento 000 — Project Charter:** É a constituição. Nenhuma decisão pode violá-lo.
2. **RFCs Aprovadas:** Requests For Change que alteram formalmente o Charter.
3. **Documento 000A — Core Architecture Principles:** As leis imutáveis da engenharia e código.
4. **ADRs Aprovados (Architecture Decision Records):** Histórico de escolhas tecnológicas pontuais (ex: qual banco de dados?).
5. **Documento 000B — Glossário Oficial:** Referência transversal. Torna-se normativo somente após aprovação humana.
6. **Documentos Específicos do Domínio (001-003):** Visão de produto, modelagem.
7. **Especificações Funcionais e Técnicas (004-015):** Guias de UX, UI e Arquiteturas específicas (ex: AI, Banco).
8. **Backlog e Tarefas:** O escopo diário de execução.
9. **Decisões Locais de Implementação:** Escolhas efêmeras no código não cobertas pela documentação sênior.

## Regras de Conflito
Quando dois documentos divergirem em suas orientações, o agente (ou desenvolvedor) **não pode escolher silenciosamente**. O fluxo deve ser interrompido e a decisão solicitada ao responsável pela Arquitetura.

## Relações Documentais (Metadados OBRIGATÓRIOS)
Todo documento futuro a ser criado nesta base (exceto RFCs/ADRs efêmeros) deve possuir o seguinte cabeçalho estrutural YAML (ou similar em Markdown) para rastreabilidade:
```yaml
id: [Identificador único]
status: [Em revisão | Aprovado | Depreciado]
version: [X.Y.Z]
governed_by: [IDs dos documentos que este obedece]
depends_on: [IDs dos documentos pré-requisito]
governs: [IDs dos documentos que este comanda]
related_adrs: [Links para ADRs]
related_rfcs: [Links para RFCs]
```

## Matriz Detalhada por Tarefa

Antes de atuar em uma funcionalidade, os seguintes documentos são considerados de **leitura obrigatória**.

| Domínio de Atuação | Documentos Obrigatórios (Governantes) |
| :--- | :--- |
| **Referência Transversal de Termos** | `000B` (Documento aprovado. Referência normativa oficial para toda terminologia, documentação e código do projeto.) |
| **Telegram / Mensageria** | `000`, `000A`, `004`, `005`, `011` e `012` |
| **Processamento de Imagens** | `000`, `000A`, `003`, `004`, `007`, `008`, `011` e `012` |
| **Brand e Layout (Design System)**| `000`, `000A`, `003`, `004`, `006`, `008` e documentos das Engines |
| **Banco de Dados e Multitenancy**| `000A`, `003`, `008`, `010` e `012` |

## Status dos Documentos Atuais

| Documento | Título | Status |
| :--- | :--- | :--- |
| **000** | Project Charter | 🟢 Aprovado (Congelado) |
| **000A** | Core Architecture Principles | 🟢 Aprovado (Congelado) |
| **[000B](000B-official-glossary/README.md)** | Glossário Oficial | 🟢 Aprovado (1.0.0) |
| **[001](001-product-vision/README.md)** | Product Vision (orienta requisitos, UX, roadmap e validação comercial; depende de 000, 000A, 000B) | 🟢 Aprovado (1.0.0) |
| **[004](004-functional-requirements/README.md)** | Requisitos Funcionais Essenciais do MVP (governa comportamento funcional, critérios de aceite, escopo do spike técnico e backlog inicial; depende de 000, 000A, 000B, 001) | 🟢 Aprovado (1.0.0) |
| **[007](007-spike-technical-architecture/README.md)** | Arquitetura Técnica Mínima do Spike Local (governa arquitetura do spike, pipeline local e benchmark técnico; depende de 004) | 🟢 Aprovado (1.0.0) |
