// Supabase Edge Function: notificar-solicitacao
// Secrets: RESEND_API_KEY, RESEND_FROM_EMAIL, ADMIN_EMAIL (optional), SUPABASE_SERVICE_ROLE_KEY
import { createClient } from 'npm:@supabase/supabase-js@2';
const cors={
 'Access-Control-Allow-Origin':'*',
 'Access-Control-Allow-Headers':'authorization, x-client-info, apikey, content-type',
 'Access-Control-Allow-Methods':'POST, OPTIONS',
};
const json=(status,body)=>new Response(JSON.stringify(body),{status,headers:{...cors,'Content-Type':'application/json'}});
Deno.serve(async req=>{
 if(req.method==='OPTIONS')return new Response(null,{headers:cors});
 if(req.method!=='POST')return json(405,{error:'Método inválido'});
 try{
  const url=Deno.env.get('SUPABASE_URL')!;
  const anon=Deno.env.get('SUPABASE_ANON_KEY')!;
  const service=Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
  const resend=Deno.env.get('RESEND_API_KEY');
  const from=Deno.env.get('RESEND_FROM_EMAIL');
  const adminEmail=Deno.env.get('ADMIN_EMAIL');
  if(!resend||!from||!adminEmail)return json(503,{error:'Envio de e-mails não configurado'});
  const bearer=req.headers.get('authorization')||'';
  if(!bearer.startsWith('Bearer '))return json(401,{error:'Não autenticado'});
  const client=createClient(url,anon,{global:{headers:{Authorization:bearer}}});
  const {data:{user},error:userErr}=await client.auth.getUser();
  if(userErr||!user)return json(401,{error:'Não autenticado'});
  const {request_id}=await req.json();
  if(typeof request_id!=='string'||! /^[0-9a-f-]{36}$/i.test(request_id))return json(400,{error:'ID inválido'});
  const db=createClient(url,service);
  const {data:request,error:fetchErr}=await db.from('solicitacoes_professor')
   .select('id,user_id,nome,email,status,notification_sent_at,notification_claimed_at')
   .eq('id',request_id).eq('user_id',user.id).single();
  if(fetchErr||!request||request.status!=='pendente')return json(404,{error:'Solicitação não encontrada'});
  if(request.notification_sent_at)return json(200,{ok:true,already_sent:true});
  const deadline=new Date(Date.now()-5*60*1000).toISOString();
  const {data:claimed,error:claimErr}=await db.from('solicitacoes_professor')
   .update({notification_claimed_at:new Date().toISOString()})
   .eq('id',request.id).is('notification_sent_at',null)
   .or('notification_claimed_at.is.null,notification_claimed_at.lt.'+deadline)
   .select('id').maybeSingle();
  if(claimErr)return json(500,{error:'Falha ao reservar notificação'});
  if(!claimed)return json(200,{ok:true,already_processing:true});
  const body={
   from, to:[adminEmail], subject:'Nova solicitação de acesso de professor — Otimizador de Grade',
   text:'Uma conta solicitou acesso como professor.\n\nNome: '+request.nome+
    '\nE-mail: '+request.email+'\nSolicitação: '+request.id+
    '\n\nAcesse o painel administrativo autenticado para aprovar ou rejeitar.\n'+
    'https://vivian123888.github.io/-VLL_OT_-/admin.html'
  };
  const response=await fetch('https://api.resend.com/emails',{
   method:'POST',headers:{Authorization:'Bearer '+resend,'Content-Type':'application/json'},
   body:JSON.stringify(body)
  });
  if(!response.ok){
   await db.from('solicitacoes_professor').update({notification_claimed_at:null}).eq('id',request.id).is('notification_sent_at',null);
   return json(502,{error:'Não foi possível enviar o aviso ao administrador'});
  }
  await db.from('solicitacoes_professor').update({notification_sent_at:new Date().toISOString()}).eq('id',request.id);
  return json(200,{ok:true});
 }catch(e){return json(500,{error:'Falha interna ao processar a notificação'});}
});