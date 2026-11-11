import 'dotenv/config';
import { readFile } from 'node:fs/promises';
import { db } from '../src/lib/db';
import { initialCategories,defaultSettings } from '../src/lib/catalogue';
async function main(){const c=await db.connect();try{await c.query('BEGIN');await c.query(await readFile('scripts/001-initial.sql','utf8'));for(const x of initialCategories){const keys=Object.keys(x);await c.query(`INSERT INTO categories (${keys.join(',')}) VALUES (${keys.map((_,i)=>'$'+(i+1)).join(',')}) ON CONFLICT DO NOTHING`,Object.values(x));}await c.query('INSERT INTO settings VALUES (1,$1) ON CONFLICT DO NOTHING',[JSON.stringify(defaultSettings)]);await c.query('COMMIT');console.log('Schema and category seed ready.');}catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();await db.end();}}main().catch(()=>{console.error('Migration failed. Check database configuration.');process.exitCode=1;});
