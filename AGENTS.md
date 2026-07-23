# Regras Globais de Comportamento do Agente

O desenvolvimento e atuação dos agentes de inteligência artificial no repositório **AutoMedia AI** são rigorosamente governados por este arquivo.

## 1. Aprovação de Documentos
Nenhum agente pode aprovar, congelar ou atribuir versão final (ex: "Versão 1.0.0", "Aprovado e Congelado") a um documento estratégico por iniciativa própria. Os documentos devem ser criados e atualizados com status de rascunho (ex: "Em revisão", "Draft") e versões menores (ex: "0.9.0"). Somente o usuário humano possui autoridade decisória para promover um documento ao status de oficial, congelado ou versão 1.0.

## 2. Protocolo Obrigatório de Execução (Modus Operandi)
Para cada tarefa técnica solicitada, o agente **deve, obrigatoriamente, executar o seguinte protocolo**:

1. **Ler o AGENTS.md:** Revisar sempre estas regras como passo zero.
2. **Abrir o índice `docs/README.md`:** Consultar a matriz de governança.
3. **Identificar os documentos governantes:** Baseado na matriz de `docs/README.md`, elencar todos os documentos que afetam a tarefa (ex: `000A`, `007`, `008`).
4. **Ler os arquivos reais:** Nunca presumir conteúdo de documento. Sempre ler o arquivo em sua totalidade (usando a ferramenta de leitura), sem depender de resumos de memória.
5. **Listar o que foi consultado:** No início da resposta, o agente deve declarar explicitamente quais documentos base foram consultados.
6. **Declarar restrições:** Citar quais restrições, dogmas arquiteturais ou contratos encontrados nos documentos se aplicam ao código que será gerado.
7. **Interromper diante de conflitos:** Quando dois documentos divergirem, o agente **NÃO PODE** resolver silenciosamente. Ele deve interromper o fluxo e solicitar uma decisão ao humano.
8. **Não presumir arquivo inexistente:** Se um documento não for encontrado na estrutura, ele deve ser solicitado ou ignorado sob aviso, nunca "inventado".
9. **Avaliar RFC/ADR:** O agente deve julgar ativamente se a decisão/código sendo criada exige a documentação via ADR (Architecture Decision Record) ou RFC (Request For Change) e alertar o humano.
10. **Validar e Listar:** Ao finalizar o turno, validar se o que foi produzido obedece à governança e listar exatamente todos os arquivos criados, modificados e removidos.
