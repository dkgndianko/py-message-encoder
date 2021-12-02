def left_pad(value: str, target_length: int, pad_char: str) -> str:
    diff = target_length - len(value)
    return f"{pad_char * diff}{value}"


def right_pad(value: str, target_length: int, pad_char: str):
    diff = target_length - len(value)
    return f"{value}{pad_char * diff}"


class CustomIntegerBase:
    def __init__(self, alphabet: str):
        self.alphabet = alphabet
        self.alphabet_len = len(alphabet)

    def encode(self, number: int) -> str:
        if number == 0:
            return "0"
        result = ""
        while number != 0:
            number, q = divmod(number, self.alphabet_len)
            result = self.alphabet[q] + result
        return result

    def decode(self, encoded: str) -> int:
        result = 0
        for c in encoded:
            index = self.alphabet.index(c)
            if index == -1:
                raise ValueError(f"invalid character {c}")
            result = result * self.alphabet_len + index
        return result

    def __call__(self, number):
        return self.encode(number)

    @property
    def zero(self):
        return self.alphabet[0]

    @property
    def one(self):
        return self.alphabet[self.alphabet_len - 1]


custom_alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{};'\"\\/.,?><"
# custom_alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
custom_base_64 = CustomIntegerBase(custom_alpha)
