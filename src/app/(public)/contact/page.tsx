import {categories,settings} from '@/lib/db';
import {Intro} from '@/components/site';
import {QuoteForm} from '@/components/quote-form';
export const metadata={title:'Contact',alternates:{canonical:'/contact'}};
export default async function Page(){const s=await settings();return <><Intro label="CONTACT" title="Good business starts with a conversation."/><section className="wrap quote-section"><div><h2>Let’s connect.</h2><h3>{s.company}</h3><p>{s.location}</p><a className="text-link" href={`mailto:${s.email}`}>{s.email}</a>{s.phone&&<p><a href={`tel:${s.phone}`}>{s.phone}</a></p>}<p>For quotation enquiries, share your category and product requirements using the form.</p></div><QuoteForm categories={await categories()} contact/></section></>}
