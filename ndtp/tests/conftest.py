import pytest
from datetime import datetime

from ndtp.schemas import (NPLPacket,
                          NPLHeader,
                          NPHPacket,
                          NPHHeader,
                          NphSrvNavData,
                          InnerDeviceData,
                          NPLTypes,
                          NPHServiceTypes,
                          NphSndNav,
                          NphSndDev)


@pytest.fixture
def npl_header():
    return NPLHeader(signature=32382,
                     data_size=66,
                     flags='0000000000000010',
                     crc=23142,
                     packet_type=NPLTypes.NPL_TYPE_NPH,
                     peer_address=0,
                     request_id=0)


@pytest.fixture
def nph_header_with_real_nav_data():
    return NPHHeader(service_id=NPHServiceTypes.NPH_SRV_NAVDATA,
                     packet_type=101,
                     flags='0000000000000001',
                     request_id=1433)


@pytest.fixture
def nph_snd_nav(nph_srv_nav_data):
    return NphSndNav(data_type=0,
                     number=0,
                     data=nph_srv_nav_data)


@pytest.fixture
def nph_snd_dev(inner_device_data):
    return NphSndDev(data_type=2,
                     number=0,
                     data=inner_device_data)


@pytest.fixture
def nph_srv_nav_data():
    return NphSrvNavData(time_stamp=datetime.fromtimestamp(1330518931),
                         longitude=496715249,
                         latitude=585969583,
                         extra_dop='11100000',
                         bat_voltage=208,
                         speed_avg=0,
                         speed_max=0,
                         course=81,
                         track=0,
                         altitude=141,
                         nsat=8,
                         pdop=0)


@pytest.fixture
def inner_device_data():
    return InnerDeviceData(an_in0=0,
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
                           ext_volt=0)


@pytest.fixture
def nph_packed(nph_header_with_real_nav_data, nph_snd_nav, nph_snd_dev):
    return NPHPacket(header=nph_header_with_real_nav_data,
                     data=[nph_snd_nav, nph_snd_dev])


@pytest.fixture
def ndtp_packet(npl_header, nph_packed):
    return NPLPacket(header=npl_header, nph_packet=nph_packed)


@pytest.fixture
def full_raw_ndtp():
    ndtp = '7E7E42000200665A02000000000000010065000100990500000000931B4E4FF1459B1DAF2FED22E0D00000' \
           '0000510000008D00080002000000000000000000000000000000000000002FC800001F040000'
    return ndtp
