# Otimizador de Grade Curricular — Engenharia de Produção

Aplicação web estática para planejamento de disciplinas da matriz 2026.

## Publicar no GitHub Pages

1. Abra **Settings** do repositório.
2. Selecione **Pages** no menu lateral.
3. Em **Build and deployment**, escolha **Deploy from a branch**.
4. Selecione a branch **main**, pasta **/(root)**, e clique em **Save**.
5. Aguarde a publicação e use o endereço exibido em Pages.

A aplicação está em `index.html` e não exige Google Colab, servidor ou banco de dados.

## Utilização

- Marque as disciplinas já concluídas.
- Defina o número máximo de períodos e o limite de disciplinas por período.
- Marque **Considerar conflitos de horário** somente quando quiser usar os horários históricos.
- Clique em **Gerar plano de estudos**.
- Use **Salvar grade em PDF** e escolha **Salvar como PDF** no destino de impressão do navegador.
- Opcionalmente baixe um CSV ou salve sua seleção no navegador.

## Observações

A aplicação usa uma **heurística**, não um algoritmo de otimização exata: a grade encontrada não é necessariamente a de menor duração. Requisitos de créditos acumulados são verificados antes de cada período. As ofertas e horários devem ser validados junto à coordenação; horários vazios não indicam disponibilidade confirmada.

As disciplinas concluídas são armazenadas somente no navegador do aluno quando ele clica em **Salvar seleção neste navegador**.


## Login de alunos e professores (Supabase)

