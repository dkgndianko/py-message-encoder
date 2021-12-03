class MessageHeader:

    def __init__(self, number_of_parts):
        self.number_of_parts = number_of_parts
        self.state = [False for _ in range(number_of_parts)]

    def set_presence(self, index: int, present: bool = True):
        assert 0 <= index < self.number_of_parts, f"wrong index {index}"
        self.state[index] = present
        return self

    def is_present(self, index: int):
        assert 0 <= index < self.number_of_parts, f"wrong index {index}"
        return self.state[index]

    def dump(self) -> str:
        return "".join(["1" if x else "0" for x in self.state])

    @classmethod
    def parse(cls, value: str):
        mh = MessageHeader(len(value))
        for i, c in enumerate(value):
            if c not in ["0", "1"]:
                raise ValueError(f"Invalid character {c}")
            mh.set_presence(i, c == "1")
        return mh

    def __str__(self):
        return self.dump()
