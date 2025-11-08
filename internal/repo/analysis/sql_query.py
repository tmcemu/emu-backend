create_analysis = """
INSERT INTO analyses (
    patient_full_name,
    nurse_id,
    analysis_type,
    study_file_fid,
    activity_diary_image_fid,
    status,
    conclusion_file_fid,
    rejection_comment,
    doctor_id,
    started_at,
    finished_at,
    created_at,
    updated_at
)
VALUES (
    :patient_full_name,
    :nurse_id,
    :analysis_type,
    :study_file_fid,
    :activity_diary_image_fid,
    'pending',
    '',
    '',
    0,
    NULL,
    NULL,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
)
RETURNING id;
"""

get_analysis_by_id = """
SELECT * FROM analyses
WHERE id = :analysis_id;
"""

get_all_analyses = """
SELECT * FROM analyses
ORDER BY created_at DESC;
"""

get_analyses_by_nurse = """
SELECT * FROM analyses
WHERE nurse_id = :nurse_id
ORDER BY created_at DESC;
"""

set_doctor_and_start = """
UPDATE analyses
SET doctor_id = :doctor_id,
    started_at = CURRENT_TIMESTAMP,
    status = 'in_work',
    updated_at = CURRENT_TIMESTAMP
WHERE id = :analysis_id;
"""

set_rejection = """
UPDATE analyses
SET status = 'rejected',
    rejection_comment = :rejection_comment,
    finished_at = CURRENT_TIMESTAMP,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :analysis_id;
"""

set_conclusion = """
UPDATE analyses
SET conclusion_file_fid = :conclusion_file_fid,
    finished_at = CURRENT_TIMESTAMP,
    status = 'completed',
    updated_at = CURRENT_TIMESTAMP
WHERE id = :analysis_id;
"""
