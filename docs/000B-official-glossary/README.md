---
id: 000B
title: Glossário Oficial
status: Aprovado
version: 1.0.0
owner: Produto e Arquitetura
governed_by:
  - 000
  - 000A
depends_on:
  - 000
  - 000A
governs:
  - terminologia do projeto
  - documentação futura
related_adrs: []
related_rfcs: []
---

# Documento 000B — Glossário Oficial

**Status:** Aprovado  
**Versão:** 1.0.0  

---

## 1. Introdução

O objetivo deste **Glossário Oficial** é estabelecer a linguagem canônica do ecossistema AutoMedia AI, eliminando ambiguidades entre produto, negócio, arquitetura, inteligência artificial, processamento de imagens, identidade visual, infraestrutura e operação. Uma linguagem comum evita erros de interpretação que causam bugs e desalinhamentos estratégicos.

**Quem deve utilizá-lo:** Arquitetos, engenheiros, PMs, designers e Agentes de Inteligência Artificial. Este documento será obrigatório para documentação, código, nomes de módulos, contratos, APIs, eventos, banco de dados, backlog, UX e prompts.

**Atualização e Relacionamento:** Este glossário consolida termos; não toma decisões arquiteturais. A relação com ADRs e RFCs é restrita: definições terminológicas são registradas aqui, mas decisões tecnológicas exigem documentos específicos.

---

## 2. Regras de Nomenclatura

*   **Idioma principal da documentação:** Português Brasileiro (pt-BR).
*   **Termos técnicos em Inglês:** Permitidos e encorajados para jargões de software (ex: *Pipeline, Gateway, Adapter*).
*   **Capitalização oficial:** Termos próprios do projeto sempre capitalizados no texto.
*   **Convenções de Código:** As regras estritas de nomenclatura no código (ex: DTO, pluralidade de rotas, eventos no passado, snake_case) são definidas no documento **013 - Development Standards**. O glossário mapeia o significado, mas não impõe a sintaxe física do repositório antes de uma decisão formal de implementação aprovada.

---

## 3. Formato das Entradas do Glossário

Cada termo documentado apresenta obrigatoriamente 12 campos: Categoria, Nome oficial, Nome técnico, Definição, Uso no AutoMedia AI, O que não significa, Sinônimos aceitáveis, Termos desencorajados ou proibidos, Exemplo correto, Exemplo incorreto, Documentos relacionados e Termos relacionados.

---


## 4. Conceitos de Produto e Negócio

### Administrador do Workspace

* **Categoria**: Sistema
* **Nome oficial**: Administrador do Workspace
* **Nome técnico**: Workspace Admin
* **Definição**: Usuário com privilégios de configuração e gestão de acessos dentro de um Workspace.
* **Uso no AutoMedia AI**: Responsável por aprovar faturamento e gerir outros usuários.
* **O que não significa**: O administrador do banco de dados global.
* **Sinônimos aceitáveis**: Gestor do Workspace
* **Termos desencorajados ou proibidos**: administrador do sistema
* **Exemplo correto**: O administrador do workspace convidou um novo operador.
* **Exemplo incorreto**: O sistema bloqueou o usuário sem aviso prévio.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Workspace

### Anúncio Automotivo

* **Categoria**: Negócio
* **Nome oficial**: Anúncio Automotivo
* **Nome técnico**: Automotive Advertisement
* **Definição**: Conjunto de informações e mídias que promove a venda de um veículo.
* **Uso no AutoMedia AI**: Unidade principal de saída gerada pelo sistema.
* **O que não significa**: Um contrato de venda.
* **Sinônimos aceitáveis**: Publicação de Veículo
* **Termos desencorajados ou proibidos**: Propaganda definitiva
* **Exemplo correto**: O sistema gerou o anúncio automotivo.
* **Exemplo incorreto**: A IA gerou um anúncio com dados não confirmados.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Criativo

### Aprovação Humana

* **Categoria**: Sistema
* **Nome oficial**: Aprovação Humana
* **Nome técnico**: Human In The Loop
* **Definição**: Etapa do fluxo de trabalho que requer intervenção explícita de um usuário.
* **Uso no AutoMedia AI**: Garante o controle de qualidade antes da publicação em canais.
* **O que não significa**: Um gargalo de processo.
* **Sinônimos aceitáveis**: Revisão Manual
* **Termos desencorajados ou proibidos**: Processo manual não automatizado
* **Exemplo correto**: O fluxo exige aprovação humana para orçamentos grandes.
* **Exemplo incorreto**: O fluxo dependeu de etapas manuais repetitivas para prosseguir.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Sugestão da IA

### Assinatura

* **Categoria**: Negócio
* **Nome oficial**: Assinatura
* **Nome técnico**: Subscription
* **Definição**: Contrato recorrente que concede acesso contínuo aos serviços da plataforma.
* **Uso no AutoMedia AI**: Mecanismo de controle de faturamento e acesso.
* **O que não significa**: Uma rubrica em papel.
* **Sinônimos aceitáveis**: Contrato Recorrente
* **Termos desencorajados ou proibidos**: Algema financeira
* **Exemplo correto**: A assinatura foi renovada automaticamente.
* **Exemplo incorreto**: Prendemos o cliente na algema.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Plano

### AutoMedia AI

* **Categoria**: Produto
* **Nome oficial**: AutoMedia AI
* **Nome técnico**: AutoMedia AI Platform
* **Definição**: Plataforma de inteligência artificial para automação de criação de anúncios automotivos.
* **Uso no AutoMedia AI**: Nome principal do produto de software.
* **O que não significa**: Uma agência de marketing humana.
* **Sinônimos aceitáveis**: Plataforma AutoMedia
* **Termos desencorajados ou proibidos**: Robô de vendas, Sistema mágico
* **Exemplo correto**: O usuário acessou o AutoMedia AI.
* **Exemplo incorreto**: O robô mágico AutoMedia fez tudo.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Workspace

### Brand DNA

* **Categoria**: Produto
* **Nome oficial**: Brand DNA
* **Nome técnico**: Brand DNA
* **Definição**: Estrutura de dados fundamental que armazena as características semânticas e visuais de um cliente.
* **Uso no AutoMedia AI**: Objeto base consumido pela inteligência artificial para decisões de design.
* **O que não significa**: Material genético biológico.
* **Sinônimos aceitáveis**: Essência da Marca
* **Termos desencorajados ou proibidos**: Alma do negócio
* **Exemplo correto**: O motor de inferência consultou o Brand DNA.
* **Exemplo incorreto**: Lemos a alma do negócio.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Brand Kit

### Brand Kit

* **Categoria**: Sistema
* **Nome oficial**: Brand Kit
* **Nome técnico**: Brand Kit
* **Definição**: Pacote de arquivos estáticos contendo logotipos, fontes e paletas de cores aprovados.
* **Uso no AutoMedia AI**: Recurso técnico importado e validado no sistema.
* **O que não significa**: Um pacote de marketing físico.
* **Sinônimos aceitáveis**: Kit de Marca
* **Termos desencorajados ou proibidos**: Pacote inviolável
* **Exemplo correto**: O usuário fez upload do Brand Kit atualizado.
* **Exemplo incorreto**: O sistema corrompeu o pacote de dados irrecuperavelmente.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Brand DNA

### Canal de Publicação

* **Categoria**: Negócio
* **Nome oficial**: Canal de Publicação
* **Nome técnico**: Publishing Channel
* **Definição**: Plataforma externa onde o anúncio automotivo é distribuído e exibido.
* **Uso no AutoMedia AI**: Destino de integração via API para envio de anúncios.
* **O que não significa**: Um canal de televisão.
* **Sinônimos aceitáveis**: Portal de Integração
* **Termos desencorajados ou proibidos**: Tubo de despejo
* **Exemplo correto**: O anúncio foi enviado ao canal de publicação.
* **Exemplo incorreto**: Despejamos os anúncios no tubo.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Formato de Publicação

### Capa do Anúncio

* **Categoria**: Produto
* **Nome oficial**: Capa do Anúncio
* **Nome técnico**: MainPhoto
* **Definição**: Imagem principal exibida como representação visual do anúncio automotivo.
* **Uso no AutoMedia AI**: Primeira imagem visualizada nos portais de venda.
* **O que não significa**: O único criativo do anúncio.
* **Sinônimos aceitáveis**: Imagem Principal
* **Termos desencorajados ou proibidos**: Foto isca
* **Exemplo correto**: A capa do anúncio foi renderizada.
* **Exemplo incorreto**: A isca fisgou o cliente.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Galeria

### Carrossel

* **Categoria**: Produto
* **Nome oficial**: Carrossel
* **Nome técnico**: Carousel
* **Definição**: Componente de interface que exibe múltiplos itens de mídia sequencialmente.
* **Uso no AutoMedia AI**: Formato de exibição da galeria nas redes sociais.
* **O que não significa**: Um brinquedo de parque.
* **Sinônimos aceitáveis**: Contêiner Sequencial
* **Termos desencorajados ou proibidos**: Roda de fotos
* **Exemplo correto**: O carrossel possui cinco imagens.
* **Exemplo incorreto**: A roda gira sem parar.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Galeria

### Cliente

* **Categoria**: Negócio
* **Nome oficial**: Cliente
* **Nome técnico**: Customer
* **Definição**: Entidade jurídica ou física que contrata os serviços da plataforma.
* **Uso no AutoMedia AI**: Detentor do contrato e pagador da assinatura.
* **O que não significa**: O comprador do veículo.
* **Sinônimos aceitáveis**: Contratante
* **Termos desencorajados ou proibidos**: Vítima, Alvo
* **Exemplo correto**: O cliente renovou seu plano anual.
* **Exemplo incorreto**: Arrancamos dinheiro do alvo.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Tenant

### Concessionária

* **Categoria**: Negócio
* **Nome oficial**: Concessionária
* **Nome técnico**: Franchised Dealership
* **Definição**: Loja de veículos autorizada oficialmente por uma montadora específica.
* **Uso no AutoMedia AI**: Tipo de organização com requisitos estritos de Brand Kit.
* **O que não significa**: Um fabricante de veículos.
* **Sinônimos aceitáveis**: Revenda Autorizada
* **Termos desencorajados ou proibidos**: Máfia das marcas
* **Exemplo correto**: A concessionária importou seu Brand Kit.
* **Exemplo incorreto**: A máfia impôs sua cor.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Loja de Veículos

### Consistência de Marca

* **Categoria**: Negócio
* **Nome oficial**: Consistência de Marca
* **Nome técnico**: Brand Consistency
* **Definição**: Manutenção uniforme dos elementos da marca em todos os canais de publicação.
* **Uso no AutoMedia AI**: Benefício central provido pela automação de design do sistema.
* **O que não significa**: Ausência de criatividade.
* **Sinônimos aceitáveis**: Padronização Visual
* **Termos desencorajados ou proibidos**: Ditadura visual
* **Exemplo correto**: O sistema garante a consistência de marca nas exportações.
* **Exemplo incorreto**: O sistema impõe a ditadura visual.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Identidade Visual

### Criativo

* **Categoria**: Produto
* **Nome oficial**: Criativo
* **Nome técnico**: Creative Asset
* **Definição**: Arquivo de mídia visual ou visual que compõe um anúncio.
* **Uso no AutoMedia AI**: Elemento gráfico individual gerado pelo sistema.
* **O que não significa**: Uma pessoa com ideias originais.
* **Sinônimos aceitáveis**: Peça Gráfica
* **Termos desencorajados ou proibidos**: Arte genial
* **Exemplo correto**: O criativo foi atualizado com sucesso.
* **Exemplo incorreto**: A arte ficou divina.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Capa do Anúncio

### CTA

* **Categoria**: Produto
* **Nome oficial**: CTA
* **Nome técnico**: Call To Action
* **Definição**: Elemento de interface ou texto projetado para induzir o usuário a realizar uma ação específica.
* **Uso no AutoMedia AI**: Botão ou instrução final em um anúncio gerado.
* **O que não significa**: Um evento do sistema.
* **Sinônimos aceitáveis**: Chamada para Ação
* **Termos desencorajados ou proibidos**: Grito de comando
* **Exemplo correto**: O CTA incentiva o envio de mensagens no WhatsApp.
* **Exemplo incorreto**: O grito de comando forçou o clique.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Criativo

### Dados do Veículo

* **Categoria**: Produto
* **Nome oficial**: Dados do Veículo
* **Nome técnico**: Vehicle Data
* **Definição**: Conjunto de especificações técnicas, características e histórico de um automóvel.
* **Uso no AutoMedia AI**: Entrada estruturada para o modelo de linguagem gerar as descrições.
* **O que não significa**: O estado físico do motor.
* **Sinônimos aceitáveis**: Ficha Técnica
* **Termos desencorajados ou proibidos**: Tripas do carro
* **Exemplo correto**: A API importou os dados do veículo via placa.
* **Exemplo incorreto**: Lemos as tripas do carro com sucesso.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Informação Confirmada

### Formato de Publicação

* **Categoria**: Negócio
* **Nome oficial**: Formato de Publicação
* **Nome técnico**: Publishing Format
* **Definição**: Especificação técnica e estrutural de como o conteúdo é apresentado em um canal.
* **Uso no AutoMedia AI**: Define proporções e limites dos criativos.
* **O que não significa**: O conteúdo em si.
* **Sinônimos aceitáveis**: Especificação de Mídia
* **Termos desencorajados ou proibidos**: Molde engessado
* **Exemplo correto**: O formato de publicação foi ajustado para 16:9.
* **Exemplo incorreto**: O formato quebrou a internet.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Canal de Publicação

### Galeria

* **Categoria**: Produto
* **Nome oficial**: Galeria
* **Nome técnico**: Media Gallery
* **Definição**: Coleção de imagens tratadas associada a um veículo específico.
* **Uso no AutoMedia AI**: Agrupamento de criativos de um anúncio.
* **O que não significa**: Um museu de arte.
* **Sinônimos aceitáveis**: Coleção de Mídia
* **Termos desencorajados ou proibidos**: Álbum infinito
* **Exemplo correto**: O usuário adicionou fotos à galeria.
* **Exemplo incorreto**: A galeria engoliu as fotos.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Carrossel

### Identidade Comercial

* **Categoria**: Negócio
* **Nome oficial**: Identidade Comercial
* **Nome técnico**: Commercial Identity
* **Definição**: Conjunto de informações cadastrais e públicas que representam a loja.
* **Uso no AutoMedia AI**: Dados usados para preencher os rodapés dos anúncios.
* **O que não significa**: O logotipo apenas.
* **Sinônimos aceitáveis**: Perfil Comercial
* **Termos desencorajados ou proibidos**: Máscara corporativa
* **Exemplo correto**: A identidade comercial foi sincronizada com o canal.
* **Exemplo incorreto**: A máscara enganou o público.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Identidade Visual

### Informação Confirmada

* **Categoria**: Sistema
* **Nome oficial**: Informação Confirmada
* **Nome técnico**: Verified Data
* **Definição**: Dado validado contra uma base de registros oficiais ou via revisão humana.
* **Uso no AutoMedia AI**: Atributo marcado como imutável pelas otimizações de IA.
* **O que não significa**: Uma verdade absoluta inquestionável.
* **Sinônimos aceitáveis**: Dado Validado
* **Termos desencorajados ou proibidos**: regra estrita de dados
* **Exemplo correto**: A quilometragem é tratada como informação confirmada.
* **Exemplo incorreto**: O regra estrita do ano do carro é lei.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Dados do Veículo

### Loja de Veículos

* **Categoria**: Negócio
* **Nome oficial**: Loja de Veículos
* **Nome técnico**: Dealership
* **Definição**: Entidade comercial física ou digital que atua na venda de automóveis.
* **Uso no AutoMedia AI**: Organização que detém a assinatura do sistema.
* **O que não significa**: Um estacionamento privado.
* **Sinônimos aceitáveis**: Comércio Automotivo
* **Termos desencorajados ou proibidos**: Garagem de vendas
* **Exemplo correto**: A loja de veículos cadastrou novos usuários.
* **Exemplo incorreto**: A garagem socou carros no sistema.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Concessionária

### Lote Padrão

* **Categoria**: Sistema
* **Nome oficial**: Lote Padrão
* **Nome técnico**: Standard Batch
* **Definição**: Conjunto de anúncios processados simultaneamente com as mesmas regras de formatação.
* **Uso no AutoMedia AI**: Unidade de processamento assíncrono para eficiência de sistema.
* **O que não significa**: Um terreno físico.
* **Sinônimos aceitáveis**: Agrupamento de Processamento
* **Termos desencorajados ou proibidos**: sobrecarga de dados
* **Exemplo correto**: O lote padrão processou trinta criativos.
* **Exemplo incorreto**: O sobrecarga sobrecarregou o servidor.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Anúncio Automotivo

### Material Publicitário

* **Categoria**: Negócio
* **Nome oficial**: Material Publicitário
* **Nome técnico**: Advertising Material
* **Definição**: Conjunto de ativos digitais usados em campanhas de marketing.
* **Uso no AutoMedia AI**: Refere-se aos artefatos gerados para distribuição.
* **O que não significa**: Código-fonte.
* **Sinônimos aceitáveis**: Ativos de Marketing
* **Termos desencorajados ou proibidos**: Panfleto virtual
* **Exemplo correto**: O material publicitário foi exportado.
* **Exemplo incorreto**: O panfleto explodiu na rede.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Anúncio Automotivo

### MVP

* **Categoria**: Negócio
* **Nome oficial**: MVP
* **Nome técnico**: Minimum Viable Product
* **Definição**: Versão inicial do sistema com os requisitos fundamentais para validação de mercado.
* **Uso no AutoMedia AI**: Fase atual de desenvolvimento da plataforma para lojas parceiras.
* **O que não significa**: Um sistema quebrado ou incompleto.
* **Sinônimos aceitáveis**: Produto Viável Mínimo
* **Termos desencorajados ou proibidos**: Protótipo não padronizado
* **Exemplo correto**: O MVP inclui integração com os dois maiores portais.
* **Exemplo incorreto**: O protótipo não padronizado foi lançado aos clientes.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Validação Comercial

### Operador

* **Categoria**: Sistema
* **Nome oficial**: Operador
* **Nome técnico**: Operator
* **Definição**: Usuário com permissão para criar e editar anúncios no sistema.
* **Uso no AutoMedia AI**: Perfil de uso diário sem acesso a configurações financeiras.
* **O que não significa**: Uma máquina de processamento.
* **Sinônimos aceitáveis**: Assistente de Mídia
* **Termos desencorajados ou proibidos**: Apertador de botão
* **Exemplo correto**: O operador gerou uma nova campanha.
* **Exemplo incorreto**: O robô humano clicou ali.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Usuário

### Plano

* **Categoria**: Negócio
* **Nome oficial**: Plano
* **Nome técnico**: Plan
* **Definição**: Pacote comercial que define os limites de uso e funcionalidades disponíveis.
* **Uso no AutoMedia AI**: Determina a cota de anúncios mensais do Workspace.
* **O que não significa**: Uma estratégia militar.
* **Sinônimos aceitáveis**: Nível de Serviço
* **Termos desencorajados ou proibidos**: Nível de extorsão
* **Exemplo correto**: O workspace migrou para um plano superior.
* **Exemplo incorreto**: Ele comprou o plano mais caro e sangrou.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Assinatura

### Reconhecimento de Marca

* **Categoria**: Negócio
* **Nome oficial**: Reconhecimento de Marca
* **Nome técnico**: Brand Awareness
* **Definição**: Métrica que avalia a familiaridade do público com a loja.
* **Uso no AutoMedia AI**: Objetivo indireto das campanhas padronizadas geradas.
* **O que não significa**: Um algoritmo de visão computacional.
* **Sinônimos aceitáveis**: Lembrança de Marca
* **Termos desencorajados ou proibidos**: Lavagem cerebral
* **Exemplo correto**: Os anúncios padronizados auxiliam no reconhecimento de marca.
* **Exemplo incorreto**: O anúncio causou lavagem cerebral no lead.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Consistência de Marca

### Revendedor Independente

* **Categoria**: Negócio
* **Nome oficial**: Revendedor Independente
* **Nome técnico**: Independent Dealer
* **Definição**: Loja de veículos multimarcas sem afiliação exclusiva com montadoras.
* **Uso no AutoMedia AI**: Perfil de cliente com flexibilidade na Identidade Visual.
* **O que não significa**: Um vendedor pessoa física.
* **Sinônimos aceitáveis**: Lojista Multimarcas
* **Termos desencorajados ou proibidos**: Vendedor de esquina
* **Exemplo correto**: O revendedor independente personalizou a paleta de cores.
* **Exemplo incorreto**: O lojista bagunçou as cores.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Loja de Veículos

### Tenant

* **Categoria**: Arquitetura
* **Nome oficial**: Tenant
* **Nome técnico**: Tenant
* **Definição**: Isolamento lógico de dados pertencentes a um cliente específico na arquitetura multilocatário.
* **Uso no AutoMedia AI**: Garante que dados de diferentes lojas não se misturem.
* **O que não significa**: Um aluguel de imóvel.
* **Sinônimos aceitáveis**: Inquilino Lógico
* **Termos desencorajados ou proibidos**: Feudo de dados
* **Exemplo correto**: As requisições validam o identificador do tenant.
* **Exemplo incorreto**: O sistema invadiu o feudo vizinho.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Workspace

### Usuário

* **Categoria**: Sistema
* **Nome oficial**: Usuário
* **Nome técnico**: User
* **Definição**: Pessoa física com credenciais de acesso ao sistema.
* **Uso no AutoMedia AI**: Indivíduo que interage com a interface do software.
* **O que não significa**: Um sistema automatizado externo.
* **Sinônimos aceitáveis**: Operador do Sistema
* **Termos desencorajados ou proibidos**: Peão, Escravo digital
* **Exemplo correto**: O usuário redefiniu sua senha.
* **Exemplo incorreto**: O peão travou o sistema.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Operador

### Validação Comercial

* **Categoria**: Negócio
* **Nome oficial**: Validação Comercial
* **Nome técnico**: Market Validation
* **Definição**: Processo de confirmação da viabilidade financeira e técnica do sistema junto aos clientes.
* **Uso no AutoMedia AI**: Fase de coleta de métricas de aceitação do MVP.
* **O que não significa**: Um teste de software unitário.
* **Sinônimos aceitáveis**: Prova de Mercado
* **Termos desencorajados ou proibidos**: Cobaia de negócios
* **Exemplo correto**: As entrevistas auxiliaram na validação comercial.
* **Exemplo incorreto**: Usamos as lojas como cobaias.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: MVP

### Vendedor

* **Categoria**: Negócio
* **Nome oficial**: Vendedor
* **Nome técnico**: Salesperson
* **Definição**: Profissional responsável pelo atendimento aos interessados nos veículos.
* **Uso no AutoMedia AI**: Contato associado ao anúncio para receber leads.
* **O que não significa**: A entidade que paga a plataforma.
* **Sinônimos aceitáveis**: Consultor de Vendas
* **Termos desencorajados ou proibidos**: Tubarão de vendas
* **Exemplo correto**: O vendedor recebeu o contato do lead.
* **Exemplo incorreto**: O tubarão abocanhou a venda.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Loja de Veículos

### Workspace

* **Categoria**: Sistema
* **Nome oficial**: Workspace
* **Nome técnico**: Workspace
* **Definição**: Ambiente virtual isolado onde os recursos e usuários de um cliente são gerenciados.
* **Uso no AutoMedia AI**: Representação da interface de usuário de um Tenant.
* **O que não significa**: Um escritório físico.
* **Sinônimos aceitáveis**: Área de Trabalho
* **Termos desencorajados ou proibidos**: Caixa de areia
* **Exemplo correto**: O usuário alternou seu workspace ativo.
* **Exemplo incorreto**: O usuário pulou de caixa.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Tenant


## 5. Conceitos de Experiência e Fluxo

### Aprovação

* **Categoria**: Operação
* **Nome oficial**: Aprovação
* **Nome técnico**: State Validation
* **Definição**: Validação explícita de uma etapa intermediária pelo usuário. Condiciona a execução da próxima fase do fluxo ao aceite manual.
* **Uso no AutoMedia AI**: Requerida quando a IA gera uma prévia que precisa de validação humana antes da renderização final.
* **O que não significa**: Não substitui auditorias sistêmicas de segurança e formato.
* **Sinônimos aceitáveis**: Aceite, Autorização
* **Termos desencorajados ou proibidos**: Carimbo do chefe, Visto genérico
* **Exemplo correto**: A Aprovação do script é necessária para iniciar a processamento da imagem.
* **Exemplo incorreto**: Sem a Aprovação, executamos um processo não autorizado.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Confirmação, Intervenção Manual

### Arquivo ZIP

* **Categoria**: Artefato
* **Nome oficial**: Arquivo ZIP
* **Nome técnico**: Compressed Archive
* **Definição**: Formato de compressão de dados sem perda. Utilizado para consolidar múltiplos arquivos em um único contêiner com tamanho reduzido.
* **Uso no AutoMedia AI**: Formato padrão de compressão do Pacote Final para Entrega.
* **O que não significa**: Não altera a qualidade ou o codec das mídias internas.
* **Sinônimos aceitáveis**: Arquivo Compactado, Pacote Comprimido
* **Termos desencorajados ou proibidos**: Caixa preta, Arquivo sem validação de integridade
* **Exemplo correto**: A plataforma disponibiliza os resultados em um Arquivo ZIP.
* **Exemplo incorreto**: Compactamos tudo num Arquivo ZIP para burlar a validação de formato.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Pacote Final, Upload

### Cancelamento

* **Categoria**: Operação
* **Nome oficial**: Cancelamento
* **Nome técnico**: Process Termination
* **Definição**: Interrupção intencional de um fluxo em andamento. Libera os recursos computacionais alocados e exclui arquivos temporários associados.
* **Uso no AutoMedia AI**: Acionado pelo usuário via Telegram caso desista da edição em andamento.
* **O que não significa**: Não exclui o cadastro da conta do usuário no sistema.
* **Sinônimos aceitáveis**: Interrupção, Aborto de Processo
* **Termos desencorajados ou proibidos**: Assassinato de tarefa, Destruição total
* **Exemplo correto**: O Cancelamento libera a CPU para outros processos pendentes.
* **Exemplo incorreto**: O Cancelamento pune usuários impacientes.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Comando, Fluxo

### Comando

* **Categoria**: Interação
* **Nome oficial**: Comando
* **Nome técnico**: Executable Directive
* **Definição**: Instrução explícita enviada pelo usuário. Aciona uma função ou API específica no sistema.
* **Uso no AutoMedia AI**: Recebido via texto ou botão no Telegram para iniciar rotinas.
* **O que não significa**: Não é linguagem natural não estruturada; comandos seguem sintaxe mapeada.
* **Sinônimos aceitáveis**: Instrução, Diretiva
* **Termos desencorajados ou proibidos**: Ordem absoluta, Magia
* **Exemplo correto**: O Comando /start inicializa a Sessão Conversacional.
* **Exemplo incorreto**: O Comando faz o servidor apresentar falha crítica por sobrecarga.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Mensagem, Sessão Conversacional

### Conexão com Telegram

* **Categoria**: Integração
* **Nome oficial**: Conexão com Telegram
* **Nome técnico**: Telegram Webhook Integration
* **Definição**: Estabelecimento de comunicação via Webhook entre a plataforma AutoMedia AI e a API do Telegram. Permite o envio e recebimento de mensagens.
* **Uso no AutoMedia AI**: Usada como principal interface de entrada de comandos do usuário para o sistema.
* **O que não significa**: Não estabelece acesso irrestrito aos contatos pessoais do usuário.
* **Sinônimos aceitáveis**: Integração com Telegram, Vínculo de Bot
* **Termos desencorajados ou proibidos**: retenção indevida do Telegram, Espionagem de chat
* **Exemplo correto**: A Conexão com Telegram utiliza tokens de autenticação padrão.
* **Exemplo incorreto**: A conexão com o Telegram substitui o backend de processamento da aplicação.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Sessão Conversacional

### Configuração Inicial

