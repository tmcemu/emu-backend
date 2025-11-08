account_by_id = """
SELECT * FROM accounts
WHERE id = :account_id;
"""

account_by_refresh_token = """
SELECT * FROM accounts
WHERE refresh_token = :refresh_token;
"""

update_refresh_token = """
UPDATE accounts
SET refresh_token = :refresh_token
WHERE id = :account_id;
"""