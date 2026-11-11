import type {MetadataRoute} from 'next';
import {categories,products} from '@/lib/db';
export const dynamic='force-dynamic';
export default async function sitemap():Promise<MetadataRoute.Sitemap>{const base=process.env.SITE_URL||'http://localhost:3000';const [cats,items]=await Promise.all([categories(),products()]);return ['','/about','/products','/trading-solutions','/contact','/request-quote','/privacy',...cats.map(c=>`/categories/${c.slug}`),...items.map(p=>`/products/${p.slug}`)].map(url=>({url:base+url}));}
