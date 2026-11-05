-- Brand Gate Sample Data
-- Insert sample data for development and testing

-- Sample Users
INSERT INTO users (id, email, hashed_password, full_name, role, is_active) VALUES
    ('11111111-1111-1111-1111-111111111111', 'admin@brandgate.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', 'Brand Admin', 'brand_admin', TRUE),
    ('22222222-2222-2222-2222-222222222222', 'creator@brandgate.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', 'Content Creator', 'creator', TRUE),
    ('33333333-3333-3333-3333-333333333333', 'reviewer@brandgate.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', 'Content Reviewer', 'reviewer', TRUE),
    ('44444444-4444-4444-4444-444444444444', 'approver@brandgate.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', 'Content Approver', 'approver', TRUE)
ON CONFLICT (id) DO NOTHING;

-- Sample Brand Guidelines
INSERT INTO brand_guidelines (id, name, description, category, rule_text, rule_type, severity, is_active) VALUES
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'No Superlatives', 'Avoid using superlative claims without evidence', 'terminology', 'Do not use words like "best", "greatest", "ultimate", "perfect", "unbeatable" without supporting data', 'deterministic', 'high', TRUE),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Approved Product Names', 'Use only approved product names', 'terminology', 'Refer to products only by their approved names: "BrandGate Pro", "BrandGate Enterprise", "BrandGate Analytics"', 'deterministic', 'critical', TRUE),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Brand Tone - Professional', 'Maintain professional and trustworthy tone', 'tone', 'Content should be professional, clear, and trustworthy. Avoid overly casual language, slang, or emotional manipulation', 'llm_based', 'medium', TRUE),
    ('dddddddd-dddd-dddd-dddd-dddddddddddd', 'Primary Color Usage', 'Use only approved primary brand colors', 'visual', 'Primary colors: #1E3A8A (Navy), #3B82F6 (Blue), #FFFFFF (White). Do not modify hue, saturation, or brightness', 'deterministic', 'critical', TRUE),
    ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'Logo Clear Space', 'Maintain minimum clear space around logo', 'visual', 'Minimum clear space equal to the height of the "B" in BrandGate logo on all sides', 'deterministic', 'high', TRUE),
    ('ffffffff-ffff-ffff-ffff-ffffffffffff', 'Accessibility - Contrast', 'Ensure sufficient color contrast for accessibility', 'accessibility', 'All text must meet WCAG AA contrast ratios: 4.5:1 for normal text, 3:1 for large text', 'deterministic', 'high', TRUE),
    ('11111111-2222-3333-4444-555555555555', 'Claim Substantiation', 'All promotional claims must be backed by approved facts', 'claims', 'Any claim about product capabilities, performance, or market position must reference an approved fact from the ledger', 'hybrid', 'critical', TRUE),
    ('22222222-3333-4444-5555-666666666666', 'Readability', 'Content should be readable and accessible', 'readability', 'Target Flesch-Kincaid grade level of 8 or below for general audience content', 'deterministic', 'medium', TRUE)
ON CONFLICT (id) DO NOTHING;

