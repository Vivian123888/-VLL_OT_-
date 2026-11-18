# Arquitetura incremental e roadmap

**Sistema analisado:** Otimizador de Grade Curricular — Engenharia de Produção, matriz 2026  
**Revisão:** 17/11/2026  
**Escopo:** diagnóstico do repositório atual e evolução incremental, sem substituir o sistema existente.

## Resumo executivo

O repositório entrega um planejador funcional de pequeno porte, publicado como site estático e conectado ao Supabase para autenticação e alguns fluxos de professor/admin. A interface, o catálogo da matriz e a heurística de planejamento rodam no navegador. A seleção de disciplinas concluídas fica no localStorage. O banco atual não contém histórico acadêmico oficial, versões de matriz, ofertas, turmas, vagas ou planos de estudo.

Isso não é evidência de que a solução comporte 500 mil alunos em período de matrícula. Arquivos estáticos podem ser distribuídos por CDN, mas o pico simultâneo, o banco, as funções Supabase e o cálculo precisam ser dimensionados com métricas e testes de carga. O número de contas cadastradas, por si só, não define a capacidade.

A evolução recomendada é manter a interface atual e primeiro corrigir a qualidade e a explicabilidade dos dados; em seguida extrair o domínio para uma API e um banco versionado; só então integrar o sistema acadêmico e mover otimizações demoradas para workers. A universidade ainda não identificou o SIS/ERP nem o protocolo de acesso, então a integração institucional não pode ser implementada sem essa informação e sem acesso técnico autorizado.

## 1. Diagnóstico do repositório

### O que existe hoje

- index.html contém a interface, o catálogo da matriz 2026 e o algoritmo JavaScript na mesma página.
- otimizador_grade.py mantém outra cópia do catálogo e uma heurística para uso em notebook/Colab. As duas cópias podem divergir.
- O algoritmo é guloso: ordena disciplinas por profundidade de dependência, dificuldade e número de dependentes. Não prova ótimo global.
- A lista marcada como concluída é gravada no navegador. Ela não vem do histórico oficial e não é compartilhada entre dispositivos.
- Os requisitos são listas de strings, interpretadas como conjunção: todos precisam estar atendidos. Não há tipo explícito para co-requisito, equivalência ou vigência.
- Os horários são estimativas da base anterior. Não existem ofertas confirmadas, turmas, dias e intervalos por turma, vagas ou ocupação atualizadas.
- supabase.sql contém perfis e dados de acompanhamento do professor; os scripts SQL adicionam fluxos de aprovação e índices. Não é ainda um modelo acadêmico.
- A função administrativa usa a chave service role somente no servidor e verifica sessão e papel antes de operar. O cabeçalho CORS da função está aberto a qualquer origem; isso não substitui autenticação, mas deve ser restrito ao domínio publicado.
- Não há integração conhecida com SIS/ERP, identidade institucional, fila, cache distribuído, métricas ou traces de execução acadêmica.

### Conflito acadêmico que precisa de validação

A matriz cadastrada põe **Cálculo Numérico** no 3º período e lista **Introd. Equações Diferenciais Ordinárias**, também no 3º, como pré-requisito. O sistema interpreta o requisito como estrito e, por isso, precisa alocar a disciplina requerida antes de Cálculo Numérico. A coordenação deve confirmar se a regra é co-requisito ou se um dos períodos/requisitos está errado. O alerta já é exibido na página; nenhuma regra acadêmica foi alterada por inferência.

## 2. Problemas priorizados

