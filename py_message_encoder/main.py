from typing import List, Tuple, Any

from py_message_encoder.body import MessageBody
from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.encoders.float_encoders import float_encoder, FloatEncoder
from py_message_encoder.encoders.integer_encoders import small_int, _small_int, big_int
from py_message_encoder.encoders.message_body_encoder import FieldMapping, MessageField, BodyEncoder
from py_message_encoder.encoders.message_header_encoder import header_encoder
from py_message_encoder.header import MessageHeader
from .encoders.boolean_encoder import BooleanEncoder
from .encoders.string_encoders import FixedLengthEncoder, LVAR, LLVAR, LLLVAR


def test():
    message_headers = [
        MessageHeader(7).set_presence(0).set_presence(4).set_presence(6),
        MessageHeader(7).set_presence(4).set_presence(5).set_presence(6),
        MessageHeader(13).set_presence(0).set_presence(6).set_presence(9).set_presence(10),
    ]
    mapping = FieldMapping([MessageField("first_name", LVAR), MessageField("last_name", LVAR), MessageField("score", FloatEncoder(2))])
    print(f"mapping.names: {mapping.names}")
    body_encoder = BodyEncoder(mapping)
    test_cases: List[Tuple[PartialEncoder, List[Any]]] = [
        # (BooleanEncoder(), [True, False, 0, 1, 2, 3, -1, "str", "", [1, 2], []]),
        # (FixedLengthEncoder(10), ["", "Hi @team", "This is a very long tutorial"]),
        # (LVAR, ["Hi", "Hi team", "This is a very long text"]),
        # (LLVAR, ["Hi", "Hi team", "This is a very long text", "This is a very long text" * 7]),
        # (LLLVAR, ["Hi", "Hi team", "This is a very long text", "a long text" * 7, "This is a very long text" * 13]),
        # (small_int, [0, 23, 56, 7, 345]),
        # (_small_int, [0, 23, 56, 7, 345]),
        # (big_int, [0, 7, 9, 23, 56, 99, 100, 345, 999, 1000, 1999, 9999, 567893980834]),
        # (float_encoder, [round(x, float_encoder.precision) for x in [0.0, 23434., 0.23, .23, 123.0000345, 123.124242424242424423223]]),
        # (header_encoder, message_headers),
        (body_encoder, [MessageBody(mapping.names, data) for data in [
            {"first_name": "Thiam", "score": 45.34}, {"first_name": "DKG", "last_name": "Cidemia"},
            {"last_name": "Mouhidine", "score": 34.02, "first_name": "Pathe"},
            {"score": 509.34}, {}
        ]])
    ]
    for encoder, cases in test_cases:
        print(f"\n-------------------------Testing {str(encoder)} ... -----------------------------\n")
        for case in cases:
            try:
                encoded = encoder.encode(case)
                print(f"[ENCODE] '{case}' ({len(str(case))})    ->     '{encoded}' ({len(encoded)})")
                decoded, _ = encoder.decode(encoded)
                print(f"[DECODE] '{encoded}' ({len(encoded)})   ->    '{decoded}' ({len(str(decoded))})")

            except ValueError as e:
                print(f"'{case}' raised error: '{e}'")


if __name__ == "__main__":
    test()
