import struct
from dataclasses import asdict
from typing import Any

from ndtp.schemas import NPLPacket, NPLHeader
from ndtp.schemas import NPHPacket, NPHHeader, NphSnd, NphSrvNavData, Inner_Device_Data, NphSndDev, NphSndNav
from ndtp.schemas import Ndtp_Service_Type_dict
from ndtp.functions import length

NPL_HEADER_SIZE = 15
NPH_HEADER_SIZE = 10
NPH_SND_HEADER_SIZE = 2


def unpack(raw_packet: str) -> NPLPacket:
    bytes_data = bytes.fromhex(raw_packet)
    header = unpack_packet(NPLHeader, bytes_data[:NPL_HEADER_SIZE])
    bytes_data = bytes_data[NPL_HEADER_SIZE:]
    npl_data = unpack_nph_packet(bytes_data)
    return NPLPacket(header=header, nph_packet=npl_data)


def unpack_nph_packet(raw: bytes) -> NPHPacket:
    header = unpack_packet(NPHHeader, raw[:NPH_HEADER_SIZE])
    packet_type = get_nph_packet_type(header)
    if packet_type == NphSnd:
        data = unpack_nph_snd(raw[NPH_HEADER_SIZE:])
        return NPHPacket(header, data)

    packet_raw_data = raw[NPH_HEADER_SIZE:NPH_HEADER_SIZE + length(packet_type)]
    data = unpack_packet(packet_type, packet_raw_data)
    return NPHPacket(header, data)


def unpack_nph_snd(raw: bytes) -> list[NphSnd]:
    data = []

    while len(raw) > 0:
        header = unpack_packet(NphSnd, raw[:NPH_SND_HEADER_SIZE])
        nph_snd_packed: NphSnd | None = None
        match header.data_type:
            case 0:
                raw_data = raw[NPH_SND_HEADER_SIZE:NPH_SND_HEADER_SIZE + length(NphSrvNavData)]
                nav_data = unpack_packet(NphSrvNavData, raw_data)
                nph_snd_packed = NphSndNav(**asdict(header), data=nav_data)
            case 1:
                pass
            case 2:
                raw_data = raw[NPH_SND_HEADER_SIZE:NPH_SND_HEADER_SIZE + length(Inner_Device_Data)]
                inner_device_data = unpack_packet(Inner_Device_Data, raw_data)
                nph_snd_packed = NphSndDev(**asdict(header), data=inner_device_data)
            case _:
                pass

        if nph_snd_packed:
            data.append(nph_snd_packed)
        raw = raw[NPH_SND_HEADER_SIZE + len(raw_data):]

    return data


def get_nph_packet_type(header: NPHHeader) -> type:
    _type = Ndtp_Service_Type_dict[header.service_id][header.packet_type]
    return _type


def unpack_packet(packet_type: type, raw_data: bytes) -> Any:
    format_string = '<'
    fields = []
    attr = {}
    for field, _type in packet_type.__annotations__.items():
        format_string += _type.value.code
        fields.append((field, _type))
    packet_data = struct.unpack(format_string, raw_data)
    for param, value in zip(fields, packet_data):
        attr[param[0]] = param[1].value.constructor(value)
    return packet_type(**attr)
