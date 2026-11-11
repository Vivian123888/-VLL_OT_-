-- Execute no SQL Editor do Supabase, após a versão anterior de supabase.sql.
-- Contas novas continuam com role='aluno'; apenas RPC administrativa promove professores.
alter table public.profiles drop constraint if exists profiles_role_check;
alter table public.profiles add constraint profiles_role_check check (role in ('aluno','professor','admin'));

create table if not exists public.solicitacoes_professor (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null unique references auth.users(id) on delete cascade,
 nome text not null check (length(trim(nome)) between 2 and 150),
 email text not null,
 status text not null default 'pendente' check (status in ('pendente','aprovada','rejeitada')),
 created_at timestamptz not null default now(),
 reviewed_at timestamptz,
 reviewed_by uuid references auth.users(id),
 notification_sent_at timestamptz,
 notification_claimed_at timestamptz
);
alter table public.solicitacoes_professor enable row level security;
revoke all on public.solicitacoes_professor from anon,authenticated;
grant select on public.solicitacoes_professor to authenticated;
drop policy if exists "Solicitante ve pedido" on public.solicitacoes_professor;
create policy "Solicitante ve pedido" on public.solicitacoes_professor
for select to authenticated using (
 user_id=(select auth.uid()) or exists(
 select 1 from public.profiles where id=(select auth.uid()) and role='admin'));

-- Solicitação autenticada; e-mail é lido do auth.users, nunca confiado ao navegador.
create or replace function public.solicitar_acesso_professor()
returns uuid language plpgsql security definer set search_path = ''
as $$
declare uid uuid := auth.uid(); request_id uuid; user_email text; user_name text;
begin
 if uid is null then raise exception 'Autenticação obrigatória'; end if;
 select email,coalesce(nullif(trim(raw_user_meta_data->>'nome'),''),'Usuário')
 into user_email,user_name from auth.users where id=uid and email_confirmed_at is not null;
 if user_email is null then raise exception 'Confirme seu e-mail antes de solicitar'; end if;
 if exists(select 1 from public.profiles where id=uid and role in ('admin','professor')) then
  raise exception 'Conta já autorizada';
 end if;
 insert into public.solicitacoes_professor(user_id,nome,email)
 values(uid,user_name,user_email)
 on conflict(user_id) do update set
  nome=excluded.nome,email=excluded.email
  -- Rejeições não são automaticamente revertidas; aprovação não pode ser alterada aqui.
  where public.solicitacoes_professor.status='pendente'
 returning id into request_id;
 if request_id is null then raise exception 'Solicitação já analisada'; end if;
 return request_id;
end $$;
revoke all on function public.solicitar_acesso_professor() from public,anon;
grant execute on function public.solicitar_acesso_professor() to authenticated;

-- Apenas administradores podem consultar a fila completa.
create or replace function public.listar_solicitacoes_professor()
returns table(id uuid,nome text,email text,status text,created_at timestamptz,reviewed_at timestamptz)
language plpgsql security definer set search_path = ''
as $$
begin
 if not exists(select 1 from public.profiles p where p.id=auth.uid() and p.role='admin') then
  raise exception 'Acesso negado';
 end if;
 return query select s.id,s.nome,s.email,s.status,s.created_at,s.reviewed_at
 from public.solicitacoes_professor s order by s.created_at desc;
end $$;
revoke all on function public.listar_solicitacoes_professor() from public,anon;
grant execute on function public.listar_solicitacoes_professor() to authenticated;

create or replace function public.analisar_solicitacao_professor(p_id uuid,p_aprovar boolean)
returns void language plpgsql security definer set search_path = ''
as $$
declare solicitante uuid;
begin
 if not exists(select 1 from public.profiles where id=auth.uid() and role='admin') then
  raise exception 'Acesso negado';
 end if;
 select user_id into solicitante from public.solicitacoes_professor
 where id=p_id and status='pendente' for update;
 if solicitante is null then raise exception 'Solicitação inexistente ou já analisada'; end if;
 update public.solicitacoes_professor set
 status=case when p_aprovar then 'aprovada' else 'rejeitada' end,
 reviewed_at=now(),reviewed_by=auth.uid()
 where id=p_id;
 if p_aprovar then
  update public.profiles set role='professor' where id=solicitante and role='aluno';
  if not found then raise exception 'Perfil não encontrado ou não elegível'; end if;
 end if;
end $$;
revoke all on function public.analisar_solicitacao_professor(uuid,boolean) from public,anon;
grant execute on function public.analisar_solicitacao_professor(uuid,boolean) to authenticated;

-- EXECUTE ESTA ETAPA MANUALMENTE COM ACESSO ADMINISTRATIVO NO SQL EDITOR.
-- A conta precisa ter sido criada e seu e-mail confirmado no Supabase Auth.
-- Nunca transforme usuários em administradores a partir do JavaScript.
-- update public.profiles set role='admin'
-- where id=(select id from auth.users
--           where lower(email)='vivianlauriano02@gmail.com' and email_confirmed_at is not null);
