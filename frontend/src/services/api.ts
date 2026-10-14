import type {
  SearchResponse,
  DatasetInfo,
  ModelInfo,
  EvaluationSummaryItem,
  ErrorCase,
  CustomDocumentItem
} from '../types';

export const api = {
  async getHealth() {
    const res = await fetch('/api/health');
    return res.json();
  },

  async getDatasetInfo(): Promise<DatasetInfo> {
    const res = await fetch('/api/dataset/info');
    if (!res.ok) throw new Error('Failed to fetch dataset info');
    return res.json();
  },

  async getModels(): Promise<{ models: ModelInfo[] }> {
    const res = await fetch('/api/models');
    if (!res.ok) throw new Error('Failed to fetch models');
    return res.json();
  },

  async search(query: string, model: string = 'semantic', top_k: number = 10): Promise<SearchResponse> {
    const res = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, model, top_k })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Search failed');
    }
    return res.json();
  },

  async getDocument(docId: string) {
    const res = await fetch(`/api/documents/${docId}`);
    if (!res.ok) throw new Error('Failed to fetch document');
    return res.json();
  },

  async getEvaluationSummary(): Promise<EvaluationSummaryItem[]> {
    const res = await fetch('/api/evaluation/summary');
    if (!res.ok) throw new Error('Failed to fetch evaluation summary');
    return res.json();
  },

  async getEvaluationErrors(): Promise<ErrorCase[]> {
    const res = await fetch('/api/evaluation/errors?limit=50');
    if (!res.ok) throw new Error('Failed to fetch evaluation errors');
    return res.json();
  },

  async getHistory() {
    const res = await fetch('/api/history');
    return res.json();
  },

  async uploadPdf(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch('/api/custom/upload', {
      method: 'POST',
      body: formData
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Failed to upload PDF');
    }
    return res.json();
  },

  async getCustomDocuments(): Promise<CustomDocumentItem[]> {
    const res = await fetch('/api/custom/documents');
    if (!res.ok) throw new Error('Failed to fetch custom documents');
    return res.json();
  },

  async deleteCustomDocument(docId: string) {
    const res = await fetch(`/api/custom/documents/${docId}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error('Failed to delete document');
    return res.json();
  }
};
