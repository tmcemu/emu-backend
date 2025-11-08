create_account = """
INSERT INTO accounts (
    login,
    password,
    account_type
)
VALUES (
    :login,
    :password,
    :account_type
)
RETURNING id;
"""

get_account_by_id = """
SELECT * FROM accounts
WHERE id = :account_id;
"""

get_account_by_login = """
SELECT * FROM accounts
WHERE login = :login;
"""

update_password = """
UPDATE accounts
SET password = :new_password
WHERE id = :account_id;
"""
