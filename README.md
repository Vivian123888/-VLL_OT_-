# Otimizador de Grade Curricular — Engenharia de Produção

Aplicação web para planejamento de disciplinas da matriz 2026, com autenticação Supabase para alunos, professores e administradora.

## Publicar no GitHub Pages

1. Em **Settings > Pages**, escolha **Deploy from a branch**.
2. Selecione a branch **main** e a pasta **/(root)**.
3. Aguarde a publicação do site.

## Utilização

- Marque as disciplinas já concluídas, defina o limite de períodos e clique em **Gerar plano de estudos**.
- A grade é calculada por uma heurística e deve ser validada com a coordenação.
- A seleção de disciplinas concluídas fica no navegador do aluno.

## Login e permissões

O site usa Supabase para autenticação e armazenamento protegido. A configuração do projeto fica em [supabase-config.js](./supabase-config.js), com URL e chave publicável. Nunca exponha uma chave secreta ou `service_role` no GitHub Pages.

- Em **Authentication > URL Configuration**, configure a URL de login do GitHub Pages e os redirecionamentos permitidos.
- Em **Authentication > Providers > Email**, mantenha o cadastro habilitado e deixe **Confirm email** desligado para que alunos possam entrar sem confirmação.
- [supabase.sql](./supabase.sql) cria perfis e regras RLS.
- [supabase-aprovacao.sql](./supabase-aprovacao.sql) adiciona solicitações de professor e o papel de administradora.

### Páginas

- `login.html`: entrar, criar conta de aluno ou solicitar acesso de professor.
- `index.html`: área do aluno.
- `professor.html`: área de professor aprovado.
- `admin.html`: fila de solicitações e lista de contas de usuário.

A única forma de conceder os papéis `professor` e `admin` é por rotinas protegidas ou operações administrativas no banco. O navegador não pode promover uma conta. O painel administrativo impede excluir a própria conta e protege outras contas administrativas. Ao excluir um professor, os registros de alunos vinculados também são removidos.

## Configuração administrativa e funções

A conta administradora deve existir em Supabase Auth. Depois de executar [supabase-aprovacao.sql](./supabase-aprovacao.sql), conceda o papel no SQL Editor, substituindo `admin@example.com` pelo endereço da conta:

```sql
update public.profiles set role='admin'
where id=(select id from auth.users
          where lower(email)='admin@example.com');
```

A função [admin-usuarios](./supabase/functions/admin-usuarios/index.ts) lista as contas e exclui usuários usando privilégios de servidor. O segredo `service_role` nunca deve ir para o navegador. Implante as funções `admin-usuarios` e `notificar-solicitacao` no Supabase a partir dos arquivos em `supabase/functions/`.

## Notificação de pedidos de professor

A função [notificar-solicitacao](./supabase/functions/notificar-solicitacao/index.ts) envia para o destinatário configurado no segredo privado `ADMIN_EMAIL` o nome, e-mail e identificador do pedido. O administrador analisa o pedido em `admin.html`; o e-mail não aprova o acesso sozinho.

O destinatário `ADMIN_EMAIL` já está salvo como segredo no projeto Supabase conectado. Para ativar o envio, crie uma conta no [Resend](https://resend.com), verifique um domínio remetente e salve no Supabase **Edge Functions > Secrets**:

- `RESEND_API_KEY`: chave da API Resend.
- `RESEND_FROM_EMAIL`: remetente verificado, por exemplo `Notificacoes <avisos@seudominio.com>`.

Não coloque essas credenciais em arquivos do site ou no GitHub. Sem esses dois segredos, o pedido ainda fica visível no painel administrativo, mas o e-mail automático não é enviado.

As funções validam a sessão Supabase antes de realizar operações protegidas. Apenas uma administradora pode listar/excluir contas ou analisar pedidos de professor.
