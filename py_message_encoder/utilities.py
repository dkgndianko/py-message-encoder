def left_pad(value: str, target_length: int, pad_char: str) -> str:
    diff = target_length - len(value)
    return f"{pad_char * diff}{value}"


def right_pad(value: str, target_length: int, pad_char: str):
    diff = target_length - len(value)
    return f"{value}{pad_char * diff}"