* **Categoria**: Produto
* **Nome oficial**: Configuração Inicial
* **Nome técnico**: Initial Setup
* **Definição**: Definição dos parâmetros obrigatórios para o funcionamento da plataforma. Inclui a parametrização de integrações e preferências de conta.
* **Uso no AutoMedia AI**: Necessária antes da execução do primeiro fluxo de automação de mídia.
* **O que não significa**: Não é um processo repetitivo; ocorre apenas na ativação da conta ou de novas integrações.
* **Sinônimos aceitáveis**: Setup, Parametrização Básica
* **Termos desencorajados ou proibidos**: Configuração torturante, Burocracia de entrada
* **Exemplo correto**: A Configuração Inicial requer as chaves de API das plataformas de mídia.
* **Exemplo incorreto**: A Configuração Inicial é um experiência confusa para o usuário sem treinamento.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Onboarding, Conexão com Telegram

### Confirmação

* **Categoria**: Interação
* **Nome oficial**: Confirmação
* **Nome técnico**: Acknowledgement Protocol
* **Definição**: Sinal de retorno enviado pelo sistema para atestar o recebimento de uma ação. Garante consistência transacional na interface de usuário.
* **Uso no AutoMedia AI**: Usada para evitar requisições duplicadas quando o usuário envia mensagens idênticas em curto prazo.
* **O que não significa**: Não implica a conclusão do processamento em background.
* **Sinônimos aceitáveis**: Recibo, Validação de Recebimento
* **Termos desencorajados ou proibidos**: Bênção, Amém digital
* **Exemplo correto**: A Confirmação é enviada assim que o Upload termina.
* **Exemplo incorreto**: Se a Confirmação não chegar, o sistema cometeu roubo de dados.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Mensagem, Aprovação

### Entrega

* **Categoria**: Operação
* **Nome oficial**: Entrega
* **Nome técnico**: Asset Delivery
* **Definição**: Disponibilização do resultado final do processamento ao usuário. Pode ocorrer via link de download ou envio direto de arquivo.
* **Uso no AutoMedia AI**: Etapa final onde o arquivo processado é retornado via bot.
* **O que não significa**: Não garante armazenamento vitalício do arquivo gerado.
* **Sinônimos aceitáveis**: Disponibilização, Resultado Final
* **Termos desencorajados ou proibidos**: Desova de arquivo, Presente de administrador
* **Exemplo correto**: A Entrega do arquivo ocorre via URL assinada.
* **Exemplo incorreto**: A Entrega é o momento de glória do sistema.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Pacote Final, Arquivo ZIP

### Etapa

* **Categoria**: Processamento
* **Nome oficial**: Etapa
* **Nome técnico**: Pipeline Stage
* **Definição**: Unidade individual de processamento dentro de um fluxo maior. Executa uma tarefa específica e retorna um estado de sucesso ou falha.
* **Uso no AutoMedia AI**: Compõe os fluxos de automação, como tratamento de imagem e renderização de layout.
* **O que não significa**: Não é um processo independente; depende da etapa anterior e afeta a subsequente.
* **Sinônimos aceitáveis**: Fase, Passo
* **Termos desencorajados ou proibidos**: Gargalo, Pedreira
* **Exemplo correto**: A Etapa de redimensionamento de fotos concluiu sem erros.
* **Exemplo incorreto**: A Etapa de renderização é um processo com alto consumo não otimizado de CPU.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Fluxo, Jornada

### Fluxo

* **Categoria**: Processamento
* **Nome oficial**: Fluxo
* **Nome técnico**: Processing Pipeline
* **Definição**: Sequência ordenada de etapas executadas para concluir uma operação complexa. Possui início, processamento intermediário e fim definidos.
* **Uso no AutoMedia AI**: Orquestra as ações de IA desde a entrada do usuário até o pacote final.
* **O que não significa**: Não permite ciclos infinitos sem condição de saída.
* **Sinônimos aceitáveis**: Pipeline, Sequência de Execução
* **Termos desencorajados ou proibidos**: Esteira infinita, Rolo compressor
* **Exemplo correto**: O Fluxo de processamento requer validação dos arquivos de entrada.
* **Exemplo incorreto**: Esse Fluxo é uma bagunça sem fim.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Etapa, Jornada

### Intervenção Manual

* **Categoria**: Operação
* **Nome oficial**: Intervenção Manual
* **Nome técnico**: Human-in-the-Loop Override
* **Definição**: Ação executada por um operador humano para alterar o comportamento de uma automação. Pode corrigir erros ou ajustar parâmetros em tempo de execução.
* **Uso no AutoMedia AI**: Permitida para administradores do sistema em fluxos com falha não tratada.
* **O que não significa**: Não é a operação padrão; o sistema deve priorizar automação sem intervenção.
* **Sinônimos aceitáveis**: Correção Manual, Ação de Operador
* **Termos desencorajados ou proibidos**: Intervenção manual não auditada
* **Exemplo correto**: A Intervenção Manual corrigiu os metadados da foto do veículo corrompida.
* **Exemplo incorreto**: A Intervenção Manual é a prova de que nossa IA é burra.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Reprocessamento, Aprovação

> [!WARNING] Revisão de Arquitetura Pendente
> Conceito conflita parcialmente com a premissa de Zero Manual Work; necessita alinhamento sobre permissões de admin versus usuário.

### Jornada

* **Categoria**: UX
* **Nome oficial**: Jornada
* **Nome técnico**: User Journey
* **Definição**: Caminho lógico percorrido pelo usuário na plataforma. Mapeia a interação desde o Onboarding até a utilização avançada do produto.
* **Uso no AutoMedia AI**: Baseia o design de interfaces e a estrutura de respostas do bot.
* **O que não significa**: Não é um componente de software, mas um modelo de experiência do usuário.
* **Sinônimos aceitáveis**: Caminho do Usuário, Experiência de Uso
* **Termos desencorajados ou proibidos**: Processo manual extenso
* **Exemplo correto**: A Jornada do novo usuário é monitorada via eventos de analytics.
* **Exemplo incorreto**: Nossa Jornada é um regra estrita inviolável do produto.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Fluxo, Onboarding

### Mensagem

* **Categoria**: Interação
* **Nome oficial**: Mensagem
* **Nome técnico**: Data Payload
* **Definição**: Unidade de comunicação entre o sistema e o usuário. Pode conter texto, mídia ou metadados de formatação.
* **Uso no AutoMedia AI**: Transmite feedbacks, solicitações de input e resultados via Telegram.
* **O que não significa**: Não é um arquivo persistido em banco de dados relacional de longo prazo.
* **Sinônimos aceitáveis**: Notificação, Resposta
* **Termos desencorajados ou proibidos**: Ruído, Spam
* **Exemplo correto**: O sistema enviou uma Mensagem com o relatório de erros.
* **Exemplo incorreto**: A Mensagem explode na tela do usuário para forçar a atenção.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Comando, Upload

### Onboarding

* **Categoria**: Produto
* **Nome oficial**: Onboarding
* **Nome técnico**: User Provisioning Pipeline
* **Definição**: Processo de inicialização e registro de um novo usuário no sistema. Envolve a criação de credenciais e configuração de parâmetros básicos de perfil.
* **Uso no AutoMedia AI**: Executado automaticamente quando um usuário acessa a plataforma pela primeira vez. Responsável por inicializar o tenant do cliente.
* **O que não significa**: Não significa treinamento ou doutrinação do usuário no uso do sistema.
* **Sinônimos aceitáveis**: Registro de Usuário, Inicialização de Conta
* **Termos desencorajados ou proibidos**: Batismo de usuário, Integração mágica
* **Exemplo correto**: O módulo de Onboarding registrou o usuário no banco de dados.
* **Exemplo incorreto**: O Onboarding é o nosso funil de conversão inviolável que não pode falhar.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Configuração Inicial

### Reprocessamento

* **Categoria**: Operação
* **Nome oficial**: Reprocessamento
* **Nome técnico**: Pipeline Retry
* **Definição**: Execução repetida de um fluxo em caso de falha ou requisição do usuário. Utiliza cache de etapas anteriores quando aplicável.
* **Uso no AutoMedia AI**: Permite correções automáticas caso um modelo de IA retorne um erro temporário.
* **O que não significa**: Não recomeça obrigatoriamente a partir do Upload inicial, podendo reaproveitar arquivos já armazenados.
* **Sinônimos aceitáveis**: Nova Execução, Retentativa
* **Termos desencorajados ou proibidos**: Reativação manual sem validação
* **Exemplo correto**: O Reprocessamento foi acionado devido a uma falha na rede.
* **Exemplo incorreto**: O Reprocessamento salva o sistema da falha irrecuperável súbita.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Fluxo, Intervenção Manual

### Sessão Conversacional

* **Categoria**: Interação
* **Nome oficial**: Sessão Conversacional
* **Nome técnico**: Conversation Session State
* **Definição**: Período de interação contínua entre o usuário e o bot. Mantém o estado da conversa em memória temporária para processamento de contexto.
* **Uso no AutoMedia AI**: Gerencia o histórico de mensagens recentes para entender comandos complexos.
* **O que não significa**: Não armazena os dados indefinidamente, sendo encerrada após inatividade.
* **Sinônimos aceitáveis**: Sessão de Chat, Estado de Conversa
* **Termos desencorajados ou proibidos**: Bate-papo robótico, Interrogatório
* **Exemplo correto**: O timeout da Sessão Conversacional é de trinta minutos.
* **Exemplo incorreto**: A Sessão Conversacional prende o usuário numa conversa infinita.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Mensagem, Comando

### Software Invisível

* **Categoria**: Visão
* **Nome oficial**: Software Invisível
* **Nome técnico**: Headless Architecture Experience
* **Definição**: Conceito de design onde o usuário interage apenas com as interfaces nativas do Telegram. Minimiza o uso de painéis web externos para configuração.
* **Uso no AutoMedia AI**: Define que a interface de chat deve prover todas as funções operacionais necessárias.
* **O que não significa**: Não se refere a processos não auditáveis ou operações secretas de backend.
* **Sinônimos aceitáveis**: Interface Transparente, Operação via Chat
* **Termos desencorajados ou proibidos**: Código fantasma, Magia negra
* **Exemplo correto**: O conceito de Software Invisível foca na interação natural do usuário.
* **Exemplo incorreto**: O Software Invisível é uma forma de ocultar falhas de integração do usuário.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Zero Manual Work, Conexão com Telegram

### Upload

* **Categoria**: Infraestrutura
* **Nome oficial**: Upload
* **Nome técnico**: File Ingestion
* **Definição**: Processo de transferência de arquivos do cliente para os servidores do sistema. Envolve validação de formato e armazenamento temporário.
* **Uso no AutoMedia AI**: Usado para receber mídias brutas que serão processadas pelos modelos de IA.
* **O que não significa**: Não inclui o processamento da mídia; apenas a sua recepção e armazenamento.
* **Sinônimos aceitáveis**: Envio de Arquivo, Ingestão de Mídia
* **Termos desencorajados ou proibidos**: Despejo de dados, Entulho digital
* **Exemplo correto**: O Upload das fotos do veículo foi concluído em trinta segundos.
* **Exemplo incorreto**: O usuário fez Upload de um arquivo corrompido ou mal formatado.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Pacote Final, Arquivo ZIP

### Zero Manual Work

* **Categoria**: Visão
* **Nome oficial**: Zero Manual Work
* **Nome técnico**: Full Pipeline Automation
* **Definição**: Princípio arquitetural que visa eliminar etapas repetitivas no processamento de mídia. Enfatiza o acionamento de fluxos com configurações pré-determinadas.
* **Uso no AutoMedia AI**: Norteia o desenvolvimento das integrações diretas entre IA e plataformas de entrega.
* **O que não significa**: Não exclui a necessidade de validações de qualidade e Aprovações pelo usuário.
* **Sinônimos aceitáveis**: Automação Completa, Redução de Atrito
* **Termos desencorajados ou proibidos**: falha irrecuperável ao trabalho, Eliminação do humano
* **Exemplo correto**: A diretriz Zero Manual Work orienta o design das APIs.
* **Exemplo incorreto**: Zero Manual Work é nossa regra de negócio estrita.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Software Invisível, Fluxo


## 6. Conceitos de Arquitetura

### Adapter

* **Categoria**: Arquitetura
* **Nome oficial**: Adapter
* **Nome técnico**: Adapter
* **Definição**: Componente de software que traduz chamadas entre a porta da aplicação e a tecnologia externa.
* **Uso no AutoMedia AI**: Isola a aplicação das mudanças em APIs e bibliotecas de terceiros.
* **O que não significa**: Não significa adaptador de hardware.
* **Sinônimos aceitáveis**: Adaptador
* **Termos desencorajados ou proibidos**: Script de correção informal
* **Exemplo correto**: O Adapter REST converte JSON em chamadas de domínio.
* **Exemplo incorreto**: Comprei um Adapter de tomada.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Port, Provider

### Aplicação

* **Categoria**: Arquitetura
* **Nome oficial**: Aplicação
* **Nome técnico**: Aplicação
* **Definição**: Conjunto integrado de software projetado para realizar um grupo de funções coordenadas.
* **Uso no AutoMedia AI**: Representa o produto de software entregue ao usuário final.
* **O que não significa**: Não significa a infraestrutura subjacente.
* **Sinônimos aceitáveis**: Software
* **Termos desencorajados ou proibidos**: Programinha
* **Exemplo correto**: A Aplicação requer autenticação para ser acessada.
* **Exemplo incorreto**: A Aplicação é um servidor Linux.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Camada de Aplicação

### Assíncrono

* **Categoria**: Arquitetura
* **Nome oficial**: Assíncrono
* **Nome técnico**: Assíncrono
* **Definição**: Modelo de processamento onde a execução não bloqueia o fluxo principal e a resposta é gerida separadamente.
* **Uso no AutoMedia AI**: Padrão mandatório para processamentos longos e integração de eventos.
* **O que não significa**: Não significa execução paralela imediata ou simultaneidade perfeita.
* **Sinônimos aceitáveis**: Não-bloqueante
* **Termos desencorajados ou proibidos**: Execução sem monitoramento, processo abandonado
* **Exemplo correto**: O worker envia e-mails em lote de forma assíncrona.
* **Exemplo incorreto**: A resposta da tela de login demorou de forma assíncrona.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Síncrono, Event-driven

### Bounded Context

* **Categoria**: Arquitetura
* **Nome oficial**: Bounded Context
* **Nome técnico**: Bounded Context
* **Definição**: Fronteira explícita dentro da qual um modelo de domínio específico é definido e aplicável.
* **Uso no AutoMedia AI**: Isola modelos conceituais para evitar ambiguidades de linguagem e regras.
* **O que não significa**: Não significa fronteira de rede ou de banco de dados.
* **Sinônimos aceitáveis**: Contexto delimitado
* **Termos desencorajados ou proibidos**: Cercadinho seguro
* **Exemplo correto**: O conceito de Cliente tem modelos diferentes dependendo do Bounded Context.
* **Exemplo incorreto**: O Bounded Context bloqueia requisições HTTP inválidas.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Domínio, Subdomínio

### Camada de Aplicação

* **Categoria**: Arquitetura
* **Nome oficial**: Camada de Aplicação
* **Nome técnico**: Camada de Aplicação
* **Definição**: Camada responsável por orquestrar fluxos de casos de uso e mediar a comunicação entre a interface e o domínio.
* **Uso no AutoMedia AI**: Contém os serviços de aplicação que coordenam tarefas sem possuir regras de negócio próprias.
* **O que não significa**: Não significa a aplicação em si, nem a camada de interface do usuário.
* **Sinônimos aceitáveis**: Application Layer
* **Termos desencorajados ou proibidos**: O meio de campo
* **Exemplo correto**: A Camada de Aplicação carrega a entidade e invoca a regra de negócio.
* **Exemplo incorreto**: A Camada de Aplicação executa a validação de formato de e-mail e salva no banco.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Use Case

### Camada de Domínio

* **Categoria**: Arquitetura
* **Nome oficial**: Camada de Domínio
* **Nome técnico**: Camada de Domínio
* **Definição**: Camada que encapsula a lógica, estado e regras fundamentais do negócio.
* **Uso no AutoMedia AI**: Isola a lógica principal de qualquer dependência externa ou infraestrutura.
* **O que não significa**: Não significa a definição de tabelas de banco de dados.
* **Sinônimos aceitáveis**: Domain Layer
* **Termos desencorajados ou proibidos**: Coração inviolável do software
* **Exemplo correto**: A Camada de Domínio não possui importações de pacotes de banco de dados.
* **Exemplo incorreto**: A Camada de Domínio conecta-se diretamente à API externa.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Entidade, Value Object

### Camada de Infraestrutura

* **Categoria**: Arquitetura
* **Nome oficial**: Camada de Infraestrutura
* **Nome técnico**: Camada de Infraestrutura
* **Definição**: Camada responsável pelas implementações técnicas de IO, banco de dados, mensageria e frameworks.
* **Uso no AutoMedia AI**: Contém adaptadores e drivers que conectam as necessidades da aplicação aos recursos externos.
* **O que não significa**: Não significa provisão de recursos em nuvem (ex: Terraform).
* **Sinônimos aceitáveis**: Infrastructure Layer
* **Termos desencorajados ou proibidos**: Esgoto do sistema
* **Exemplo correto**: O repositório do banco de dados é implementado na Camada de Infraestrutura.
* **Exemplo incorreto**: A regra de negócio está na Camada de Infraestrutura.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Adapter, Provider

### Circuit Breaker

* **Categoria**: Arquitetura
* **Nome oficial**: Circuit Breaker
* **Nome técnico**: Circuit Breaker
* **Definição**: Padrão de resiliência que interrompe chamadas a um serviço remoto que apresenta alta taxa de falhas repetidas.
* **Uso no AutoMedia AI**: Previne o colapso de serviços dependentes limitando solicitações em estado aberto.
* **O que não significa**: Não significa um mecanismo de tratamento isolado de exceções simples de negócio.
* **Sinônimos aceitáveis**: Disjuntor
* **Termos desencorajados ou proibidos**: Cortador de cabos elétricos
* **Exemplo correto**: O Circuit Breaker abriu o circuito após cinco timeouts seguidos no serviço parceiro.
* **Exemplo incorreto**: O Circuit Breaker bloqueou a inserção por conta de campo não preenchido pelo usuário.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Retry, Fallback

### Configuração de Provider

* **Categoria**: Arquitetura
* **Nome oficial**: Configuração de Provider
* **Nome técnico**: Configuração de Provider
* **Definição**: Conjunto de metadados, credenciais e parâmetros injetados para inicializar um Provider corretamente.
* **Uso no AutoMedia AI**: Gerido via variáveis de ambiente seguras e serviços de secrets.
* **O que não significa**: Não significa hardcode de chaves diretamente na base de código fonte.
* **Sinônimos aceitáveis**: Parâmetros do Provider
* **Termos desencorajados ou proibidos**: Configurações soltas
* **Exemplo correto**: A Configuração de Provider foi carregada via cofre de senhas em memória.
* **Exemplo incorreto**: Gravei a Configuração de Provider num txt público.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Provider

### Core

* **Categoria**: Arquitetura
* **Nome oficial**: Core
* **Nome técnico**: Core
* **Definição**: O componente essencial do sistema, concentrando o diferencial estratégico e a maior complexidade de negócio.
* **Uso no AutoMedia AI**: Representa o núcleo da plataforma, focado no processamento crítico e inovação.
* **O que não significa**: Não significa infraestrutura básica ou código utilitário compartilhado.
* **Sinônimos aceitáveis**: Núcleo
* **Termos desencorajados ou proibidos**: A joia da coroa
* **Exemplo correto**: O subdomínio Core possui a equipe de engenharia mais experiente alocada.
* **Exemplo incorreto**: O script de formatação de datas fica no Core do sistema.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Domínio

### Correlation ID

* **Categoria**: Arquitetura
* **Nome oficial**: Correlation ID
* **Nome técnico**: Correlation ID
* **Definição**: Identificador único atrelado a um processo lógico completo distribuído através de múltiplos serviços.
* **Uso no AutoMedia AI**: Vital para ligar os logs de uma transação distribuída de ponta a ponta.
* **O que não significa**: Não significa um Request ID exclusivo de chamadas HTTP individuais.
* **Sinônimos aceitáveis**: ID de Correlação
* **Termos desencorajados ou proibidos**: Passaporte mágico
* **Exemplo correto**: O Correlation ID acompanhou o log de todos os três microsserviços envolvidos.
* **Exemplo incorreto**: O Correlation ID mudava toda vez que o arquivo mudava de pasta.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Trace ID, Request ID

### Dependency Inversion

* **Categoria**: Arquitetura
* **Nome oficial**: Dependency Inversion
* **Nome técnico**: Dependency Inversion
* **Definição**: Princípio arquitetural onde abstrações não dependem de detalhes, mas os detalhes dependem de abstrações.
* **Uso no AutoMedia AI**: Essencial para proteger o Domínio Core contra dependências da camada de infraestrutura.
* **O que não significa**: Não significa injetar qualquer classe concretamente em outra (Injeção de Dependência simples).
* **Sinônimos aceitáveis**: Inversão de Dependência
* **Termos desencorajados ou proibidos**: Inversão cósmica de dados
* **Exemplo correto**: O repositório de clientes implementa a interface definida pelo Domínio.
* **Exemplo incorreto**: O Domínio importa diretamente a biblioteca SQL via Dependency Inversion.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Interface, Port

### Domain Event

* **Categoria**: Arquitetura
* **Nome oficial**: Domain Event
* **Nome técnico**: Domain Event
* **Definição**: Evento focado inteiramente na linguagem do domínio, expressando uma mudança de negócio significativa.
* **Uso no AutoMedia AI**: Comunica mudanças de estado essenciais dentro da mesma fronteira contextual.
* **O que não significa**: Não significa um clique de mouse em tela.
* **Sinônimos aceitáveis**: Evento de domínio
* **Termos desencorajados ou proibidos**: Aviso local
* **Exemplo correto**: PedidoFinalizado é um Domain Event.
* **Exemplo incorreto**: BotaoPedidoClicado é um Domain Event.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Event, Integration Event

### Domínio

* **Categoria**: Arquitetura
* **Nome oficial**: Domínio
* **Nome técnico**: Domínio
* **Definição**: Esfera de conhecimento, influência ou atividade referente à regra de negócio principal.
* **Uso no AutoMedia AI**: Define a área de problema que o software pretende resolver.
* **O que não significa**: Não significa domínio de internet (DNS).
* **Sinônimos aceitáveis**: Área de negócio
* **Termos desencorajados ou proibidos**: Território inviolável
* **Exemplo correto**: O Domínio de faturamento contém as regras lógicas de cobrança.
* **Exemplo incorreto**: O Domínio pontocom expirou.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Subdomínio

### Driver

* **Categoria**: Arquitetura
* **Nome oficial**: Driver
* **Nome técnico**: Driver
* **Definição**: Componente de software que permite a interação entre o sistema operacional ou aplicação e um dispositivo ou subsistema.
* **Uso no AutoMedia AI**: Usado para gerenciar interações em baixo nível com bancos de dados e sistemas de arquivos.
* **O que não significa**: Não significa interface com o usuário final.
* **Sinônimos aceitáveis**: Controlador
* **Termos desencorajados ou proibidos**: Piloto do sistema
* **Exemplo correto**: O Driver do banco de dados gerencia o pool de conexões.
* **Exemplo incorreto**: O Driver renderiza os botões na tela.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Adapter

### Engine

* **Categoria**: Arquitetura
* **Nome oficial**: Engine
* **Nome técnico**: Engine
* **Definição**: Motor de processamento central responsável por executar lógica complexa de negócios.
* **Uso no AutoMedia AI**: Utilizado para orquestrar fluxos de automação pesados de forma centralizada.
* **O que não significa**: Não significa um banco de dados ou interface de usuário.
* **Sinônimos aceitáveis**: Motor
* **Termos desencorajados ou proibidos**: Coração do sistema, cérebro
* **Exemplo correto**: A Engine processa as regras de negócio de forma assíncrona.
* **Exemplo incorreto**: A Engine exibe a tela inicial para o usuário.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Orchestrator

### Event

* **Categoria**: Arquitetura
* **Nome oficial**: Event
* **Nome técnico**: Event
* **Definição**: Fato ocorrido no sistema no passado, portando informação sobre uma mudança de estado.
* **Uso no AutoMedia AI**: Ponto de comunicação primária entre sistemas assíncronos.
* **O que não significa**: Não significa um comando para executar uma ação.
* **Sinônimos aceitáveis**: Evento
* **Termos desencorajados ou proibidos**: Grito de notificação
* **Exemplo correto**: O Event de UsuárioCriado foi emitido.
* **Exemplo incorreto**: O Event de CriarUsuário disparou no sistema.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Domain Event, Integration Event

### Event-driven

* **Categoria**: Arquitetura
* **Nome oficial**: Event-driven
* **Nome técnico**: Event-driven
* **Definição**: Paradigma arquitetural baseado na produção, detecção e consumo de eventos em tempo real.
* **Uso no AutoMedia AI**: Fornece escalabilidade e desacoplamento para fluxos de dados de alto volume.
* **O que não significa**: Não significa requisições HTTP REST contínuas.
* **Sinônimos aceitáveis**: Orientado a eventos
* **Termos desencorajados ou proibidos**: Arquitetura reativa anárquica
* **Exemplo correto**: A arquitetura Event-driven reage quando novas imagens são importadas.
* **Exemplo incorreto**: O sistema Event-driven consulta o banco a cada segundo verificando mudanças.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Event, Assíncrono

### Fallback

* **Categoria**: Arquitetura
* **Nome oficial**: Fallback
* **Nome técnico**: Fallback
* **Definição**: Plano ou método alternativo que é executado quando o mecanismo primário falha sistematicamente.
* **Uso no AutoMedia AI**: Provisão de dados cacheados ou comportamentos padrão para manter o sistema operacional em degradação.
* **O que não significa**: Não significa relatar erro fatal imediatamente.
* **Sinônimos aceitáveis**: Alternativa de contingência
* **Termos desencorajados ou proibidos**: Gambito de salvação
* **Exemplo correto**: O Fallback exibiu as categorias em cache após falha na consulta ao banco principal.
* **Exemplo incorreto**: O Fallback deletou os arquivos após erro de leitura.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Circuit Breaker

### Health Check

* **Categoria**: Arquitetura
* **Nome oficial**: Health Check
* **Nome técnico**: Health Check
* **Definição**: Endpoint projetado para retornar o status de saúde e conectividade das dependências de um serviço.
* **Uso no AutoMedia AI**: Configurado nos pods do Kubernetes para reinício automático ou roteamento de tráfego seguro.
* **O que não significa**: Não significa monitoramento de performance detalhado ou telemetria profunda.
* **Sinônimos aceitáveis**: Verificação de integridade
* **Termos desencorajados ou proibidos**: Batimento cardíaco vital
* **Exemplo correto**: O load balancer testou o endpoint de Health Check.
* **Exemplo incorreto**: O Health Check apagou arquivos de cache expirados.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Observabilidade

### Idempotência

* **Categoria**: Arquitetura
* **Nome oficial**: Idempotência
* **Nome técnico**: Idempotência
* **Definição**: Propriedade de operações matemáticas ou de software em que múltiplas aplicações têm o mesmo efeito que a aplicação única.
* **Uso no AutoMedia AI**: Requisito obrigatório para APIs de retentativa e processamento seguro de mensagens duplicadas.
* **O que não significa**: Não significa que as operações sempre falham igual.
* **Sinônimos aceitáveis**: Idempotent
* **Termos desencorajados ou proibidos**: A prova de burrice
* **Exemplo correto**: A transação de exclusão de arquivo garantiu idempotência mesmo executada três vezes.
* **Exemplo incorreto**: Devido à idempotência, cada requisição faturou o cliente novamente.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Retry

### Integration Event

* **Categoria**: Arquitetura
* **Nome oficial**: Integration Event
* **Nome técnico**: Integration Event
* **Definição**: Evento usado especificamente para comunicar fatos através de fronteiras de diferentes microsserviços.
* **Uso no AutoMedia AI**: Contém apenas dados essenciais para propagar mudanças pelo barramento de mensagens.
* **O que não significa**: Não significa eventos internos de domínio vazados com dados privados.
* **Sinônimos aceitáveis**: Evento de integração
* **Termos desencorajados ou proibidos**: Notícia global
* **Exemplo correto**: O Integration Event notificou o serviço de faturamento sobre o pedido concluído.
* **Exemplo incorreto**: O Integration Event transmitiu toda a base de clientes do módulo local.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Domain Event, Event-driven

