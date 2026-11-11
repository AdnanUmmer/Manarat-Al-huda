import 'dotenv/config';
import { randomUUID } from 'node:crypto';
import { scryptSync,randomBytes } from 'node:crypto';
import { db } from '../src/lib/db';
const email=process.env.ADMIN_EMAIL?.toLowerCase();const password=process.env.ADMIN_PASSWORD;
if(!email||!password||password.length<14)throw new Error('Set ADMIN_EMAIL and ADMIN_PASSWORD (at least 14 characters) for this command only.');
const salt=randomBytes(16).toString('hex');
db.query('INSERT INTO admins(id,email,password_hash) VALUES($1,$2,$3)',[randomUUID(),email,`${salt}:${scryptSync(password,salt,64).toString('hex')}`]).then(()=>console.log('Administrator created.')).finally(()=>db.end());
