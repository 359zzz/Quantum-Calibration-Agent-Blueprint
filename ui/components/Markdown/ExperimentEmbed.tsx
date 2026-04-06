'use client';

import React, { useEffect, useState } from 'react';
import { ExperimentDetails } from '@/components/Experiments/ExperimentDetails';
import { ExperimentResult } from '@/types/qcal';

interface ExperimentEmbedProps {
  'experiment-id': string;
}

export const ExperimentEmbed: React.FC<ExperimentEmbedProps> = (props) => {
  const experimentId = props['experiment-id'];
  const [experiment, setExperiment] = useState<ExperimentResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!experimentId) {
      setError('No experiment ID provided');
      setLoading(false);
      return;
    }

    const fetchExperiment = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(`/api/history/${experimentId}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch experiment: ${response.statusText}`);
        }

        const data = await response.json();
        if (data.error) {
          throw new Error(data.error);
        }

        setExperiment(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load experiment');
      } finally {
        setLoading(false);
      }
    };

    fetchExperiment();
  }, [experimentId]);

  return (
    <div className="my-4 border border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden max-w-full">
      <ExperimentDetails
        experiment={experiment}
        loading={loading}
        error={error || undefined}
        compact={true}
      />
    </div>
  );
};
