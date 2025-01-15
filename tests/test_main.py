import pytest

from ndtp1.main import unpack_packet, unpack
from ndtp1.schemas import (NPLHeader,
                           NPHHeader,
                           NPLTypes)
from ndtp1.functions import to_bin8, to_bin16, get_length


@pytest.mark.parametrize(
    "value, bin_str",
    [
        (0, '00000000'),
        (1, '00000001'),
        (2, '00000010')
    ]
)
def test__to_bin8__return_correct_bin_string_of_decimal_value(value, bin_str):
    assert to_bin8(value) == bin_str


@pytest.mark.parametrize(
    "value, bin_str",
    [
        (0, '0000000000000000'),
        (1, '0000000000000001'),
        (2, '0000000000000010')
    ]
)
def test__to_bin16__return_correct_bin_string_of_decimal_value(value, bin_str):
    assert to_bin16(value) == bin_str


def test__unpack_packet__correct_unpack_NPLHeader(npl_header):
    ndtp = bytes.fromhex('7E7E42000200665A02000000000000')
    data = unpack_packet(NPLHeader, ndtp)
    assert data == npl_header


def test__unpack_packet__return_correct_NPHHeader(nph_header_with_real_nav_data):
    ndtp = bytes.fromhex('01006500010099050000')
    data = unpack_packet(NPHHeader, ndtp)
    assert data == nph_header_with_real_nav_data


def test__unpack__return_correct_npl_header(ndtp_packet, full_raw_ndtp):
    data = unpack(full_raw_ndtp)
    assert data.header == ndtp_packet.header
    assert data == ndtp_packet


def test__unpack_npl_header__return_correct_packet_from_hex_string(npl_header):
    ndtp = '7E7E42000200665A02000000000000'
    data = unpack_packet(NPLHeader, bytes.fromhex(ndtp))
    assert data == npl_header
