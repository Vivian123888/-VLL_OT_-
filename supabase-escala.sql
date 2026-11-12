-- Índices incrementais para consultas paginadas.
-- Aplicar após supabase.sql e supabase-aprovacao.sql no SQL Editor do Supabase.

-- Suporta a listagem por professor ordenada por data e ID.
create index if not exists ix_alunos_acompanhados_professor_data
 on public.alunos_acompanhados (professor_id, created_at desc, id desc);

-- Suporta a fila administrativa ordenada por data e ID.
create index if not exists ix_solicitacoes_professor_data
 on public.solicitacoes_professor (created_at desc, id desc);
