import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-links">
          <Link href="/terms">Terms & Conditions</Link>
          <Link href="/contact">Contact</Link>
          <Link href="/privacy">Privacy Policy</Link>
          <Link href="/about">About</Link>
        </div>
        <div className="footer-copyright">
          © 2026 LegaLens. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
