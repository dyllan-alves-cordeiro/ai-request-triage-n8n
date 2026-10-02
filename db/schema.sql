-- Synthetic Vértice IA lab schema. Never connect this database to Digytron production.
CREATE TABLE IF NOT EXISTS knowledge_base (
  id VARCHAR(40) PRIMARY KEY,
  kind VARCHAR(40) NOT NULL,
  intent VARCHAR(48) NOT NULL,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  keywords TEXT[] NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lab_customers (
  customer_id VARCHAR(96) PRIMARY KEY,
  customer_tier VARCHAR(32) NOT NULL,
  customer_name VARCHAR(120) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS triage_requests (
  request_id VARCHAR(96) PRIMARY KEY,
  customer_id VARCHAR(96) NOT NULL,
  customer_tier VARCHAR(32) NOT NULL DEFAULT 'prospect',
  inquiry_text TEXT NOT NULL,
  classification VARCHAR(48) NOT NULL,
  confidence NUMERIC(4,3) NOT NULL,
  status VARCHAR(40) NOT NULL,
  proposed_response TEXT NOT NULL,
  source_ids TEXT[] NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS approval_tokens (
  token VARCHAR(96) PRIMARY KEY,
  request_id VARCHAR(96) NOT NULL REFERENCES triage_requests(request_id) ON DELETE CASCADE,
  status VARCHAR(16) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING','USED')),
  decision VARCHAR(16) CHECK (decision IN ('APPROVED','REJECTED')),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  used_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS execution_audits (
  id BIGSERIAL PRIMARY KEY,
  request_id VARCHAR(96) NOT NULL,
  workflow_version VARCHAR(32) NOT NULL,
  prompt_version VARCHAR(32) NOT NULL,
  status VARCHAR(40) NOT NULL,
  fallback_reason VARCHAR(64),
  sources_used TEXT[] NOT NULL DEFAULT '{}',
  duration_ms INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS execution_errors (
  id BIGSERIAL PRIMARY KEY,
  workflow_id VARCHAR(64),
  execution_id VARCHAR(64),
  error_message TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_triage_requests_status ON triage_requests(status);
CREATE INDEX IF NOT EXISTS idx_approval_tokens_request ON approval_tokens(request_id);
CREATE INDEX IF NOT EXISTS idx_execution_audits_request ON execution_audits(request_id);

-- Retry-safe seeding: the JSON source of truth is imported by a bounded admin step.