| Prioridade | Problema | Efeito | Ação |
| --- | --- | --- | --- |
| P0 | Histórico, matriz e horários são dados locais/estimados | Plano pode não refletir o registro oficial, a oferta ou a vaga real | Rotular origem e validade; validar com a coordenação; não apresentar plano como matrícula |
| P0 | Requisitos sem tipo, grupos lógicos ou vigência | Co-requisitos, “A ou B”, equivalências e transições curriculares não são representados | Introduzir modelo versionado e validação administrativa antes de migrar regras |
| P1 | Regra da matriz duplicada no JS e Python | Correções podem divergir entre site e notebook | Definir catálogo canônico com versão e gerar/validar os dois consumidores |
| P1 | Planejador roda integralmente no navegador e só salva seleção local | Sem histórico compartilhado, execução rastreável ou processamento assíncrono | API autenticada para planos; manter cálculo local como fallback durante a transição |
| P1 | Não há dados de turmas, ofertas e vagas | Conflitos reais e disponibilidade não podem ser afirmados | Integrar dados de oferta e representar horários por seção, com carimbo de atualização |
| P1 | Identidade atual não está ligada ao provedor institucional | Contas do site não provam vínculo acadêmico | Escolher OIDC ou SAML com a universidade quando o IdP for conhecido |
| P2 | Sem telemetria de latência, erros e uso | Incapacidade de definir SLOs ou diagnosticar pico | Instrumentar antes de escolher Redis, réplicas ou orquestrador |
| P2 | CORS aberto na função administrativa | Origem do navegador não é limitada ao site | Permitir apenas origens de produção e desenvolvimento necessárias |

## 3. Arquitetura incremental recomendada

Começar com um monólito modular, não com microserviços. A página estática pode continuar como front-end no início. Extrair as regras para uma API protegida e organizar o servidor por domínios: identidade e perfis, catálogo curricular, histórico, ofertas, planos, integrações e relatórios. A otimização pode virar um worker quando seu tempo de execução ou pico justificar.

Fluxo futuro:

~~~text
SIS / ERP -> adaptador de importação -> staging e reconciliação -> PostgreSQL
Aluno/professor -> front-end -> API autenticada -> regras e planos
                                      |-> cache curto de catálogo
                                      |-> fila de otimização/exportação -> worker
                                      |-> métricas, auditoria e notificações
~~~ 

O navegador nunca deve receber service role. Consultas diretas ao Supabase podem continuar para dados de baixo risco protegidos por RLS; alterações curriculares, importações e operações privilegiadas devem passar por funções/serviços autenticados e auditáveis.

## 4. Modelo de dados de destino

Preservar identificadores de origem, vigência e instante de ingestão. Não sobrescrever regras históricas que já foram usadas para produzir um plano.

Entidades recomendadas:

- courses: código e identidade estável da disciplina.
- curriculum_versions: curso, versão, campus, vigência inicial/final, situação e fonte normativa.
- curriculum_courses: vínculo entre versão, disciplina, categoria e período sugerido.
- curriculum_rules: disciplina alvo, tipo (pré ou co-requisito), expressão lógica, vigência, fonte e aprovador.
- equivalence_groups: disciplinas que podem satisfazer o mesmo requisito, com direção, condição e vigência.
- academic_terms, offerings, sections e section_meetings: semestre, oferta, turma, docente, capacidade e horários concretos.
- student_academic_records: tentativas e resultados vindos do SIS, separados de preferências e dados de acesso.
- study_plans, plan_items e planner_runs: cenário, semestre, justificativa, versão das regras, versão do algoritmo, fotografia das entradas e estado da busca.
- import_batches e import_rejections: checksum, sistema de origem, contagens, erros e estado de reprocessamento.
- audit_events: usuário/serviço, ação, entidade, data e identificador de correlação.

Para requisitos compostos, usar uma expressão booleana em JSONB com esquema validado, operadores permitidos AND/OR e referências a IDs de disciplinas. Não avaliar código arbitrário recebido do banco ou do usuário. Para regras simples, tabelas normalizadas de grupos e itens são mais fáceis de consultar e validar.

Exemplo inicial de tabelas de catálogo e ofertas, a adaptar numa migração revisada:

~~~sql
create table public.curriculum_versions (
  id uuid primary key default gen_random_uuid(),
  course_id uuid not null references public.courses(id),
  version text not null,
  valid_from date not null,
  valid_to date,
  source text not null,
  created_at timestamptz not null default now(),
  unique (course_id, version),
  check (valid_to is null or valid_to >= valid_from)
);

create table public.curriculum_courses (
  curriculum_version_id uuid not null references public.curriculum_versions(id),
  discipline_id uuid not null references public.disciplines(id),
  suggested_period smallint,
  category text not null check (category in ('obrigatoria','optativa','eletiva')),
  primary key (curriculum_version_id, discipline_id)
);

create index ix_offerings_term_course_status
  on public.offerings (academic_term_id, discipline_id, status);

create index ix_sections_offering_status
  on public.sections (offering_id, status);

