'use client';

import { useState, useEffect } from 'react';
import { ModelStats, getModelStats } from '@/lib/model-stats';

/**
 * React hook to fetch and manage model statistics
 */
export function useModelStats() {
  const [stats, setStats] = useState<ModelStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function loadStats() {
      try {
        setLoading(true);
        const data = await getModelStats();
        setStats(data);
        setError(null);
      } catch (err) {
        setError(err as Error);
        // Still use fallback stats even on error
        setStats({
          accuracy: 0.52,
          roc_auc: 0.5126,
          matches_count: 12834,
          timestamp: new Date().toISOString()
        });
      } finally {
        setLoading(false);
      }
    }

    loadStats();
  }, []);

  return { stats, loading, error };
}
