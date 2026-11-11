import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
import { SUPABASE_URL, SUPABASE_ANON_KEY } from './supabase-config.js';
export const configured = SUPABASE_URL.startsWith('https://') && !SUPABASE_ANON_KEY.startsWith('COLE_');
export const supabase = configured ? createClient(SUPABASE_URL, SUPABASE_ANON_KEY) : null;
export async function currentProfile(){
 if(!configured) throw new Error('Configure supabase-config.js para ativar o login.');
 const {data:{user},error}=await supabase.auth.getUser();
 if(error||!user)return null;
 const {data,error:profileError}=await supabase.from('profiles').select('id,nome,role').eq('id',user.id).single();
 if(profileError)throw profileError;
 return data;
}
export async function requireRole(role){
 const p=await currentProfile();
 if(!p){location.replace('./login.html');return null;}
 if(p.role!==role){location.replace(p.role==='professor'?'./professor.html':'./index.html');return null;}
 return p;
}
export async function logout(){if(supabase)await supabase.auth.signOut();location.replace('./login.html');}
