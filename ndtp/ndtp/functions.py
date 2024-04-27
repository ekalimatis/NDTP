from typing import Any


def to_bin8(data: int) -> str:
    bin_data = bin(data)[2:]
    bin_str = '0' * (8 - len(bin_data)) + bin_data
    return bin_str


def to_bin16(data: int) -> str:
    bin_data = bin(data)[2:]
    bin_str = '0' * (16 - len(bin_data)) + bin_data
    return bin_str


def get_length(packet_type: Any) -> int:
    # length = 0
    # for field_param in packet_type.__annotations__.values():
    #     length += field_param.value.length
    return packet_type.get_length()


def get_fields_and_struct(packet_type: type) -> tuple[list[tuple[str, Any]], str]:
    format_string = '<'
    fields = []

    for field, _type in packet_type.__annotations__.items():
        format_string += _type.value.code
        fields.append((field, _type))

    return fields, format_string
