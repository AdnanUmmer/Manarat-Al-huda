import { randomBytes,scryptSync,timingSafeEqual,createHash } from 'node:crypto';
import { cookies,headers } from 'next/headers';
import { redirect } from 'next/navigation';
import { db } from './db';
export const hashToken=(s:string)=>createHash('sha256').update(s).digest('hex');
export function passwordHash(password:string){const salt=randomBytes(16).toString('hex');return `${salt}:${scryptSync(password,salt,64).toString('hex')}`;}
export function passwordValid(password:string,hash:string){const [salt,key]=hash.split(':');const actual=scryptSync(password,salt,64);const expected=Buffer.from(key,'hex');return actual.length===expected.length&&timingSafeEqual(actual,expected);}
export async function admin(){const token=(await cookies()).get('mah_session')?.value;if(!token||!process.env.DATABASE_URL)return null;return (await db.query('SELECT a.id,a.email FROM sessions s JOIN admins a ON a.id=s.admin_id WHERE s.token_hash=$1 AND s.expires_at>now()',[hashToken(token)])).rows[0]??null;}
export async function requireAdmin(){const user=await admin();if(!user)redirect('/admin/login');return user;}
export async function sameOrigin(){const h=await headers();const expected=new URL(process.env.SITE_URL||'http://localhost:3000').origin;if(h.get('origin')!==expected)throw new Error('Invalid request origin');}
export async function rateLimit(scope:string,limit=5){const h=await headers();const ip=process.env.TRUST_PROXY==='true'?(h.get('x-real-ip')||'unknown'):'direct';const key=hashToken(scope+':'+ip);const r=await db.query(`INSERT INTO rate_limits(key,hits,expires_at) VALUES($1,1,now()+interval '15 minutes') ON CONFLICT(key) DO UPDATE SET hits=CASE WHEN rate_limits.expires_at<now() THEN 1 ELSE rate_limits.hits+1 END,expires_at=CASE WHEN rate_limits.expires_at<now() THEN now()+interval '15 minutes' ELSE rate_limits.expires_at END RETURNING hits`,[key]);if(r.rows[0].hits>limit)throw new Error('Too many attempts. Please try again in 15 minutes.');}
