from datetime import date, time, datetime
from typing import List, Tuple, Any

from py_message_encoder.body import MessageBody
from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.encoders.date_encoders import date_encoder, time_encoder, date_time_encoder, DateEncoder, \
    DateTimeEncoder, TimeEncoder
from py_message_encoder.encoders.float_encoders import float_encoder, FloatEncoder
from py_message_encoder.encoders.integer_encoders import small_int, _small_int, big_int, IntFixedLengthEncoder, \
    _IntFixedLengthEncoder, IntegerVarLengthEncoder
from py_message_encoder.encoders.high_order_encoders.message_body_encoder import FieldMapping, MessageField, BodyEncoder
from py_message_encoder.encoders.message_header_encoder import header_encoder, MessageHeaderEncoder
from py_message_encoder.header import MessageHeader
from .encoders.boolean_encoder import BooleanEncoder
from .encoders.string_encoders import FixedLengthEncoder, LVAR, LLVAR, LLLVAR, VariableLengthEncoder


def test():
    message_headers = [
        MessageHeader(7).set_presence(0).set_presence(4).set_presence(6),
        MessageHeader(7).set_presence(4).set_presence(5).set_presence(6),
        MessageHeader(13).set_presence(0).set_presence(6).set_presence(9).set_presence(10),
    ]
    mapping = FieldMapping([MessageField("first_name", LVAR), MessageField("last_name", LVAR), MessageField("score", FloatEncoder(2))])
    body_encoder = BodyEncoder(mapping)
    bool_cases: List[Tuple[BooleanEncoder, List[bool]]] = \
        (BooleanEncoder(), [True, False, 0, 1, 2, 3, -1, "str", "", [1, 2], []])
    fixed_length_cases: List[Tuple[FixedLengthEncoder, List[str]]] = \
        (FixedLengthEncoder(10), ["", "Hi @team", "This is a very long tutorial"])
    l_var_cases: List[Tuple[VariableLengthEncoder, List[str]]] = \
        (LVAR, ["Hi", "Hi team", "This is a very long text"])
    ll_var_cases: List[Tuple[VariableLengthEncoder, List[str]]] = \
        (LLVAR, ["Hi", "Hi team", "This is a very long text", "This is a very long text" * 7])
    lll_var_cases: List[Tuple[VariableLengthEncoder, List[str]]] = \
        (LLLVAR, ["Hi", "Hi team", "This is a very long text", "a long text" * 7, "This is a very long text" * 13])
    int_fixed_length_cases: List[Tuple[IntFixedLengthEncoder, List[int]]] = \
        (small_int, [0, 23, 56, 7, 345])
    _int_fixed_length_cases: List[Tuple[_IntFixedLengthEncoder, List[int]]] = \
        (_small_int, [0, 23, 56, 7, 345])
    int_var_length_cases: List[Tuple[IntegerVarLengthEncoder, List[int]]] = \
        (big_int, [0, 7, -7, 9, 23, 56, 99, 100, 345, 999, 1000, 1999, 9999, 567893980834])
    float_cases: List[Tuple[FloatEncoder, List[float]]] = \
        (float_encoder, [round(x, float_encoder.precision) for x in [0.0, 23434., 0.23, .23, 123.0000345, 123.1242424242424]])
    header_cases: List[Tuple[MessageHeaderEncoder, List[MessageHeader]]] = \
        (header_encoder, message_headers)
    body_cases: List[Tuple[BodyEncoder, List[bool]]] = \
        (body_encoder, [MessageBody(mapping.names, data) for data in [
            {"first_name": "Thiam", "score": 45.34}, {"first_name": "DKG", "last_name": "Cidemia"},
            {"last_name": "Mouhidine", "score": 34.02, "first_name": "Pathe"},
            {"score": 509.34}, {}
        ]])
    date_cases: List[Tuple[DateEncoder, List[date]]] = \
        (date_encoder, [date.fromisoformat(s) for s in ["2021-12-06", "1980-01-02", "1970-01-01", "1960-01-02"]])
    time_cases: List[Tuple[TimeEncoder, List[time]]] = \
        (time_encoder, [time.fromisoformat(s) for s in ["11:23:10", "17:34:11+02:00", "23:59:59+14:00", "00:00:00-12:00"]])
    date_time_cases: List[Tuple[DateTimeEncoder, List[datetime]]] = \
        (date_time_encoder, [
            datetime.fromisoformat(s) for s in ["2021-12-06 11:23:10", "2021-12-04 22:51:10-05:30"]
        ] + [datetime.utcnow(), datetime.now()])
    test_cases: List[Tuple[PartialEncoder, List[Any]]] = [
        date_time_cases
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