create index ix_plans_student_updated
  on public.study_plans (student_id, updated_at desc);

create index ix_plan_items_plan_period
  on public.plan_items (study_plan_id, period_number);
~~~

Aplicar migrações com ferramenta e revisão de esquema; não executar este exemplo diretamente sem criar antes as tabelas referenciadas e políticas RLS. Índices devem corresponder a consultas observadas. Particionar só quando tamanho, retenção e padrão de leitura justificarem.

## 5. Segurança e LGPD

- Separar autenticação de autorização. O papel precisa ter escopo: aluno próprio, professor por turma, coordenação por curso e secretaria por função operacional.
- Manter RLS como defesa adicional no banco e testar cada perfil com casos positivos e negativos.
- Restringir CORS da Edge Function ao Pages de produção e origens de desenvolvimento autorizadas; continuar exigindo Bearer válido e papel admin no servidor.
- Ativar MFA para perfis administrativos quando disponível; manter service role em segredo de runtime.
- Registrar alterações de matriz, importações e operações privilegiadas, sem copiar histórico sensível para logs.
- Definir com a universidade finalidade, base legal, retenção, controlador/operador, processo para titulares e minimização dos dados importados. Separar identificadores pessoais do conjunto necessário ao cálculo quando possível.
- Recomendações devem ser explicáveis e corrigíveis. Nota ou desempenho anterior não deve bloquear opção automaticamente. O aluno precisa poder contestar dados divergentes do SIS.

## 6. Cache e escalabilidade

1. Antes de escalar, medir tráfego, simultaneidade, consultas lentas, conexões, erros, latência e duração do cálculo em janela normal e de matrícula.
2. Distribuir HTML, CSS, JS e catálogo versionado pela CDN do host estático. O catálogo pode ter cache longo associado à versão/ETag; invalidar quando publicar nova matriz.
3. Usar índices e paginação keyset nas listagens grandes. Os índices de paginação já existentes são um passo útil; conferir plano de execução e índices com dados representativos.
4. Não guardar vagas ou ocupação com TTL longo. Retornar timestamp e origem; perto da matrícula usar atualização mais frequente e TTL curto.
5. Introduzir Redis apenas se medições mostrarem ganho para sessão, catálogo dinâmico ou resultado temporário. Evitar cachear dados pessoais entre alunos; chavear pelo escopo e versão.
6. Usar pool de conexões, limites de concorrência e réplicas de leitura apenas quando a carga medida justificar. Isolar consultas analíticas do banco transacional.
7. Colocar importações, PDFs e otimizações que excedam o orçamento de resposta numa fila durável com retries limitados, idempotência e fila de falhas. Não adotar Kafka ou Kubernetes no MVP sem necessidade operacional demonstrada.
8. Modelar picos por simultaneidade real e taxa de solicitações. As metas iniciais de P95/P99, disponibilidade, RPO/RTO e 99,9% são hipóteses a validar com a instituição, não capacidade já comprovada.

## 7. Melhorias no algoritmo

### Fase atual

A heurística continua apropriada como baseline para um único curso e matriz pequena, desde que o resultado seja chamado de recomendação e explique limites. Não usar o conjunto de códigos em horários como prova de conflito entre turmas: o modelo ainda não contém turmas nem alternativas de seção completas.

A avaliação deve tratar separadamente:

- aprovado, reprovado, em andamento, trancado e crédito reconhecido;
- pré-requisito estrito e co-requisito;
- grupos AND/OR e equivalências vigentes;
- conclusão anterior versus disciplina planejada em período anterior;
- oferta confirmada, prevista e desconhecida;
- limite de carga, conflito de horários de turmas reais e disciplinas sem oferta.

### Evolução

1. Validar o grafo curricular, desconhecidos e ciclos antes de calcular.
2. Construir o conjunto elegível com histórico oficial e versão de matriz aplicável.
3. Gerar alternativas reais de turma; impedir sobreposição por dia/intervalo e aplicar preferências.
4. Primeiro encontrar plano válido; depois otimizar, em ordem lexicográfica, semestres até conclusão, disciplinas gargalo/baixa frequência e distribuição de carga/preferências.
5. Gravar versão de algoritmo, snapshot de entradas, estado do solver e justificativa por item.
6. Distinguir “plano viável”, “melhor plano encontrado até agora” e “nenhuma solução no limite de tempo”. Timeout não prova inexistência.

