-- Run once in the SQL editor of the dedicated personal Supabase project.
CREATE TABLE IF NOT EXISTS public.practice_review_events (
    event_id uuid PRIMARY KEY,
    collection_id text NOT NULL,
    exercise_id text NOT NULL,
    review_datetime timestamptz NOT NULL,
    final_rating text NOT NULL CHECK (final_rating IN ('fail', 'acceptable', 'good', 'excellent')),
    compiled boolean NOT NULL,
    proposed_rating text CHECK (proposed_rating IS NULL OR proposed_rating IN ('fail', 'acceptable', 'good', 'excellent')),
    review_status text NOT NULL,
    reviewer_name text,
    reviewer_model text,
    reviewer_reasoning_effort text,
    review_attempts integer NOT NULL DEFAULT 0 CHECK (review_attempts >= 0),
    solve_duration_ms bigint CHECK (solve_duration_ms >= 0),
    feedback_duration_ms bigint CHECK (feedback_duration_ms >= 0),
    CHECK ((solve_duration_ms IS NULL) = (feedback_duration_ms IS NULL))
);

CREATE INDEX IF NOT EXISTS practice_review_events_collection_time_idx
    ON public.practice_review_events (collection_id, review_datetime, event_id);

ALTER TABLE public.practice_review_events ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.practice_review_events FROM anon, authenticated;
GRANT SELECT, INSERT ON public.practice_review_events TO service_role;

-- The client uses INSERT ... ON CONFLICT DO NOTHING. Updates and deletes are
-- intentionally not granted: synchronized history is an append-only ledger.
