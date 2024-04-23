def to_bin(data: int) -> str:
    bin_data = bin(data)[2:]
    bin_str = '0' * (8 - len(bin_data)) + bin_data
    return bin_str


def length(packet_type: type) -> int:
    length = 0
    for field, field_param in packet_type.__annotations__.items():
        length += field_param.value.length
    return length
