-- AutoStory Builder Database Schema
-- Run this in your Supabase SQL editor to set up the database

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Stories table
CREATE TABLE IF NOT EXISTS stories (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content JSONB NOT NULL,
    tone TEXT NOT NULL,
    images TEXT[] DEFAULT '{}',
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    version INTEGER DEFAULT 1,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Story versions table for version control
CREATE TABLE IF NOT EXISTS story_versions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    story_id UUID REFERENCES stories(id) ON DELETE CASCADE,
    content JSONB NOT NULL,
    version_number INTEGER NOT NULL,
    version_notes TEXT DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_stories_user_id ON stories(user_id);
CREATE INDEX IF NOT EXISTS idx_stories_created_at ON stories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_stories_tone ON stories(tone);
CREATE INDEX IF NOT EXISTS idx_stories_status ON stories(status);
CREATE INDEX IF NOT EXISTS idx_story_versions_story_id ON story_versions(story_id);
CREATE INDEX IF NOT EXISTS idx_story_versions_version_number ON story_versions(version_number DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for stories table
DROP TRIGGER IF EXISTS update_stories_updated_at ON stories;
CREATE TRIGGER update_stories_updated_at
    BEFORE UPDATE ON stories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create storage bucket for images
INSERT INTO storage.buckets (id, name, public) 
VALUES ('story-images', 'story-images', true)
ON CONFLICT (id) DO NOTHING;

-- Set up Row Level Security (RLS)
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;
ALTER TABLE story_versions ENABLE ROW LEVEL SECURITY;

-- Create policies for stories table
CREATE POLICY "Users can view their own stories" ON stories
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert their own stories" ON stories
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update their own stories" ON stories
    FOR UPDATE USING (auth.uid()::text = user_id);

CREATE POLICY "Users can delete their own stories" ON stories
    FOR DELETE USING (auth.uid()::text = user_id);

-- Create policies for story_versions table
CREATE POLICY "Users can view versions of their own stories" ON story_versions
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM stories 
            WHERE stories.id = story_versions.story_id 
            AND stories.user_id = auth.uid()::text
        )
    );

CREATE POLICY "Users can insert versions of their own stories" ON story_versions
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM stories 
            WHERE stories.id = story_versions.story_id 
            AND stories.user_id = auth.uid()::text
        )
    );

-- Create storage policies
CREATE POLICY "Users can upload their own images" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'story-images' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can view their own images" ON storage.objects
    FOR SELECT USING (bucket_id = 'story-images' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can delete their own images" ON storage.objects
    FOR DELETE USING (bucket_id = 'story-images' AND auth.uid()::text = (storage.foldername(name))[1]);

-- Insert sample data (optional)
-- Uncomment the following lines to add sample stories for testing

/*
INSERT INTO stories (user_id, title, content, tone, status) VALUES 
(
    'demo_user',
    'The Power of Innovation',
    '{
        "title": "The Power of Innovation",
        "hook": "In a world where change is the only constant, innovation becomes our compass.",
        "body": ["Every breakthrough starts with a simple question: What if we could do this better?", "Innovation is not just about technology; it''s about reimagining possibilities and creating solutions that matter.", "The most successful organizations are those that embrace change and turn challenges into opportunities."],
        "call_to_action": "What innovation will you create today? Share your ideas and let''s build the future together.",
        "full_text": "In a world where change is the only constant, innovation becomes our compass. Every breakthrough starts with a simple question: What if we could do this better? Innovation is not just about technology; it''s about reimagining possibilities and creating solutions that matter. The most successful organizations are those that embrace change and turn challenges into opportunities. What innovation will you create today? Share your ideas and let''s build the future together."
    }',
    'inspirational',
    'published'
),
(
    'demo_user',
    'Understanding Machine Learning',
    '{
        "title": "Understanding Machine Learning",
        "hook": "Machine learning is transforming how we solve complex problems across industries.",
        "body": ["At its core, machine learning is about pattern recognition and prediction.", "Algorithms learn from data to make decisions without being explicitly programmed for every scenario.", "From recommendation systems to autonomous vehicles, ML applications are everywhere around us."],
        "call_to_action": "Ready to dive deeper into machine learning? Explore our comprehensive courses and start your AI journey.",
        "full_text": "Machine learning is transforming how we solve complex problems across industries. At its core, machine learning is about pattern recognition and prediction. Algorithms learn from data to make decisions without being explicitly programmed for every scenario. From recommendation systems to autonomous vehicles, ML applications are everywhere around us. Ready to dive deeper into machine learning? Explore our comprehensive courses and start your AI journey."
    }',
    'educational',
    'published'
);
*/