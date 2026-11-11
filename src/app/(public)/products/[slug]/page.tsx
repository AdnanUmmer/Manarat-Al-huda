import {products} from '@/lib/db';
import {notFound} from 'next/navigation';
import {Intro} from '@/components/site';
import {AddToQuote} from '@/components/quote-form';
import Image from 'next/image';
export async function generateMetadata({params}:{params:Promise<{slug:string}>}){const {slug}=await params;const p=(await products()).find(p=>p.slug===slug);return {title:p?.name,description:p?.description,alternates:{canonical:`/products/${slug}`}};}
export default async function Page({params}:{params:Promise<{slug:string}>}){const {slug}=await params;const p=(await products()).find(p=>p.slug===slug);if(!p)notFound();return <><Intro label={p.brand||'OUR PRODUCTS'} title={p.name}><p>{p.description}</p></Intro><section className="wrap quote-section"><div>{p.images.map((src:string)=><div className="product-photo" key={src}><Image src={src} alt={p.name} fill sizes="50vw"/></div>)}</div><div><h2>Product details</h2>{[['Packaging',p.packaging],['Case quantity',p.case_quantity],['Variants',p.variants],['Availability',p.availability]].filter(([,v])=>v).map(([k,v])=><p key={k}><strong>{k}</strong><br/>{v}</p>)}<AddToQuote product={p}/></div></section></>}
