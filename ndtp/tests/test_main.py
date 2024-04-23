from ndtp.main import unpack_packet, unpack
from ndtp.schemas import (NPLHeader,
                          NPLTypes,
                          NPHHeader,
                          NPLPacket,
                          NPHServiceTypes,
                          NPHPacket,
                          NphSnd,
                          Inner_Device_Data,
                          NphSrvNavData)




def test__to_bin__return_correct_bin_format_of_decimal_value():
    pass


def test__unpack_packet__correct_unpack_NPLHeader():
    ndtp = bytes.fromhex('7E7E42000200665A02000000000000')
    data = unpack_packet(NPLHeader, ndtp)
    assert data == NPLHeader(signature=32382,
                             data_size=66,
                             flags='00000010',
                             crc=23142,
                             packet_type=NPLTypes.NPL_TYPE_NPH,
                             peer_address=0,
                             request_id=0)


def test__unpack__return_correct_ndtp_packet():
    ndtp = '7E7E42000200665A02000000000000010065000100990500000000931B4E4FF1459B1DAF2FED22E0D000000000510000008D00080002000000000000000000000000000000000000002FC800001F040000'
    data = unpack(ndtp)
    assert data == NPLPacket(header=NPLHeader(signature=32382,
                                              data_size=66,
                                              flags='00000010',
                                              crc=23142,
                                              packet_type=NPLTypes.NPL_TYPE_NPH,
                                              peer_address=0,
                                              request_id=0),
                             nph_packet=NPHPacket(header=NPHHeader(service_id=NPHServiceTypes.NPH_SRV_NAVDATA,
                                                                   packet_type=101,
                                                                   flags='00000001',
                                                                   request_id=1433),
                                                  data=[NphSnd(data_type=0,
                                                               number=0,
                                                               data=NphSrvNavData(time_stamp=1330518931,
                                                                                  longitude=496715249,
                                                                                  latitude=585969583,
                                                                                  extra_dop='0b100000',
                                                                                  bat_voltage=-48,
                                                                                  speed_avg=0,
                                                                                  speed_max=0,
                                                                                  course=81,
                                                                                  track=0,
                                                                                  altitude=141,
                                                                                  nsat=8,
                                                                                  pdop=0)),
                                                        NphSnd(data_type=2,
                                                               number=0,
                                                               data=Inner_Device_Data(an_in0=0,
                                                                                      an_in1=0,
                                                                                      an_in2=0,
                                                                                      an_in3=0,
                                                                                      di_in=0,
                                                                                      di_out=0,
                                                                                      di0_counter=0,
                                                                                      di1_counter=0,
                                                                                      di2_counter=0,
                                                                                      di3_counter=0,
                                                                                      odometer=51247,
                                                                                      CSQ=31,
                                                                                      GPRS_State=4,
                                                                                      Accel_Energ=0,
                                                                                      ext_volt=0))]))



def test__unpack_packet__return_correct_NPHHeader():
    ndtp = bytes.fromhex('01006500010099050000')
    data =  unpack_packet(NPHHeader, ndtp)
    assert data == NPHHeader(service_id=NPHServiceTypes.NPH_SRV_NAVDATA,
                             packet_type=101,
                             flags='00000001',
                             request_id=1433)

# def test__unpack_npl_header__return_correct_packet_from_hex_string():
#     ndtp = '7E7E42000200665A02000000000000'
#     data = unpack_npl_header(ndtp)
#     assert data == NPLHeader(signature=32382, data_size=66, flags='00000010', crc=23142, type=NPLTypes.NPL_TYPE_NPH, peer_address=0, request_id=0)
