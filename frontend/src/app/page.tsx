'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { FileText, Shield, CheckCircle, AlertTriangle, Scale } from 'lucide-react';
import AuthSection from '@/components/AuthSection';
import VideoDemo from '@/components/VideoDemo';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated]);

  const handleAuthSuccess = () => {
    setIsAuthenticated(true);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Hero Section Container wrapped perfectly */}
      <div className="flex flex-col items-center justify-center">
        <div className="w-full max-w-4xl flex flex-col items-center text-center gap-6 mb-12">
          {/* Title */}
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-foreground via-primary to-primary-dark bg-clip-text text-transparent">
            ⚖️ LegalLens
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl font-semibold text-foreground/80 max-w-2xl">
            AI-Powered Document Compliance Review
          </p>

          {/* Description Paragraph */}
          <p className="text-base md:text-lg text-accent max-w-3xl leading-relaxed mt-2">
            Legal agreements often contain non-compliant clauses that violate local statutes.
            <strong className="text-foreground font-semibold"> LegalLens</strong> performs automated compliance checks on rental agreements against current housing regulations.
          </p>

          {/* Disclaimer Box */}
          <div className="mt-8 p-5 mb-10 bg-red-50/60 border border-red-100 rounded-xl max-w-2xl w-full text-center shadow-sm backdrop-blur-sm">
            <p className="text-xs md:text-sm text-red-700 font-medium leading-relaxed" style={{ padding: '20px' }}>
              <span className="font-bold">⚠️ Important Disclaimer:</span> This is a document review automation assistant. Results generated do not constitute formal legal advice and must not replace professional legal consultation.
            </p>
          </div>
        </div>

        {/* How It Works */}
        <div className="mb-12 mt-2.5 w-full" style={{
    marginTop: '15px',
  }}
>
          <h2 className="text-3xl font-bold text-center mb-8 text-black">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="card text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🔑</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-black">1. Get Your Key</h3>
              <p className="text-gray-600">
                Purchase a key via Stripe. It is emailed to you instantly.
              </p>
            </div>
            <div className="card text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                <FileText className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-black">2. Secure Audit</h3>
              <p className="text-gray-600">
                Upload your PDF. AI scans for potential compliance issues based on 2026 regulations.
              </p>
            </div>
            <div className="card text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-black">3. Review Results</h3>
              <p className="text-gray-600">
                Download a detailed compliance report to review with your legal professional.
              </p>
            </div>
          </div>
        </div>

        {/* Video Demo */}
        <VideoDemo />

        {/* Authentication Section */}
        <AuthSection onAuthSuccess={handleAuthSuccess} />

        {/* Features */}
        <div className="mb-12 w-full">
          <h2 className="text-3xl font-bold text-center mb-8 text-black">Why Choose LegalLens?</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="card text-center hover:shadow-lg transition-shadow">
              <Shield className="w-12 h-12 text-primary mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2 text-black">Jurisdiction-Specific</h3>
              <p className="text-gray-600 text-sm">
                Analyzes agreements against specific local housing regulations
              </p>
            </div>
            <div className="card text-center hover:shadow-lg transition-shadow">
              <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2 text-black">Risk Assessment</h3>
              <p className="text-gray-600 text-sm">
                Identifies high-risk clauses and potential legal issues
              </p>
            </div>
            <div className="card text-center hover:shadow-lg transition-shadow">
              <Scale className="w-12 h-12 text-green-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2 text-black">Compliance Scoring</h3>
              <p className="text-gray-600 text-sm">
                Provides overall risk scores and severity ratings
              </p>
            </div>
            <div className="card text-center hover:shadow-lg transition-shadow">
              <FileText className="w-12 h-12 text-blue-500 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2 text-black">Professional Reports</h3>
              <p className="text-gray-600 text-sm">
                Generates detailed PDF reports for legal review
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center w-full">
          <div className="card max-w-2xl mx-auto hover:shadow-lg transition-shadow">
            <h2 className="text-2xl font-bold mb-4 text-black">Ready to Secure Your Rental Agreement?</h2>
            <p className="text-gray-600 mb-6">
              Get professional AI-powered lease analysis for only $49.99 USD
            </p>
            <a
              href={process.env.NEXT_PUBLIC_STRIPE_PAYMENT_LINK || "#"}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary inline-block"
            >
              Get Your Access Key 💳
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}