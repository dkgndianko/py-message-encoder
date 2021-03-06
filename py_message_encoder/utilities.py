def left_pad(value: str, target_length: int, pad_char: str) -> str:
    diff = target_length - len(value)
    return f"{pad_char * diff}{value}"


def right_pad(value: str, target_length: int, pad_char: str):
    diff = target_length - len(value)
    return f"{value}{pad_char * diff}"


class CustomIntegerBaseMixin:
    def __init__(self, alphabet: str):
        self.alphabet = alphabet
        self.alphabet_len = len(alphabet)

    def encode(self, number: int) -> str:
        assert number >= 0, "Number should be positive"
        if number == 0:
            return self.zero
        result = ""
        while number != 0:
            number, q = divmod(number, self.alphabet_len)
            result = self.alphabet[q] + result
        return result

    def decode(self, encoded: str) -> int:
        if encoded == "":
            return 0
        result = 0
        for c in encoded:
            index = self.alphabet.index(c)
            if index == -1:
                raise ValueError(f"invalid character {c}")
            result = result * self.alphabet_len + index
        return result

    def max_encodable_with_len(self, target_len: int) -> int:
        return self.decode(self.one * target_len)

    def __call__(self, number):
        return self.encode(number)

    @property
    def zero(self):
        return self.alphabet[0]

    @property
    def one(self):
        return self.alphabet[-1]


class CustomIntegerBase(CustomIntegerBaseMixin):
    def encode(self, number: int) -> str:
        is_negative = False
        if number < 0:
            is_negative = True
            number *= -1
        if number == 0:
            return self.zero
        result = super(CustomIntegerBase, self).encode(number)
        if is_negative:
            result = self.one + result
        elif result[0] == self.one:
            result = self.zero + result
        return result

    def decode(self, encoded: str) -> int:
        if encoded == "":
            return 0
        is_negative = False
        if encoded[0] == self.one:
            is_negative = True
            encoded = encoded[1:]
        result = super(CustomIntegerBase, self).decode(encoded)
        if is_negative:
            result *= -1
        return result

    def max_encodable_with_len(self, target_len: int) -> int:
        return self.decode(self.alphabet[-2] + self.one * (target_len - 1))


class CustomUnsignedIntegerBase(CustomIntegerBaseMixin):
    pass


custom_alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{};'\"\\/.,?><"
# custom_alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
custom_base_64 = CustomIntegerBase(custom_alpha)
custom_binary = CustomIntegerBase("01")
custom_unsigned_base_64 = CustomUnsignedIntegerBase(custom_alpha)
