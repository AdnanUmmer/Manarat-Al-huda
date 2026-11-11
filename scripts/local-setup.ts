import 'dotenv/config';
import {randomBytes,randomUUID,scryptSync} from 'node:crypto';
import {mkdir,writeFile} from 'node:fs/promises';
import {db} from '../src/lib/db';
async function main(){
if(process.env.LOCAL_ONLY!=='true')throw new Error('Local bootstrap requires LOCAL_ONLY=true');
await mkdir('.local',{recursive:true});
const email='admin@manarat.local';
const exists=await db.query('SELECT id FROM admins WHERE email=$1',[email]);
if(!exists.rowCount){const password=randomBytes(18).toString('base64url');const salt=randomBytes(16).toString('hex');await db.query('INSERT INTO admins(id,email,password_hash) VALUES($1,$2,$3)',[randomUUID(),email,`${salt}:${scryptSync(password,salt,64).toString('hex')}`]);await writeFile('.local/ADMIN-ACCESS.txt',`Local admin only\nURL: http://127.0.0.1:3000/admin\nEmail: ${email}\nPassword: ${password}\n\nKeep this file private. Never deploy this file or the local database publicly.\n`,{mode:0o600});console.log('Local administrator created. Credentials are in .local/ADMIN-ACCESS.txt.');}else console.log('Existing local administrator retained.');
await db.end();

}
main().catch(()=>{console.error("Local setup failed");process.exitCode=1;});
