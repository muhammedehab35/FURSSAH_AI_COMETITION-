// File: pages/index.tsx
import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

export default function TrafficAnalyzer() {
  const [features, setFeatures] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ features })
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error('Error:', err);
      alert('Failed to analyze traffic.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-center">Cyber Traffic Analyzer</h1>
      <Textarea
        rows={10}
        placeholder="Paste your flow features here..."
        value={features}
        onChange={(e) => setFeatures(e.target.value)}
      />
      <Button onClick={handleAnalyze} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze Traffic'}
      </Button>

      {result && (
        <Card className="mt-6">
          <CardContent className="space-y-2">
            <h2 className="text-xl font-semibold">Analysis Result</h2>
            <pre className="bg-gray-100 p-4 rounded text-sm overflow-x-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}
    </div>
  );
}