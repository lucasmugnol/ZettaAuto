---
id: 000A
status: Aprovado
version: 1.0.0
governed_by: [000]
depends_on: [000]
governs: [001-015, ADRs, RFCs]
related_adrs: []
related_rfcs: []
---

# Documento 000A — Core Architecture Principles

**Status:** Aprovado e Congelado  
**Última Atualização:** 21 de Julho de 2026  
**Versão:** 1.0.0  
**Responsável:** Arquitetura / Engenharia Principal  
**Resumo:** Manual Oficial da Engenharia contendo as regras arquiteturais e princípios para o desenvolvimento de todo o ecossistema AutoMedia AI.

---

## 1. Introdução

### 1.1 Objetivo do documento
Este documento estabelece as leis arquiteturais do projeto **AutoMedia AI**. Enquanto o Documento 000 (Project Charter) define *o que* estamos construindo e o *porquê*, o **Documento 000A** define estritamente *como* construiremos, focando na sustentabilidade, escalabilidade e qualidade do código. Não elegemos provedores tecnológicos específicos aqui (isso pertence aos ADRs), mas definimos os moldes de como qualquer provedor deve ser integrado.

### 1.2 Escopo
Abarca todos os repositórios, serviços, microsserviços, plugins, integrações e componentes de infraestrutura criados sob a bandeira da AutoMedia AI.

### 1.3 Responsabilidades
É dever ético e técnico de todo Desenvolvedor, Arquiteto ou Agente de IA aderir rigorosamente a este documento. Os princípios são obrigatórios enquanto vigentes e só podem ser alterados mediante RFC aprovada. O não cumprimento leva à rejeição sumária em fase de Code Review.

### 1.4 Como utilizar este documento
Este manual atua como o principal balizador de *Trade-offs* da equipe. Ele deve ser lido *antes* de iniciar qualquer *Feature Branch*.

---

## 2. Filosofia da Arquitetura

O ecossistema é mantido vivo pelos seguintes dogmas fundamentais:

*   **Engine First:** Interfaces (UI) são efêmeras, Motores (Engines) são duradouros. Toda regra de negócio é construída dentro de Engines que não possuem conhecimento da camada de apresentação.
*   **Automation First:** Se uma tarefa humana pode ser repetida logicamente, ela deve ser codificada.
*   **Open Source First:** O código deve priorizar ecossistemas abertos maduros. Contudo, "Open Source" não significa "Custo Zero". A licença deve permitir uso comercial, pesos de modelos de ML precisam de validação legal, e os custos de GPU, infraestrutura, maturidade e manutenção permanecem sendo critérios obrigatórios (a serem aprofundados no Documento 007).
*   **Brand First:** O respeito matemático ao *Design Token* da empresa antecede decisões estéticas genéricas da IA.
*   **AI Replaceable:** O sistema trata toda IA como uma *dependência periférica injetada*, nunca acoplada ao core.
*   **Zero Vendor Lock-in:** O núcleo da aplicação independe de nuvens ou infraestruturas específicas.
*   **Zero Manual Work:** Fluxos inteiros devem transitar como linhas de montagem automáticas.
*   **Invisible Software:** As integrações devem operar em background, não exigindo portais complexos.
*   **Customer Owns the Data:** A arquitetura garante que imagens operem efemeramente.
*   **Human Approval:** A IA sugere, o sistema processa mediante regras, e dados vitais exigem confirmação.
*   **Single Responsibility:** Cada módulo ou engine faz *apenas* uma coisa.
*   **Keep It Simple (KISS):** Abstrações prematuras devem ser evitadas.
*   **Documentation Driven Development:** Código não documentado é código legado.

---

## 3. Princípios Arquiteturais

### 3.1 SOLID
Obediência restrita aos princípios SOLID em toda a base de código orientada a objetos.

### 3.2 Clean Architecture & Hexagonal Architecture (Ports & Adapters)
A comunicação com o mundo externo (APIs, Mensageria, Bancos) se dá via *Ports* (interfaces do domínio) implementadas por *Adapters* na infraestrutura.

### 3.3 Domain-Driven Design (DDD)
A modelagem do sistema refletirá os domínios de negócio automotivos. 

### 3.4 Composition over Inheritance
Favorecemos a injeção de comportamentos isolados por meio da composição.