O site usa [Supabase](https://supabase.com) para autenticação real e armazenamento protegido. **O login não funciona até concluir esta configuração**:

1. Crie um projeto no Supabase.
2. No **SQL Editor**, execute todo o conteúdo de [supabase.sql](./supabase.sql). Isso cria os perfis, a tabela de acompanhamento e as políticas RLS.
3. Em **Project Settings > API** (ou **Connect**), copie a **Project URL** e a chave **anon/publishable** pública para [supabase-config.js](./supabase-config.js). **Nunca** publique a chave `service_role` ou `secret`.
4. Em **Authentication > URL Configuration**, configure a **Site URL** como `https://vivian123888.github.io/-VLL_OT_-/login.html` e adicione `https://vivian123888.github.io/-VLL_OT_-/**` às URLs de redirecionamento permitidas.
5. Em **Authentication > Providers > Email**, habilite o cadastro por e-mail e a confirmação de e-mail (recomendado).
6. Para um professor, crie a conta no **Authentication > Users** (informe nome no metadata `nome`, se possível) e, no SQL Editor, execute o comando comentado no fim de `supabase.sql` para promover seu perfil a `professor`. **Não existe cadastro público de professores**, evitando que alunos se atribuam permissões.
7. Publique o site pelo GitHub Pages (branch `main`, pasta `/(root)`).

### Rotas

- `login.html`: entrar com e-mail/senha ou criar conta de aluno com nome, e-mail e senha.
- `index.html`: otimizador acessível apenas ao perfil `aluno`, após autenticação.
- `professor.html`: painel restrito ao perfil `professor`, com nome, matrícula e período do aluno.
- `supabase.sql`: esquema do banco e regras de segurança.

**Privacidade:** o nome, a matrícula e o período dos alunos são dados pessoais. Informe aos usuários a finalidade do cadastro e mantenha o acesso restrito. O painel atualmente permite ao professor ver somente os alunos que ele mesmo cadastrou. O cadastro de um aluno pelo professor **não vincula automaticamente** a matrícula à conta criada pelo aluno; essa associação exige uma etapa adicional com verificação de identidade.

**Importante:** o arquivo `index.html` contém a interface e os dados públicos da matriz. O bloqueio de acesso é implementado pela autenticação da página; os dados protegidos dos professores permanecem no Supabase sob políticas RLS.

## Aprovação de professores e notificações por e-mail

**Implementação no código concluída, mas depende de ativação manual dos serviços externos.** O administrador designado é **vivianlauriano02@gmail.com**.

### 1. Criar a conta de administrador

1. Configure o Supabase conforme as etapas anteriores.
2. Crie uma conta de aluno com o e-mail **vivianlauriano02@gmail.com** e confirme o e-mail.
3. No **SQL Editor**, execute [supabase-aprovacao.sql](./supabase-aprovacao.sql), que cria a tabela de solicitações e as funções protegidas.
4. Execute, **apenas no SQL Editor com privilégios administrativos**, o comando abaixo. A promoção só ocorrerá se a conta já existir e tiver e-mail confirmado:

```sql
update public.profiles set role='admin'
where id=(select id from auth.users
          where lower(email)='vivianlauriano02@gmail.com' and email_confirmed_at is not null);
```

O endereço de e-mail sozinho não dá privilégios: a promoção é uma operação administrativa no banco. **Não coloque essa instrução em código executado no navegador.**

### 2. Envio automático de e-mails

1. Crie uma conta no [Resend](https://resend.com), verifique um domínio remetente e obtenha uma API key.
2. No projeto Supabase, configure os segredos da Edge Function: `RESEND_API_KEY`, `RESEND_FROM_EMAIL` (ex.: `Notificacoes <avisos@seudominio.com>`) e `ADMIN_EMAIL=vivianlauriano02@gmail.com`. **Não coloque esses segredos no GitHub Pages, nem em `supabase-config.js`.**
3. Publique a função em [supabase/functions/notificar-solicitacao/index.ts](./supabase/functions/notificar-solicitacao/index.ts). Com o [Supabase CLI](https://supabase.com/docs/guides/local-development/cli/getting-started), a partir da raiz do repositório:

```bash
supabase login
supabase link --project-ref SEU_PROJECT_REF
supabase secrets set RESEND_API_KEY=SUA_CHAVE RESEND_FROM_EMAIL=avisos@seudominio.com ADMIN_EMAIL=vivianlauriano02@gmail.com
supabase functions deploy notificar-solicitacao
```

O Supabase disponibiliza automaticamente as variáveis `SUPABASE_URL`, `SUPABASE_ANON_KEY` e `SUPABASE_SERVICE_ROLE_KEY` para Edge Functions hospedadas. Mantenha a verificação JWT habilitada.

**Atenção:** se você usar apenas um endereço de testes do Resend, pode haver restrições de destinatários. Verifique o domínio remetente para notificações de produção.

### 3. Fluxo de uso

- **Professor:** abre `login.html`, escolhe **Solicitar acesso de professor**, informa nome/e-mail/senha e confirma o e-mail. Na próxima entrada, o sistema registra a solicitação e chama a função de notificação. Também é possível solicitar usando uma conta existente.
- **Administrador:** recebe e-mail de aviso e entra em `admin.html` para aprovar ou rejeitar. A notificação **não contém um link de aprovação sem autenticação**.
- **Professor aprovado:** passa a ter o perfil `professor` e é direcionado ao painel `professor.html`.
- **Aluno:** continua com o perfil `aluno` e acessa o otimizador normalmente.

As funções SQL validam a identidade pelo Supabase Auth; o navegador não pode atribuir a si mesmo a função de professor ou administrador. Solicitações são únicas por usuário, e a Edge Function limita reenvios do mesmo aviso.

### 4. Testes de aceitação

1. Cadastre um aluno comum e verifique que não acessa `admin.html` nem `professor.html`.
2. Solicite uma conta de professor, confirme o e-mail e faça login. Verifique o status **pendente**.
3. Confirme que o e-mail chegou à caixa de **vivianlauriano02@gmail.com** (e verifique logs da função se não chegar).
4. Entre como administrador e aprove a solicitação em `admin.html`.
5. Faça novo login com a conta aprovada e confirme o acesso ao painel de professor.
6. Repita com outra conta e rejeite para confirmar que ela não ganha acesso.

**Limite:** a publicação do código no GitHub não cria automaticamente um projeto Supabase, não define os segredos do Resend e não envia e-mails antes da configuração acima.