### Microsserviço

* **Categoria**: Arquitetura
* **Nome oficial**: Microsserviço
* **Nome técnico**: Microsserviço
* **Definição**: Padrão de arquitetura de software onde a aplicação é composta por serviços pequenos, independentes e fracamente acoplados.
* **Uso no AutoMedia AI**: Utilizado apenas em domínios que requerem escalabilidade ou ciclos de deploy independentes.
* **O que não significa**: Não significa divisão arbitrária de código baseada em tamanho de arquivo.
* **Sinônimos aceitáveis**: Microservice
* **Termos desencorajados ou proibidos**: Mini-api, servicinho
* **Exemplo correto**: O Microsserviço de notificações escala horizontalmente de forma independente.
* **Exemplo incorreto**: Cada função do sistema virou um Microsserviço.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Serviço, Monólito Modular

### Módulo

* **Categoria**: Arquitetura
* **Nome oficial**: Módulo
* **Nome técnico**: Módulo
* **Definição**: Agrupamento lógico e coeso de funcionalidades com responsabilidades bem definidas.
* **Uso no AutoMedia AI**: Aplicado para separar domínios lógicos dentro do sistema.
* **O que não significa**: Não significa um servidor físico isolado.
* **Sinônimos aceitáveis**: Componente modular
* **Termos desencorajados ou proibidos**: Pedaço de código
* **Exemplo correto**: O Módulo de pagamentos foi atualizado independentemente.
* **Exemplo incorreto**: O Módulo travou a máquina inteira.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Monólito Modular

### Monólito Modular

* **Categoria**: Arquitetura
* **Nome oficial**: Monólito Modular
* **Nome técnico**: Monólito Modular
* **Definição**: Padrão arquitetural onde o sistema é implantado como uma unidade única, mas internamente dividido em módulos independentes.
* **Uso no AutoMedia AI**: Padrão recomendado para sistemas de médio porte para equilibrar manutenibilidade e complexidade de deploy.
* **O que não significa**: Não significa um código fortemente acoplado (big ball of mud).
* **Sinônimos aceitáveis**: Monólito estruturado
* **Termos desencorajados ou proibidos**: Monossauro, sistema legado gigante
* **Exemplo correto**: O Monólito Modular permite escalabilidade de desenvolvimento com um único pipeline de deploy.
* **Exemplo incorreto**: O Monólito Modular exige que todos os times toquem no mesmo arquivo.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Módulo, Microsserviço

### Observabilidade

* **Categoria**: Arquitetura
* **Nome oficial**: Observabilidade
* **Nome técnico**: Observabilidade
* **Definição**: Grau de capacidade que permite compreender o estado interno de um sistema com base nas saídas externas.
* **Uso no AutoMedia AI**: Composta fundamentalmente por logs estruturados, métricas e tracing distribuído.
* **O que não significa**: Não significa apenas verificar se o servidor está ligado.
* **Sinônimos aceitáveis**: Observability
* **Termos desencorajados ou proibidos**: Vigilância massiva
* **Exemplo correto**: Aumentamos a Observabilidade incorporando métricas de tempo de renderização.
* **Exemplo incorreto**: Instalamos câmeras na sala de servidores para Observabilidade.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Trace ID, Health Check

### Orchestrator

* **Categoria**: Arquitetura
* **Nome oficial**: Orchestrator
* **Nome técnico**: Orchestrator
* **Definição**: Componente responsável por coordenar múltiplas tarefas ou serviços de forma centralizada.
* **Uso no AutoMedia AI**: Controla fluxos de processos complexos através de sagas ou workflows stateful.
* **O que não significa**: Não significa uma arquitetura orientada a eventos coreografada (choreography).
* **Sinônimos aceitáveis**: Orquestrador
* **Termos desencorajados ou proibidos**: Maestro de marionetes
* **Exemplo correto**: O Orchestrator inicia as três etapas sequenciais de criação de conta.
* **Exemplo incorreto**: O Orchestrator fica escutando eventos soltos na fila.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Pipeline, Workflow

### Pipeline

* **Categoria**: Arquitetura
* **Nome oficial**: Pipeline
* **Nome técnico**: Pipeline
* **Definição**: Sequência de estágios de processamento de dados onde a saída de um é a entrada do próximo.
* **Uso no AutoMedia AI**: Utilizado para processamento em lote e transformação sucessiva de dados de mídia.
* **O que não significa**: Não significa fluxo de navegação do usuário.
* **Sinônimos aceitáveis**: Fluxo de processamento
* **Termos desencorajados ou proibidos**: Esteira rolante infinita
* **Exemplo correto**: O arquivo passa pelo Pipeline de codificação e redimensionamento.
* **Exemplo incorreto**: O Pipeline do usuário vai da tela de login até o checkout.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Workflow

### Plugin

* **Categoria**: Arquitetura
* **Nome oficial**: Plugin
* **Nome técnico**: Plugin
* **Definição**: Componente modular adicionado dinamicamente para estender capacidades de software sem modificar seu núcleo.
* **Uso no AutoMedia AI**: Adotado para criar integrações extensíveis no processamento de mídia de terceiros.
* **O que não significa**: Não significa uma API externa hospedada separadamente.
* **Sinônimos aceitáveis**: Extensão
* **Termos desencorajados ou proibidos**: Penduricalho técnico
* **Exemplo correto**: O Plugin de compressão H265 foi registrado no motor principal.
* **Exemplo incorreto**: Instalamos um Plugin no cabo de força do servidor.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Interface, Módulo

### Port

* **Categoria**: Arquitetura
* **Nome oficial**: Port
* **Nome técnico**: Port
* **Definição**: Interface ou contrato que define como o núcleo da aplicação interage com atores externos.
* **Uso no AutoMedia AI**: Utilizado para aplicar o princípio de inversão de dependência em arquiteturas hexagonais.
* **O que não significa**: Não significa porta de rede lógica TCP/UDP.
* **Sinônimos aceitáveis**: Porta
* **Termos desencorajados ou proibidos**: Buraco de entrada
* **Exemplo correto**: A aplicação expõe um Port para permitir envio de notificações.
* **Exemplo incorreto**: Abra o Port 80 no firewall.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Adapter, Interface

### Provider

* **Categoria**: Arquitetura
* **Nome oficial**: Provider
* **Nome técnico**: Provider
* **Definição**: Implementação concreta que fornece um serviço externo ou configuração para o sistema.
* **Uso no AutoMedia AI**: Encapsula serviços de nuvem e ferramentas fornecidas por terceiros.
* **O que não significa**: Não significa provedor de internet local.
* **Sinônimos aceitáveis**: Fornecedor de serviço
* **Termos desencorajados ou proibidos**: Terceirizado
* **Exemplo correto**: O Provider da AWS lida com a conexão aos buckets S3.
* **Exemplo incorreto**: O Provider cortou nossa conexão Wi-Fi.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Configuração de Provider

### Request ID

* **Categoria**: Arquitetura
* **Nome oficial**: Request ID
* **Nome técnico**: Request ID
* **Definição**: Identificador gerado no momento da entrada de uma requisição específica para rastreabilidade de log pontual.
* **Uso no AutoMedia AI**: Identifica chamadas HTTP individuais que chegam ao API Gateway.
* **O que não significa**: Não significa o identificador do usuário ou entidade.
* **Sinônimos aceitáveis**: ID da Requisição
* **Termos desencorajados ou proibidos**: Crachá do pacote
* **Exemplo correto**: Incluímos o Request ID no cabeçalho de resposta para facilitar suporte ao cliente.
* **Exemplo incorreto**: Usamos o Request ID como chave primária de cliente no banco.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Correlation ID

### Retry

* **Categoria**: Arquitetura
* **Nome oficial**: Retry
* **Nome técnico**: Retry
* **Definição**: Mecanismo automático para reexecutar uma operação que falhou, tipicamente devido a falhas transitórias.
* **Uso no AutoMedia AI**: Integrado em comunicação HTTP externa e consumo de filas com estratégias de backoff.
* **O que não significa**: Não significa forçar indefinidamente requisições em falhas definitivas de regra de negócio.
* **Sinônimos aceitáveis**: Retentativa
* **Termos desencorajados ou proibidos**: Tentar na marra
* **Exemplo correto**: A política de Retry com backoff exponencial lidou com a indisponibilidade momentânea da rede.
* **Exemplo incorreto**: O Retry continuou chamando o serviço que exigia credenciais inválidas.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Idempotência, Circuit Breaker

### Serviço

* **Categoria**: Arquitetura
* **Nome oficial**: Serviço
* **Nome técnico**: Serviço
* **Definição**: Componente de software autônomo que provê uma funcionalidade específica via rede ou API.
* **Uso no AutoMedia AI**: Responsável por fornecer capacidades de negócio reutilizáveis.
* **O que não significa**: Não significa uma classe utilitária interna.
* **Sinônimos aceitáveis**: Web service
* **Termos desencorajados ou proibidos**: Trabalhador mágico
* **Exemplo correto**: O Serviço de autenticação emitiu o token de acesso.
* **Exemplo incorreto**: O Serviço de formatação de string falhou.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Microsserviço

### Síncrono

* **Categoria**: Arquitetura
* **Nome oficial**: Síncrono
* **Nome técnico**: Síncrono
* **Definição**: Modelo de comunicação ou processamento em que a execução é bloqueada aguardando o retorno da resposta.
* **Uso no AutoMedia AI**: Utilizado para leitura de dados e validações imediatas onde a latência é baixa.
* **O que não significa**: Não significa desempenho rápido garantido.
* **Sinônimos aceitáveis**: Bloqueante
* **Termos desencorajados ou proibidos**: Em tempo real, travante
* **Exemplo correto**: A requisição HTTP aguarda de forma síncrona pelo token JWT.
* **Exemplo incorreto**: O processamento síncrono de um lote de fotos bloqueou a execução da thread principal.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Assíncrono

### State Machine

* **Categoria**: Arquitetura
* **Nome oficial**: State Machine
* **Nome técnico**: State Machine
* **Definição**: Modelo computacional abstrato que transita entre um número finito de estados com base em transições e eventos.
* **Uso no AutoMedia AI**: Controla explicitamente o ciclo de vida e mudanças de status de entidades complexas.
* **O que não significa**: Não significa estado armazenado em memória local temporária.
* **Sinônimos aceitáveis**: Máquina de estados finitos
* **Termos desencorajados ou proibidos**: Controlador maluco
* **Exemplo correto**: A State Machine impede a transição do estado 'Pendente' direto para 'Concluído'.
* **Exemplo incorreto**: A variável booleana foi renomeada para State Machine.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Workflow

### Subdomínio

* **Categoria**: Arquitetura
* **Nome oficial**: Subdomínio
* **Nome técnico**: Subdomínio
* **Definição**: Uma parte focada e especializada de um Domínio maior.
* **Uso no AutoMedia AI**: Utilizado para quebrar a complexidade do negócio em partes menores e gerenciáveis.
* **O que não significa**: Não significa um subdomínio de rede ou DNS.
* **Sinônimos aceitáveis**: Área de negócio secundária
* **Termos desencorajados ou proibidos**: Puxadinho do domínio
* **Exemplo correto**: O Subdomínio de logística apoia o Domínio principal de e-commerce.
* **Exemplo incorreto**: Criei um Subdomínio na AWS para o sistema.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Domínio, Bounded Context

### Trace ID

* **Categoria**: Arquitetura
* **Nome oficial**: Trace ID
* **Nome técnico**: Trace ID
* **Definição**: Identificador que mapeia a execução de uma solicitação no contexto de telemetria e rastreamento distribuído.
* **Uso no AutoMedia AI**: Inserido pelo sistema de OpenTelemetry para formar a cadeia completa de spans.
* **O que não significa**: Não significa log de auditoria de alteração de banco de dados.
* **Sinônimos aceitáveis**: Identificador de Rastreio
* **Termos desencorajados ou proibidos**: Detetive de pacotes
* **Exemplo correto**: O Trace ID permitiu visualizar a latência entre API e Banco no grafana.
* **Exemplo incorreto**: Envie o Trace ID via email de marketing para o cliente.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Correlation ID

### Vendor Lock-in

* **Categoria**: Arquitetura
* **Nome oficial**: Vendor Lock-in
* **Nome técnico**: Vendor Lock-in
* **Definição**: Situação de dependência forte a uma tecnologia ou fornecedor proprietário onde o custo de troca é alto.
* **Uso no AutoMedia AI**: Minimizado pelo uso de interfaces que encapsulam a infraestrutura e padrões abertos.
* **O que não significa**: Não significa que evitar fornecedores seja mandatório se a agilidade compensar o risco.
* **Sinônimos aceitáveis**: Prisão tecnológica
* **Termos desencorajados ou proibidos**: Refém da Big Tech
* **Exemplo correto**: Adoção de padrões OCI evita o Vendor Lock-in de imagens Docker.
* **Exemplo incorreto**: Sofremos Vendor Lock-in porque programamos em Português.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Interface

### Workflow

* **Categoria**: Arquitetura
* **Nome oficial**: Workflow
* **Nome técnico**: Workflow
* **Definição**: Série de etapas, decisões e regras lógicas que concluem um processo de negócio de ponta a ponta.
* **Uso no AutoMedia AI**: Modela aprovações e processos longos que exigem controle de estado e intervenções.
* **O que não significa**: Não significa apenas uma sequência linear simples sem decisões.
* **Sinônimos aceitáveis**: Fluxo de trabalho
* **Termos desencorajados ou proibidos**: Burocracia automatizada
* **Exemplo correto**: O Workflow de aprovação aguarda a assinatura do gestor.
* **Exemplo incorreto**: Salvar um registro simples no banco aciona um Workflow complexo.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: State Machine


## 6. Conceitos de Código

### Aggregate

* **Categoria**: Arquitetura
* **Nome oficial**: Aggregate
* **Nome técnico**: Aggregate
* **Definição**: Agrupamento transacional e lógico de Entidades e Value Objects em torno de um Aggregate Root principal.
* **Uso no AutoMedia AI**: Define consistência de dados em salva-guardas onde a atualização precisa ocorrer por inteira.
* **O que não significa**: Não significa agrupar todos os objetos no sistema sob a mesma tabela.
* **Sinônimos aceitáveis**: Agregado
* **Termos desencorajados ou proibidos**: Bola de neve de dados
* **Exemplo correto**: A manipulação das sub-entidades ocorre unicamente via Aggregate Root.
* **Exemplo incorreto**: Editei os itens do pedido burlando o Aggregate Root principal.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Entidade, Repository

### Contrato

* **Categoria**: Arquitetura
* **Nome oficial**: Contrato
* **Nome técnico**: Contrato
* **Definição**: Acordo rigoroso do formato de dados de entrada e saída esperado por um sistema ou API.
* **Uso no AutoMedia AI**: Assegura estabilidade na comunicação REST ou gRPC documentada por especificações (ex: OpenAPI).
* **O que não significa**: Não significa documento jurídico assinado pelas partes.
* **Sinônimos aceitáveis**: Especificação de API
* **Termos desencorajados ou proibidos**: Contrato jurídico sem aprovação
* **Exemplo correto**: A API v2 quebrou o Contrato ao remover campos obrigatórios.
* **Exemplo incorreto**: O Contrato de software exige a assinatura física da equipe.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Interface

### DTO

* **Categoria**: Arquitetura
* **Nome oficial**: DTO
* **Nome técnico**: DTO
* **Definição**: Data Transfer Object, um objeto projetado puramente para portar dados entre processos, sem comportamento lógico.
* **Uso no AutoMedia AI**: Padrão no isolamento das propriedades recebidas de controladores ou filas antes de mapeá-las.
* **O que não significa**: Não significa uma classe de Entidade com modelo de persistência.
* **Sinônimos aceitáveis**: Objeto de Transferência
* **Termos desencorajados ou proibidos**: Pacote mudo de dados
* **Exemplo correto**: O DTO agrupa as informações de tela antes de repassar ao serviço de aplicação.
* **Exemplo incorreto**: O DTO executa cálculos de juros internamente.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Contrato

### Entidade

* **Categoria**: Arquitetura
* **Nome oficial**: Entidade
* **Nome técnico**: Entidade
* **Definição**: Objeto de domínio central possuidor de identidade única e contínua e lógica de negócio.
* **Uso no AutoMedia AI**: Centraliza o estado rico da aplicação e garante as invariantes do negócio.
* **O que não significa**: Não significa um simples espelho (schema) estático de tabela de banco de dados relacional.
* **Sinônimos aceitáveis**: Domain Entity
* **Termos desencorajados ou proibidos**: Objeto inviolável master
* **Exemplo correto**: A Entidade Cliente gera um identificador unívoco no seu construtor.
* **Exemplo incorreto**: A Entidade serve apenas como uma struct para mapear JSON.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Value Object, Aggregate

### Interface

* **Categoria**: Arquitetura
* **Nome oficial**: Interface
* **Nome técnico**: Interface
* **Definição**: Assinatura ou contrato de métodos e propriedades sem sua implementação efetiva.
* **Uso no AutoMedia AI**: Aplicada para estabelecer a separação estrita de contratos nas portas do sistema.
* **O que não significa**: Não significa interface visual de usuário (UI).
* **Sinônimos aceitáveis**: Contrato abstrato
* **Termos desencorajados ou proibidos**: Pacto irrevogável
* **Exemplo correto**: A classe concretizou os métodos exigidos pela Interface abstrata.
* **Exemplo incorreto**: A Interface possui três botões coloridos na web.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Contrato, Port

### Repository

* **Categoria**: Arquitetura
* **Nome oficial**: Repository
* **Nome técnico**: Repository
* **Definição**: Padrão que atua como mediador entre domínio e infraestrutura de persistência, similar a uma coleção em memória.
* **Uso no AutoMedia AI**: Encapsula consultas complexas e lida exclusivamente com persistência de Aggregates inteiros.
* **O que não significa**: Não significa gerenciador direto de conexões SQL.
* **Sinônimos aceitáveis**: Repositório
* **Termos desencorajados ou proibidos**: Saco sem fundo de banco
* **Exemplo correto**: O Repository foi injetado na aplicação buscando os registros via interface genérica.
* **Exemplo incorreto**: O Repository enviou um email de confirmação.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Aggregate, Interface

### Use Case

* **Categoria**: Arquitetura
* **Nome oficial**: Use Case
* **Nome técnico**: Use Case
* **Definição**: Interação delimitada focada em atingir um objetivo prático do usuário coordenando domínio e serviços externos.
* **Uso no AutoMedia AI**: Implementa funções cruciais na Camada de Aplicação como criar pedidos e autenticar acessos.
* **O que não significa**: Não significa um documento descritivo imenso formatado no Word.
* **Sinônimos aceitáveis**: Caso de Uso
* **Termos desencorajados ou proibidos**: Drama de uso contínuo
* **Exemplo correto**: O Use Case buscou dados do repositório, executou a regra e salvou o resultado.
* **Exemplo incorreto**: O Use Case de front-end reordenou listas CSS no navegador.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Camada de Aplicação

### Value Object

* **Categoria**: Arquitetura
* **Nome oficial**: Value Object
* **Nome técnico**: Value Object
* **Definição**: Objeto tipado sem identidade conceitual cujo estado é imutável, focado nas propriedades contidas.
* **Uso no AutoMedia AI**: Representa elementos tipicamente comparáveis por valor como Moeda, Email ou Distância.
* **O que não significa**: Não significa tipos primitivos simples sem validação anexada.
* **Sinônimos aceitáveis**: Objeto de Valor
* **Termos desencorajados ou proibidos**: Variável inútil estática
* **Exemplo correto**: Dois Value Objects são iguais se todos os seus atributos internos forem iguais.
* **Exemplo incorreto**: Alterei a propriedade do Value Object diretamente via setter mutável.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Entidade


## 6. Conceitos de Infraestrutura

### Job

* **Categoria**: Arquitetura
* **Nome oficial**: Job
* **Nome técnico**: Job
* **Definição**: Unidade de trabalho encapsulada projetada para execução em plano de fundo ou lote, geralmente programada.
* **Uso no AutoMedia AI**: Executa processos pesados programados, como sincronização noturna.
* **O que não significa**: Não significa solicitação de visualização da web instantânea.
* **Sinônimos aceitáveis**: Tarefa em lote
* **Termos desencorajados ou proibidos**: Trabalho não padronizado escondido
* **Exemplo correto**: O Job noturno limpou os registros temporários de sessões prescritas.
* **Exemplo incorreto**: Um novo Job foi disparado sempre que o usuário digitava na busca.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Task, Worker

### Queue

* **Categoria**: Arquitetura
* **Nome oficial**: Queue
* **Nome técnico**: Queue
* **Definição**: Estrutura de dados arquitetural onde itens são acumulados sequencialmente permitindo consumo assíncrono.
* **Uso no AutoMedia AI**: Mecanismo essencial para absorver surtos de tráfego (buffering) no sistema de processamento de fotos do veículo.
* **O que não significa**: Não significa estrutura exclusiva em memória RAM estática sem persistência.
* **Sinônimos aceitáveis**: Fila
* **Termos desencorajados ou proibidos**: Salsicha de eventos longa
* **Exemplo correto**: As mensagens de confirmação de conta entraram na Queue de emails.
* **Exemplo incorreto**: O HTML renderizou a Queue de elementos visuais do menu web.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Worker, Assíncrono

### Task

* **Categoria**: Arquitetura
* **Nome oficial**: Task
* **Nome técnico**: Task
* **Definição**: Fragmento discreto de processamento derivado de um Job maior.
* **Uso no AutoMedia AI**: Empregado para paralelizar o trabalho fragmentando um Job em Tasks distribuídas.
* **O que não significa**: Não significa anotação manual em lista de afazeres.
* **Sinônimos aceitáveis**: Tarefa isolada
* **Termos desencorajados ou proibidos**: Pingo de esforço
* **Exemplo correto**: A thread pool processou dez Tasks simultâneas.
* **Exemplo incorreto**: A Task desenhou a tela HTML principal.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Job, Worker

### Worker

* **Categoria**: Arquitetura
* **Nome oficial**: Worker
* **Nome técnico**: Worker
* **Definição**: Processo de software executando continuamente em segundo plano consumindo tarefas alocadas em filas.
* **Uso no AutoMedia AI**: Responsável pela execução escalável de codificação de mídia e retentativas.
* **O que não significa**: Não significa empregado humano de suporte técnico.
* **Sinônimos aceitáveis**: Processo de fila
* **Termos desencorajados ou proibidos**: Escravo de fila, capacho da memória
* **Exemplo correto**: Subimos dez instâncias de Worker para zerar o acúmulo da fila de processamento.
* **Exemplo incorreto**: O Worker atendeu ligações telefônicas dos clientes.
* **Documentos relacionados**: architecture.md
* **Termos relacionados**: Job, Queue


## 7. Engines Oficiais

### AI Gateway

* **Categoria**: Componente de Integração
* **Nome oficial**: AI Gateway
* **Nome técnico**: AIGateway
* **Definição**: Ponto de entrada unificado para o roteamento de chamadas destinadas a modelos de inteligência artificial. O componente gerencia quotas, telemetria e balanceamento de carga entre provedores.
* **Uso no AutoMedia AI**: Utilizado para centralizar todas as requisições dos motores internos para APIs de modelos de linguagem e visão externos.
* **O que não significa**: Não é o modelo de inteligência artificial em si, mas sim o seu gerenciador de tráfego.
* **Sinônimos aceitáveis**: Gateway de IA, Proxy de Inteligência Artificial
* **Termos desencorajados ou proibidos**: Cérebro Supremo, administrador da Máquina
* **Exemplo correto**: O AI Gateway roteou a requisição para o provedor secundário devido à indisponibilidade do principal.
* **Exemplo incorreto**: O AI Gateway puniu o servidor instável com um banimento eterno.
* **Documentos relacionados**: 008_gateway_roteamento.md
* **Termos relacionados**: Vision Engine, Image Engine

### Brand Engine

* **Categoria**: Componente de Configuração
* **Nome oficial**: Brand Engine
* **Nome técnico**: BrandEngine
* **Definição**: Serviço que gerencia as diretrizes e os ativos de identidade visual de uma marca. O componente assegura que as regras de tipografia, cores e logotipos sejam aplicadas uniformemente.
* **Uso no AutoMedia AI**: Utilizado para fornecer as regras de marca aos outros motores durante a geração de conteúdo.
* **O que não significa**: Não é uma ferramenta de criação de logotipos.
* **Sinônimos aceitáveis**: Gerenciador de Marca, Motor de Identidade Visual
* **Termos desencorajados ou proibidos**: Polícia da Marca, Ditador de Estilo
* **Exemplo correto**: O Brand Engine forneceu a paleta de cores correta para o Layout Engine.
* **Exemplo incorreto**: O Brand Engine forçou sua vontade sobre o design do sistema.
* **Documentos relacionados**: 002_diretrizes_marca.md
* **Termos relacionados**: Layout Engine, Identity Engine

### Delivery Engine

* **Categoria**: Componente de Distribuição
* **Nome oficial**: Delivery Engine
* **Nome técnico**: DeliveryEngine
* **Definição**: Serviço encarregado de empacotar e transmitir os artefatos gerados para plataformas externas. O componente gerencia o roteamento, formato de entrega e conexões com APIs de destino.
* **Uso no AutoMedia AI**: Utilizado para publicar os anúncios e mídias sociais diretamente nas plataformas parceiras após a aprovação.
* **O que não significa**: Não é uma rede de distribuição de conteúdo para hospedagem pública.
* **Sinônimos aceitáveis**: Motor de Entrega, Distribuidor de Mídia
* **Termos desencorajados ou proibidos**: Canhão de Publicação, Disparador Mortal
* **Exemplo correto**: O Delivery Engine enviou o pacote de imagens para a API da rede social.
* **Exemplo incorreto**: O Delivery Engine bombardeou a internet com os novos anúncios.
* **Documentos relacionados**: 005_integracoes_api.md
* **Termos relacionados**: AI Gateway

### Identity Engine

* **Categoria**: Componente de Segurança
* **Nome oficial**: Identity Engine
* **Nome técnico**: IdentityEngine
* **Definição**: Serviço de autenticação e autorização centralizado. O componente verifica credenciais, emite tokens de acesso e gerencia ciclos de vida de sessão de usuários e serviços.
* **Uso no AutoMedia AI**: Utilizado para autenticar requisições na plataforma e garantir o controle de acesso baseado em funções.
* **O que não significa**: Não é um diretório de recursos humanos ou cadastro de clientes de marketing.
* **Sinônimos aceitáveis**: Motor de Identidade, Provedor de Autenticação
* **Termos desencorajados ou proibidos**: Cão de Guarda, Porteiro de Balada
* **Exemplo correto**: O Identity Engine renovou o token de acesso após a verificação das credenciais.
* **Exemplo incorreto**: O Identity Engine barrou o intruso com força total.
* **Documentos relacionados**: 007_autenticacao.md
* **Termos relacionados**: Workspace Engine

### Image Engine

* **Categoria**: Componente de Processamento
* **Nome oficial**: Image Engine
* **Nome técnico**: ImageEngine
* **Definição**: Serviço dedicado à manipulação, transformação e geração de imagens. O componente aplica filtros, redimensionamentos e composições baseadas em parâmetros predefinidos.
* **Uso no AutoMedia AI**: Utilizado para gerar as variações de imagens necessárias para diferentes plataformas e formatos de publicação.
* **O que não significa**: Não é um armazenamento de arquivos de imagem estáticos.
* **Sinônimos aceitáveis**: Processador de Imagem, Gerador de Imagem
* **Termos desencorajados ou proibidos**: Fábrica de Imagens, Gerador não padronizado
* **Exemplo correto**: O Image Engine redimensionou o arquivo para as dimensões exigidas pela rede social.
* **Exemplo incorreto**: O Image Engine sobrescreveu o arquivo original do veículo sem manter o backup efêmero.
* **Documentos relacionados**: 001_arquitetura_modulos.md
* **Termos relacionados**: Vision Engine, Layout Engine

### Layout Engine

