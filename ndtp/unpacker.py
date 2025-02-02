import struct
from dataclasses import asdict
from typing import Any

from schemas import NPLPacket, NPLHeader, NPHPacket, NPHHeader, NphSnd
from schemas import NphSrvNavData, NphSndNav, InnerDeviceData, NphSndDev, KoronaDeviceData, NphSndKorona
from schemas import Ndtp_Service_Type_dict
from functions import get_length, get_fields_and_struct

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

    packet_raw_data = raw[NPH_HEADER_SIZE:NPH_HEADER_SIZE + get_length(packet_type)]
    data = unpack_packet(packet_type, packet_raw_data)
    return NPHPacket(header, data)


def unpack_nph_snd(raw: bytes) -> list[NphSndNav | NphSndDev | NphSndKorona]:
    data = []

    while len(raw) > 0:
        header = unpack_packet(NphSnd, raw[:NPH_SND_HEADER_SIZE])
        nph_snd_packed: NphSndNav | NphSndDev | NphSndKorona
        raw = raw[NPH_SND_HEADER_SIZE:]
        match header.data_type:
            case 0:
                raw_data = raw[:get_length(NphSrvNavData)]
                nav_data = unpack_packet(NphSrvNavData, raw_data)
                nph_snd_packed = NphSndNav(**asdict(header), data=nav_data)
            case 1:
                raise KeyError  # Дополнительные навигационные данные Type=1 (структура на данный моментне реализована).
            case 2:
                raw_data = raw[:get_length(InnerDeviceData)]
                inner_device_data = unpack_packet(InnerDeviceData, raw_data)
                nph_snd_packed = NphSndDev(**asdict(header), data=inner_device_data)
            case 3:
                raw_data = raw[:get_length(KoronaDeviceData)]
                korona_device_data = unpack_packet(KoronaDeviceData, raw_data)
                nph_snd_packed = NphSndKorona(**asdict(header), data=korona_device_data)
            case _:
                raise KeyError

        if nph_snd_packed:
            data.append(nph_snd_packed)
        raw = raw[len(raw_data):]

    return data


def get_nph_packet_type(header: NPHHeader) -> type:
    _type = Ndtp_Service_Type_dict[header.service_id][header.packet_type]
    return _type


def unpack_packet(packet_type: type, raw_data: bytes) -> Any:
    fields, format_string = get_fields_and_struct(packet_type)
    packet_data = struct.unpack(format_string, raw_data)

    attr = {}
    for param, value in zip(fields, packet_data):
        attr[param[0]] = param[1].value.constructor(value)

    return packet_type(**attr)
