-- ===============================
-- Supabase schema for MIL project
-- ===============================

-- Table: analyzed_pages
-- Stores each page/article the extension sends to the API
CREATE TABLE IF NOT EXISTS analyzed_pages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url TEXT NOT NULL,
    content TEXT NOT NULL,
    credibility_score FLOAT CHECK (credibility_score >= 0 AND credibility_score <= 1),
    tips TEXT, -- JSON or plain text with MIL education tips
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: user_feedback
-- Stores feedback from browser extension users
CREATE TABLE IF NOT EXISTS user_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    page_id UUID REFERENCES analyzed_pages(id) ON DELETE CASCADE,
    was_helpful BOOLEAN,
    forwarded_to_bot BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: bot_interactions
-- Stores queries from Telegram/Discord bot users
CREATE TABLE IF NOT EXISTS bot_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform TEXT CHECK (platform IN ('telegram', 'discord')),
    user_id TEXT NOT NULL, -- platform-specific user ID
    query TEXT NOT NULL,
    response TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ===============================
-- Indexes for faster lookups
-- ===============================
CREATE INDEX IF NOT EXISTS idx_analyzed_pages_url ON analyzed_pages(url);
CREATE INDEX IF NOT EXISTS idx_user_feedback_page_id ON user_feedback(page_id);
CREATE INDEX IF NOT EXISTS idx_bot_interactions_platform ON bot_interactions(platform);
