'use client';

import { useState } from 'react';
import { Lock, Key, AlertCircle } from 'lucide-react';
import { authAPI } from '@/utils/api';

interface AuthSectionProps {
  onAuthSuccess: () => void;
}

export default function AuthSection({ onAuthSuccess }: AuthSectionProps) {
  const [accessKey, setAccessKey] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!accessKey.trim()) return;

    setIsLoading(true);
    setError('');

    try {
      const response = await authAPI.login({ access_key: accessKey.trim() });
      localStorage.setItem('access_token', response.access_token);
      onAuthSuccess();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid access key. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mb-16">
      <div className="card max-w-md mx-auto shadow-xl">
        <div className="flex items-center justify-center mb-6">
          <Lock className="w-8 h-8 text-primary mr-3" />
          <h2 className="text-2xl font-bold text-black">Professional Access</h2>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6" style={{ padding: '10px' }}>
          <p className="text-black font-medium text-center">
            One-time analysis for $49.99 USD
          </p>
          <p className="text-gray-600 text-sm text-center mt-1">
            Key will be emailed immediately after payment.
          </p>
        </div>

        <a
          href={process.env.NEXT_PUBLIC_STRIPE_PAYMENT_LINK || "#"}
          target="_blank"
          rel="noopener noreferrer"
          className="btn-primary w-full text-center mb-6 block"
        >
          Don't have a key? Get one here 💳
        </a>

        <div className="border-t border-gray-200 pt-6">
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="accessKey" className="block text-sm font-medium text-black mb-2">
                Enter Access Key
              </label>
              <div className="relative">
                <input
                  type="password"
                  id="accessKey"
                  value={accessKey}
                  onChange={(e) => setAccessKey(e.target.value)}
                  placeholder="PASTE-KEY-HERE"
                  className="input-primary pl-10 w-full"
                  disabled={isLoading}
                />
              </div>
            </div>

            {error && (
              <div className="mb-6 p-4 ml-10 bg-red-50 border border-red-200 rounded-lg shadow-sm">
                <div className="flex items-center">
                  <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading || !accessKey.trim()}
              className="btn-primary w-full"
            >
              {isLoading ? 'Unlocking...' : 'Unlock Dashboard'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
