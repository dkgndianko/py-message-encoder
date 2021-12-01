from typing import List, Tuple, Any

from py_message_encoder.encoders import PartialEncoder
from .encoders.boolean_encoder import BooleanEncoder
from .encoders.string_encoders import FixedLengthEncoder, LVAR, LLVAR, LLLVAR


def test():
    test_cases: List[Tuple[PartialEncoder, List[Any]]] = [
        (BooleanEncoder(), [True, False, 0, 1, 2, 3, -1, "str", "", [1, 2], []]),
        (FixedLengthEncoder(10), ["", "Hi @team", "This is a very long tutorial"]),
        (LVAR, ["Hi", "Hi team", "This is a very long text"]),
        (LLVAR, ["Hi", "Hi team", "This is a very long text", "This is a very long text" * 7]),
        (LLLVAR, ["Hi", "Hi team", "This is a very long text", "a long text" * 7, "This is a very long text" * 13]),
    ]
    for encoder, cases in test_cases:
        print(f"\n-------------------------Testing {str(encoder)} ... -----------------------------\n")
        for case in cases:
            try:
                encoded = encoder.encode(case)
                print(f"[ENCODE] '{case}' ({len(str(case))})    ->     '{encoded}' ({len(encoded)})")
                decoded = encoder.decode(encoded)
                print(f"[DECODE] '{encoded}' ({len(encoded)})   ->    '{decoded}' ({len(str(decoded))})")

            except ValueError as e:
                print(f"'{case}' raised error: '{e}'")


if __name__ == "__main__":
    test()