* **Categoria**: Componente de Composição
* **Nome oficial**: Layout Engine
* **Nome técnico**: LayoutEngine
* **Definição**: Serviço responsável por organizar espacialmente os elementos visuais e textuais em uma mídia. O componente calcula posições, margens e alinhamentos conforme templates definidos.
* **Uso no AutoMedia AI**: Utilizado para posicionar textos, logotipos e imagens base de acordo com as regras estruturais e de marca.
* **O que não significa**: Não é um editor visual interativo de arrastar e soltar para usuários finais.
* **Sinônimos aceitáveis**: Motor de Diagramação, Compositor de Layout
* **Termos desencorajados ou proibidos**: Arquiteto Mágico, Pintor de Telas
* **Exemplo correto**: O Layout Engine posicionou o texto promocional na parte inferior da imagem.
* **Exemplo incorreto**: O Layout Engine fez uma mágica para encaixar os textos na tela.
* **Documentos relacionados**: 003_templates_design.md
* **Termos relacionados**: Brand Engine, Image Engine

### Marketing Engine

* **Categoria**: Componente de Regras de Negócio
* **Nome oficial**: Marketing Engine
* **Nome técnico**: MarketingEngine
* **Definição**: Serviço que aplica lógicas de campanhas promocionais e estratégias de engajamento ao conteúdo. O componente seleciona textos persuasivos e chamadas para ação adequadas.
* **Uso no AutoMedia AI**: Utilizado para adaptar a mensagem gerada aos objetivos de conversão e ao público-alvo da campanha.
* **O que não significa**: Não é uma plataforma de automação de envio de e-mails.
* **Sinônimos aceitáveis**: Motor de Marketing, Otimizador de Campanhas
* **Termos desencorajados ou proibidos**: Máquina de Vendas, Manipulador de Clientes, Captador sem filtro
* **Exemplo correto**: O Marketing Engine selecionou a chamada para ação com base no segmento do usuário.
* **Exemplo incorreto**: O Marketing Engine aniquilou a concorrência com seus textos letais.
* **Documentos relacionados**: 004_regras_campanha.md
* **Termos relacionados**: Brand Engine, Delivery Engine

### Vision Engine

* **Categoria**: Componente de Análise
* **Nome oficial**: Vision Engine
* **Nome técnico**: VisionEngine
* **Definição**: Serviço responsável por processar e analisar mídias visuais utilizando modelos de inteligência artificial. O componente extrai metadados, identifica elementos e classifica o conteúdo da imagem.
* **Uso no AutoMedia AI**: Utilizado para interpretar imagens enviadas pelos usuários e fornecer dados estruturados para outras etapas do pipeline de processamento.
* **O que não significa**: Não é um serviço de edição de imagens ou de renderização gráfica.
* **Sinônimos aceitáveis**: Módulo de Visão, Analisador Visual
* **Termos desencorajados ou proibidos**: Olho Mágico, Vidente, Analisador Supremo
* **Exemplo correto**: O Vision Engine classificou a imagem como contendo um veículo e extraiu a cor predominante.
* **Exemplo incorreto**: O Vision Engine usou seus poderes mágicos para adivinhar a foto.
* **Documentos relacionados**: 001_arquitetura_modulos.md
* **Termos relacionados**: Image Engine, AI Gateway

### Workspace Engine

* **Categoria**: Componente de Organização
* **Nome oficial**: Workspace Engine
* **Nome técnico**: WorkspaceEngine
* **Definição**: Serviço que isola e gerencia os recursos, permissões e projetos de diferentes clientes ou equipes. O componente garante a segregação lógica dos dados no sistema.
* **Uso no AutoMedia AI**: Utilizado para criar ambientes de trabalho separados, permitindo o gerenciamento independente de ativos e usuários.
* **O que não significa**: Não é um ambiente de virtualização de sistema operacional.
* **Sinônimos aceitáveis**: Gerenciador de Área de Trabalho, Motor de Workspace
* **Termos desencorajados ou proibidos**: Prisão de Usuários, Feudo de Clientes
* **Exemplo correto**: O Workspace Engine validou as permissões antes de permitir a alteração do projeto.
* **Exemplo incorreto**: O Workspace Engine trancou o usuário na masmorra do sistema.
* **Documentos relacionados**: 006_controle_acesso.md
* **Termos relacionados**: Identity Engine


## 8. Conceitos de Imagem e Visão Computacional

### Alpha Mask

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Alpha Mask
* **Nome técnico**: Alpha Mask
* **Definição**: Processamento técnico correspondente a Alpha Mask.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Alpha Mask foi concluída no tempo esperado.
* **Exemplo incorreto**: A geração de alpha mask removeu partes da lataria do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Alteração Indevida do Veículo

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Alteração Indevida do Veículo
* **Nome técnico**: Alteração Indevida do Veículo
* **Definição**: Processamento técnico correspondente a Alteração Indevida do Veículo.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Alteração Indevida do Veículo foi concluída no tempo esperado.
* **Exemplo incorreto**: A alteração de imagem modificou a cor original do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Aspect Ratio

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Aspect Ratio
* **Nome técnico**: Aspect Ratio
* **Definição**: Processamento técnico correspondente a Aspect Ratio.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Aspect Ratio foi concluída no tempo esperado.
* **Exemplo incorreto**: A alteração de aspect ratio distorceu as proporções do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Asset

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Asset
* **Nome técnico**: Asset
* **Definição**: Processamento técnico correspondente a Asset.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Asset foi concluída no tempo esperado.
* **Exemplo incorreto**: O asset visual foi renderizado em resolução incompatível.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Background

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Background
* **Nome técnico**: Background
* **Definição**: Processamento técnico correspondente a Background.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Background foi concluída no tempo esperado.
* **Exemplo incorreto**: O background gerado cobriu elementos da lataria do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Balanço de Branco

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Balanço de Branco
* **Nome técnico**: Balanço de Branco
* **Definição**: Processamento técnico correspondente a Balanço de Branco.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Balanço de Branco foi concluída no tempo esperado.
* **Exemplo incorreto**: O balanço de branco alterou a tonalidade real da pintura do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Bounding Box

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Bounding Box
* **Nome técnico**: Bounding Box
* **Definição**: Processamento técnico correspondente a Bounding Box.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Bounding Box foi concluída no tempo esperado.
* **Exemplo incorreto**: A bounding box delimitou uma área fora dos limites do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Censura de Placa

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Censura de Placa
* **Nome técnico**: Censura de Placa
* **Definição**: Processamento técnico correspondente a Censura de Placa.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Censura de Placa foi concluída no tempo esperado.
* **Exemplo incorreto**: A censura de placa removeu metadados essenciais da imagem.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Classificação

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Classificação
* **Nome técnico**: Classificação
* **Definição**: Processamento técnico correspondente a Classificação.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Classificação foi concluída no tempo esperado.
* **Exemplo incorreto**: A classificação atribuiu uma categoria incorreta ao veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Cobertura de Placa com Logo

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Cobertura de Placa com Logo
* **Nome técnico**: Cobertura de Placa com Logo
* **Definição**: Processamento técnico correspondente a Cobertura de Placa com Logo.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Cobertura de Placa com Logo foi concluída no tempo esperado.
* **Exemplo incorreto**: A cobertura de placa ocultou áreas externas à placa do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Compressão

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Compressão
* **Nome técnico**: Compressão
* **Definição**: Processamento técnico correspondente a Compressão.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Compressão foi concluída no tempo esperado.
* **Exemplo incorreto**: A compressão reduziu a qualidade visual abaixo do limite aceitável.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Contraste

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Contraste
* **Nome técnico**: Contraste
* **Definição**: Processamento técnico correspondente a Contraste.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Contraste foi concluída no tempo esperado.
* **Exemplo incorreto**: O ajuste de contraste estourou os destaques da iluminação do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Correção de Cor

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Correção de Cor
* **Nome técnico**: Correção de Cor
* **Definição**: Processamento técnico correspondente a Correção de Cor.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Correção de Cor foi concluída no tempo esperado.
* **Exemplo incorreto**: A correção de cor descaracterizou a cor comercial da lataria.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Cropping

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Cropping
* **Nome técnico**: Cropping
* **Definição**: Processamento técnico correspondente a Cropping.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Cropping foi concluída no tempo esperado.
* **Exemplo incorreto**: O cropping cortou partes das rodas e extremidades do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Desfoque de Placa

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Desfoque de Placa
* **Nome técnico**: Desfoque de Placa
* **Definição**: Processamento técnico correspondente a Desfoque de Placa.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Desfoque de Placa foi concluída no tempo esperado.
* **Exemplo incorreto**: O desfoque de placa aplicou efeito borrado fora da área da placa.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Detecção

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Detecção
* **Nome técnico**: Detecção
* **Definição**: Processamento técnico correspondente a Detecção.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Detecção foi concluída no tempo esperado.
* **Exemplo incorreto**: A detecção alterou indevidamente o arquivo original.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Enquadramento

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Enquadramento
* **Nome técnico**: Enquadramento
* **Definição**: Processamento técnico correspondente a Enquadramento.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Enquadramento foi concluída no tempo esperado.
* **Exemplo incorreto**: O enquadramento descentralizou o veículo na imagem da capa.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Exposição

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Exposição
* **Nome técnico**: Exposição
* **Definição**: Processamento técnico correspondente a Exposição.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Exposição foi concluída no tempo esperado.
* **Exemplo incorreto**: A exposição excessiva ocultou detalhes do acabamento interno.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Foreground

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Foreground
* **Nome técnico**: Foreground
* **Definição**: Processamento técnico correspondente a Foreground.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Foreground foi concluída no tempo esperado.
* **Exemplo incorreto**: O foreground foi isolado com recortes imprecisos nas bordas.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Foto Principal

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Foto Principal
* **Nome técnico**: Foto Principal
* **Definição**: Processamento técnico correspondente a Foto Principal.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Foto Principal foi concluída no tempo esperado.
* **Exemplo incorreto**: A foto principal foi definida sem validação do ângulo do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Foto Secundária

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Foto Secundária
* **Nome técnico**: Foto Secundária
* **Definição**: Processamento técnico correspondente a Foto Secundária.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Foto Secundária foi concluída no tempo esperado.
* **Exemplo incorreto**: A foto secundária foi colocada em destaque no lugar da foto de capa.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Geração de Estúdio

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Geração de Estúdio
* **Nome técnico**: Geração de Estúdio
* **Definição**: Processamento técnico correspondente a Geração de Estúdio.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Geração de Estúdio foi concluída no tempo esperado.
* **Exemplo incorreto**: A geração de estúdio substituiu o veículo por outro modelo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Geração Realista

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Geração Realista
* **Nome técnico**: Geração Realista
* **Definição**: Processamento técnico correspondente a Geração Realista.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Geração Realista foi concluída no tempo esperado.
* **Exemplo incorreto**: A geração realista adicionou elementos inexistentes ao veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Imagem Original

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Imagem Original
* **Nome técnico**: Imagem Original
* **Definição**: Processamento técnico correspondente a Imagem Original.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Imagem Original foi concluída no tempo esperado.
* **Exemplo incorreto**: A imagem original foi modificada sem preservar o arquivo fonte.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Imagem Processada

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Imagem Processada
* **Nome técnico**: Imagem Processada
* **Definição**: Processamento técnico correspondente a Imagem Processada.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Imagem Processada foi concluída no tempo esperado.
* **Exemplo incorreto**: A imagem processada apresentou artefatos visuais de interpolação.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Inpainting

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Inpainting
* **Nome técnico**: Inpainting
* **Definição**: Processamento técnico correspondente a Inpainting.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Inpainting foi concluída no tempo esperado.
* **Exemplo incorreto**: O inpainting alterou o design das rodas originais do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Marca d'água

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Marca d'água
* **Nome técnico**: Marca d'água
* **Definição**: Processamento técnico correspondente a Marca d'água.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Marca d'água foi concluída no tempo esperado.
* **Exemplo incorreto**: A marca d'água foi aplicada sobre o centro do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Máscara

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Máscara
* **Nome técnico**: Máscara
* **Definição**: Processamento técnico correspondente a Máscara.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Máscara foi concluída no tempo esperado.
* **Exemplo incorreto**: A máscara de segmentação vazou para a área de sombra do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Nitidez

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Nitidez
* **Nome técnico**: Nitidez
* **Definição**: Processamento técnico correspondente a Nitidez.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Nitidez foi concluída no tempo esperado.
* **Exemplo incorreto**: A nitidez excessiva gerou ruído digital nos reflexos da lataria.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Orientação

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Orientação
* **Nome técnico**: Orientação
* **Definição**: Processamento técnico correspondente a Orientação.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Orientação foi concluída no tempo esperado.
* **Exemplo incorreto**: A orientação da imagem foi rotacionada incorretamente.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Outpainting

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Outpainting
* **Nome técnico**: Outpainting
* **Definição**: Processamento técnico correspondente a Outpainting.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Outpainting foi concluída no tempo esperado.
* **Exemplo incorreto**: O outpainting gerou proporções irrealistas no cenário de fundo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Preservação do Veículo

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Preservação do Veículo
* **Nome técnico**: Preservação do Veículo
* **Definição**: Processamento técnico correspondente a Preservação do Veículo.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Preservação do Veículo foi concluída no tempo esperado.
* **Exemplo incorreto**: A preservação do veículo permitiu a alteração da geometria original.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Proporção

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Proporção
* **Nome técnico**: Proporção
* **Definição**: Processamento técnico correspondente a Proporção.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Proporção foi concluída no tempo esperado.
* **Exemplo incorreto**: A proporção da imagem foi alterada sem aplicar letterboxing.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Qualidade Visual

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Qualidade Visual
* **Nome técnico**: Qualidade Visual
* **Definição**: Processamento técnico correspondente a Qualidade Visual.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Qualidade Visual foi concluída no tempo esperado.
* **Exemplo incorreto**: A qualidade visual foi avaliada sem análise de resolução mínima.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Recorte

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Recorte
* **Nome técnico**: Recorte
* **Definição**: Processamento técnico correspondente a Recorte.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Recorte foi concluída no tempo esperado.
* **Exemplo incorreto**: O recorte eliminou o teto do veículo na imagem gerada.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Redução de Ruído

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Redução de Ruído
* **Nome técnico**: Redução de Ruído
* **Definição**: Processamento técnico correspondente a Redução de Ruído.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Redução de Ruído foi concluída no tempo esperado.
* **Exemplo incorreto**: A redução de ruído suavizou detalhes dos faróis e textura da pintura.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Remoção de Fundo

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Remoção de Fundo
* **Nome técnico**: Remoção de Fundo
* **Definição**: Processamento técnico correspondente a Remoção de Fundo.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Remoção de Fundo foi concluída no tempo esperado.
* **Exemplo incorreto**: A remoção de fundo apagou os espelhos retrovisores do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Resolução

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Resolução
* **Nome técnico**: Resolução
* **Definição**: Processamento técnico correspondente a Resolução.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Resolução foi concluída no tempo esperado.
* **Exemplo incorreto**: A resolução final foi exportada abaixo do padrão exigido pelos portais.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Saturação

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Saturação
* **Nome técnico**: Saturação
* **Definição**: Processamento técnico correspondente a Saturação.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Saturação foi concluída no tempo esperado.
* **Exemplo incorreto**: A saturação excessiva desbotou os detalhes das sombras do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Score de Qualidade

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Score de Qualidade
* **Nome técnico**: Score de Qualidade
* **Definição**: Processamento técnico correspondente a Score de Qualidade.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Score de Qualidade foi concluída no tempo esperado.
* **Exemplo incorreto**: O score de qualidade aprovou uma imagem com desfoque excessivo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Segmentação

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Segmentação
* **Nome técnico**: Segmentação
* **Definição**: Processamento técnico correspondente a Segmentação.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Segmentação foi concluída no tempo esperado.
* **Exemplo incorreto**: A segmentação falhou ao separar os vidros do veículo do cenário.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Seleção da Melhor Foto

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Seleção da Melhor Foto
* **Nome técnico**: Seleção da Melhor Foto
* **Definição**: Processamento técnico correspondente a Seleção da Melhor Foto.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Seleção da Melhor Foto foi concluída no tempo esperado.
* **Exemplo incorreto**: A seleção da melhor foto escolheu uma imagem desfocada como capa.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Substituição de Fundo

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Substituição de Fundo
* **Nome técnico**: Substituição de Fundo
* **Definição**: Processamento técnico correspondente a Substituição de Fundo.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Substituição de Fundo foi concluída no tempo esperado.
* **Exemplo incorreto**: A substituição de fundo insere iluminação incompatível com o veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Super-resolução

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Super-resolução
* **Nome técnico**: Super-resolução
* **Definição**: Processamento técnico correspondente a Super-resolução.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Super-resolução foi concluída no tempo esperado.
* **Exemplo incorreto**: A super-resolução gerou bordas duplicadas na lataria.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Upscale

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Upscale
* **Nome técnico**: Upscale
* **Definição**: Processamento técnico correspondente a Upscale.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Upscale foi concluída no tempo esperado.
* **Exemplo incorreto**: O upscale introduziu suavização excessiva nos detalhes do veículo.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A

### Visual Asset

* **Categoria**: Visão Computacional e Processamento de Imagem
* **Nome oficial**: Visual Asset
* **Nome técnico**: Visual Asset
* **Definição**: Processamento técnico correspondente a Visual Asset.
* **Uso no AutoMedia AI**: Utilizado nos fluxos de processamento visual.
* **O que não significa**: Não se aplica a contextos fora de processamento digital.
* **Sinônimos aceitáveis**: N/A
* **Termos desencorajados ou proibidos**: N/A
* **Exemplo correto**: A operação de Visual Asset foi concluída no tempo esperado.
* **Exemplo incorreto**: O visual asset foi exportado em formato não suportado pelo canal.
* **Documentos relacionados**: Guia de Arquitetura Visual
* **Termos relacionados**: N/A


## 9. Conceitos de Marca, Design e Layout

### Assinatura Visual

* **Categoria**: Marca e Layout
* **Nome oficial**: Assinatura Visual
* **Nome técnico**: Visual Signature
* **Definição**: Combinação estruturada de elementos como logo, slogan e informações oficiais formatada de maneira padronizada.
* **Uso no AutoMedia AI**: Inserida automaticamente em marcas de água, rodapés de artes e criativos visuais gerados.
* **O que não significa**: Não corresponde a um campo de assinatura manual do usuário.
* **Sinônimos aceitáveis**: Assinatura Institucional
* **Termos desencorajados ou proibidos**: Chancela Monstruosa
* **Exemplo correto**: O documento oficial contém a Assinatura Visual ao final.
* **Exemplo incorreto**: O documento termina com aquela chancela monstruosa.
* **Documentos relacionados**: docs/brand_assets.md
* **Termos relacionados**: Rodapé, Logo

### Brand Snapshot

* **Categoria**: Marca e Layout
* **Nome oficial**: Brand Snapshot
* **Nome técnico**: Brand Snapshot
* **Definição**: Estrutura de dados imutável que registra o estado exato dos tokens e assets visuais em um dado momento.
* **Uso no AutoMedia AI**: Armazenada nos projetos para garantir que a renderização não se altere acidentalmente com mudanças futuras da marca.
* **O que não significa**: Não é uma ferramenta de backup geral do banco de dados.
* **Sinônimos aceitáveis**: Cópia da Marca
* **Termos desencorajados ou proibidos**: Túmulo da Identidade
* **Exemplo correto**: A exportação em lote utiliza o Brand Snapshot do momento da criação.
* **Exemplo incorreto**: O lote foi parar no túmulo da identidade antiga.
* **Documentos relacionados**: docs/architecture.md
* **Termos relacionados**: Identidade Visual, RenderRequestDTO

### Coleção de Identidade

* **Categoria**: Marca e Layout
* **Nome oficial**: Coleção de Identidade
* **Nome técnico**: Identity Collection
* **Definição**: Grupo estruturado de ativos e tokens relacionados a uma variação específica de identidade visual.
* **Uso no AutoMedia AI**: Permite alternar temas e conjuntos de estilos no sistema.
* **O que não significa**: Não substitui as diretrizes gerais de usabilidade.
* **Sinônimos aceitáveis**: Conjunto de Identidade
* **Termos desencorajados ou proibidos**: Bazar de Estilos
* **Exemplo correto**: O sistema importou a Coleção de Identidade para a nova campanha.
* **Exemplo incorreto**: O sistema puxou os assets daquele bazar de estilos soltos.
* **Documentos relacionados**: docs/brand_guidelines.md
* **Termos relacionados**: Identidade Visual

### Componente Visual

* **Categoria**: Marca e Layout
* **Nome oficial**: Componente Visual
* **Nome técnico**: UI Component
* **Definição**: Elemento encapsulado de interface de usuário que agrupa lógica, estrutura e estilo.
* **Uso no AutoMedia AI**: Unidade básica para a montagem de layouts parametrizados.
* **O que não significa**: Não é apenas um fragmento de código HTML sem comportamento.
* **Sinônimos aceitáveis**: Elemento de Interface
* **Termos desencorajados ou proibidos**: Caixa Burra
* **Exemplo correto**: O Componente Visual do botão foi atualizado.
* **Exemplo incorreto**: Fizeram uma caixa burra nova na tela.
* **Documentos relacionados**: docs/components.md
* **Termos relacionados**: Design System

### Composição

* **Categoria**: Marca e Layout
* **Nome oficial**: Composição
* **Nome técnico**: Composition
* **Definição**: Estrutura resultante do agrupamento coordenado de múltiplos componentes visuais.
* **Uso no AutoMedia AI**: Utilizada para criar seções completas de uma página a partir de partes menores.
* **O que não significa**: Não significa a mistura desordenada de elementos desconexos.
* **Sinônimos aceitáveis**: Estrutura Visual
* **Termos desencorajados ou proibidos**: Mistureba
* **Exemplo correto**: A Composição do cabeçalho agrupa o logo e a navegação.
* **Exemplo incorreto**: O topo do site é uma mistureba de botões.
* **Documentos relacionados**: docs/components.md
* **Termos relacionados**: Layout, Componente Visual

### Cor de Contraste

* **Categoria**: Marca e Layout
* **Nome oficial**: Cor de Contraste
* **Nome técnico**: Contrast Color
* **Definição**: Cor configurada para garantir a legibilidade de textos sobre fundos coloridos.
* **Uso no AutoMedia AI**: Garante acessibilidade visual na renderização dos layouts.
* **O que não significa**: Não é utilizada como cor principal de preenchimento.
* **Sinônimos aceitáveis**: Cor Acessível
* **Termos desencorajados ou proibidos**: Cor Berrante
* **Exemplo correto**: O texto sobre o fundo primário utiliza a Cor de Contraste.
* **Exemplo incorreto**: O texto tem uma cor berrante para não sumir no fundo.
* **Documentos relacionados**: docs/accessibility.md
* **Termos relacionados**: Acessibilidade

### Cor Primária

* **Categoria**: Marca e Layout
* **Nome oficial**: Cor Primária
* **Nome técnico**: Primary Color
* **Definição**: Cor principal utilizada para elementos de maior destaque na interface.
* **Uso no AutoMedia AI**: Aplicada em botões principais e ações afirmativas.
* **O que não significa**: Não é a única cor permitida na aplicação.
* **Sinônimos aceitáveis**: Cor Principal
* **Termos desencorajados ou proibidos**: Cor inviolável
* **Exemplo correto**: O botão de submissão utiliza a Cor Primária.
* **Exemplo incorreto**: O botão tem a cor inviolável da marca.
* **Documentos relacionados**: docs/design_system.md
* **Termos relacionados**: Cor Secundária, Paleta de Cores

### Cor Secundária

* **Categoria**: Marca e Layout
* **Nome oficial**: Cor Secundária
* **Nome técnico**: Secondary Color
* **Definição**: Cor auxiliar que acompanha a cor primária, oferecendo opções de contraste.
* **Uso no AutoMedia AI**: Empregada em elementos secundários e destaques menores.
* **O que não significa**: Não substitui a cor primária em ações principais.
* **Sinônimos aceitáveis**: Cor Auxiliar
* **Termos desencorajados ou proibidos**: Cor Secundária Inútil
* **Exemplo correto**: O botão de cancelar utiliza a Cor Secundária.
* **Exemplo incorreto**: Cancelamento tem aquela cor inútil.
* **Documentos relacionados**: docs/design_system.md
* **Termos relacionados**: Cor Primária

### CTA Visual

* **Categoria**: Marca e Layout
* **Nome oficial**: CTA Visual
* **Nome técnico**: Call-to-Action
* **Definição**: Elemento de interface proeminente concebido para impulsionar a interação do usuário.
* **Uso no AutoMedia AI**: Estrutura botões e links críticos seguindo regras de contraste para maximizar engajamento.
* **O que não significa**: Não é um simples texto informativo estático.
* **Sinônimos aceitáveis**: Botão de Ação
* **Termos desencorajados ou proibidos**: Isca de Clique
* **Exemplo correto**: O CTA Visual de conversão segue o contraste primário.
* **Exemplo incorreto**: Aquela isca de clique tenta forçar a compra.
* **Documentos relacionados**: docs/components.md
* **Termos relacionados**: Destaque, Cor Primária

### Design System

* **Categoria**: Marca e Layout
* **Nome oficial**: Design System
* **Nome técnico**: Design System
* **Definição**: Conjunto de padrões, princípios e componentes reutilizáveis que orientam o desenvolvimento de interfaces.
* **Uso no AutoMedia AI**: Utilizado para garantir consistência visual nas aplicações geradas.
* **O que não significa**: Não significa apenas uma biblioteca de componentes ou guia de estilo.
* **Sinônimos aceitáveis**: Sistema de Design
* **Termos desencorajados ou proibidos**: Bíblia de Estilos
* **Exemplo correto**: O botão primário utiliza a cor definida no Design System.
* **Exemplo incorreto**: O botão pega a cor daquela inviolável Bíblia de Estilos.
* **Documentos relacionados**: docs/design_system.md
* **Termos relacionados**: Design Token, Componente Visual

### Design Token

* **Categoria**: Marca e Layout
* **Nome oficial**: Design Token
* **Nome técnico**: Design Token
* **Definição**: Variável semântica que armazena decisões de design, como cores, tipografia e espaçamento.
* **Uso no AutoMedia AI**: Aplicado na padronização de valores visuais no código.
* **O que não significa**: Não é um componente funcional isolado.
* **Sinônimos aceitáveis**: Variável de Estilo
* **Termos desencorajados ou proibidos**: Variável Mágica
* **Exemplo correto**: A cor de fundo utiliza o Design Token correspondente.
* **Exemplo incorreto**: A cor foi setada com um valor mágico aleatório no código.
* **Documentos relacionados**: docs/design_tokens.md
* **Termos relacionados**: Design System

### Destaque

* **Categoria**: Marca e Layout
* **Nome oficial**: Destaque
* **Nome técnico**: Highlight
* **Definição**: Recurso visual que eleva a hierarquia de um elemento na tela através de contraste, escala ou espaço.
* **Uso no AutoMedia AI**: Empregado para direcionar a atenção do usuário para alertas, avisos ou áreas prioritárias.
* **O que não significa**: Não significa animar agressivamente o elemento.
* **Sinônimos aceitáveis**: Área de Foco
* **Termos desencorajados ou proibidos**: Grito Visual
* **Exemplo correto**: A mensagem de erro foi renderizada com o estilo de Destaque.
* **Exemplo incorreto**: Deram um grito visual com letreiros gigantes.
* **Documentos relacionados**: docs/layout_guidelines.md
* **Termos relacionados**: Selo, CTA Visual

### Escala Tipográfica

* **Categoria**: Marca e Layout
* **Nome oficial**: Escala Tipográfica
* **Nome técnico**: Type Scale
* **Definição**: Hierarquia de tamanhos de fonte baseada em proporções matemáticas.
* **Uso no AutoMedia AI**: Define a estrutura de cabeçalhos e textos de corpo de forma sistemática.
* **O que não significa**: Não representa escolhas arbitrárias de tamanhos de fonte.
* **Sinônimos aceitáveis**: Escala de Tamanhos
* **Termos desencorajados ou proibidos**: Tamanhos Chutados
* **Exemplo correto**: Os títulos H1 e H2 seguem a Escala Tipográfica.
* **Exemplo incorreto**: Os tamanhos foram chutados pelo desenvolvedor.
* **Documentos relacionados**: docs/design_system.md
* **Termos relacionados**: Tipografia

