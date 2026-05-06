'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, Target, CheckCircle, FileText, Heart } from 'lucide-react';
import { pagesAPI } from '@/utils/api';

export default function AboutPage() {
  const [content, setContent] = useState<string>('');
  const [title, setTitle] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPageContent();
  }, []);

  const loadPageContent = async () => {
    try {
      const response = await pagesAPI.getPage('about');
      setTitle(response.title);
      setContent(response.content);
    } catch (err) {
      console.error('Failed to load page content:', err);
      // Fallback content
      setTitle('About LegaLens');
      setContent(`
#### Our Mission
LegaLens empowers renters and landlords with **AI-powered document analysis** to identify potential
compliance issues in rental agreements before signing.

#### What We Do
We review rental agreements for:
- Compliance with local housing regulations
- Missing mandatory clauses
- Unfair or risky terms
- Red flags and negotiation opportunities

#### Important Disclaimer
⚠️ **LegaLens is NOT a substitute for professional legal advice.**

Our service provides **document review only**. Always consult with a licensed attorney in your
jurisdiction before signing any legal document or making legal decisions.

#### How We Analyze Documents
- AI scans for jurisdiction-specific compliance issues
- Generates detailed reports with severity ratings
- Provides negotiation suggestions
- Includes confidence levels for all findings

#### Our Commitment
We believe renters deserve clarity and protection. Rental agreements can be complex,
and our goal is to help you understand potential risks before it's too late.

**Always seek professional legal advice for legal decisions.**
      `);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex justify-center items-center min-h-[400px]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-6">
        <Link
          href="/"
          className="inline-flex items-center text-gray-600 hover:text-primary transition-colors"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back Home
        </Link>
      </div>

      <div className="card">
        <div className="flex items-center mb-6">
          <Heart className="w-8 h-8 text-primary mr-3" />
          <h1 className="text-3xl font-bold text-black">ℹ️ {title}</h1>
        </div>

        <div className="space-y-6">
          {content.split('\n').map((line, index) => {
            if (line.startsWith('#### Our Mission')) {
              return (
                <div key={index}>
                  <h4 className="text-xl font-semibold text-black mb-3 flex items-center">
                    <Target className="w-5 h-5 text-primary mr-2" />
                    Our Mission
                  </h4>
                  <p className="text-gray-700 leading-relaxed">
                    {content.split('\n')[index + 1]}
                  </p>
                </div>
              );
            } else if (line.startsWith('#### What We Do')) {
              return (
                <div key={index}>
                  <h4 className="text-xl font-semibold text-black mb-3 flex items-center">
                    <CheckCircle className="w-5 h-5 text-primary mr-2" />
                    What We Do
                  </h4>
                  <p className="text-gray-700 mb-2">We review rental agreements for:</p>
                  <ul className="space-y-2 ml-7">
                    {content.split('\n').slice(index + 1, index + 5).map((item, i) => (
                      item.startsWith('-') && (
                        <li key={i} className="text-gray-700 flex items-start">
                          <span className="text-primary mr-2">•</span>
                          {item.replace('-', '').trim()}
                        </li>
                      )
                    ))}
                  </ul>
                </div>
              );
            } else if (line.startsWith('#### Important Disclaimer')) {
              return (
                <div key={index} className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <h4 className="text-xl font-semibold text-yellow-800 mb-3">⚠️ Important Disclaimer</h4>
                  <p className="text-yellow-800 font-medium mb-2">
                    {content.split('\n')[index + 1]}
                  </p>
                  <p className="text-gray-700">
                    {content.split('\n')[index + 2]}
                  </p>
                </div>
              );
            } else if (line.startsWith('#### How We Analyze Documents')) {
              return (
                <div key={index}>
                  <h4 className="text-xl font-semibold text-black mb-3 flex items-center">
                    <FileText className="w-5 h-5 text-primary mr-2" />
                    How We Analyze Documents
                  </h4>
                  <ul className="space-y-2 ml-7">
                    {content.split('\n').slice(index + 1, index + 5).map((item, i) => (
                      item.startsWith('-') && (
                        <li key={i} className="text-gray-700 flex items-start">
                          <span className="text-primary mr-2">•</span>
                          {item.replace('-', '').trim()}
                        </li>
                      )
                    ))}
                  </ul>
                </div>
              );
            } else if (line.startsWith('#### Our Commitment')) {
              return (
                <div key={index}>
                  <h4 className="text-xl font-semibold text-black mb-3">Our Commitment</h4>
                  <p className="text-gray-700 leading-relaxed mb-3">
                    {content.split('\n')[index + 1]}
                  </p>
                  <p className="text-gray-700 font-medium">
                    {content.split('\n')[index + 2]}
                  </p>
                </div>
              );
            }
            return null;
          })}
        </div>
      </div>
    </div>
  );
}
