def validate_file(my_file):

    MAX_FILENAME_LENGTH = 40
    MAX_FILESIZE_BYTES = 5243000
    VALID_CONTENT_TYPES = [
        "text/plain",
        "application/msword",
        "application/pdf", 
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.oasis.opendocument.text",
    ]

    is_valid = True

    if len(my_file.name) > MAX_FILENAME_LENGTH:
        is_valid = False
    if my_file.size > MAX_FILESIZE_BYTES:
        is_valid = False
    if my_file.content_type not in VALID_CONTENT_TYPES:
        is_valid = False

    return is_valid