### 3.5 Dependency Inversion (DI)
Módulos de alto nível *jamais* instanciam dependências concretas diretamente.

### 3.6 Event-driven e Assincronia Consciente
A orquestração obedece a critérios mistos. Operações pesadas, demoradas, reprocessáveis ou sujeitas a picos devem ser assíncronas (filas/eventos). Operações locais, rápidas e transacionais podem ser síncronas por chamadas a interfaces internas (ports). Abstrações prematuras e assincronia absoluta devem ser evitadas para não inflar a complexidade do monólito.

### 3.7 Workflow Orientado a Estado Persistido
A arquitetura utilizará um *Event-driven workflow* com estado persistido convencional. Uma máquina de estados controlará o avanço do anúncio na esteira (ex: "Processando", "Renderizando"), guardando histórico operacional básico. A adoção de *Event Sourcing* real está explicitamente fora do escopo do MVP.

### 3.8 Modular Monolith Ready → Future Microservices
No dia 1, nasceremos como um **Monolito Modular** altamente coeso, onde cada contexto (Engine) vive no mesmo repositório sob módulos isolados. Isso reduz custos de deploy e simplifica a observabilidade no MVP. Extrairemos serviços físicos somente quando houver uma razão mensurável e inegociável.

---

## 4. Estrutura Oficial do Projeto

O layout do monorepo segue o padrão estrito de separação de domínios.

```text
automedia-ai/
├── docs/                 # Documentação oficial, RFCs, ADRs e especificações técnicas
├── backend/              # Core Services e Engines 
├── frontend/             # Dashboards e web components 
├── ai-services/          # Adapters, Plugins de inferência e workers
├── infrastructure/       # IaC, configurações de Nuvem e Manifestos
├── docker/               # Dockerfiles de ambiente local/dev
├── scripts/              # Automações de CI/CD, scaffolding, dev-tools
├── tests/                # Testes end-to-end e testes de integração globais
├── assets/               # Recursos estáticos primários
└── README.md
```

**Justificativa:** Garantir o desacoplamento visual. Ao olhar o diretório raiz, identifica-se imediatamente a fronteira entre lógica de negócio (`backend`), workers intensivos (`ai-services`) e infraestrutura (`infrastructure`).

---

## 5. Engines Oficiais

Cada domínio principal é encapsulado no que chamamos de **Engines**.

### 5.1 Vision Engine
* **Objetivo:** Interpretar e analisar a imagem bruta (O "olho" autônomo).
* **Entradas:** Imagem original.
* **Saídas:** Metadados estruturados (Bounding Boxes, Condições de iluminação, Ângulo de câmera).
* **Responsabilidades:** Contextualizar a semântica da cena fotográfica.
* **O que NÃO pode fazer:** Modificar a imagem ou ler tabelas de marca.

### 5.2 Image Engine
* **Objetivo:** Preparar tecnicamente a infraestrutura dos ativos visuais.
* **Entradas:** Imagem bruta + Metadados + Regras de Cropping.
* **Saídas:** Blob da Imagem polida (ex: fundo cortado).
* **Responsabilidades:** Trabalhar os pixels em nível atômico.
* **O que NÃO pode fazer:** Diagramar criativos ou formatar textos.

### 5.3 Brand Engine
* **Objetivo:** Gerenciar regras de identidade visual.
* **Entradas:** Identifier do Tenant/Cliente.
* **Saídas:** Design Tokens em formato de DTO (Paletas, Tipografia, Logo).
* **Responsabilidades:** Fornecer átomos vitais de configuração.
* **O que NÃO pode fazer:** Transformar tokens diretamente num PNG.

### 5.4 Layout Engine
* **Objetivo:** O motor final de orquestração gráfica visual.
* **Entradas:** `RenderRequestDTO` (Orquestrado externamente, contendo Imagem Processada, Brand Snapshot, Variação de Layout e Copy aprovado).
* **Saídas:** Arquivo final exportado.
* **Responsabilidades:** Fundir logicamente o contexto semântico à identidade do lojista de forma orgânica.
* **O que NÃO pode fazer:** Buscar informações ativamente no banco de dados de outras Engines. Ele recebe o contrato fechado e o obedece.

