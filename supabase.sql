-- Execute no SQL Editor do Supabase.
-- Auth gerencia senhas com hash; jamais salve senhas em tabelas próprias.
create table if not exists public.profiles (
 id uuid primary key references auth.users(id) on delete cascade,
 nome text not null,
 role text not null default 'aluno' check (role in ('aluno','professor')),
 created_at timestamptz not null default now()
);
alter table public.profiles enable row level security;
drop policy if exists "Ler proprio perfil" on public.profiles;
create policy "Ler proprio perfil" on public.profiles for select to authenticated using (id = (select auth.uid()));
-- Não existe política de UPDATE para profiles: aluno não pode se promover a professor.
create or replace function public.criar_perfil()
returns trigger language plpgsql security definer set search_path = '' as $$
begin
 insert into public.profiles (id,nome,role)
 values (new.id,coalesce(nullif(trim(new.raw_user_meta_data ->> 'nome'),''),'Aluno'),'aluno');
 return new;
end; $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
for each row execute function public.criar_perfil();

create table if not exists public.alunos_acompanhados (
 id uuid primary key default gen_random_uuid(),
 professor_id uuid not null references public.profiles(id),
 nome text not null check (length(trim(nome)) >= 2),
 matricula text not null,
 periodo integer not null check (periodo between 1 and 30),
 created_at timestamptz not null default now(),
 unique(professor_id,matricula)
);
alter table public.alunos_acompanhados enable row level security;
drop policy if exists "Professor ve seus alunos" on public.alunos_acompanhados;
create policy "Professor ve seus alunos" on public.alunos_acompanhados
 for select to authenticated using (
 professor_id = (select auth.uid()) and exists (
 select 1 from public.profiles p where p.id = (select auth.uid()) and p.role = 'professor'));
drop policy if exists "Professor cadastra seus alunos" on public.alunos_acompanhados;
create policy "Professor cadastra seus alunos" on public.alunos_acompanhados
 for insert to authenticated with check (
 professor_id = (select auth.uid()) and exists (
 select 1 from public.profiles p where p.id = (select auth.uid()) and p.role = 'professor'));

-- Para habilitar um professor: crie a conta pelo painel Authentication > Users
-- e execute com privilégios administrativos, substituindo o email:
-- update public.profiles set role = 'professor' where id = (
--   select id from auth.users where email = 'professor@instituicao.edu.br'
-- );
