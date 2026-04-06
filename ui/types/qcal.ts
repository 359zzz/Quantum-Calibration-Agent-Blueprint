/**
 * TypeScript types for qcal backend integration.
 */

export interface ParameterSpec {
  name: string;
  type: 'int' | 'float' | 'str' | 'bool' | 'list';
  default?: unknown;
  range?: [number, number];
  required: boolean;
}

export interface ExperimentSchema {
  name: string;
  description: string;
  parameters: ParameterSpec[];
  module_path: string;
}

export interface ExperimentResult {
  id: string;
  type: string;
  timestamp: string;
  status: 'success' | 'failed';
  target?: string;
  params: Record<string, unknown>;
  results: Record<string, unknown>;
  arrays: Record<string, number[]>;
  plots: PlotData[];
  notes: string;
  file_path: string;
}

export interface PlotData {
  name: string;
  format: 'plotly' | 'png' | 'base64';
  data: unknown;
}

export interface ExperimentListItem {
  id: string;
  type: string;
  target?: string;
  timestamp: string;
  status: 'success' | 'failed';
}

export interface ArrayInfo {
  name: string;
  shape: number[];
  dtype: string;
}

export interface ArrayStats {
  min: number;
  max: number;
  mean: number;
  std: number;
  count: number;
}
