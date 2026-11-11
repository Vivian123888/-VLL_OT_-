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
