import Link from 'next/link';
export default function NotFound(){return <main id="main" className="wrap page-intro"><span className="eyebrow">404</span><h1>This page isn’t available.</h1><p>The category or product may not be published.</p><Link className="button" href="/products">Explore categories ↗</Link></main>}