### 5.5 Marketing Engine
* **Objetivo:** Transformar os specs do veículo em *copywriting* persuasivo.
* **Entradas:** Dados do veículo explicitamente informados ou confirmados pelo usuário.
* **Saídas:** Títulos de impacto, Descrições, CTAs.
* **Responsabilidades:** Geração e otimização de texto orientada a conversão.
* **O que NÃO pode fazer:** Tomar dados sugeridos por IA (como "teto solar detectado na imagem") como verdades absolutas sem confirmação. A origem do dado publicado deve ser segura e auditável.

### 5.6 Delivery Engine
* **Objetivo:** Encaminhar a entrega final para o ecossistema de origem.
* **Entradas:** Payload de artefatos + Canal de Destino.
* **Saídas:** Status de sucesso ou arquivo ZIP.
* **Responsabilidades:** Comprimir pacotes e postar no webhook correto.
* **O que NÃO pode fazer:** Processar ou validar assets lógicos.

### 5.7 Workspace Engine
* **Objetivo:** O gestor do isolamento multitenancy do sistema. Blinda e protege o escopo de cada empresa.

### 5.8 Identity Engine
* **Objetivo:** Autenticação e controle de escopo estrito no acesso à plataforma.

---

## 6. Comunicação e Isolamento de Banco no Monólito

> [!CAUTION]
> **A Regra de Ouro do Acoplamento:** Nenhuma Engine poderá conhecer a implementação de outra.

### 6.1 Contratos Puros (Interfaces & Ports)
A comunicação inter-domínios ocorrerá mediante DTOs e Interfaces Puras.

### 6.2 Regra de Banco de Dados no Monolito Modular
* Cada módulo/engine é dono exclusivo de suas próprias tabelas.
* Outros módulos não escrevem nessas tabelas diretamente.
* Leituras cruzadas podem ocorrer via serviços de aplicação, *views* específicas ou read models (projeções) para garantir performance.
* A proibição absoluta de `JOINs` físicos será postergada e avaliada apenas no dia em que houver a separação real de microsserviços.

---

## 7. Arquitetura do AI Gateway

O **AI Gateway** garante a portabilidade e segurança na comunicação com LLMs e Modelos de Visão. Suas responsabilidades são divididas internamente em:

1. **AI Provider Port:** A interface unificada esperada pelos módulos internos.
2. **Model Adapter:** A tradução técnica para o SDK do modelo (*exemplo meramente ilustrativo: Adapter do Claude, Adapter da OpenAI*).
3. **AI Policy:** Regras de permissões e sanitização do prompt/output.
4. **Resilience Layer:** Rate limiting, Retry e Circuit Breaker.
5. **Result Normalizer:** Converte as respostas caóticas das APIs externas no DTO formatado que o sistema espera.

### 7.1 Regras de Fallback
A troca de um modelo principal por um substituto (Fallback) **jamais** deve ser invisível.
Modelos geram resultados visualmente e textualmente variados. O fallback deve ser permitido por operação, configurável, rigorosamente registrado nos logs, validado por métricas de qualidade e totalmente visível para o time de observabilidade.

---

## 8. Estratégia de Plugins e Adapters (MVP)

A complexidade de um "Plugin Manager" dinâmico carregando arquivos em *runtime* num marketplace interno foi preterida para o MVP.
Adotamos uma estratégia simples e robusta de **Adapters Selecionados por Configuração**.

O ambiente dita o provedor a ser instanciado via Dependency Injection. Exemplo (Variáveis de Ambiente meramente ilustrativas e não vinculantes):
```env
BACKGROUND_REMOVER_PROVIDER=provider_a
TEXT_PROVIDER=provider_b
RENDER_PROVIDER=provider_c
```
Somente se houver extrema necessidade futura evoluiremos para uma descoberta dinâmica em tempo de execução.

---

## 9. Contratos (Regras Oficiais de Isolamento)

*   **Somente Data Transfer Objects (DTO):** Se uma Engine necessitar compartilhar seu produto com outra Engine, ela repassa DTOs. As `Entities` (Classes do DB de origem) nunca podem vazar suas bordas.
*   **Identificação Temporária:** Arquivos e processos terão `UUIDs` efêmeros.

---

## 10. Versionamento

O sistema utilizará Semantic Versioning (SemVer) aplicado não só no código base, mas de forma fragmentada:
*   **APIs (Síncronas):** Versionamento via rota explícita `/api/v1/resource` ou via Headers.
*   **Eventos:** O Payload dos eventos será versionado no namespace. (Ex: `VehicleDetected.v1`).

