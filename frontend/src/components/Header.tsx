'use client';

import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/navigation';

export default function Header() {
  const router = useRouter();

  const handleLogoClick = () => {
    router.push('/');
  };

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-logo" onClick={handleLogoClick}>
          <Image
            src="/logo.png"
            alt="LegaLens Logo"
            width={40}
            height={40}
            className="cursor-pointer"
          />
          <span className="header-title">LegaLens</span>
        </div>
        <nav className="header-nav">
          <Link href="/terms">Terms</Link>
          <Link href="/contact">Contact</Link>
          <Link href="/privacy">Privacy</Link>
          <Link href="/about">About</Link>
          <span className="text-accent text-sm">AI-Powered Document Compliance Review</span>
        </nav>
      </div>
    </header>
  );
}
