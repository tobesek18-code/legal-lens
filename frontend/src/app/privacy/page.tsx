'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, Shield, Database, Eye, Trash } from 'lucide-react';
import { pagesAPI } from '@/utils/api';

export default function PrivacyPage() {
  const [content, setContent] = useState<string>('');
  const [title, setTitle] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPageContent();
  }, []);

  const loadPageContent = async () => {
    try {
      const response = await pagesAPI.getPage('privacy');
      setTitle(response.title);
      setContent(response.content);
    } catch (err) {
      console.error('Failed to load page content:', err);
      // Fallback content
      setTitle('Privacy Policy');
      setContent(`
#### Data Collection
LegaLens collects:
- PDF documents you upload for analysis
- User email and access key information
- Usage analytics (non-personally identifiable)

#### Data Usage
- Documents are used solely for AI analysis
- Data is NOT stored permanently after analysis
- We do NOT share your data with third parties
- All data transmission is encrypted (HTTPS)

#### Data Retention
- Analysis results are deleted within 30 days
- Metadata may be retained for service improvement
- You can request data deletion at any time

#### Security
We implement industry-standard security measures to protect your information.

#### Your Rights
You have the right to:
- Access what data we hold about you
- Request deletion of your data
- Opt-out of analytics
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
          <Shield className="w-8 h-8 text-primary mr-3" />
          <h1 className="text-3xl font-bold text-black">🔒 {title}</h1>
        </div>

        <div className="space-y-6">
          {content.split('\n').map((line, index) => {
            if (line.startsWith('#### Data Collection')) {
              return (
                <div key={index}>
                  <h4 className="text-xl font-semibold text-black mb-3 flex items-center">
                    <Database className="w-5 h-5 text-primary mr-2" />
                    Data Collection
                  </h4>
                  <ul className="space-y-2 ml-7">
                    {content.split('\n').slice(index + 1, index + 4).map((item, i) => (
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
            } else if (line.startsWith('#### Data Usage')) {
              return (
                <div key={index}>
                  <h4 className="text-xl font-semibold text-black mb-3 flex items-center">
                    <Eye className="w-5 h-5 text-primary mr-2" />
                    Data Usage
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
            } else if (line.startsWith('#### Data Retention')) {
              return (
                <div key={index}>
                  <h4 className="text-xl font-semibold text-black mb-3">Data Retention</h4>
                  <ul className="space-y-2 ml-7">
                    {content.split('\n').slice(index + 1, index + 4).map((item, i) => (
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
            } else if (line.startsWith('#### Security')) {
              return (
                <div key={index}>
                  <h4 className="text-xl font-semibold text-black mb-3">Security</h4>
                  <p className="text-gray-700 ml-7">
                    {content.split('\n')[index + 1]}
                  </p>
                </div>
              );
            } else if (line.startsWith('#### Your Rights')) {
              return (
                <div key={index}>
                  <h4 className="text-xl font-semibold text-black mb-3 flex items-center">
                    <Trash className="w-5 h-5 text-primary mr-2" />
                    Your Rights
                  </h4>
                  <p className="text-gray-700 mb-2">You have the right to:</p>
                  <ul className="space-y-2 ml-7">
                    {content.split('\n').slice(index + 1).map((item, i) => (
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
            }
            return null;
          })}
        </div>
      </div>
    </div>
  );
}