---

## 11. Logging (Observabilidade Ouro)

O projeto possui banimento moral do log caótico desestruturado.
Os registros (logs) operam obrigatoriamente no padrão **ESTRUTURADO (JSON)**, gerenciados por um *Telemetry Provider*.

Cada log *obriga* a injeção do cabeçalho de rastreio contendo:
* **Level:** INFO / WARN / ERROR.
* **Correlation ID:** Identificador único desde a entrada da requisição, propagado até a saída final. Essencial para rastrear toda a saga da imagem.
* **Component:** A Engine culpada.

---

## 12. Tratamento de Erros

**Nenhum módulo poderá lançar *Uncaught Exceptions* que causem crash no worker.** Erros devem ser capturados e encapsulados.

Todos os erros emitidos devem possuir:
1.  **Código (Code)**
2.  **Categoria:** `Validation` | `Network` | `Infrastructure` | `External`
3.  **Mensagem Clara**
4.  **Sugestão (Hint)**
5.  **Stack Trace** (Apenas ambientes dev/homolog ou exportado centralizadamente).

---

## 13. Observabilidade

*   **Health Check:** Pontos de checagem automatizados (`/readiness`, `/liveness`).
*   **Metrics e Tracing:** Adoção de padrões abertos (ex: OpenTelemetry spec) para rastrear o tempo de execução entre eventos e gargalos da rede.

---

## 14. Performance (Metas Percentis)

A meta de velocidade não deve ser um número fixo isolado, pois depende de variáveis mutáveis (resolução das fotos, filas, hardware).
* A meta real deve ser estabelecida via *percentis*, vinculada a um cenário controlado (baseline).
* Exemplo Prático: **P95 inferior a 90 segundos para um lote padrão de até 12 fotos (resolução média 12MP).**
* Um *Queue Provider* atuará como amortecedor de requisições de pico para proteger a escalabilidade estável.

---

## 15. Segurança Inegociável

*   **Least Privilege (Menor Privilégio):** Aplicações, roles e tokens operam com escopo mínimo.
*   **Temporary Storage:** A foto recebida é apagada em X horas. O *Object Storage Provider* gerenciará o TTL (Time-To-Live).
*   **No Hardcoded Credentials:** Repositórios limpos. Uso de variáveis de ambiente.

---

## 16. Padrões de Código

*   **Naming:** Intenção é tudo. Variáveis revelam conteúdo sem ambiguidades.
*   **Estrutura de Pastas:** Consistente através das lógicas de Contexto Delimitado.
*   **Comentários de Decisão:** O código descreve "o que". Comentários descrevem "por que" foi feito daquela maneira.

---

## 17. Padrões para IA

1.  **A IA nunca inventa.** Alucinações não são toleradas em campos rígidos.
2.  **A IA apenas interpreta** e sugere dados não confiáveis até que o operador humano confirme.
3.  **Toda IA deve ser substituível** de maneira programática sem afetar a lógica central.

---

## 18. Padrões de Construção de Layout

*   **Não existem Templates puros; Existem Identidades Reativas.**
*   Construímos através de **Design Tokens** (As constantes atômicas da marca, como Cor, Fonte).
*   A variação gráfica atende à Identidade, jamais sacrificando o Brand DNA da empresa para aplicar estéticas genéricas.

---

## 19. Checklist Arquitetural Obrigatório

Pull Requests necessitarão de resposta aos seguintes critérios:
- [ ] Respeitou os princípios do Documento 000A?
- [ ] Criou acoplamento direto desnecessário?
- [ ] Injetou dependência concreta ao invés de abstração?
- [ ] Incluiu bibliotecas que forçam *Vendor Lock-in*?
- [ ] Documentou as interfaces públicas e contratos modificados?

---

## 20. Conclusão e Governança

Este manual é vivo e evolui, porém os princípios estabelecidos nele são de cumprimento obrigatório enquanto vigentes. Operações que desafiam este *Core Architecture Principles* demandam discussão técnica aberta através de RFC. Estabelecemos o Monólito Modular para acelerar o desenvolvimento inicial com consistência de alto nível, preparando o terreno de longo prazo para um futuro microsserviço sem a necessidade de reescrever todo o software.

---
*Fim do Documento 000A.*
