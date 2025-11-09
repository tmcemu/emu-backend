create_analysis = """
INSERT INTO analyses (
    nurse_id,
    analysis_type,
    study_file_fid,
    study_file_original_name,
    activity_diary_image_fid,
    activity_diary_original_name,
    status,
    conclusion_file_fid,
    conclusion_file_original_name,
    rejection_comment,
    doctor_id,
    started_at,
    finished_at,
    created_at,
    updated_at
)
VALUES (
    :nurse_id,
    :analysis_type,
    :study_file_fid,
    :study_file_original_name,
    :activity_diary_image_fid,
    :activity_diary_original_name,
    'pending',
    '',
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
    conclusion_file_original_name = :conclusion_file_original_name,
    finished_at = CURRENT_TIMESTAMP,
    status = 'completed',
    updated_at = CURRENT_TIMESTAMP
WHERE id = :analysis_id;
"""
