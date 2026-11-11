'use client';
export default function ErrorPage({reset}:{reset:()=>void}){return <main id="main" className="wrap page-intro"><h1>We couldn’t load this page.</h1><p>Please try again, or email Manaratalhudallc@gmail.com.</p><button className="button" onClick={reset}>Try again</button></main>}