### Espaçamento

* **Categoria**: Marca e Layout
* **Nome oficial**: Espaçamento
* **Nome técnico**: Spacing
* **Definição**: Distância definida entre os elementos da interface.
* **Uso no AutoMedia AI**: Implementado através de valores pré-definidos para margens e preenchimentos.
* **O que não significa**: Não é um valor aleatório de pixels em cada tela.
* **Sinônimos aceitáveis**: Margem e Padding
* **Termos desencorajados ou proibidos**: Buraco Branco
* **Exemplo correto**: O componente tem Espaçamento uniforme definido no sistema.
* **Exemplo incorreto**: Colocaram um buraco branco gigante entre os botões.
* **Documentos relacionados**: docs/design_system.md
* **Termos relacionados**: Grid

### Fonte

* **Categoria**: Marca e Layout
* **Nome oficial**: Fonte
* **Nome técnico**: Font Family
* **Definição**: Família de caracteres com um estilo visual específico.
* **Uso no AutoMedia AI**: Aplicada por meio de Design Tokens nos elementos de texto.
* **O que não significa**: Não se refere ao arquivo executável da aplicação.
* **Sinônimos aceitáveis**: Família Tipográfica
* **Termos desencorajados ou proibidos**: Letrinha
* **Exemplo correto**: O título utiliza a Fonte definida como padrão corporativo.
* **Exemplo incorreto**: O título usa a letrinha da moda.
* **Documentos relacionados**: docs/design_system.md
* **Termos relacionados**: Tipografia

### Grid

* **Categoria**: Marca e Layout
* **Nome oficial**: Grid
* **Nome técnico**: Grid System
* **Definição**: Estrutura de linhas e colunas utilizada para alinhar e organizar elementos de layout.
* **Uso no AutoMedia AI**: Orienta o posicionamento responsivo dos componentes na tela.
* **O que não significa**: Não é uma tabela de dados ou estrutura inflexível.
* **Sinônimos aceitáveis**: Sistema de Grades
* **Termos desencorajados ou proibidos**: Jaula de Componentes
* **Exemplo correto**: A página divide o conteúdo usando o Grid de 12 colunas.
* **Exemplo incorreto**: A página prende os elementos naquela jaula de componentes.
* **Documentos relacionados**: docs/design_system.md
* **Termos relacionados**: Layout

### Identidade Premium

* **Categoria**: Marca e Layout
* **Nome oficial**: Identidade Premium
* **Nome técnico**: Premium Identity
* **Definição**: Conjunto de recursos visuais de alta fidelidade e opções avançadas de personalização.
* **Uso no AutoMedia AI**: Oferece templates e componentes exclusivos para usuários com licenciamento específico.
* **O que não significa**: Não significa que as demais identidades possuam menor qualidade técnica.
* **Sinônimos aceitáveis**: Plano Visual Premium
* **Termos desencorajados ou proibidos**: Camarote da Marca
* **Exemplo correto**: O plano acessa os templates da Identidade Premium.
* **Exemplo incorreto**: O cliente rico comprou acesso ao camarote da marca.
* **Documentos relacionados**: docs/subscriptions.md
* **Termos relacionados**: Marketplace de Identidades

### Identidade Visual

* **Categoria**: Produto
* **Nome oficial**: Identidade Visual
* **Nome técnico**: Visual Identity
* **Definição**: Conjunto de regras gráficas, cores e tipografias que caracterizam a marca.
* **Uso no AutoMedia AI**: Parâmetros aplicados durante a renderização dos criativos.
* **O que não significa**: Apenas uma imagem isolada.
* **Sinônimos aceitáveis**: Padrão Gráfico
* **Termos desencorajados ou proibidos**: Maquiagem da marca
* **Exemplo correto**: A identidade visual foi aplicada ao carrossel.
* **Exemplo incorreto**: Passamos a maquiagem no anúncio.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Brand Kit

### Identidade Visual

* **Categoria**: Marca e Layout
* **Nome oficial**: Identidade Visual
* **Nome técnico**: Visual Identity
* **Definição**: Conjunto sistematizado de elementos gráficos e características visuais que representam a marca.
* **Uso no AutoMedia AI**: Assegura que todo material gerado esteja alinhado às diretrizes da marca cliente.
* **O que não significa**: Não é restrito a apenas logotipo e cores base.
* **Sinônimos aceitáveis**: Sistema Visual
* **Termos desencorajados ou proibidos**: Maquiagem de Marca
* **Exemplo correto**: Os banners respeitam as especificações da Identidade Visual.
* **Exemplo incorreto**: Os banners ganharam uma maquiagem de marca brega.
* **Documentos relacionados**: docs/brand_guidelines.md
* **Termos relacionados**: Brand Snapshot

### Layout

* **Categoria**: Marca e Layout
* **Nome oficial**: Layout
* **Nome técnico**: Layout
* **Definição**: Organização espacial dos componentes em uma tela ou documento.
* **Uso no AutoMedia AI**: Define a estrutura geral de posicionamento visual.
* **O que não significa**: Não é restrito a uma única visualização estática.
* **Sinônimos aceitáveis**: Arranjo Espacial
* **Termos desencorajados ou proibidos**: Esqueleto
* **Exemplo correto**: O Layout suporta múltiplas resoluções.
* **Exemplo incorreto**: O esqueleto da página está quebrado no celular.
* **Documentos relacionados**: docs/layout_guidelines.md
* **Termos relacionados**: Composição, Grid

### Logo

* **Categoria**: Marca e Layout
* **Nome oficial**: Logo
* **Nome técnico**: Logo
* **Definição**: Representação gráfica base da marca, composta geralmente pela combinação de símbolo e tipografia.
* **Uso no AutoMedia AI**: Renderizado nos cabeçalhos e marcações oficiais de autoria no sistema.
* **O que não significa**: Não inclui, neste contexto, variações secundárias ou favicons isolados.
* **Sinônimos aceitáveis**: Logotipo Principal
* **Termos desencorajados ou proibidos**: Carimbo da Marca
* **Exemplo correto**: O Logo é alinhado à esquerda na barra de navegação.
* **Exemplo incorreto**: Socaram o carimbo da marca no canto.
* **Documentos relacionados**: docs/brand_assets.md
* **Termos relacionados**: Logotipo, Símbolo

### Logotipo

* **Categoria**: Marca e Layout
* **Nome oficial**: Logotipo
* **Nome técnico**: Logotype
* **Definição**: Forma textual desenhada ou estilizada que representa o nome da marca.
* **Uso no AutoMedia AI**: Aplicado como identificador primário onde não há suporte para símbolos complexos.
* **O que não significa**: Não contém ícones abstratos independentes.
* **Sinônimos aceitáveis**: Assinatura Textual
* **Termos desencorajados ou proibidos**: Textinho Bonito
* **Exemplo correto**: O Logotipo possui especificações restritas de proporção.
* **Exemplo incorreto**: O textinho bonito tem que caber ali.
* **Documentos relacionados**: docs/brand_assets.md
* **Termos relacionados**: Logo

### Margem de Segurança

* **Categoria**: Marca e Layout
* **Nome oficial**: Margem de Segurança
* **Nome técnico**: Safe Area
* **Definição**: Espaço reservado nas bordas da tela para evitar sobreposição com elementos do sistema operacional.
* **Uso no AutoMedia AI**: Aplicada nos layouts para assegurar a visualização integral do conteúdo em diferentes dispositivos.
* **O que não significa**: Não é a mesma coisa que margem entre componentes.
* **Sinônimos aceitáveis**: Área Segura
* **Termos desencorajados ou proibidos**: Zona Morta
* **Exemplo correto**: O menu respeita a Margem de Segurança do dispositivo móvel.
* **Exemplo incorreto**: O menu foi jogado para fora da zona morta.
* **Documentos relacionados**: docs/layout_guidelines.md
* **Termos relacionados**: Layout

### Marketplace de Identidades

* **Categoria**: Marca e Layout
* **Nome oficial**: Marketplace de Identidades
* **Nome técnico**: Identity Marketplace
* **Definição**: Plataforma integrada para descoberta, aquisição e gerenciamento de coleções e templates de design.
* **Uso no AutoMedia AI**: Disponibiliza pacotes de identidade que os usuários podem aplicar a seus projetos.
* **O que não significa**: Não é um repositório irrestrito para envios sem curadoria técnica.
* **Sinônimos aceitáveis**: Catálogo de Temas
* **Termos desencorajados ou proibidos**: Feira de Estilos
* **Exemplo correto**: Novos templates foram publicados no Marketplace de Identidades.
* **Exemplo incorreto**: Novos temas foram jogados na feira de estilos livre.
* **Documentos relacionados**: docs/marketplace.md
* **Termos relacionados**: Identidade Premium, Coleção de Identidade

### Paleta de Cores

* **Categoria**: Marca e Layout
* **Nome oficial**: Paleta de Cores
* **Nome técnico**: Color Palette
* **Definição**: Conjunto definido de cores utilizadas sistematicamente na interface.
* **Uso no AutoMedia AI**: Fornece os valores hexadecimais ou RGB para os componentes visuais.
* **O que não significa**: Não representa cores arbitrárias fora da identidade visual.
* **Sinônimos aceitáveis**: Esquema de Cores
* **Termos desencorajados ou proibidos**: Arco-íris de Design
* **Exemplo correto**: Os botões utilizam as cores da paleta oficial.
* **Exemplo incorreto**: Os botões foram pintados com cores daquele arco-íris de design ridículo.
* **Documentos relacionados**: docs/design_system.md
* **Termos relacionados**: Cor Primária, Cor Secundária

### Preço

* **Categoria**: Marca e Layout
* **Nome oficial**: Preço
* **Nome técnico**: Price Display
* **Definição**: Componente especializado em formatar e exibir valores monetários obedecendo padrões de localização.
* **Uso no AutoMedia AI**: Garante consistência na exibição de moedas e casas decimais nos catálogos gerados.
* **O que não significa**: Não realiza processamento de pagamentos ou cálculos complexos.
* **Sinônimos aceitáveis**: Exibição de Valor
* **Termos desencorajados ou proibidos**: Número Sangrento
* **Exemplo correto**: O componente Preço formata o valor em Reais (BRL).
* **Exemplo incorreto**: O número sangrento mostra o custo absurdo ao cliente.
* **Documentos relacionados**: docs/components.md
* **Termos relacionados**: Destaque

### Regra de Layout

* **Categoria**: Marca e Layout
* **Nome oficial**: Regra de Layout
* **Nome técnico**: Layout Rule
* **Definição**: Conjunto de condições técnicas que determinam o comportamento responsivo e posicional dos elementos.
* **Uso no AutoMedia AI**: Aplicada pelo motor de renderização para adaptar a interface dinamicamente.
* **O que não significa**: Não é uma preferência subjetiva de estilo.
* **Sinônimos aceitáveis**: Regra de Exibição
* **Termos desencorajados ou proibidos**: Ditadura de Design
* **Exemplo correto**: A Regra de Layout oculta o menu lateral em telas menores.
* **Exemplo incorreto**: A ditadura de design cortou o menu fora.
* **Documentos relacionados**: docs/layout_guidelines.md
* **Termos relacionados**: Layout

### RenderRequestDTO

* **Categoria**: Marca e Layout
* **Nome oficial**: RenderRequestDTO
* **Nome técnico**: RenderRequestDTO
* **Definição**: Objeto de transferência de dados que contém as propriedades e referências necessárias para a renderização do layout.
* **Uso no AutoMedia AI**: Enviado pela API para solicitar a geração de peças estáticas pelo serviço de renderização.
* **O que não significa**: Não contém lógica de negócio nem regras de validação profundas.
* **Sinônimos aceitáveis**: Payload de Renderização
* **Termos desencorajados ou proibidos**: DTO genérico sem escopo definido
* **Exemplo correto**: O backend recebe as informações formatadas via RenderRequestDTO.
* **Exemplo incorreto**: O sistema joga tudo naquele objeto de dados não estruturado.
* **Documentos relacionados**: docs/api_contracts.md
* **Termos relacionados**: Brand Snapshot

### Rodapé

* **Categoria**: Marca e Layout
* **Nome oficial**: Rodapé
* **Nome técnico**: Footer
* **Definição**: Seção inferior de uma página ou template que contém informações secundárias, links e créditos institucionais.
* **Uso no AutoMedia AI**: Delimita o término do conteúdo principal e abriga a assinatura visual e termos legais.
* **O que não significa**: Não deve ser utilizado para funcionalidades principais da aplicação.
* **Sinônimos aceitáveis**: Área Inferior
* **Termos desencorajados ou proibidos**: Esgoto da Página
* **Exemplo correto**: O Rodapé exibe os avisos de privacidade e direitos autorais.
* **Exemplo incorreto**: O esgoto da página guarda os links chatos legais.
* **Documentos relacionados**: docs/components.md
* **Termos relacionados**: Assinatura Visual

### Selo

* **Categoria**: Marca e Layout
* **Nome oficial**: Selo
* **Nome técnico**: Badge
* **Definição**: Elemento gráfico complementar usado para denotar status, certificação, promoção ou atributo específico de um item.
* **Uso no AutoMedia AI**: Sobreposto em cards ou imagens para sinalizar categorias como 'Novo' ou 'Premium'.
* **O que não significa**: Não atua como logotipo principal ou botão funcional isolado.
* **Sinônimos aceitáveis**: Badge
* **Termos desencorajados ou proibidos**: Adesivo Safado
* **Exemplo correto**: O card do produto possui o Selo de verificação ativado.
* **Exemplo incorreto**: O card tem um adesivo safado de 'promoção'.
* **Documentos relacionados**: docs/components.md
* **Termos relacionados**: Destaque

### Símbolo

* **Categoria**: Marca e Layout
* **Nome oficial**: Símbolo
* **Nome técnico**: Symbol
* **Definição**: Elemento gráfico isolado, muitas vezes abstrato ou icônico, que identifica a marca de maneira concisa.
* **Uso no AutoMedia AI**: Empregado em espaços reduzidos como favicons, avatares ou botões.
* **O que não significa**: Não é um ícone genérico do sistema.
* **Sinônimos aceitáveis**: Ícone da Marca
* **Termos desencorajados ou proibidos**: Desenhozinho
* **Exemplo correto**: O avatar de perfil carrega o Símbolo da empresa.
* **Exemplo incorreto**: O perfil usa aquele desenhozinho da marca.
* **Documentos relacionados**: docs/brand_assets.md
* **Termos relacionados**: Logo

### Template Estático

* **Categoria**: Marca e Layout
* **Nome oficial**: Template Estático
* **Nome técnico**: Static Template
* **Definição**: Modelo de layout cujo formato base e componentes não sofrem alterações em tempo de execução.
* **Uso no AutoMedia AI**: Aplicado para gerar peças visuais com posições e tamanhos estritamente controlados.
* **O que não significa**: Não impede a injeção de dados ou texto dinâmico nas áreas permitidas.
* **Sinônimos aceitáveis**: Modelo Estático
* **Termos desencorajados ou proibidos**: Arte Engessada
* **Exemplo correto**: A fatura foi gerada usando um Template Estático.
* **Exemplo incorreto**: Foi gerada aquela arte engessada que ninguém muda.
* **Documentos relacionados**: docs/templates.md
* **Termos relacionados**: Template Parametrizado

### Template Parametrizado

* **Categoria**: Marca e Layout
* **Nome oficial**: Template Parametrizado
* **Nome técnico**: Parameterized Template
* **Definição**: Modelo de layout estruturado com variáveis que adaptam dimensões e comportamentos com base em dados de entrada.
* **Uso no AutoMedia AI**: Gera saídas visuais variadas mantendo consistência com as regras de layout.
* **O que não significa**: Não gera layouts imprevisíveis e sem restrição.
* **Sinônimos aceitáveis**: Modelo Dinâmico
* **Termos desencorajados ou proibidos**: Frankenstein Visual
* **Exemplo correto**: O Template Parametrizado ajustou o cabeçalho de acordo com o JSON fornecido.
* **Exemplo incorreto**: O Frankenstein visual juntou pedaços dos dados.
* **Documentos relacionados**: docs/templates.md
* **Termos relacionados**: Template Estático

### Tipografia

* **Categoria**: Marca e Layout
* **Nome oficial**: Tipografia
* **Nome técnico**: Typography
* **Definição**: Conjunto de regras de estilos de fontes, tamanhos e pesos estruturados para textos.
* **Uso no AutoMedia AI**: Padroniza a apresentação textual da interface gerada.
* **O que não significa**: Não diz respeito ao conteúdo ou redação dos textos.
* **Sinônimos aceitáveis**: Estilos de Texto
* **Termos desencorajados ou proibidos**: Salada de Fontes
* **Exemplo correto**: A interface obedece às definições de Tipografia do sistema.
* **Exemplo incorreto**: A tela virou uma salada de fontes misturadas.
* **Documentos relacionados**: docs/design_system.md
* **Termos relacionados**: Fonte, Escala Tipográfica

### Variante de Layout

* **Categoria**: Marca e Layout
* **Nome oficial**: Variante de Layout
* **Nome técnico**: Layout Variant
* **Definição**: Variação estrutural aprovada de um layout base para contextos ou dados específicos.
* **Uso no AutoMedia AI**: Alterna a exibição de componentes com base nos dados do usuário.
* **O que não significa**: Não constitui um novo produto visual independente.
* **Sinônimos aceitáveis**: Variação de Layout
* **Termos desencorajados ou proibidos**: Puxadinho Visual
* **Exemplo correto**: A página carrega a Variante de Layout adequada ao dispositivo.
* **Exemplo incorreto**: Fizeram um puxadinho visual para o mobile.
* **Documentos relacionados**: docs/layout_guidelines.md
* **Termos relacionados**: Layout


## 10. Conceitos de Inteligência Artificial

### AI Policy

* **Categoria**: Segurança
* **Nome oficial**: AI Policy
* **Nome técnico**: AI Policy
* **Definição**: Conjunto de diretrizes e regras codificadas que regulam o uso aceitável, limites operacionais e conformidade dos modelos de IA na plataforma.
* **Uso no AutoMedia AI**: Garante que o conteúdo gerado respeite as normas legais e diretrizes de marca do produto.
* **O que não significa**: Não significa uma lei estatal, mas sim regras de sistema internas.
* **Sinônimos aceitáveis**: Política de IA, Diretriz de IA
* **Termos desencorajados ou proibidos**: Lei marcial da IA, constituição intocável
* **Exemplo correto**: A AI Policy bloqueia a geração de conteúdo relacionado a categorias não autorizadas.
* **Exemplo incorreto**: A AI Policy pune não autorizadomente os provedores que falham.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Guardrail, Constraint

### AI Provider Port

* **Categoria**: Arquitetura
* **Nome oficial**: AI Provider Port
* **Nome técnico**: AI Provider Port
* **Definição**: Interface de entrada ou saída no padrão de arquitetura hexagonal que define os contratos de comunicação com serviços de IA.
* **Uso no AutoMedia AI**: Especifica os métodos de inferência que devem ser implementados pelos Model Adapters.
* **O que não significa**: Não significa uma porta de rede ou conexão TCP/IP física.
* **Sinônimos aceitáveis**: Porta de Provedor
* **Termos desencorajados ou proibidos**: Buraco negro de dados, portal dimensional
* **Exemplo correto**: A AI Provider Port garante que o domínio desconheça a implementação da API externa.
* **Exemplo incorreto**: A AI Provider Port é uma porta de segurança impenetrável.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Model Adapter, Model Provider

### Alucinação

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Alucinação
* **Nome técnico**: Hallucination
* **Definição**: Fenômeno no qual um modelo de IA gera informações factualmente incorretas, inconsistentes ou não fundamentadas nos dados fornecidos.
* **Uso no AutoMedia AI**: Tratada como um erro de precisão a ser mitigado através de Guardrails e validação de confiança.
* **O que não significa**: Não significa que o modelo possui intenção maliciosa ou consciência de estar mentindo.
* **Sinônimos aceitáveis**: Inconsistência Factual, Falsa Geração
* **Termos desencorajados ou proibidos**: Mentira da IA, delírio digital
* **Exemplo correto**: A revisão da saída identificou uma Alucinação técnica na descrição do software.
* **Exemplo incorreto**: A IA estava completamente drogada de dados e gerou uma Alucinação.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Confiança, Guardrail

### Benchmark

* **Categoria**: Qualidade
* **Nome oficial**: Benchmark
* **Nome técnico**: Benchmark
* **Definição**: Processo padronizado de avaliação de desempenho e precisão de modelos de IA utilizando conjuntos de dados e métricas pré-definidos.
* **Uso no AutoMedia AI**: Utilizado para comparar a eficácia de diferentes provedores antes da implantação em produção.
* **O que não significa**: Não significa uma métrica isolada ou uma opinião subjetiva de qualidade.
* **Sinônimos aceitáveis**: Avaliação de Desempenho, Teste de Referência
* **Termos desencorajados ou proibidos**: Arena de batalha, teste mortal
* **Exemplo correto**: O novo modelo obteve pontuação superior no Benchmark de categorização de mídia.
* **Exemplo incorreto**: O Benchmark destruiu as expectativas dos concorrentes.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Dataset, Qualidade de Saída

### Confiança

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Confiança
* **Nome técnico**: Confidence
* **Definição**: Medida estatística que representa o grau de certeza do modelo em relação à precisão ou adequação da saída gerada.
* **Uso no AutoMedia AI**: Utilizada para definir se uma saída automática pode ser aceita sem revisão humana.
* **O que não significa**: Não significa garantia absoluta de veracidade ou exatidão.
* **Sinônimos aceitáveis**: Certeza, Nível de Confiança
* **Termos desencorajados ou proibidos**: Fé inabalável, verdade absoluta
* **Exemplo correto**: Resultados com nível de Confiança baixo são encaminhados para a fila de revisão.
* **Exemplo incorreto**: O sistema tem fé cega nos resultados do modelo.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Confidence Score, Confirmação Humana

### Confidence Score

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Confidence Score
* **Nome técnico**: Confidence Score
* **Definição**: Valor numérico atribuído a uma predição ou geração de IA que quantifica a probabilidade de a resposta estar correta.
* **Uso no AutoMedia AI**: Parâmetro utilizado na lógica de roteamento para acionar o Fallback de Modelo ou exigir intervenção humana.
* **O que não significa**: Não significa uma métrica de qualidade visual ou estética.
* **Sinônimos aceitáveis**: Pontuação de Confiança, Score de Predição
* **Termos desencorajados ou proibidos**: Nota divina, selo de aprovação
* **Exemplo correto**: O Confidence Score de 0.85 atendeu ao limite mínimo de aprovação automática.
* **Exemplo incorreto**: O Confidence Score aniquila resultados de baixa qualidade.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Confiança, Dado Confiável

### Confirmação Humana

* **Categoria**: Fluxo de Trabalho
* **Nome oficial**: Confirmação Humana
* **Nome técnico**: Human-in-the-loop
* **Definição**: Etapa do processo em que um operador humano revisa, valida ou corrige a saída gerada por um modelo antes da sua utilização final.
* **Uso no AutoMedia AI**: Requisitada quando o Confidence Score está abaixo do limiar operacional definido pela AI Policy.
* **O que não significa**: Não significa incapacidade técnica do sistema.
* **Sinônimos aceitáveis**: Revisão Manual, Human-in-the-loop
* **Termos desencorajados ou proibidos**: Babá de IA, salvamento humano
* **Exemplo correto**: O fluxo exige Confirmação Humana para publicações em redes sociais corporativas.
* **Exemplo incorreto**: Precisamos de Confirmação Humana porque a IA é burra.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Sugestão da IA, Confidence Score

### Constraint

* **Categoria**: Arquitetura
* **Nome oficial**: Constraint
* **Nome técnico**: Constraint
* **Definição**: Restrição de negócio, técnica ou regulatória aplicada ao escopo de operação dos modelos de linguagem.
* **Uso no AutoMedia AI**: Define limites como tamanho máximo de saída, idiomas suportados e formatos de resposta.
* **O que não significa**: Não significa uma falha ou bug do sistema.
* **Sinônimos aceitáveis**: Restrição Técnica, Limite Operacional
* **Termos desencorajados ou proibidos**: Camisa de força, sufocamento do sistema
* **Exemplo correto**: Uma Constraint foi configurada para forçar o retorno apenas no idioma português.
* **Exemplo incorreto**: A Constraint estrangula a capacidade criativa do modelo.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Guardrail, AI Policy

### Custo de GPU

* **Categoria**: Finanças
* **Nome oficial**: Custo de GPU
* **Nome técnico**: GPU Cost
* **Definição**: Despesa relacionada à locação ou manutenção de Unidades de Processamento Gráfico necessárias para o treinamento ou inferência de modelos locais.
* **Uso no AutoMedia AI**: Fator crítico no planejamento de capacidade da infraestrutura para processamento multimodal intensivo.
* **O que não significa**: Não significa o custo total de operação em nuvem.
* **Sinônimos aceitáveis**: Despesa de Hardware, Custos de Processamento
* **Termos desencorajados ou proibidos**: Rombo de infraestrutura, taxa extorsiva
* **Exemplo correto**: O projeto avaliou o Custo de GPU antes de optar pelo treinamento in-house.
* **Exemplo incorreto**: O Custo de GPU é um roubo praticado pelas provedoras de nuvem.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Custo de Inferência, Treinamento

### Custo de Inferência

* **Categoria**: Finanças
* **Nome oficial**: Custo de Inferência
* **Nome técnico**: Inference Cost
* **Definição**: Valor financeiro associado ao consumo de recursos computacionais, geralmente medido por tokens ou tempo de processamento, durante a geração de saídas por um modelo de IA.
* **Uso no AutoMedia AI**: Monitorado para garantir a viabilidade econômica das funcionalidades baseadas em linguagem e visão.
* **O que não significa**: Não significa custo de treinamento inicial ou infraestrutura fixa.
* **Sinônimos aceitáveis**: Custo de Predição, Preço por Token
* **Termos desencorajados ou proibidos**: Conta absurda, sangria financeira
* **Exemplo correto**: O Custo de Inferência foi otimizado através de prompts mais concisos.
* **Exemplo incorreto**: O Custo de Inferência está consumindo excessivamente todo o nosso orçamento.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Custo de GPU, Inferência

### Dado Confiável

* **Categoria**: Dados
* **Nome oficial**: Dado Confiável
* **Nome técnico**: Trusted Data
* **Definição**: Informação que foi validada, verificada ou originada de uma fonte autorizada, considerada segura para uso em processos sistêmicos.
* **Uso no AutoMedia AI**: Dados de contexto validados internamente e usados como referência no System Prompt.
* **O que não significa**: Não significa que o dado está isento de atualizações futuras.
* **Sinônimos aceitáveis**: Dado Validado, Fonte Confiável
* **Termos desencorajados ou proibidos**: Verdade universal, ouro limpo
* **Exemplo correto**: O catálogo de produtos é considerado um Dado Confiável para a geração de conteúdo.
* **Exemplo incorreto**: O Dado Confiável é intocável e absoluto.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Dado Não Confiável, Confirmação Humana

### Dado Não Confiável

* **Categoria**: Dados
* **Nome oficial**: Dado Não Confiável
* **Nome técnico**: Untrusted Data
* **Definição**: Informação proveniente de fontes externas não verificadas, entradas diretas de usuários ou saídas brutas de modelos não filtradas.
* **Uso no AutoMedia AI**: Requer processos de sanitização e validação antes de ser armazenado ou exibido.
* **O que não significa**: Não significa necessariamente que o dado é malicioso, apenas que seu formato e conteúdo não foram atestados.
* **Sinônimos aceitáveis**: Dado Bruto, Dado Não Validado
* **Termos desencorajados ou proibidos**: Dados residuais não higienizados
* **Exemplo correto**: O input do usuário foi sanitizado por ser tratado como Dado Não Confiável.
* **Exemplo incorreto**: Bloqueamos o Dado Não Confiável porque é venenoso.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Dado Confiável, Guardrail