-- Sample Approved Facts
INSERT INTO approved_facts (id, fact_text, fact_type, source_url, tags, is_active) VALUES
    ('aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 'BrandGate Pro processes up to 10,000 content items per hour', 'claim', 'https://docs.brandgate.com/performance', ARRAY['performance', 'pro'], TRUE),
    ('bbbbbbbb-cccc-dddd-eeee-ffffffffffff', 'BrandGate Enterprise supports 50+ concurrent users', 'claim', 'https://docs.brandgate.com/enterprise', ARRAY['enterprise', 'scalability'], TRUE),
    ('cccccccc-dddd-eeee-ffff-aaaaaaaaaaaa', 'Founded in 2024, headquartered in Bangalore, India', 'company_info', 'https://brandgate.com/about', ARRAY['company', 'history'], TRUE),
    ('dddddddd-eeee-ffff-aaaa-bbbbbbbbbbbb', 'ISO 27001 certified for information security', 'claim', 'https://brandgate.com/security', ARRAY['security', 'compliance'], TRUE),
    ('eeeeeeee-ffff-aaaa-bbbb-cccccccccccc', '99.9% uptime SLA for Enterprise tier', 'statistic', 'https://brandgate.com/sla', ARRAY['reliability', 'enterprise'], TRUE),
    ('ffffffff-aaaa-bbbb-cccc-dddddddddddd', 'Supports 15+ file formats including PDF, DOCX, PPTX, JPG, PNG', 'product_info', 'https://docs.brandgate.com/formats', ARRAY['formats', 'features'], TRUE)
ON CONFLICT (id) DO NOTHING;

-- Sample Brand Assets
INSERT INTO brand_assets (id, name, asset_type, file_path, file_hash, metadata, is_active) VALUES
    ('aaaaaaaa-1111-bbbb-2222-cccccccccccc', 'Primary Logo - Full Color', 'logo', '/assets/logos/brandgate-primary.svg', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', '{"colors": ["#1E3A8A", "#3B82F6"], "format": "SVG", "variants": ["full-color", "white", "monochrome"]}', TRUE),
    ('bbbbbbbb-2222-cccc-3333-dddddddddddd', 'Color Palette - Primary', 'color_palette', '/assets/colors/primary-palette.json', 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef12345678', '{"primary": "#1E3A8A", "secondary": "#3B82F6", "background": "#FFFFFF", "text": "#111827", "accent": "#F59E0B"}', TRUE),
    ('cccccccc-3333-dddd-4444-eeeeeeeeeeee', 'Typography - Inter Font', 'font', '/assets/fonts/inter/', 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890', '{"fontFamily": "Inter", "weights": [400, 500, 600, 700], "source": "Google Fonts"}', TRUE),
    ('dddddddd-4444-eeee-5555-ffffffffffff', 'Social Media Template', 'template', '/assets/templates/social-post.fig', 'd4e5f6789012345678901234567890abcdef1234567890abcdef123456789012', '{"format": "Figma", "dimensions": "1080x1080", "platforms": ["LinkedIn", "Twitter", "Instagram"]}', TRUE)
ON CONFLICT (id) DO NOTHING;

-- Sample Content Submissions
INSERT INTO content_submissions (id, title, content_type, original_content, status, creator_id, created_at) VALUES
    ('eeeeeeee-5555-ffff-6666-aaaaaaaaaaaa', 'Q4 Product Launch Announcement', 'text', 'We are excited to announce the launch of BrandGate Pro - the ultimate solution for brand governance! This best-in-class platform will revolutionize how you manage brand consistency.', 'pending', '22222222-2222-2222-2222-222222222222', CURRENT_TIMESTAMP),
    ('ffffffff-6666-aaaa-7777-bbbbbbbbbbbb', 'Social Media Post - Feature Highlight', 'mixed', 'Check out our new AI-powered brand checking! It''s perfect for teams of any size. #BrandGovernance #AI', 'reviewing', '22222222-2222-2222-2222-222222222222', CURRENT_TIMESTAMP),
    ('aaaaaaaa-7777-bbbb-8888-cccccccccccc', 'Enterprise Datasheet', 'document', '', 'approved', '22222222-2222-2222-2222-222222222222', CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

-- Sample Findings
INSERT INTO findings (id, content_submission_id, guideline_id, tier, finding_type, severity, title, description, evidence, location, suggested_correction, correction_reasoning, status) VALUES
    ('11111111-1111-2222-3333-444444444444', 'eeeeeeee-5555-ffff-6666-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 0, 'violation', 'high', 'Unsubstantiated Superlative: "ultimate"', 'The word "ultimate" is used without supporting evidence', '{"matched_word": "ultimate", "rule": "No Superlatives"}', '{"start_offset": 85, "end_offset": 93}', 'Remove "ultimate" or add supporting data', 'Superlative claims require evidence per brand guidelines', 'open'),
    ('22222222-2222-3333-4444-555555555555', 'eeeeeeee-5555-ffff-6666-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 0, 'violation', 'high', 'Unsubstantiated Superlative: "best-in-class"', 'The phrase "best-in-class" is used without supporting evidence', '{"matched_word": "best-in-class", "rule": "No Superlatives"}', '{"start_offset": 105, "end_offset": 118}', 'Replace with "leading" or add benchmark data', 'Superlative claims require evidence per brand guidelines', 'open'),
    ('33333333-3333-4444-5555-666666666666', 'ffffffff-6666-aaaa-7777-bbbbbbbbbbbb', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 0, 'violation', 'medium', 'Unsubstantiated Superlative: "perfect"', 'The word "perfect" is used without supporting evidence', '{"matched_word": "perfect", "rule": "No Superlatives"}', '{"start_offset": 52, "end_offset": 59}', 'Replace with "ideal" or "well-suited"', 'Superlative claims require evidence per brand guidelines', 'open'),
    ('44444444-4444-5555-6666-777777777777', 'eeeeeeee-5555-ffff-6666-aaaaaaaaaaaa', '11111111-2222-3333-4444-555555555555', 1, 'inconsistency', 'critical', 'Unverified Claim: Processing Speed', 'Claims "revolutionize how you manage brand consistency" without referencing approved performance facts', '{"claim": "revolutionize brand consistency management", "referenced_facts": []}', '{"start_offset": 120, "end_offset": 170}', 'Add reference to "BrandGate Pro processes up to 10,000 content items per hour"', 'All promotional claims must reference approved facts from the ledger', 'open')
ON CONFLICT (id) DO NOTHING;

-- Sample Reviews
INSERT INTO reviews (id, content_submission_id, reviewer_id, decision, comments, created_at) VALUES
    ('55555555-5555-6666-7777-888888888888', 'ffffffff-6666-aaaa-7777-bbbbbbbbbbbb', '33333333-3333-3333-3333-333333333333', 'request_changes', 'Please address the superlative violations before proceeding.', CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

-- Sample Approvals
INSERT INTO approvals (id, content_submission_id, approver_id, decision, comments, created_at) VALUES
    ('66666666-6666-7777-8888-999999999999', 'aaaaaaaa-7777-bbbb-8888-cccccccccccc', '44444444-4444-4444-4444-444444444444', 'approved', 'Enterprise datasheet meets all brand guidelines.', CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

-- Sample Audit Logs
INSERT INTO audit_logs (id, user_id, action, resource_type, resource_id, details, created_at) VALUES
    ('77777777-7777-8888-9999-aaaaaaaaaaaa', '22222222-2222-2222-2222-222222222222', 'create', 'content_submission', 'eeeeeeee-5555-ffff-6666-aaaaaaaaaaaa', '{"title": "Q4 Product Launch Announcement"}', CURRENT_TIMESTAMP),
    ('88888888-8888-9999-aaaa-bbbbbbbbbbbb', '33333333-3333-3333-3333-333333333333', 'review', 'content_submission', 'ffffffff-6666-aaaa-7777-bbbbbbbbbbbb', '{"decision": "request_changes"}', CURRENT_TIMESTAMP),
    ('99999999-9999-aaaa-bbbb-cccccccccccc', '44444444-4444-4444-4444-444444444444', 'approve', 'content_submission', 'aaaaaaaa-7777-bbbb-8888-cccccccccccc', '{"decision": "approved"}', CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;