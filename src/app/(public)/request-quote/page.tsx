import {categories} from '@/lib/db';
import {Intro} from '@/components/site';
import {QuoteForm} from '@/components/quote-form';
export const metadata={title:'Request a Quote',alternates:{canonical:'/request-quote'}};
export default async function Page(){return <><Intro label="LET’S DO BUSINESS" title="Tell us what you need."><p>One enquiry. Multiple categories. Share your requirements and our team will review them with you.</p></Intro><section className="wrap quote-section"><div><h2>A conversation,<br/>built around you.</h2><p>Include your preferred brands, pack sizes and estimated quantities. Availability and supply arrangements are confirmed directly.</p><a className="text-link" href="mailto:Manaratalhudallc@gmail.com">Prefer email? Get in touch ↗</a></div><QuoteForm categories={await categories()}/></section></>}