### Dataset

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Dataset
* **Nome técnico**: Dataset
* **Definição**: Conjunto estruturado de dados utilizado para treinamento, validação ou teste de modelos de aprendizado de máquina.
* **Uso no AutoMedia AI**: Contém exemplos de mídias, textos e metadados organizados para treinamento ou avaliação.
* **O que não significa**: Não significa um banco de dados transacional em tempo real.
* **Sinônimos aceitáveis**: Conjunto de Dados
* **Termos desencorajados ou proibidos**: Repositório de verdades, ouro digital
* **Exemplo correto**: O Dataset de validação foi atualizado com novos casos de teste.
* **Exemplo incorreto**: O dataset foi utilizado para treino sem verificação da licença de uso.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Treinamento, Benchmark

### Fallback de Modelo

* **Categoria**: Resiliência
* **Nome oficial**: Fallback de Modelo
* **Nome técnico**: Model Fallback
* **Definição**: Mecanismo de contingência que aciona um modelo secundário quando o modelo principal apresenta falha técnica ou degradação de desempenho.
* **Uso no AutoMedia AI**: Garante a continuidade do serviço caso o provedor primário fique indisponível.
* **O que não significa**: Não significa uma reexecução do mesmo modelo com parâmetros diferentes.
* **Sinônimos aceitáveis**: Contingência de IA, Failover de Modelo
* **Termos desencorajados ou proibidos**: Plano de fuga, sobrevivência de emergência
* **Exemplo correto**: O sistema iniciou o Fallback de Modelo após timeout na conexão principal.
* **Exemplo incorreto**: O Fallback de Modelo evitou a falha irrecuperável súbita da plataforma.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Model Provider, AI Provider Port

### Fine-tuning

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Fine-tuning
* **Nome técnico**: Fine-tuning
* **Definição**: Processo de ajuste de um modelo pré-treinado utilizando um conjunto de dados específico para melhorar seu desempenho em uma tarefa direcionada.
* **Uso no AutoMedia AI**: Empregado para alinhar as saídas dos modelos genéricos ao padrão editorial esperado pela plataforma.
* **O que não significa**: Não significa a criação de um modelo do zero.
* **Sinônimos aceitáveis**: Ajuste Fino, Transfer Learning
* **Termos desencorajados ou proibidos**: Lapidação mágica, lavagem cerebral da IA
* **Exemplo correto**: Aplicamos Fine-tuning para adequar o tom de voz do gerador de texto.
* **Exemplo incorreto**: Fizemos um Fine-tuning e agora a IA está domada.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Treinamento, Modelo

### Guardrail

* **Categoria**: Segurança
* **Nome oficial**: Guardrail
* **Nome técnico**: Guardrail
* **Definição**: Mecanismo de controle técnico implementado para monitorar, limitar ou modificar as interações com modelos de IA, prevenindo saídas indesejadas.
* **Uso no AutoMedia AI**: Intercepta e filtra as respostas da API de modelos para garantir conformidade com a AI Policy.
* **O que não significa**: Não significa uma barreira de infraestrutura de rede, como um firewall.
* **Sinônimos aceitáveis**: Filtro de Segurança, Barreira de Contenção
* **Termos desencorajados ou proibidos**: Algemas da IA, jaula do modelo
* **Exemplo correto**: O Guardrail identificou e bloqueou a inclusão de dados sensíveis na resposta.
* **Exemplo incorreto**: O Guardrail prende a IA para que ela não cause danos.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Constraint, AI Policy

### Inferência

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Inferência
* **Nome técnico**: Inference
* **Definição**: Processo de execução de um modelo treinado sobre novos dados para gerar previsões ou saídas.
* **Uso no AutoMedia AI**: Ocorre quando a plataforma processa a solicitação do usuário e retorna um resultado gerado.
* **O que não significa**: Não significa treinamento do modelo ou aprendizado contínuo.
* **Sinônimos aceitáveis**: Predição, Geração
* **Termos desencorajados ou proibidos**: Adivinhação, pensamento da máquina
* **Exemplo correto**: O tempo de Inferência aumentou com a nova versão do modelo.
* **Exemplo incorreto**: A IA está adivinhando os resultados na Inferência.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Modelo, Custo de Inferência

### Inteligência Artificial

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Inteligência Artificial
* **Nome técnico**: Artificial Intelligence
* **Definição**: Campo da ciência da computação dedicado à criação de sistemas capazes de realizar tarefas que requerem processamento cognitivo.
* **Uso no AutoMedia AI**: Refere-se aos sistemas computacionais utilizados para análise e geração de mídia.
* **O que não significa**: Não significa consciência artificial, senciência ou tomada de decisão sem regras predefinidas.
* **Sinônimos aceitáveis**: IA, AI
* **Termos desencorajados ou proibidos**: Cérebro eletrônico, robô pensante
* **Exemplo correto**: O sistema utiliza Inteligência Artificial para classificar as imagens.
* **Exemplo incorreto**: A Inteligência Artificial vai roubar nossos empregos.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Modelo, Machine Learning

### Licença de Uso Comercial

* **Categoria**: Legal
* **Nome oficial**: Licença de Uso Comercial
* **Nome técnico**: Commercial License
* **Definição**: Permissão jurídica que autoriza a utilização de modelos, pesos ou dados em aplicações com fins lucrativos.
* **Uso no AutoMedia AI**: Critério obrigatório para a incorporação de qualquer modelo Open Source na plataforma.
* **O que não significa**: Não significa propriedade intelectual sobre a arquitetura do modelo.
* **Sinônimos aceitáveis**: Licença Comercial
* **Termos desencorajados ou proibidos**: Passaporte de lucros, bilhete dourado
* **Exemplo correto**: A equipe jurídica aprovou a Licença de Uso Comercial do novo modelo.
* **Exemplo incorreto**: A licença de uso comercial isenta a verificação da origem dos modelos reutilizados.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Modelo Open Source

### LLM

* **Categoria**: Inteligência Artificial
* **Nome oficial**: LLM
* **Nome técnico**: Large Language Model
* **Definição**: Modelo de aprendizado de máquina projetado para compreender e gerar linguagem natural, treinado em grandes volumes de texto.
* **Uso no AutoMedia AI**: Responsável pela geração de roteiros, reescrita de textos e sumarização de conteúdos.
* **O que não significa**: Não significa uma base de conhecimento factual atualizada em tempo real.
* **Sinônimos aceitáveis**: Modelo de Linguagem Grande
* **Termos desencorajados ou proibidos**: Cérebro falante, oráculo de texto
* **Exemplo correto**: O LLM foi acionado para gerar a descrição comercial a partir dos metadados do veículo.
* **Exemplo incorreto**: O LLM é um especialista humano em disfarce.
* **Documentos relacionados**: N/A
* **Termos relacionados**: VLM, Prompt

### Model Adapter

* **Categoria**: Arquitetura
* **Nome oficial**: Model Adapter
* **Nome técnico**: Model Adapter
* **Definição**: Componente de software que padroniza a interface de comunicação entre o sistema central e diferentes modelos de inteligência artificial.
* **Uso no AutoMedia AI**: Isola a lógica de negócio das especificidades de implementação de cada provedor de modelo.
* **O que não significa**: Não significa o modelo de IA em si, mas sim a interface de integração.
* **Sinônimos aceitáveis**: Adaptador de IA, Wrapper de Modelo
* **Termos desencorajados ou proibidos**: Tradutor mágico, ponte milagrosa
* **Exemplo correto**: O Model Adapter converte o payload interno para o formato esperado pela API externa.
* **Exemplo incorreto**: O Model Adapter domou a API rebelde do provedor.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Model Provider, AI Provider Port

### Model Provider

* **Categoria**: Arquitetura
* **Nome oficial**: Model Provider
* **Nome técnico**: Model Provider
* **Definição**: Entidade ou serviço externo que hospeda e disponibiliza acesso a modelos de inteligência artificial via API.
* **Uso no AutoMedia AI**: Refere-se aos serviços contratados para fornecer capacidades de inferência para a plataforma.
* **O que não significa**: Não significa os modelos de código aberto executados localmente pela equipe.
* **Sinônimos aceitáveis**: Provedor de IA, Serviço de Inferência
* **Termos desencorajados ou proibidos**: Monopólio da IA, ditador de preços
* **Exemplo correto**: A configuração permite alternar entre mais de um Model Provider para garantir disponibilidade.
* **Exemplo incorreto**: O Model Provider está nos extorquindo por cada token.
* **Documentos relacionados**: N/A
* **Termos relacionados**: AI Provider Port, Model Adapter

### Modelo

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Modelo
* **Nome técnico**: Model
* **Definição**: Representação matemática de um sistema ou processo gerada através de algoritmos de aprendizado de máquina.
* **Uso no AutoMedia AI**: Utilizado para processamento de dados, geração de texto e análise de imagem.
* **O que não significa**: Não significa um sistema infalível ou uma entidade consciente.
* **Sinônimos aceitáveis**: Modelo de Machine Learning, Modelo Preditivo
* **Termos desencorajados ou proibidos**: Oráculo, cérebro mágico
* **Exemplo correto**: O Modelo foi atualizado com novos dados de treinamento.
* **Exemplo incorreto**: O Modelo sabe tudo sobre o usuário.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Treinamento, Pesos do Modelo

### Modelo Local

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Modelo Local
* **Nome técnico**: Local Model
* **Definição**: Modelo de aprendizado de máquina executado inteiramente na infraestrutura local ou no dispositivo do usuário.
* **Uso no AutoMedia AI**: Aplicado quando há restrições de privacidade de dados ou ausência de conectividade com a internet.
* **O que não significa**: Não significa um modelo de baixa qualidade ou necessariamente limitado em recursos.
* **Sinônimos aceitáveis**: On-premise Model, Edge Model
* **Termos desencorajados ou proibidos**: Modelo isolado, IA de bolso
* **Exemplo correto**: A inferência ocorre no Modelo Local para garantir a privacidade dos dados.
* **Exemplo incorreto**: O Modelo Local é um caos operacional de manter.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Modelo Open Source, Inferência

### Modelo Open Source

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Modelo Open Source
* **Nome técnico**: Open Source Model
* **Definição**: Modelo de aprendizado de máquina cujo código e parâmetros estão disponíveis publicamente sob uma licença de código aberto.
* **Uso no AutoMedia AI**: Utilizado para personalização de arquiteturas e implantação em infraestrutura própria.
* **O que não significa**: Não significa necessariamente que o modelo é gratuito para uso comercial irrestrito.
* **Sinônimos aceitáveis**: Modelo de Código Aberto
* **Termos desencorajados ou proibidos**: IA gratuita, modelo solto
* **Exemplo correto**: A equipe avaliou um Modelo Open Source para a nova funcionalidade.
* **Exemplo incorreto**: Modelos Open Source são uma bagunça total.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Licença de Uso Comercial, Fine-tuning

### Multimodal

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Multimodal
* **Nome técnico**: Multimodal
* **Definição**: Capacidade de um modelo processar e relacionar múltiplos tipos de dados simultaneamente, como texto e imagem.
* **Uso no AutoMedia AI**: Permite a análise conjunta de metadados textuais e fotos do veículo para geração de descrições.
* **O que não significa**: Não significa que o modelo possui percepção sensorial humana.
* **Sinônimos aceitáveis**: IA Multimodal
* **Termos desencorajados ou proibidos**: Visão divina, modelo onisciente
* **Exemplo correto**: O processamento Multimodal extrai entidades tanto do texto quanto das fotos do veículo.
* **Exemplo incorreto**: O modelo Multimodal assumiu atributos do veículo não confirmados no input.
* **Documentos relacionados**: N/A
* **Termos relacionados**: VLM, Visão Computacional

### Pesos do Modelo

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Pesos do Modelo
* **Nome técnico**: Model Weights
* **Definição**: Parâmetros numéricos aprendidos por um modelo de rede neural durante o processo de treinamento.
* **Uso no AutoMedia AI**: Determinam o comportamento e as predições do modelo nas tarefas de processamento de mídia.
* **O que não significa**: Não significa conhecimento explícito ou banco de dados pesquisável.
* **Sinônimos aceitáveis**: Parâmetros do Modelo, Weights
* **Termos desencorajados ou proibidos**: Memória da IA, neurônios artificiais
* **Exemplo correto**: Os Pesos do Modelo foram ajustados durante a etapa de fine-tuning.
* **Exemplo incorreto**: Os Pesos do Modelo são como o parâmetro inalterável.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Modelo, Treinamento, Fine-tuning

### Prompt

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Prompt
* **Nome técnico**: Prompt
* **Definição**: Instrução ou conjunto de dados de entrada fornecidos a um modelo para iniciar a geração de uma resposta.
* **Uso no AutoMedia AI**: Interface primária de interação entre os módulos do sistema e as APIs de modelos de linguagem.
* **O que não significa**: Não significa uma linguagem de programação ou um comando determinístico.
* **Sinônimos aceitáveis**: Comando, Instrução de Entrada
* **Termos desencorajados ou proibidos**: Feitiço, comando mágico
* **Exemplo correto**: O Prompt deve incluir o contexto necessário para a geração do resumo.
* **Exemplo incorreto**: O Prompt hipnotizou a IA para gerar a resposta.
* **Documentos relacionados**: N/A
* **Termos relacionados**: System Prompt, LLM

### Qualidade de Saída

* **Categoria**: Qualidade
* **Nome oficial**: Qualidade de Saída
* **Nome técnico**: Output Quality
* **Definição**: Métrica qualitativa e quantitativa que avalia a aderência, coerência e utilidade dos resultados gerados pelo modelo de IA.
* **Uso no AutoMedia AI**: Monitorada periodicamente para garantir que a geração de textos e legendas atende aos padrões do produto.
* **O que não significa**: Não significa ausência total de falhas em cenários anômalos.
* **Sinônimos aceitáveis**: Qualidade da Geração
* **Termos desencorajados ou proibidos**: Perfeição, arte sublime
* **Exemplo correto**: A Qualidade de Saída melhorou após o fine-tuning com o dataset revisado.
* **Exemplo incorreto**: A Qualidade de Saída deste modelo é um incompatível com os requisitos de qualidade.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Benchmark, Alucinação

### Result Normalizer

* **Categoria**: Arquitetura
* **Nome oficial**: Result Normalizer
* **Nome técnico**: Result Normalizer
* **Definição**: Componente responsável por estruturar, validar e padronizar as saídas brutas geradas pelos modelos de inteligência artificial.
* **Uso no AutoMedia AI**: Garante que respostas não estruturadas de LLMs sejam convertidas em objetos JSON estritos.
* **O que não significa**: Não significa um corretor gramatical de texto livre.
* **Sinônimos aceitáveis**: Normalizador de Resultados, Parser de IA
* **Termos desencorajados ou proibidos**: Faxineiro de logs, higienizador implacável
* **Exemplo correto**: O Result Normalizer removeu o texto Markdown antes de aplicar o parse do JSON.
* **Exemplo incorreto**: O Result Normalizer salvou o sistema de um desastre nuclear.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Model Adapter

### Sugestão da IA

* **Categoria**: Produto
* **Nome oficial**: Sugestão da IA
* **Nome técnico**: AI Recommendation
* **Definição**: Conteúdo ou ajuste gerado por inteligência artificial para otimizar um criativo.
* **Uso no AutoMedia AI**: Ação proposta pelo sistema pendente de aprovação do operador.
* **O que não significa**: Uma ordem automatizada inevitável.
* **Sinônimos aceitáveis**: Recomendação de Máquina
* **Termos desencorajados ou proibidos**: Ordem do robô
* **Exemplo correto**: O operador aceitou a sugestão da IA para o título.
* **Exemplo incorreto**: O robô mandou mudar o texto.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Aprovação Humana

### Sugestão da IA

* **Categoria**: Interface de Usuário
* **Nome oficial**: Sugestão da IA
* **Nome técnico**: AI Suggestion
* **Definição**: Recomendação gerada por um modelo de IA apresentada ao usuário para aceitação, rejeição ou edição.
* **Uso no AutoMedia AI**: Implementada em fluxos de criação de roteiros e tratamento de fotos para acelerar a produção.
* **O que não significa**: Não significa uma ação final ou execução automatizada sem controle do usuário.
* **Sinônimos aceitáveis**: Recomendação Automática
* **Termos desencorajados ou proibidos**: Ordem da máquina, palpite robótico
* **Exemplo correto**: A Sugestão da IA para o título foi exibida no formulário de edição.
* **Exemplo incorreto**: A Sugestão da IA força o usuário a aceitar o resultado.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Confirmação Humana

### System Prompt

* **Categoria**: Inteligência Artificial
* **Nome oficial**: System Prompt
* **Nome técnico**: System Prompt
* **Definição**: Instrução fundamental que define as regras de comportamento, formato e restrições de um modelo de linguagem durante uma sessão.
* **Uso no AutoMedia AI**: Utilizado para garantir que os modelos operem dentro dos limites de segurança e formato da plataforma.
* **O que não significa**: Não significa uma garantia absoluta de conformidade estrutural.
* **Sinônimos aceitáveis**: Instrução de Sistema, Contexto Global
* **Termos desencorajados ou proibidos**: Mandamento inviolável, lei absoluta
* **Exemplo correto**: O System Prompt orienta o modelo a retornar os dados em formato JSON.
* **Exemplo incorreto**: O System Prompt é o regra estrita que a máquina segue cegamente.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Prompt, Constraint, Guardrail

### Treinamento

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Treinamento
* **Nome técnico**: Training
* **Definição**: Processo iterativo de ajuste dos parâmetros de um modelo utilizando um conjunto de dados para minimizar erros de predição.
* **Uso no AutoMedia AI**: Realizado para adaptar modelos de fundação aos domínios específicos da plataforma.
* **O que não significa**: Não significa aquisição consciente de conhecimento ou memorização de fatos.
* **Sinônimos aceitáveis**: Model Training
* **Termos desencorajados ou proibidos**: Ensino da IA, educação da máquina
* **Exemplo correto**: O Treinamento do modelo exigiu quarenta horas de processamento em GPU.
* **Exemplo incorreto**: O Treinamento foi um banho de sangue para os servidores.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Dataset, Pesos do Modelo, Fine-tuning

### Visão Computacional

* **Categoria**: Inteligência Artificial
* **Nome oficial**: Visão Computacional
* **Nome técnico**: Computer Vision
* **Definição**: Campo da inteligência artificial focado em capacitar sistemas computacionais a extrair informações de imagens digitais.
* **Uso no AutoMedia AI**: Aplicada no reconhecimento de objetos, detecção de cenas e análise estrutural de arquivos de mídia.
* **O que não significa**: Não significa visão biológica ou compreensão contextual perfeita de cenas complexas.
* **Sinônimos aceitáveis**: Processamento Visual
* **Termos desencorajados ou proibidos**: Olhos biônicos, vigilante digital
* **Exemplo correto**: A API de Visão Computacional identificou as ângulo e enquadramento da foto do veículo.
* **Exemplo incorreto**: A Visão Computacional vasculha a imagem como um detetive.
* **Documentos relacionados**: N/A
* **Termos relacionados**: Multimodal, VLM

### VLM

* **Categoria**: Inteligência Artificial
* **Nome oficial**: VLM
* **Nome técnico**: Vision-Language Model
* **Definição**: Modelo de aprendizado de máquina treinado para compreender e conectar representações visuais a informações textuais.
* **Uso no AutoMedia AI**: Empregado na geração de legendas automáticas descritivas para componentes visuais.
* **O que não significa**: Não significa apenas classificação de imagens; envolve compreensão da relação com linguagem.
* **Sinônimos aceitáveis**: Modelo de Visão e Linguagem
* **Termos desencorajados ou proibidos**: Analisador supremo de imagens
* **Exemplo correto**: O VLM relacionou os objetos detectados no frame com a descrição solicitada.
* **Exemplo incorreto**: O VLM entende a imagem melhor que um ser humano.
* **Documentos relacionados**: N/A
* **Termos relacionados**: LLM, Multimodal, Visão Computacional


## 11. Conceitos de Dados e Multitenancy

### Anonimização

* **Categoria**: Segurança
* **Nome oficial**: Anonimização
* **Nome técnico**: Anonymization
* **Definição**: Processo de remoção de informações que permitem a identificação de indivíduos.
* **Uso no AutoMedia AI**: Aplicada a dados utilizados para geração de relatórios estatísticos.
* **O que não significa**: Criptografia reversível de banco de dados.
* **Sinônimos aceitáveis**: Desidentificação
* **Termos desencorajados ou proibidos**: Ocultação de dados
* **Exemplo correto**: Os registros passam por anonimização antes de compor o relatório.
* **Exemplo incorreto**: A anonimização esconde os dados de bisbilhoteiros.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Dado Pessoal

### Armazenamento Temporário

* **Categoria**: Infraestrutura
* **Nome oficial**: Armazenamento Temporário
* **Nome técnico**: Temporary Storage
* **Definição**: Área destinada a manter dados por curto prazo durante o processamento.
* **Uso no AutoMedia AI**: Usado para guardar artefatos durante pipelines de transformação.
* **O que não significa**: Banco de dados relacional principal.
* **Sinônimos aceitáveis**: Armazenamento volátil
* **Termos desencorajados ou proibidos**: Lixeira temporária
* **Exemplo correto**: Os arquivos são movidos para o armazenamento temporário.
* **Exemplo incorreto**: O armazenamento temporário apaga tudo em pânico.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Arquivo Efêmero

### Arquivo Efêmero

* **Categoria**: Dados
* **Nome oficial**: Arquivo Efêmero
* **Nome técnico**: Ephemeral File
* **Definição**: Arquivo que existe apenas durante a execução de um processo específico.
* **Uso no AutoMedia AI**: Gerado temporariamente durante conversões de mídia e descartado em seguida.
* **O que não significa**: Arquivo armazenado permanentemente no sistema.
* **Sinônimos aceitáveis**: Arquivo passageiro
* **Termos desencorajados ou proibidos**: Arquivo fantasma
* **Exemplo correto**: O conversor cria um arquivo efêmero em disco.
* **Exemplo incorreto**: O arquivo efêmero desvanece no ar.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Armazenamento Temporário

### Auditoria

* **Categoria**: Segurança
* **Nome oficial**: Auditoria
* **Nome técnico**: Auditing
* **Definição**: Processo de registro de eventos operacionais e alterações no sistema.
* **Uso no AutoMedia AI**: Utilizada para rastrear ações e verificar a conformidade das operações.
* **O que não significa**: Monitoramento de métricas de infraestrutura.
* **Sinônimos aceitáveis**: Inspeção de registros
* **Termos desencorajados ou proibidos**: Espionagem de usuários
* **Exemplo correto**: A auditoria detalha a modificação do arquivo.
* **Exemplo incorreto**: A auditoria acusa usuários de roubo.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Log de Auditoria

### Consentimento

* **Categoria**: Compliance
* **Nome oficial**: Consentimento
* **Nome técnico**: Consent
* **Definição**: Manifestação documentada onde o titular autoriza o tratamento de seus dados pessoais.
* **Uso no AutoMedia AI**: Registrado formalmente antes do processamento de dados sensíveis.
* **O que não significa**: Aceitação de termos de uso gerais.
* **Sinônimos aceitáveis**: Autorização de tratamento
* **Termos desencorajados ou proibidos**: Permissão absoluta
* **Exemplo correto**: A plataforma gerencia o status do consentimento do usuário.
* **Exemplo incorreto**: O consentimento é um contrato de sangue.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Dado Pessoal

### Credential

* **Categoria**: Segurança
* **Nome oficial**: Credential
* **Nome técnico**: Credential
* **Definição**: Conjunto de informações que valida a identidade de uma entidade.
* **Uso no AutoMedia AI**: Exigida para autorizar operações na interface de programação.
* **O que não significa**: Permissão ou função de usuário.
* **Sinônimos aceitáveis**: Credencial de acesso
* **Termos desencorajados ou proibidos**: Crachá virtual
* **Exemplo correto**: O acesso requer uma Credential ativa e válida.
* **Exemplo incorreto**: A Credential barra a entrada de invasores terríveis.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Secret

### Criptografia

* **Categoria**: Segurança
* **Nome oficial**: Criptografia
* **Nome técnico**: Encryption
* **Definição**: Transformação de dados legíveis em formato codificado utilizando algoritmos.
* **Uso no AutoMedia AI**: Empregada para proteger dados armazenados e comunicações de rede.
* **O que não significa**: Ofuscação de código-fonte de frontend.
* **Sinônimos aceitáveis**: Codificação de dados
* **Termos desencorajados ou proibidos**: Embaralhamento cego
* **Exemplo correto**: A criptografia assegura a integridade da comunicação.
* **Exemplo incorreto**: A criptografia é uma armadura impenetrável.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Secret

### Dado

* **Categoria**: Dados
* **Nome oficial**: Dado
* **Nome técnico**: Data
* **Definição**: Unidade básica de informação processada ou armazenada pelo sistema.
* **Uso no AutoMedia AI**: Representa qualquer entrada, saída ou estado manipulado pelos componentes da plataforma.
* **O que não significa**: Informação interpretada ou inteligência artificial.
* **Sinônimos aceitáveis**: Informação
* **Termos desencorajados ou proibidos**: Fato
* **Exemplo correto**: O sistema armazena o dado na base principal.
* **Exemplo incorreto**: O dado pensa por si mesmo.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Metadado

### Dado Comercial

* **Categoria**: Dados
* **Nome oficial**: Dado Comercial
* **Nome técnico**: Commercial Data
* **Definição**: Informação relacionada a transações financeiras, assinaturas e faturamento.
* **Uso no AutoMedia AI**: Utilizado para calcular cobranças e gerenciar planos dos clientes.
* **O que não significa**: Dados técnicos de infraestrutura.
* **Sinônimos aceitáveis**: Dado financeiro
* **Termos desencorajados ou proibidos**: Dado rico
* **Exemplo correto**: O histórico de pagamentos é um dado comercial.
* **Exemplo incorreto**: O dado comercial é o ouro da empresa.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Tenant ID

### Dado Operacional

* **Categoria**: Dados
* **Nome oficial**: Dado Operacional
* **Nome técnico**: Operational Data
* **Definição**: Informação gerada e utilizada durante a execução de processos do sistema.
* **Uso no AutoMedia AI**: Usado para monitorar e manter o funcionamento contínuo dos serviços.
* **O que não significa**: Dados de faturamento ou de clientes.
* **Sinônimos aceitáveis**: Dado de sistema
* **Termos desencorajados ou proibidos**: Dado de máquina
* **Exemplo correto**: Métricas de uso de processamento são dados operacionais.
* **Exemplo incorreto**: O dado operacional é o sangue do sistema.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Log de Auditoria

### Dado Pessoal

* **Categoria**: Compliance
* **Nome oficial**: Dado Pessoal
* **Nome técnico**: Personal Data
* **Definição**: Informação relacionada a uma pessoa natural identificada ou identificável.
* **Uso no AutoMedia AI**: Processado conforme as políticas de privacidade e legislações vigentes.
* **O que não significa**: Informação corporativa genérica.
* **Sinônimos aceitáveis**: Informação pessoal
* **Termos desencorajados ou proibidos**: Dado íntimo
* **Exemplo correto**: O e-mail do usuário é considerado um dado pessoal.
* **Exemplo incorreto**: O dado pessoal é inviolável.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Anonimização

### Estado Persistido

* **Categoria**: Arquitetura
* **Nome oficial**: Estado Persistido
* **Nome técnico**: Persisted State
* **Definição**: Condição atual de uma entidade gravada em armazenamento durável.
* **Uso no AutoMedia AI**: Permite a recuperação de operações após a reinicialização de componentes.
* **O que não significa**: Estado executado exclusivamente na memória.
* **Sinônimos aceitáveis**: Estado gravado
* **Termos desencorajados ou proibidos**: Memória de elefante
* **Exemplo correto**: O processo retoma a execução a partir do estado persistido.
* **Exemplo incorreto**: O estado persistido revive o servidor.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Persistência

### Exclusão Automática

