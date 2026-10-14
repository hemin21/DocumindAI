export interface SearchResultItem {
  rank: number;
  doc_id: string;
  score: number;
  title: string;
  snippet: string;
  metadata?: Record<string, any>;
  tfidf_raw?: number;
  semantic_raw?: number;
}

export interface SearchResponse {
  query: string;
  model: string;
  top_k: number;
  latency_ms: number;
  total_results: number;
  direct_answer?: string | null;
  results: SearchResultItem[];
}

export interface CustomDocumentItem {
  id: string;
  filename: string;
  page_count: number;
  total_chunks: number;
  uploaded_at: string;
}

export interface ModelInfo {
  id: string;
  name: string;
  type: string;
  description: string;
}

export interface DatasetInfo {
  dataset_name: string;
  benchmark: string;
  source_url: string;
  domain: string;
  corpus_statistics: {
    total_documents: number;
    empty_documents: number;
    avg_document_word_length: number;
    max_document_word_length: number;
    min_document_word_length: number;
    sample_document_ids: string[];
  };
  query_statistics: {
    total_queries: number;
    avg_query_word_length: number;
    max_query_word_length: number;
    min_query_word_length: number;
    sample_queries: [string, string][];
  };
  relevance_splits: Record<string, any>;
  relevance_grades_legend: Record<string, string>;
  license: string;
  reference: string;
}

export interface EvaluationSummaryItem {
  Model: string;
  "Precision@5": number;
  "Recall@5": number;
  "F1@5": number;
  MRR: number;
  "nDCG@10": number;
  "Mean Latency (ms)": number;
  "Median Latency (ms)": number;
  "P95 Latency (ms)": number;
  "Evaluated Queries": number;
  "Indexed Documents": number;
}

export interface ErrorCase {
  query_id: string;
  query_text: string;
  error_category: string;
  relevant_doc_count: number;
  tfidf_top_5: string;
  semantic_top_5: string;
  explanation: string;
}
