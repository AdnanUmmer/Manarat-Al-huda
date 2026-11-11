import { Pool } from 'pg';
import { initialCategories,defaultSettings,type Category,type Settings } from './catalogue';
const globalDb = globalThis as unknown as { pool?: Pool };
export const db = globalDb.pool ?? new Pool({connectionString:process.env.DATABASE_URL,max:process.env.LOCAL_ONLY==='true'?1:10,connectionTimeoutMillis:5000});
if(process.env.NODE_ENV!=='production') globalDb.pool=db;
export async function categories(all=false):Promise<Category[]> { if(!process.env.DATABASE_URL) {if(all) throw new Error('Database is not configured'); return initialCategories;} return (await db.query(`SELECT * FROM categories ${all?'':'WHERE published=true'} ORDER BY sort_order,name`)).rows; }
export async function settings():Promise<Settings> {if(!process.env.DATABASE_URL)return defaultSettings; const r=await db.query('SELECT data FROM settings WHERE id=1');return {...defaultSettings,...r.rows[0]?.data};}
export async function products(category?:string) {if(!process.env.DATABASE_URL)return [];return (await db.query('SELECT p.* FROM products p JOIN categories c ON c.id=p.category_id WHERE p.published AND NOT p.archived AND c.published AND ($1::text IS NULL OR c.slug=$1) ORDER BY p.name',[category??null])).rows;}