* **Categoria**: Dados
* **Nome oficial**: Exclusão Automática
* **Nome técnico**: Automatic Deletion
* **Definição**: Processo programado para remover dados sem intervenção manual após eventos específicos.
* **Uso no AutoMedia AI**: Aplicado para limpeza de dados expirados ou após solicitação do titular.
* **O que não significa**: Perda acidental ou corrupção de dados.
* **Sinônimos aceitáveis**: Purga de dados
* **Termos desencorajados ou proibidos**: falha irrecuperável súbita de registros
* **Exemplo correto**: A exclusão automática ocorre diariamente às duas horas da manhã.
* **Exemplo incorreto**: A exclusão automática aniquila os registros.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: TTL

### Isolamento Lógico

* **Categoria**: Arquitetura
* **Nome oficial**: Isolamento Lógico
* **Nome técnico**: Logical Isolation
* **Definição**: Separação de dados e processos em nível de software.
* **Uso no AutoMedia AI**: Implementado por meio de filtros de banco de dados e controle de acesso.
* **O que não significa**: Separação física em servidores distintos.
* **Sinônimos aceitáveis**: Segregação lógica
* **Termos desencorajados ou proibidos**: Isolamento cego
* **Exemplo correto**: O isolamento lógico protege os dados do locatário.
* **Exemplo incorreto**: O isolamento lógico é uma muralha impenetrável.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Multitenancy

### Log de Auditoria

* **Categoria**: Segurança
* **Nome oficial**: Log de Auditoria
* **Nome técnico**: Audit Log
* **Definição**: Registro imutável que detalha eventos relevantes de segurança.
* **Uso no AutoMedia AI**: Armazena informações sobre criação, modificação e deleção de recursos.
* **O que não significa**: Arquivo de log de erros da aplicação.
* **Sinônimos aceitáveis**: Trilha de auditoria
* **Termos desencorajados ou proibidos**: Diário secreto
* **Exemplo correto**: O sistema exporta o Log de Auditoria mensalmente.
* **Exemplo incorreto**: O Log de Auditoria dedura os erros cometidos.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Auditoria

### Metadado

* **Categoria**: Dados
* **Nome oficial**: Metadado
* **Nome técnico**: Metadata
* **Definição**: Dado estruturado que descreve características de outros dados.
* **Uso no AutoMedia AI**: Utilizado para classificar e organizar os recursos armazenados no sistema.
* **O que não significa**: O conteúdo principal do arquivo ou registro.
* **Sinônimos aceitáveis**: Atributo descritivo
* **Termos desencorajados ou proibidos**: Dado do dado
* **Exemplo correto**: O tamanho do arquivo é um metadado salvo no banco.
* **Exemplo incorreto**: O metadado é a alma do arquivo.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Dado

### Multitenancy

* **Categoria**: Arquitetura
* **Nome oficial**: Multitenancy
* **Nome técnico**: Multi-tenancy
* **Definição**: Arquitetura de software onde uma única instância atende a múltiplos locatários.
* **Uso no AutoMedia AI**: Permite o compartilhamento de recursos mantendo o isolamento de dados.
* **O que não significa**: Várias instâncias de software para vários clientes.
* **Sinônimos aceitáveis**: Multilocação
* **Termos desencorajados ou proibidos**: Hospedagem bagunçada
* **Exemplo correto**: A plataforma utiliza multitenancy para otimizar custos.
* **Exemplo incorreto**: A multitenancy causa falha irrecuperável súbita em caso de falhas.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Tenant ID

### Ownership

* **Categoria**: Segurança
* **Nome oficial**: Ownership
* **Nome técnico**: Data Ownership
* **Definição**: Atribuição formal de direitos de controle e gestão sobre um conjunto de dados.
* **Uso no AutoMedia AI**: Define qual entidade tem autoridade para modificar ou excluir recursos.
* **O que não significa**: Posse física do hardware.
* **Sinônimos aceitáveis**: Titularidade
* **Termos desencorajados ou proibidos**: Posse inviolável
* **Exemplo correto**: O ownership do arquivo pertence ao criador.
* **Exemplo incorreto**: O ownership é o regra estrita da plataforma.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Propriedade dos Dados

### Persistência

* **Categoria**: Arquitetura
* **Nome oficial**: Persistência
* **Nome técnico**: Persistence
* **Definição**: Mecanismo que garante o armazenamento de dados de forma não volátil.
* **Uso no AutoMedia AI**: Implementada através de bancos de dados e sistemas de arquivos distribuídos.
* **O que não significa**: Cache em memória RAM.
* **Sinônimos aceitáveis**: Gravação de dados
* **Termos desencorajados ou proibidos**: Congelamento eterno
* **Exemplo correto**: A persistência dos dados ocorre após a confirmação da transação.
* **Exemplo incorreto**: A persistência protege os dados da aniquilação.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Estado Persistido

### Propriedade dos Dados

* **Categoria**: Compliance
* **Nome oficial**: Propriedade dos Dados
* **Nome técnico**: Data Property
* **Definição**: Reconhecimento de direitos sobre dados armazenados em conformidade com termos de serviço.
* **Uso no AutoMedia AI**: Assegura que dados gerados por locatários permaneçam sob sua administração.
* **O que não significa**: Transferência de direitos autorais de software.
* **Sinônimos aceitáveis**: Controle de dados
* **Termos desencorajados ou proibidos**: Dono absoluto
* **Exemplo correto**: A propriedade dos dados é mantida pelo cliente.
* **Exemplo incorreto**: O sistema atua com roubo de dados.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Ownership

### Retenção

* **Categoria**: Dados
* **Nome oficial**: Retenção
* **Nome técnico**: Data Retention
* **Definição**: Período pelo qual os dados são mantidos no sistema antes de serem arquivados ou excluídos.
* **Uso no AutoMedia AI**: Configurada conforme políticas de conformidade e necessidades operacionais.
* **O que não significa**: Backup permanente de todos os dados.
* **Sinônimos aceitáveis**: Guarda de dados
* **Termos desencorajados ou proibidos**: Congelamento de dados
* **Exemplo correto**: A retenção de registros de auditoria é de um ano.
* **Exemplo incorreto**: A retenção guarda os dados pela eternidade.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: TTL

### RLS

* **Categoria**: Banco de Dados
* **Nome oficial**: RLS
* **Nome técnico**: Row-Level Security
* **Definição**: Mecanismo de segurança que restringe o acesso a registros de um banco de dados com base no contexto do usuário.
* **Uso no AutoMedia AI**: Aplicado no nível do banco de dados para garantir que usuários acessem apenas seus próprios dados.
* **O que não significa**: Criptografia de disco.
* **Sinônimos aceitáveis**: Segurança em nível de linha
* **Termos desencorajados ou proibidos**: Filtro absoluto
* **Exemplo correto**: O RLS previne acesso cruzado entre locatários.
* **Exemplo incorreto**: O RLS evita violações letais ao banco.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Isolamento Lógico

### Secret

* **Categoria**: Segurança
* **Nome oficial**: Secret
* **Nome técnico**: Secret
* **Definição**: Informação sensível utilizada para autenticação de sistemas e serviços.
* **Uso no AutoMedia AI**: Armazenado com segurança e acessado em tempo de execução pela aplicação.
* **O que não significa**: Senha utilizada por usuários humanos.
* **Sinônimos aceitáveis**: Segredo de aplicação
* **Termos desencorajados ou proibidos**: Chave mestre
* **Exemplo correto**: O microsserviço requer um Secret para conectar ao banco de dados.
* **Exemplo incorreto**: O Secret é o calcanhar de aquiles do sistema.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Credential

### Telegram Chat ID

* **Categoria**: Integrações
* **Nome oficial**: Telegram Chat ID
* **Nome técnico**: Telegram Chat Identifier
* **Definição**: Número que identifica uma conversa ou grupo no Telegram.
* **Uso no AutoMedia AI**: Utilizado como destino para mensagens automatizadas do sistema.
* **O que não significa**: Número de telefone associado ao grupo.
* **Sinônimos aceitáveis**: ID do chat Telegram
* **Termos desencorajados ou proibidos**: Identificador da sala
* **Exemplo correto**: O bot notifica o grupo utilizando o Telegram Chat ID.
* **Exemplo incorreto**: O Telegram Chat ID é a caixa preta do grupo.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Telegram User ID

### Telegram User ID

* **Categoria**: Integrações
* **Nome oficial**: Telegram User ID
* **Nome técnico**: Telegram User Identifier
* **Definição**: Número que identifica um usuário na plataforma Telegram.
* **Uso no AutoMedia AI**: Empregado para enviar notificações diretas a contas específicas.
* **O que não significa**: Nome de usuário público da conta.
* **Sinônimos aceitáveis**: ID de usuário Telegram
* **Termos desencorajados ou proibidos**: Código pessoal do usuário
* **Exemplo correto**: A mensagem de alerta foi direcionada ao Telegram User ID configurado.
* **Exemplo incorreto**: O Telegram User ID é a identidade suprema no mensageiro.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Telegram Chat ID

### Tenant ID

* **Categoria**: Multitenancy
* **Nome oficial**: Tenant ID
* **Nome técnico**: Tenant Identifier
* **Definição**: Identificador único atribuído a um locatário dentro de uma arquitetura multilocatária.
* **Uso no AutoMedia AI**: Garante o isolamento lógico e a segregação de dados entre diferentes organizações.
* **O que não significa**: Identificador de usuário individual.
* **Sinônimos aceitáveis**: ID do locatário
* **Termos desencorajados ou proibidos**: ID do dono
* **Exemplo correto**: A consulta ao banco de dados requer o Tenant ID.
* **Exemplo incorreto**: O Tenant ID impede o roubo de dados.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Workspace ID

### Token de Conexão

* **Categoria**: Segurança
* **Nome oficial**: Token de Conexão
* **Nome técnico**: Connection Token
* **Definição**: Identificador emitido para permitir comunicação autenticada entre sistemas.
* **Uso no AutoMedia AI**: Usado por webhooks para validação de requisições de entrada.
* **O que não significa**: Certificado TLS de servidor web.
* **Sinônimos aceitáveis**: Token de integração
* **Termos desencorajados ou proibidos**: Passe livre
* **Exemplo correto**: A configuração da integração depende do Token de Conexão.
* **Exemplo incorreto**: O Token de Conexão é o ingresso inviolável do webhook.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Credential

### TTL

* **Categoria**: Dados
* **Nome oficial**: TTL
* **Nome técnico**: Time To Live
* **Definição**: Mecanismo que define o tempo de vida útil de um registro antes do seu descarte automático.
* **Uso no AutoMedia AI**: Utilizado para expirar registros de cache e arquivos temporários.
* **O que não significa**: Tempo de resposta de uma requisição HTTP.
* **Sinônimos aceitáveis**: Tempo de vida
* **Termos desencorajados ou proibidos**: Contagem regressiva da falha irrecuperável
* **Exemplo correto**: O registro é removido após expirar seu TTL.
* **Exemplo incorreto**: O TTL mata o registro.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Retenção

### Workspace ID

* **Categoria**: Multitenancy
* **Nome oficial**: Workspace ID
* **Nome técnico**: Workspace Identifier
* **Definição**: Identificador único associado a um espaço de trabalho específico no sistema.
* **Uso no AutoMedia AI**: Agrupa recursos e configurações para um contexto de trabalho delimitado.
* **O que não significa**: Identificador de conta de faturamento.
* **Sinônimos aceitáveis**: ID da área de trabalho
* **Termos desencorajados ou proibidos**: ID do cantinho
* **Exemplo correto**: Os arquivos são isolados por Workspace ID.
* **Exemplo incorreto**: O Workspace ID é uma fortaleza inquebrável.
* **Documentos relacionados**: Nenhum
* **Termos relacionados**: Tenant ID


## 12. Conceitos de Integração e Entrega

### API

* **Categoria**: Arquitetura
* **Nome oficial**: API
* **Nome técnico**: Application Programming Interface
* **Definição**: Conjunto de definições e protocolos utilizados para integrar aplicações de software.
* **Uso no AutoMedia AI**: Utilizado para expor os serviços da plataforma para clientes externos.
* **O que não significa**: Não significa servidor de banco de dados ou interface visual.
* **Sinônimos aceitáveis**: Interface de programação de aplicações
* **Termos desencorajados ou proibidos**: Porta dos fundos
* **Exemplo correto**: A API retornou a confirmação da operação.
* **Exemplo incorreto**: A API é um caos operacional de erros.
* **Documentos relacionados**: docs/api.md
* **Termos relacionados**: Endpoint, Request, Response

### Arquivo Final

* **Categoria**: Produto
* **Nome oficial**: Arquivo Final
* **Nome técnico**: Final File
* **Definição**: Arquivo consolidado e renderizado contendo todas as mídias resultantes do processamento.
* **Uso no AutoMedia AI**: Utilizado como artefato para consumo do usuário após o fluxo de renderização e edição.
* **O que não significa**: Não significa o estado intermediário do projeto na base de dados.
* **Sinônimos aceitáveis**: Mídia exportada
* **Termos desencorajados ou proibidos**: Produto morto
* **Exemplo correto**: O Arquivo Final foi transferido para o repositório de armazenamento seguro.
* **Exemplo incorreto**: O Arquivo Final foi roubado do servidor.
* **Documentos relacionados**: docs/final-file.md
* **Termos relacionados**: Pacote Final, Exportação

### Bot

* **Categoria**: Integração
* **Nome oficial**: Bot
* **Nome técnico**: Bot
* **Definição**: Aplicação de software programada para executar tarefas automatizadas.
* **Uso no AutoMedia AI**: Utilizado para automatizar interações com o usuário em canais de comunicação.
* **O que não significa**: Não significa inteligência artificial geral.
* **Sinônimos aceitáveis**: Agente automatizado
* **Termos desencorajados ou proibidos**: Robô
* **Exemplo correto**: O Bot confirmou o recebimento da solicitação.
* **Exemplo incorreto**: O Bot ficou louco.
* **Documentos relacionados**: docs/bots.md
* **Termos relacionados**: Telegram Gateway, Webhook

### Callback

* **Categoria**: Arquitetura
* **Nome oficial**: Callback
* **Nome técnico**: Callback
* **Definição**: Função ou endereço executado automaticamente após a conclusão de uma operação prévia.
* **Uso no AutoMedia AI**: Utilizado para notificar sistemas clientes ao término do processamento do lote de fotos.
* **O que não significa**: Não significa log de auditoria.
* **Sinônimos aceitáveis**: Chamada de retorno
* **Termos desencorajados ou proibidos**: Eco
* **Exemplo correto**: A URL de Callback recebeu a confirmação final do processamento.
* **Exemplo incorreto**: O Callback devolveu payload mal formatado.
* **Documentos relacionados**: docs/callback.md
* **Termos relacionados**: Webhook

### Canal

* **Categoria**: Produto
* **Nome oficial**: Canal
* **Nome técnico**: Channel
* **Definição**: Meio ou destino específico para distribuição de conteúdo.
* **Uso no AutoMedia AI**: Utilizado para agrupar exportações destinadas a uma mesma plataforma social.
* **O que não significa**: Não significa protocolo de rede.
* **Sinônimos aceitáveis**: Plataforma de destino
* **Termos desencorajados ou proibidos**: Tubo
* **Exemplo correto**: O Canal selecionado requer formato de imagem vertical para Stories (9:16).
* **Exemplo incorreto**: O Canal entupiu de dados.
* **Documentos relacionados**: docs/channels.md
* **Termos relacionados**: Exportação

### Delivery Adapter

* **Categoria**: Arquitetura
* **Nome oficial**: Delivery Adapter
* **Nome técnico**: Delivery Adapter
* **Definição**: Componente responsável por adaptar dados ao formato de entrega de um sistema externo.
* **Uso no AutoMedia AI**: Utilizado para formatar publicações para diferentes redes sociais.
* **O que não significa**: Não significa armazenamento de dados ou banco de dados.
* **Sinônimos aceitáveis**: Adaptador de entrega
* **Termos desencorajados ou proibidos**: Entregador
* **Exemplo correto**: O Delivery Adapter validou a requisição antes do envio.
* **Exemplo incorreto**: O Delivery Adapter retenção indevidau a mensagem.
* **Documentos relacionados**: docs/adapters.md
* **Termos relacionados**: Storage Adapter, Render Adapter

### Endpoint

* **Categoria**: Arquitetura
* **Nome oficial**: Endpoint
* **Nome técnico**: Endpoint
* **Definição**: Ponto de acesso em uma API HTTP associado a um recurso ou serviço específico.
* **Uso no AutoMedia AI**: Utilizado para mapear as URLs que executam funções na plataforma.
* **O que não significa**: Não significa endereço IP de infraestrutura ou porta lógica de roteador.
* **Sinônimos aceitáveis**: Ponto de acesso, Rota
* **Termos desencorajados ou proibidos**: Buraco da API
* **Exemplo correto**: O Endpoint de processamento de imagens do anúncio está disponível.
* **Exemplo incorreto**: O endpoint respondeu com dados fora da especificação do contrato.
* **Documentos relacionados**: docs/endpoints.md
* **Termos relacionados**: API, Request

### Exportação

* **Categoria**: Produto
* **Nome oficial**: Exportação
* **Nome técnico**: Export
* **Definição**: Operação de processamento final para converter o projeto em um formato de consumo.
* **Uso no AutoMedia AI**: Utilizado para descrever o evento em que o pacote final de mídias é entregue pelo Telegram ao usuário.
* **O que não significa**: Não significa backup do projeto bruto.
* **Sinônimos aceitáveis**: Geração, Renderização final
* **Termos desencorajados ou proibidos**: Despejo de lote
* **Exemplo correto**: O módulo de Exportação formatou o arquivo na extensão desejada.
* **Exemplo incorreto**: A Exportação demorou uma eternidade inviolável.
* **Documentos relacionados**: docs/export.md
* **Termos relacionados**: Formato de Saída, Arquivo Final

### Facebook Marketplace

* **Categoria**: Produto
* **Nome oficial**: Facebook Marketplace
* **Nome técnico**: Facebook Marketplace
* **Definição**: Seção da rede social Facebook dedicada a anúncios e comércio entre usuários.
* **Uso no AutoMedia AI**: Utilizado como destino integrado para exibição de anúncios visuais de produtos automotivos.
* **O que não significa**: Não significa portal de e-commerce genérico fora da rede social.
* **Sinônimos aceitáveis**: Marketplace do Facebook
* **Termos desencorajados ou proibidos**: Bazar virtual
* **Exemplo correto**: A integração formatou o anúncio do veículo para publicação no Facebook Marketplace.
* **Exemplo incorreto**: O sistema enviou imagens em lote sem aplicar limites de taxa no Facebook Marketplace.
* **Documentos relacionados**: docs/facebook-marketplace.md
* **Termos relacionados**: Integração, Canal

### Formato de Saída

* **Categoria**: Produto
* **Nome oficial**: Formato de Saída
* **Nome técnico**: Output Format
* **Definição**: Parâmetros técnicos do arquivo gerado, como resolução, contêiner e codec.
* **Uso no AutoMedia AI**: Utilizado para assegurar a compatibilidade da imagem gerada com diferentes redes sociais.
* **O que não significa**: Não significa formato de código-fonte.
* **Sinônimos aceitáveis**: Formato final, Especificação de arquivo
* **Termos desencorajados ou proibidos**: Pacote rígido
* **Exemplo correto**: O Formato de Saída foi ajustado para atender aos requisitos técnicos da plataforma parceira.
* **Exemplo incorreto**: O Formato de Saída ficou um formato de saída não suportado.
* **Documentos relacionados**: docs/output-format.md
* **Termos relacionados**: Preset

### Instagram Feed

* **Categoria**: Produto
* **Nome oficial**: Instagram Feed
* **Nome técnico**: Instagram Feed
* **Definição**: Modalidade de publicação destinada ao fluxo principal de imagens do Instagram.
* **Uso no AutoMedia AI**: Utilizado para definir as proporções de imagem direcionadas ao layout em grade da rede social.
* **O que não significa**: Não significa o conteúdo em formatos efêmeros ou histórias.
* **Sinônimos aceitáveis**: Feed do Instagram
* **Termos desencorajados ou proibidos**: Vitrine
* **Exemplo correto**: A foto da capa foi formatada para as proporções ideais do Instagram Feed.
* **Exemplo incorreto**: O O formato de imagem foi rejeitado pelas restrições do Instagram Feed.
* **Documentos relacionados**: docs/instagram-feed.md
* **Termos relacionados**: Instagram Stories, Canal

### Instagram Stories

* **Categoria**: Produto
* **Nome oficial**: Instagram Stories
* **Nome técnico**: Instagram Stories
* **Definição**: Modalidade de publicação vertical de duração máxima limitada, comum na rede social Instagram.
* **Uso no AutoMedia AI**: Utilizado como alvo para exportação de campanhas verticais e ágeis.
* **O que não significa**: Não significa postagens permanentes no perfil.
* **Sinônimos aceitáveis**: Stories
* **Termos desencorajados ou proibidos**: Conteúdo não padronizado
* **Exemplo correto**: O conteúdo de Instagram Stories requer orientação vertical.
* **Exemplo incorreto**: O Instagram Stories rejeita imagens fora da proporção 9:16.
* **Documentos relacionados**: docs/instagram-stories.md
* **Termos relacionados**: Instagram Feed, Canal

### Integração

* **Categoria**: Integração
* **Nome oficial**: Integração
* **Nome técnico**: Integration
* **Definição**: Processo de conexão entre diferentes sistemas de software.
* **Uso no AutoMedia AI**: Utilizado para referenciar a comunicação com serviços de terceiros.
* **O que não significa**: Não significa a fusão completa de duas bases de código.
* **Sinônimos aceitáveis**: Conexão de sistemas
* **Termos desencorajados ou proibidos**: Casamento de software
* **Exemplo correto**: A Integração com o serviço de e-mail foi ativada.
* **Exemplo incorreto**: A Integração sangrenta falhou de novo.
* **Documentos relacionados**: docs/integrations.md
* **Termos relacionados**: API

### Pacote Final

* **Categoria**: Artefato
* **Nome oficial**: Pacote Final
* **Nome técnico**: Output Bundle
* **Definição**: Conjunto agregado de todos os arquivos gerados no fluxo de processamento. Estruturado para facilitar o download único.
* **Uso no AutoMedia AI**: Agrupa fotos de veículos, cópias e artes processadas pela esteira autônoma.
* **O que não significa**: Não contém os arquivos brutos originais do usuário.
* **Sinônimos aceitáveis**: Bundle, Arquivo de Saída
* **Termos desencorajados ou proibidos**: Pacotão, Prêmio
* **Exemplo correto**: O Pacote Final contém o fotos do veículo e a cópia comercial formatada.
* **Exemplo incorreto**: O Pacote Final é o nosso pote de ouro.
* **Documentos relacionados**: 000, 000A
* **Termos relacionados**: Entrega, Arquivo ZIP

### Pacote Final

* **Categoria**: Produto
* **Nome oficial**: Pacote Final
* **Nome técnico**: Final Package
* **Definição**: Conjunto de artefatos que inclui o fotos tratadas, a arte da capa e os metadados ou variações correspondentes.
* **Uso no AutoMedia AI**: Utilizado na entrega para serviços que requerem múltiplos formatos em um único evento.
* **O que não significa**: Não significa projeto raiz com dados editáveis pelo usuário.
* **Sinônimos aceitáveis**: Pacote de exportação
* **Termos desencorajados ou proibidos**: Sacola de arquivos
* **Exemplo correto**: O sistema encaminhou o Pacote Final completo à plataforma de destino.
* **Exemplo incorreto**: O Pacote Final engordou excessivamente a rede.
* **Documentos relacionados**: docs/final-package.md
* **Termos relacionados**: Arquivo Final

### Payload

* **Categoria**: Arquitetura
* **Nome oficial**: Payload
* **Nome técnico**: Payload
* **Definição**: O bloco de dados contido no corpo de uma mensagem ou requisição de rede.
* **Uso no AutoMedia AI**: Utilizado para transferir as especificações e parâmetros da edição via requisição.
* **O que não significa**: Não significa os cabeçalhos HTTP ou o código de status.
* **Sinônimos aceitáveis**: Carga útil
* **Termos desencorajados ou proibidos**: Bomba de dados
* **Exemplo correto**: O Payload continha as coordenadas para inserção de texto.
* **Exemplo incorreto**: O Payload explodiu o servidor.
* **Documentos relacionados**: docs/payload.md
* **Termos relacionados**: Request, Response

### Polling

* **Categoria**: Integração
* **Nome oficial**: Polling
* **Nome técnico**: Polling
* **Definição**: Técnica de consulta periódica a um serviço para verificar atualizações.
* **Uso no AutoMedia AI**: Utilizado como contingência para atualização de dados quando webhooks não estão disponíveis.
* **O que não significa**: Não significa comunicação bidirecional em tempo real.
* **Sinônimos aceitáveis**: Consulta periódica
* **Termos desencorajados ou proibidos**: Loop infinito
* **Exemplo correto**: A rotina de Polling verificou novos arquivos no repositório.
* **Exemplo incorreto**: O Polling fritou os servidores.
* **Documentos relacionados**: docs/polling.md
* **Termos relacionados**: Webhook, Request

### Preset

* **Categoria**: Produto
* **Nome oficial**: Preset
* **Nome técnico**: Preset
* **Definição**: Agrupamento salvo de propriedades de projeto, como resolução, paleta de cores e estilo visual.
* **Uso no AutoMedia AI**: Utilizado para aplicar configurações aprovadas em novos projetos rapidamente.
* **O que não significa**: Não significa que o projeto não possa receber edições customizadas.
* **Sinônimos aceitáveis**: Predefinição
* **Termos desencorajados ou proibidos**: Receita de bolo
* **Exemplo correto**: O projeto carregou o Preset corporativo adequadamente.
* **Exemplo incorreto**: O Preset matou a configurações personalizadas de marca do cliente.
* **Documentos relacionados**: docs/preset.md
* **Termos relacionados**: Formato de Saída, Canal

### Rate Limit

* **Categoria**: Infraestrutura
* **Nome oficial**: Rate Limit
* **Nome técnico**: Rate Limit
* **Definição**: Política técnica que restringe o número de acessos de um cliente a um recurso em um intervalo de tempo definido.
* **Uso no AutoMedia AI**: Utilizado para preservar o desempenho global da plataforma contra excesso de tráfego.
* **O que não significa**: Não significa banimento permanente ou falha de sistema.
* **Sinônimos aceitáveis**: Limite de taxa
* **Termos desencorajados ou proibidos**: Freio absoluto
* **Exemplo correto**: O Rate Limit evitou a sobrecarga do servidor de banco de dados.
* **Exemplo incorreto**: O sistema degolou o usuário com o Rate Limit.
* **Documentos relacionados**: docs/rate-limit.md
* **Termos relacionados**: API, Request

### Render Adapter

* **Categoria**: Arquitetura
* **Nome oficial**: Render Adapter
* **Nome técnico**: Render Adapter
* **Definição**: Componente responsável pela integração com o motor de processamento gráfico.
* **Uso no AutoMedia AI**: Utilizado para enviar tarefas de renderização de arte ao motor gráfico externo.
* **O que não significa**: Não significa a própria máquina virtual de renderização.
* **Sinônimos aceitáveis**: Adaptador de renderização
* **Termos desencorajados ou proibidos**: Gerador automático de anúncios
* **Exemplo correto**: O Render Adapter processou os parâmetros de formatação com sucesso.
* **Exemplo incorreto**: O Render Adapter engoliu a imagem.
* **Documentos relacionados**: docs/adapters.md
* **Termos relacionados**: Storage Adapter, Delivery Adapter

### Request

* **Categoria**: Arquitetura
* **Nome oficial**: Request
* **Nome técnico**: Request
* **Definição**: Mensagem enviada por um cliente para um servidor visando iniciar uma ação.
* **Uso no AutoMedia AI**: Utilizado para referenciar qualquer solicitação enviada à API da plataforma.
* **O que não significa**: Não significa o resultado da transação.
* **Sinônimos aceitáveis**: Requisição, Solicitação
* **Termos desencorajados ou proibidos**: Grito do sistema
* **Exemplo correto**: A Request incluiu as credenciais corretas de acesso.
* **Exemplo incorreto**: O usuário fuzilou o sistema com Requests.
* **Documentos relacionados**: docs/request.md
* **Termos relacionados**: Response, Payload

### Response

