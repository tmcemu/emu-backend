create_account_table = """
CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    
    login TEXT NOT NULL,
    password TEXT NOT NULL,
    refresh_token TEXT DEFAULT '',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

drop_account_table = """
DROP TABLE IF EXISTS accounts CASCADE;
"""


create_analyses_table = """
CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,

    nurse_id INTEGER,
    doctor_id INTEGER,
    
    analysis_type TEXT NOT NULL,
    study_file_fid TEXT NOT NULL,
    activity_diary_image_fid TEXT DEFAULT '',
    status TEXT NOT NULL,
    conclusion_file_fid TEXT DEFAULT '',
    rejection_comment TEXT DEFAULT '',
    patient_full_name TEXT NOT NULL,

    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

drop_analyses_table = """
DROP TABLE IF EXISTS analyses CASCADE;
"""


create_tables_queries = [
    create_account_table,
    create_analyses_table,
]

drop_queries = [
    drop_account_table,
    drop_analyses_table,
]
