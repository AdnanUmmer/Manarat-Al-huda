import type {Metadata} from 'next';
import './globals.css';
import '@fontsource/manrope/400.css';
import '@fontsource/manrope/500.css';
import '@fontsource/manrope/600.css';
import '@fontsource/manrope/700.css';
export const metadata:Metadata={metadataBase:new URL(process.env.SITE_URL||'http://localhost:3000'),title:{default:'Manarat Al Huda | Wholesale Trading, Dubai',template:'%s | Manarat Al Huda'},description:'Dubai-based wholesale supply of beverages and everyday consumer goods to trading businesses across the UAE.',openGraph:{type:'website',locale:'en_AE',siteName:'Manarat Al Huda'}};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body><a className="skip-link" href="#main">Skip to content</a>{children}</body></html>}