Esqueleto de regra, ainda não conectado ao SIS:

~~~text
elegivel(disciplina, semestre, historico, plano):
  cada grupo de pre-requisito precisa ser satisfeito pelo historico ou por
  conclusão em semestre anterior, segundo a expressão versionada
  cada co-requisito precisa estar no historico ou no mesmo semestre
  disciplina aprovada não entra novamente, salvo regra explícita
  oferta desconhecida reduz confiança; não é tratada como turma confirmada
  nenhum item do plano pode sobrepor horários concretos de turmas escolhidas
~~~ 

Só adotar OR-Tools/CP-SAT ou outro solver quando a heurística deixar de cumprir metas medidas ou surgirem muitas combinações de turmas, preferências e restrições simultâneas. Comparar o solver com planos revisados pela coordenação.

## 8. Integração com legado

O sistema acadêmico ainda não foi identificado; isso impede selecionar contrato, autenticação de serviço, campos e frequência de sincronização. Quando a universidade fornecer essa informação:

- preferir API ou eventos oficiais, em modo somente leitura no primeiro piloto;
- criar um adaptador por fornecedor, sem acesso direto ao banco do legado;
- importar para staging, validar versão/esquema, checksum, duplicidades e referências;
- usar chave idempotente de origem e lote para permitir reprocessamento seguro;
- produzir relatório de rejeitados e fila de reconciliação humana;
- manter última sincronização visível, tratar dados desatualizados e nunca sobrescrever uma correção manual sem auditoria;
- acordar limites, janela, finalidade e responsável técnico com a instituição.

## 9. Testes e observabilidade

Plano de testes antes de cada fase (ainda não executado neste trabalho):

- unitários para AND/OR, créditos, equivalências, vigência, co-requisitos, ciclos e estados de histórico;
- regressão com currículos versionados e casos revisados pela coordenação;
- propriedades: nenhuma disciplina duplicada, pré-requisito estrito sempre anterior, co-requisito respeitado no mesmo período quando permitido e limite de carga preservado;
- integração para RLS, funções Supabase, papéis e importação idempotente;
- segurança: tentativa de autoelevação de papel, acesso cruzado entre alunos, uso indevido de função admin e proteção de segredos;
- acessibilidade WCAG 2.2 AA e navegação por teclado/leitor de tela;
- carga com distribuição de pico realista, latência de leitura, conexões simultâneas, filas e solver, aumentando concorrência gradualmente;
- logs estruturados sem dados pessoais desnecessários, métricas de latência/erro/fila, traces com correlation ID e alertas por SLO.

## 10. Roadmap proposto

| Fase | Entrega | Critério para avançar |
| --- | --- | --- |
| 0 — confiabilidade local | Alertas de conflito, explicações por recomendação, base e horário de geração; corrigir matriz com a coordenação | Regras e limitações visíveis; conflito de Cálculo Numérico resolvido pela autoridade acadêmica |
| 1 — catálogo consistente | Catálogo versionado em uma única fonte, validação automática de referências e vigência; separar domínios do código da página | Site e notebook consomem a mesma versão; nenhuma referência desconhecida ou ciclo sem alerta |
| 2 — persistência e identidade | API de planos, histórico autorizado e papéis com escopo; SSO institucional quando definido | RLS testada e aluno acessa somente o próprio histórico/plano |
| 3 — integração piloto | Adaptador somente leitura para SIS/ERP, staging, idempotência, reconciliação e auditoria | Importação repetível e relatório de divergências aprovado pela secretaria |
| 4 — cálculo e escala | Worker/fila para cálculos demorados, cache seletivo, painéis e alertas | Teste de carga valida simultaneidade, SLO e custo em janela de matrícula |
| 5 — expansão | Simulações, cenários, métricas agregadas e integrações adicionais | Governança, acessibilidade e operação sustentadas pela instituição |

**Não incluído nesta entrega:** provisionar infraestrutura para 500 mil contas, ativar SSO ou integrar SIS, porque dependem de dados, credenciais, contrato e autorização da universidade. Nenhuma matrícula ou regra oficial é modificada pelo planejador.
