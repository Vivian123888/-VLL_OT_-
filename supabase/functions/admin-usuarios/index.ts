// Supabase Edge Function: admin-usuarios
// Uses the service role only on the server. Never expose it to the browser.
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
  const bearer=req.headers.get('authorization')||'';
  if(!bearer.startsWith('Bearer '))return json(401,{error:'Não autenticado'});
  const auth=createClient(url,anon,{global:{headers:{Authorization:bearer}}});
  const {data:{user},error:authError}=await auth.auth.getUser();
  if(authError||!user)return json(401,{error:'Não autenticado'});
  const db=createClient(url,service);
  const {data:profile,error:profileError}=await db.from('profiles').select('role').eq('id',user.id).maybeSingle();
  if(profileError||profile?.role!=='admin')return json(403,{error:'Acesso negado'});
  const body=await req.json();
  if(body?.action==='list'){
   const all=[];
   for(let page=1;page<=100;page++){
    const {data,error}=await db.auth.admin.listUsers({page,perPage:100});
    if(error)return json(500,{error:'Não foi possível listar as contas'});
    const batch=data?.users||[];all.push(...batch);
    if(batch.length<100)break;
   }
   const ids=all.map(x=>x.id);
   const {data:profiles,error:profilesError}=ids.length
    ?await db.from('profiles').select('id,nome,role').in('id',ids)
    :{data:[],error:null};
   if(profilesError)return json(500,{error:'Não foi possível carregar os perfis'});
   const byId=new Map((profiles||[]).map(p=>[p.id,p]));
   return json(200,{users:all.map(x=>{const p=byId.get(x.id)||{};return{
    id:x.id,email:x.email||'',created_at:x.created_at||null,last_sign_in_at:x.last_sign_in_at||null,
    nome:p.nome||x.user_metadata?.nome||'',role:p.role||''
   };})});
  }
  if(body?.action==='delete'){
   const id=body.user_id;
   if(typeof id!=='string'||! /^[0-9a-f-]{36}$/i.test(id))return json(400,{error:'ID inválido'});
   if(id===user.id)return json(400,{error:'Não é possível excluir a própria conta'});
   const {data:targetProfile,error:targetError}=await db.from('profiles').select('role').eq('id',id).maybeSingle();
   if(targetError)return json(500,{error:'Não foi possível validar a conta'});
   if(targetProfile?.role==='admin')return json(403,{error:'Contas administrativas são protegidas'});
   const {error:deleteError}=await db.auth.admin.deleteUser(id);
   if(deleteError)return json(500,{error:'Não foi possível excluir a conta'});
   return json(200,{ok:true});
  }
  return json(400,{error:'Ação inválida'});
 }catch(_){return json(500,{error:'Falha interna ao processar a solicitação'});}
});