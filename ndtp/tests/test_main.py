from ndtp.main import unpack_packet, unpack
from ndtp.schemas import (NPLHeader,
                          NPHHeader,)


def test__to_bin__return_correct_bin_format_of_decimal_value():
    pass


def test__unpack_packet__correct_unpack_NPLHeader(npl_header):
    ndtp = bytes.fromhex('7E7E42000200665A02000000000000')
    data = unpack_packet(NPLHeader, ndtp)
    assert data == npl_header


def test__unpack_packet__return_correct_NPHHeader(nph_header_with_real_nav_data):
    ndtp = bytes.fromhex('01006500010099050000')
    data =  unpack_packet(NPHHeader, ndtp)
    assert data == nph_header_with_real_nav_data


def test__unpack__return_correct_npl_header(ndtp_packet):
    ndtp = '7E7E42000200665A02000000000000010065000100990500000000931B4E4FF1459B1DAF2FED22E0D000000000510000008D00080002000000000000000000000000000000000000002FC800001F040000'
    data = unpack(ndtp)
    # assert data.header == ndtp_packet.header
    assert data == ndtp_packet

# def test__
#     assert data.data.data == ndtp_packet.data






# def test__unpack_npl_header__return_correct_packet_from_hex_string():
#     ndtp = '7E7E42000200665A02000000000000'
#     data = unpack_npl_header(ndtp)
#     assert data == NPLHeader(signature=32382, data_size=66, flags='00000010', crc=23142, type=NPLTypes.NPL_TYPE_NPH, peer_address=0, request_id=0)
