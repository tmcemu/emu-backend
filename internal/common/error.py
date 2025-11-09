class ErrTwoFaAlreadyEnabled(Exception):
    def __str__(self):
        return "TwoFA is already enabled for this account"


class ErrTwoFaCodeInvalid(Exception):
    def __str__(self):
        return "TwoFA code is invalid"


class ErrTwoFaNotEnabled(Exception):
    def __str__(self):
        return "TwoFA is not enabled"


class ErrUnauthorized(Exception):
    def __str__(self):
        return "Unauthorized"


class ErrForbidden(Exception):
    def __str__(self):
        return "Forbidden"


class ErrInvalidPassword(Exception):
    def __str__(self):
        return "Invalid password"


class ErrAccountCreate(Exception):
    def __str__(self):
        return "Unable to create account"


class ErrAccountNotFound(Exception):
    def __str__(self):
        return "Account not found"


class ErrAnalysisNotFound(Exception):
    def __str__(self):
        return "Analysis not found"


class ErrAnalysisInvalidStatus(Exception):
    def __str__(self):
        return "Invalid analysis status transition"


class ErrAnalysisUnauthorized(Exception):
    def __str__(self):
        return "Unauthorized to access this analysis"


class ErrFileUploadFailed(Exception):
    def __str__(self):
        return "Failed to upload file"