* **Categoria**: Arquitetura
* **Nome oficial**: Response
* **Nome técnico**: Response
* **Definição**: Mensagem retornada por um servidor a um cliente após processar uma requisição.
* **Uso no AutoMedia AI**: Utilizado para confirmar a criação de um recurso ou enviar metadados processados.
* **O que não significa**: Não significa comando de execução independente.
* **Sinônimos aceitáveis**: Resposta, Retorno HTTP
* **Termos desencorajados ou proibidos**: Troco
* **Exemplo correto**: A Response apresentou código de sucesso na operação.
* **Exemplo incorreto**: A Response foi porca e cheia de falhas.
* **Documentos relacionados**: docs/response.md
* **Termos relacionados**: Request, Payload

### Storage Adapter

* **Categoria**: Arquitetura
* **Nome oficial**: Storage Adapter
* **Nome técnico**: Storage Adapter
* **Definição**: Componente de software que abstrai operações de leitura e gravação no sistema de arquivos.
* **Uso no AutoMedia AI**: Utilizado para padronizar o acesso ao provedor de armazenamento em nuvem.
* **O que não significa**: Não significa disco físico ou hardware.
* **Sinônimos aceitáveis**: Adaptador de armazenamento
* **Termos desencorajados ou proibidos**: Cofre
* **Exemplo correto**: O Storage Adapter registrou o arquivo no serviço persistente.
* **Exemplo incorreto**: O Storage Adapter é um lixão de arquivos.
* **Documentos relacionados**: docs/adapters.md
* **Termos relacionados**: Delivery Adapter, Render Adapter

### Telegram Gateway

* **Categoria**: Integração
* **Nome oficial**: Telegram Gateway
* **Nome técnico**: Telegram Gateway
* **Definição**: Interface de comunicação entre o sistema interno e a API do Telegram.
* **Uso no AutoMedia AI**: Utilizado para envio e recebimento de mensagens e mídias via Telegram.
* **O que não significa**: Não significa o aplicativo Telegram em si.
* **Sinônimos aceitáveis**: Gateway do Telegram
* **Termos desencorajados ou proibidos**: Robô do Telegram
* **Exemplo correto**: O Telegram Gateway processou o envio do arquivo.
* **Exemplo incorreto**: O Telegram Gateway morreu.
* **Documentos relacionados**: docs/gateways.md
* **Termos relacionados**: Bot, Webhook

### Timeout

* **Categoria**: Infraestrutura
* **Nome oficial**: Timeout
* **Nome técnico**: Timeout
* **Definição**: Tempo limite estabelecido para a espera da conclusão de uma operação de rede ou processamento.
* **Uso no AutoMedia AI**: Utilizado para cancelar automaticamente requisições que excedam o limite estabelecido e liberar recursos.
* **O que não significa**: Não significa indisponibilidade permanente do serviço.
* **Sinônimos aceitáveis**: Tempo esgotado
* **Termos desencorajados ou proibidos**: falha irrecuperável súbita
* **Exemplo correto**: A integração apresentou Timeout ao comunicar com o servidor externo.
* **Exemplo incorreto**: O sistema morreu de Timeout.
* **Documentos relacionados**: docs/timeout.md
* **Termos relacionados**: Request, API

### Webhook

* **Categoria**: Integração
* **Nome oficial**: Webhook
* **Nome técnico**: Webhook
* **Definição**: Mecanismo de notificação assíncrona baseado no protocolo HTTP.
* **Uso no AutoMedia AI**: Utilizado para receber eventos externos em tempo real.
* **O que não significa**: Não significa conexão persistente ou banco de dados.
* **Sinônimos aceitáveis**: Callback HTTP
* **Termos desencorajados ou proibidos**: Gatilho reverso
* **Exemplo correto**: O Webhook registrou o evento de atualização.
* **Exemplo incorreto**: O Webhook foi tratado incorretamente como mecanismo de recuperação do serviço.
* **Documentos relacionados**: docs/webhooks.md
* **Termos relacionados**: Polling, Callback


## 13. Conceitos de Governança e Documentação

### ADR

* **Categoria**: Governança
* **Nome oficial**: ADR
* **Nome técnico**: Architecture Decision Record
* **Definição**: Documento que registra uma decisão arquitetural significativa. Contém o contexto, a decisão tomada e suas consequências.
* **Uso no AutoMedia AI**: Utilizado para documentar escolhas de tecnologias e padrões estruturais do sistema.
* **O que não significa**: Não é um registro de decisões de negócios ou de tarefas operacionais diárias.
* **Sinônimos aceitáveis**: Registro de Decisão Arquitetural
* **Termos desencorajados ou proibidos**: Justificativa de código, atestado de culpa
* **Exemplo correto**: Foi criada uma ADR para justificar a adoção do banco de dados não-relacional.
* **Exemplo incorreto**: A ADR foi feita para culpar a equipe anterior pela escolha ruim.
* **Documentos relacionados**: RFC, Core Architecture Principles
* **Termos relacionados**: RFC, Decisão Local

### Backlog

* **Categoria**: Gestão de Projetos
* **Nome oficial**: Backlog
* **Nome técnico**: Product Backlog
* **Definição**: Lista priorizada de trabalhos, funcionalidades e correções pendentes para um produto ou projeto.
* **Uso no AutoMedia AI**: Centraliza todas as User Stories e Bugs que necessitam de implementação ou resolução.
* **O que não significa**: Não é um arquivo de ideias rejeitadas ou um documento de planejamento concluído.
* **Sinônimos aceitáveis**: Lista de Pendências, Product Backlog
* **Termos desencorajados ou proibidos**: Cemitério de tarefas, buraco negro de ideias
* **Exemplo correto**: A nova Feature foi adicionada ao Backlog e será priorizada na próxima iteração.
* **Exemplo incorreto**: Joga no Backlog que a gente esquece.
* **Documentos relacionados**: PRD
* **Termos relacionados**: Épico, Feature, User Story

### Breaking Change

* **Categoria**: Engenharia
* **Nome oficial**: Breaking Change
* **Nome técnico**: Breaking Change
* **Definição**: Modificação em um sistema ou API que requer adaptações obrigatórias por parte dos consumidores para evitar falhas de integração.
* **Uso no AutoMedia AI**: Sinalizada antecipadamente e acompanhada de aumento na versão Maior segundo o SemVer.
* **O que não significa**: Não é uma correção interna de Bug que mantém os contratos de interface intactos.
* **Sinônimos aceitáveis**: Alteração Incompatível
* **Termos desencorajados ou proibidos**: Destruição de código, catástrofe de integração
* **Exemplo correto**: A remoção do campo de endereço na API constitui uma Breaking Change.
* **Exemplo incorreto**: Essa Breaking Change vai matar os clientes.
* **Documentos relacionados**: SemVer, Especificação
* **Termos relacionados**: SemVer, Deprecated

### Bug

* **Categoria**: Engenharia
* **Nome oficial**: Bug
* **Nome técnico**: Defect
* **Definição**: Falha, erro ou defeito no sistema que produz um resultado incorreto ou inesperado. Interfere no comportamento definido pelos requisitos.
* **Uso no AutoMedia AI**: Registrado e priorizado no Backlog para correção durante os ciclos de manutenção.
* **O que não significa**: Não é uma solicitação de nova funcionalidade ou melhoria de produto.
* **Sinônimos aceitáveis**: Defeito, Falha
* **Termos desencorajados ou proibidos**: Desastre, cagada do dev, gremlin no código
* **Exemplo correto**: Foi relatado um Bug na tela de pagamento onde o botão de confirmar não responde.
* **Exemplo incorreto**: O usuário não gostou da tela, isso é um Bug.
* **Documentos relacionados**: Especificação
* **Termos relacionados**: Tarefa, Débito Técnico

### Core Architecture Principles

* **Categoria**: Governança
* **Nome oficial**: Core Architecture Principles
* **Nome técnico**: Core Architecture Principles
* **Definição**: Conjunto de diretrizes fundamentais que orientam as decisões de design de software. Estabelece restrições e padrões arquiteturais para a plataforma.
* **Uso no AutoMedia AI**: Serve como critério de avaliação para a aprovação de ADRs.
* **O que não significa**: Não é um manual de estilo de código ou um guia de implementação de bibliotecas específicas.
* **Sinônimos aceitáveis**: Princípios Arquiteturais, Diretrizes de Arquitetura
* **Termos desencorajados ou proibidos**: Leis absolutas, regra estritas da arquitetura
* **Exemplo correto**: A proposta do novo serviço foi revisada contra os Core Architecture Principles.
* **Exemplo incorreto**: Se você violar os Core Architecture Principles será demitido.
* **Documentos relacionados**: ADR
* **Termos relacionados**: Decisão Local

### Débito Técnico

* **Categoria**: Engenharia
* **Nome oficial**: Débito Técnico
* **Nome técnico**: Technical Debt
* **Definição**: Custo implícito de manutenção futura resultante de escolhas técnicas rápidas em detrimento de soluções estruturais ideais.
* **Uso no AutoMedia AI**: Monitorado e mitigado periodicamente para manter a sustentabilidade do código.
* **O que não significa**: Não é código quebrado (Bug) ou ausência de uma Feature planejada.
* **Sinônimos aceitáveis**: Dívida Técnica
* **Termos desencorajados ou proibidos**: Código inválido, código obsoleto não mantido
* **Exemplo correto**: A refatoração do módulo de cache foi priorizada para pagar o Débito Técnico acumulado.
* **Exemplo incorreto**: Débito Técnico é qualquer código escrito pelo estagiário.
* **Documentos relacionados**: ADR
* **Termos relacionados**: Bug, Decisão Local

### Decisão Local

* **Categoria**: Engenharia
* **Nome oficial**: Decisão Local
* **Nome técnico**: Local Decision
* **Definição**: Decisão de implementação técnica cujo impacto é restrito a um único módulo ou componente isolado. Não afeta a arquitetura global do sistema.
* **Uso no AutoMedia AI**: Registrada diretamente em documentações de repositório (ex: README) sem necessidade de ADR global.
* **O que não significa**: Não é uma decisão que altera a comunicação entre microserviços estruturais.
* **Sinônimos aceitáveis**: Decisão de Componente
* **Termos desencorajados ou proibidos**: Exceção técnica não documentada
* **Exemplo correto**: A escolha da biblioteca de formatação de datas foi tratada como uma Decisão Local do frontend.
* **Exemplo incorreto**: A Decisão Local mudou o banco de dados principal de toda a empresa.
* **Documentos relacionados**: ADR
* **Termos relacionados**: ADR, Core Architecture Principles

### Deprecated

* **Categoria**: Engenharia
* **Nome oficial**: Deprecated
* **Nome técnico**: Deprecated
* **Definição**: Status de um componente, interface ou recurso que ainda funciona, mas cujo uso é desencorajado por possuir uma alternativa superior ou estar planejado para remoção futura.
* **Uso no AutoMedia AI**: Documentado em código e APIs para alertar desenvolvedores sobre a obsolescência de funções.
* **O que não significa**: Não significa que o recurso já foi completamente removido ou que parou de funcionar imediatamente.
* **Sinônimos aceitáveis**: Descontinuado, Obsoleto
* **Termos desencorajados ou proibidos**: Código depreciado sem escopo
* **Exemplo correto**: A função de autenticação legada foi marcada como Deprecated.
* **Exemplo incorreto**: Essa API está Deprecated, parem de usar essa porcaria.
* **Documentos relacionados**: Especificação
* **Termos relacionados**: Superseded, Breaking Change

### Documento Congelado

* **Categoria**: Governança
* **Nome oficial**: Documento Congelado
* **Nome técnico**: Frozen Document
* **Definição**: Documento cujo conteúdo foi finalizado e cujo status de modificação está bloqueado para preservar um registro histórico imutável.
* **Uso no AutoMedia AI**: Aplicado a versões anteriores de ADRs aprovadas ou especificações de versões descontinuadas.
* **O que não significa**: Não é um documento em rascunho ou sujeito a revisão contínua.
* **Sinônimos aceitáveis**: Registro Histórico, Documento Finalizado
* **Termos desencorajados ou proibidos**: Documento morto, texto petrificado
* **Exemplo correto**: A ADR da versão 1.0 tornou-se um Documento Congelado após o lançamento da versão 2.0.
* **Exemplo incorreto**: Vamos editar o Documento Congelado rapidinho.
* **Documentos relacionados**: ADR
* **Termos relacionados**: Deprecated, Superseded

### Documento Dependente

* **Categoria**: Governança
* **Nome oficial**: Documento Dependente
* **Nome técnico**: Dependent Document
* **Definição**: Documento técnico que deriva seu contexto, restrições ou especificações de um Documento Governante hierarquicamente superior.
* **Uso no AutoMedia AI**: Mantido em alinhamento constante com sua respectiva fonte de autoridade.
* **O que não significa**: Não é um documento obsoleto ou autônomo em suas diretrizes.
* **Sinônimos aceitáveis**: Documento Derivado
* **Termos desencorajados ou proibidos**: Documento escravo, texto inútil
* **Exemplo correto**: O manual de integração é um Documento Dependente do contrato de API.
* **Exemplo incorreto**: O Documento Dependente pode ignorar a matriz.
* **Documentos relacionados**: Documento Governante
* **Termos relacionados**: Documento Governante

### Documento Governante

* **Categoria**: Governança
* **Nome oficial**: Documento Governante
* **Nome técnico**: Governing Document
* **Definição**: Documento formal que estabelece diretrizes, políticas ou requisitos principais que outros documentos e implementações devem seguir.
* **Uso no AutoMedia AI**: Utilizado como fonte autoritativa para auditorias de conformidade e avaliações arquiteturais.
* **O que não significa**: Não é um rascunho de trabalho ou um documento de escopo temporário.
* **Sinônimos aceitáveis**: Norma, Diretriz Principal
* **Termos desencorajados ou proibidos**: Lei marcial, pergaminho inviolável
* **Exemplo correto**: A Política de Segurança é um Documento Governante para os requisitos de infraestrutura.
* **Exemplo incorreto**: O Documento Governante decreta prisão para quem vazar dados.
* **Documentos relacionados**: Core Architecture Principles, PRD
* **Termos relacionados**: Documento Dependente, Documento Congelado

### Épico

* **Categoria**: Gestão de Projetos
* **Nome oficial**: Épico
* **Nome técnico**: Epic
* **Definição**: Agrupamento lógico de alto nível para requisitos de software. Representa um grande escopo de trabalho que é dividido em Features e User Stories.
* **Uso no AutoMedia AI**: Utilizado para organizar grandes entregas de valor, como um novo módulo de faturamento.
* **O que não significa**: Não é uma tarefa técnica individual ou uma simples correção de Bug.
* **Sinônimos aceitáveis**: Iniciativa de Produto
* **Termos desencorajados ou proibidos**: gargalo de performance gigante, tarefa infinita
* **Exemplo correto**: O Épico de reformulação do painel do usuário foi dividido em vinte User Stories.
* **Exemplo incorreto**: Trocar o logo é um Épico.
* **Documentos relacionados**: PRD
* **Termos relacionados**: Feature, User Story, Backlog

### Especificação

* **Categoria**: Engenharia
* **Nome oficial**: Especificação
* **Nome técnico**: Specification
* **Definição**: Descrição detalhada de como um sistema, módulo ou componente deve ser implementado. Inclui contratos de API e modelos de dados.
* **Uso no AutoMedia AI**: Guia a implementação técnica a partir dos requisitos definidos no PRD.
* **O que não significa**: Não é o código-fonte executável ou um documento de marketing.
* **Sinônimos aceitáveis**: Spec, Especificação Técnica
* **Termos desencorajados ou proibidos**: Receita de bolo, manual para dummies
* **Exemplo correto**: A Especificação da API de pagamentos inclui os formatos de requisição e resposta.
* **Exemplo incorreto**: A Especificação proíbe escrever código ruim.
* **Documentos relacionados**: PRD, RFC
* **Termos relacionados**: Requisito Funcional, Requisito Não Funcional

### Feature

* **Categoria**: Gestão de Projetos
* **Nome oficial**: Feature
* **Nome técnico**: Feature
* **Definição**: Funcionalidade específica de um software que entrega valor direto ao usuário ou ao sistema.
* **Uso no AutoMedia AI**: Compreende um conjunto de User Stories focadas em habilitar uma capacidade no produto.
* **O que não significa**: Não é um Épico inteiro nem uma Tarefa técnica isolada.
* **Sinônimos aceitáveis**: Funcionalidade, Recurso
* **Termos desencorajados ou proibidos**: Feitiço novo, penduricalho
* **Exemplo correto**: A Feature de exportação de relatórios será lançada na próxima versão.
* **Exemplo incorreto**: O servidor ligado é uma Feature.
* **Documentos relacionados**: PRD
* **Termos relacionados**: Épico, User Story

### Glossário Oficial

* **Categoria**: Governança
* **Nome oficial**: Glossário Oficial
* **Nome técnico**: Official Glossary
* **Definição**: Repositório centralizado de termos e definições utilizados no contexto do sistema. Padroniza a comunicação técnica e de produto.
* **Uso no AutoMedia AI**: Usado para garantir consistência terminológica em documentações e no código-fonte.
* **O que não significa**: Não é um dicionário da língua portuguesa ou um repositório de jargões informais.
* **Sinônimos aceitáveis**: Glossário
* **Termos desencorajados ou proibidos**: Bíblia de termos, dicionário supremo
* **Exemplo correto**: Consulte o Glossário Oficial antes de nomear novas tabelas no banco de dados.
* **Exemplo incorreto**: O Glossário Oficial é a lei inviolável da empresa.
* **Documentos relacionados**: Core Architecture Principles
* **Termos relacionados**: Source of Truth

### PRD

* **Categoria**: Produto
* **Nome oficial**: PRD
* **Nome técnico**: Product Requirements Document
* **Definição**: Documento que detalha os requisitos, as funcionalidades e os objetivos de um produto ou funcionalidade. Orienta as equipes de desenvolvimento e design.
* **Uso no AutoMedia AI**: Define o escopo funcional antes do início do ciclo de desenvolvimento de uma Feature.
* **O que não significa**: Não é um documento de especificação técnica de arquitetura de software.
* **Sinônimos aceitáveis**: Documento de Requisitos de Produto
* **Termos desencorajados ou proibidos**: Lista de desejos, cartinha para o Papai Noel
* **Exemplo correto**: O PRD da nova tela de autenticação foi aprovado pelo gerente de produto.
* **Exemplo incorreto**: O PRD tem todas as classes que o dev tem que criar.
* **Documentos relacionados**: Project Charter, RFC
* **Termos relacionados**: Requisito Funcional, Épico

### Project Charter

* **Categoria**: Governança
* **Nome oficial**: Project Charter
* **Nome técnico**: Project Charter
* **Definição**: Documento formal que autoriza o início de um projeto. Define o escopo inicial, os objetivos e as partes interessadas.
* **Uso no AutoMedia AI**: Utilizado para formalizar a aprovação de novos módulos principais do sistema.
* **O que não significa**: Não é um documento de requisitos detalhados ou um cronograma de tarefas.
* **Sinônimos aceitáveis**: Termo de Abertura do Projeto
* **Termos desencorajados ou proibidos**: Contrato inviolável do projeto, certidão de nascimento
* **Exemplo correto**: O Project Charter do módulo de pagamentos foi aprovado pelo comitê diretivo.
* **Exemplo incorreto**: O Project Charter tem todas as tarefas que o dev precisa codar.
* **Documentos relacionados**: PRD, Core Architecture Principles
* **Termos relacionados**: Documento Governante

### Requisito Funcional

* **Categoria**: Produto
* **Nome oficial**: Requisito Funcional
* **Nome técnico**: Functional Requirement
* **Definição**: Especificação de uma ação ou comportamento que o sistema deve ser capaz de realizar. Define as funcionalidades disponíveis para o usuário.
* **Uso no AutoMedia AI**: Extraído dos PRDs para orientar o planejamento das User Stories.
* **O que não significa**: Não é uma restrição de desempenho ou critério de segurança de infraestrutura.
* **Sinônimos aceitáveis**: Requisito de Sistema
* **Termos desencorajados ou proibidos**: Comportamento mágico, regra intocável
* **Exemplo correto**: O envio de e-mail de confirmação é um Requisito Funcional do fluxo de cadastro.
* **Exemplo incorreto**: O sistema não travar é um Requisito Funcional.
* **Documentos relacionados**: PRD
* **Termos relacionados**: Requisito Não Funcional, Especificação

### Requisito Não Funcional

* **Categoria**: Engenharia
* **Nome oficial**: Requisito Não Funcional
* **Nome técnico**: Non-Functional Requirement
* **Definição**: Atributo de qualidade que especifica critérios de operação do sistema, como desempenho, segurança e disponibilidade.
* **Uso no AutoMedia AI**: Define metas de latência, tolerância a falhas e escalabilidade da plataforma.
* **O que não significa**: Não é uma funcionalidade direta utilizada pelo usuário final.
* **Sinônimos aceitáveis**: Requisito de Qualidade, Restrição Técnica
* **Termos desencorajados ou proibidos**: Requisito invisível, burocracia técnica
* **Exemplo correto**: A resposta da API em menos de 200ms é um Requisito Não Funcional.
* **Exemplo incorreto**: A cor do botão é um Requisito Não Funcional.
* **Documentos relacionados**: Core Architecture Principles, PRD
* **Termos relacionados**: Requisito Funcional, Especificação

### RFC

* **Categoria**: Governança
* **Nome oficial**: RFC
* **Nome técnico**: Request For Comments
* **Definição**: Documento de proposta formal para solicitação de feedback técnico sobre uma nova implementação ou mudança de arquitetura.
* **Uso no AutoMedia AI**: Criado antes da implementação de mudanças estruturais para obter consenso entre engenheiros.
* **O que não significa**: Não é um comando imutável ou um relatório de incidentes.
* **Sinônimos aceitáveis**: Proposta Técnica, Request For Comments
* **Termos desencorajados ou proibidos**: Pedido de socorro, brainstorm caótico
* **Exemplo correto**: A RFC para o novo sistema de mensageria está aberta para revisão.
* **Exemplo incorreto**: A RFC é só uma formalidade burra antes de codar.
* **Documentos relacionados**: ADR
* **Termos relacionados**: ADR

### SemVer

* **Categoria**: Engenharia
* **Nome oficial**: SemVer
* **Nome técnico**: Semantic Versioning
* **Definição**: Padrão de versionamento composto por três números (Maior.Menor.Correção) que indica o tipo e o impacto das alterações na versão.
* **Uso no AutoMedia AI**: Adotado para garantir previsibilidade na atualização de bibliotecas e APIs expostas.
* **O que não significa**: Não é um identificador cronológico ou um formato de nomenclatura livre.
* **Sinônimos aceitáveis**: Versionamento Semântico
* **Termos desencorajados ou proibidos**: Número mágico de release
* **Exemplo correto**: Seguindo o SemVer, a quebra de compatibilidade aumentou a versão Maior para 3.0.0.
* **Exemplo incorreto**: SemVer permite mudar a versão quando o marketing pedir.
* **Documentos relacionados**: Especificação
* **Termos relacionados**: Versão, Breaking Change

### Source of Truth

* **Categoria**: Engenharia
* **Nome oficial**: Source of Truth
* **Nome técnico**: Single Source of Truth
* **Definição**: Princípio arquitetural que define um único repositório ou sistema como a referência central e autoritativa para um determinado conjunto de dados ou regras.
* **Uso no AutoMedia AI**: Utilizado para garantir consistência de dados em um ambiente de microserviços descentralizados.
* **O que não significa**: Não é um cache distribuído ou uma cópia secundária de dados em um serviço satélite.
* **Sinônimos aceitáveis**: Fonte de Verdade, Fonte Única de Verdade
* **Termos desencorajados ou proibidos**: Oráculo inviolável, administrador dos dados
* **Exemplo correto**: O banco de dados central é a Source of Truth para o cadastro de clientes.
* **Exemplo incorreto**: O Source of Truth pune quem manda dados errados.
* **Documentos relacionados**: Core Architecture Principles
* **Termos relacionados**: Documento Governante, Glossário Oficial

### Status

* **Categoria**: Governança
* **Nome oficial**: Status
* **Nome técnico**: Status
* **Definição**: Estado atual ou condição operacional de um sistema, documento, serviço ou ciclo de desenvolvimento.
* **Uso no AutoMedia AI**: Rastreia a progressão de artefatos, como RFCs (ex: Proposto, Aceito, Rejeitado).
* **O que não significa**: Não é a identificação de versão ou a qualificação de desempenho de um serviço.
* **Sinônimos aceitáveis**: Estado, Condição
* **Termos desencorajados ou proibidos**: Humor do sistema
* **Exemplo correto**: O Status atual da RFC é 'Em Revisão'.
* **Exemplo incorreto**: O Status do servidor é falha irrecuperável súbita.
* **Documentos relacionados**: RFC, ADR
* **Termos relacionados**: Versão

### Superseded

* **Categoria**: Governança
* **Nome oficial**: Superseded
* **Nome técnico**: Superseded
* **Definição**: Status atribuído a um documento, diretriz ou componente que foi formalmente substituído por uma nova versão ou alternativa atualizada.
* **Uso no AutoMedia AI**: Aplicado em registros históricos de ADRs quando uma nova decisão arquitetural prevalece.
* **O que não significa**: Não é o mesmo que excluído do histórico; o registro é mantido para referência de auditoria.
* **Sinônimos aceitáveis**: Substituído, Superado
* **Termos desencorajados ou proibidos**: Banido, extinto da face da terra
* **Exemplo correto**: A política de senhas de 2024 foi marcada como Superseded pela revisão de 2025.
* **Exemplo incorreto**: O contrato Superseded foi marcado como depreciado.
* **Documentos relacionados**: ADR
* **Termos relacionados**: Deprecated, Documento Congelado

### Tarefa

* **Categoria**: Gestão de Projetos
* **Nome oficial**: Tarefa
* **Nome técnico**: Task
* **Definição**: Unidade individual de trabalho técnico necessária para completar uma User Story ou resolver um problema.
* **Uso no AutoMedia AI**: Usada por engenheiros para detalhar os passos de implementação durante o desenvolvimento.
* **O que não significa**: Não é uma funcionalidade visível para o usuário final de forma isolada.
* **Sinônimos aceitáveis**: Task, Atividade Técnica
* **Termos desencorajados ou proibidos**: Trabalho braçal, bucha
* **Exemplo correto**: A Tarefa de atualizar as dependências do pacote foi concluída.
* **Exemplo incorreto**: A Tarefa engloba construir o sistema inteiro.
* **Documentos relacionados**: PRD
* **Termos relacionados**: User Story, Bug

### User Story

* **Categoria**: Gestão de Projetos
* **Nome oficial**: User Story
* **Nome técnico**: User Story
* **Definição**: Descrição de uma funcionalidade do sistema escrita sob a perspectiva do usuário final. Captura o valor que a funcionalidade deve prover.
* **Uso no AutoMedia AI**: Unidade básica de planejamento de desenvolvimento, contendo critérios de aceite claros.
* **O que não significa**: Não é um detalhamento técnico de implementação de banco de dados ou código.
* **Sinônimos aceitáveis**: História de Usuário, História
* **Termos desencorajados ou proibidos**: Desejo do usuário, continho
* **Exemplo correto**: A User Story para login com autenticação de dois fatores foi refinada pela equipe.
* **Exemplo incorreto**: A User Story exige que o banco seja MongoDB.
* **Documentos relacionados**: PRD
* **Termos relacionados**: Feature, Tarefa, Épico

### Versão

* **Categoria**: Engenharia
* **Nome oficial**: Versão
* **Nome técnico**: Version
* **Definição**: Identificação única atribuída a um estado específico de um software, documento ou sistema em um determinado momento no tempo.
* **Uso no AutoMedia AI**: Gerenciada por meio de tags no repositório de código e no controle de artefatos.
* **O que não significa**: Não é o nome comercial do produto ou um ramo temporário de desenvolvimento.
* **Sinônimos aceitáveis**: Release, Revisão
* **Termos desencorajados ou proibidos**: Encarnação do software
* **Exemplo correto**: A Versão 2.1.0 inclui correções para vulnerabilidades de segurança.
* **Exemplo incorreto**: A Versão final verdadeira definitiva v3.
* **Documentos relacionados**: SemVer
* **Termos relacionados**: SemVer, Status

