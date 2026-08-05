-- Run in the SQL editor when creating or upgrading the dedicated Supabase project.
CREATE TABLE IF NOT EXISTS public.practice_review_events (
    event_id uuid PRIMARY KEY,
    sync_sequence bigint GENERATED ALWAYS AS IDENTITY,
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

-- Upgrade tables created by an older version. Adding an identity column assigns
-- every existing event a sequence before future inserts receive higher values.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'practice_review_events'
          AND column_name = 'sync_sequence'
    ) THEN
        ALTER TABLE public.practice_review_events
            ADD COLUMN sync_sequence bigint GENERATED ALWAYS AS IDENTITY;
    END IF;
END
$$;

CREATE UNIQUE INDEX IF NOT EXISTS practice_review_events_sync_sequence_idx
    ON public.practice_review_events (sync_sequence);

CREATE INDEX IF NOT EXISTS practice_review_events_collection_sequence_idx
    ON public.practice_review_events (collection_id, sync_sequence);

ALTER TABLE public.practice_review_events ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.practice_review_events FROM anon, authenticated;
GRANT SELECT, INSERT ON public.practice_review_events TO service_role;

DO $$
DECLARE
    sequence_name text;
BEGIN
    sequence_name := pg_get_serial_sequence(
        'public.practice_review_events', 'sync_sequence'
    );
    EXECUTE format(
        'GRANT USAGE, SELECT ON SEQUENCE %s TO service_role', sequence_name
    );
END
$$;

-- The client uses INSERT ... ON CONFLICT DO NOTHING. Updates and deletes are
-- intentionally not granted: synchronized history is an append-only ledger.
