import {categories} from '@/lib/db';
import {CategoryCard,Intro} from '@/components/site';
export const metadata={title:'Our Products',alternates:{canonical:'/products'}};
export default async function Page(){const cats=await categories();return <><Intro label="OUR PRODUCTS" title="Everyday categories. Wholesale possibilities."><p>Beverages at our core. A broader range of consumer goods for your business. Explore a category and tell us what you need.</p></Intro><div className="wrap catalogue-grid">{cats.map((c,i)=><CategoryCard key={c.id} category={c} index={i}/>)}</div><p className="wrap image-note">Category imagery is illustrative. Brands, packaging and availability are confirmed during your enquiry.</p></>}
