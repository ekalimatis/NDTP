import enum
from typing import Callable, Any
from dataclasses import dataclass
from datetime import datetime

from ndtp1.functions import to_bin8, to_bin16, get_length


class NPLTypes(enum.Enum):
    NPL_TYPE_ERROR = 1
    NPL_TYPE_NPH = 2
    NPL_TYPE_DEBUG = 3


class NPHServiceTypes(enum.Enum):
    NPH_SRV_GENERIC_CONTROLS = 0
    NPH_SRV_NAVDATA = 1
    NPH_SRV_FILE_TRANSFER = 3
    NPH_SRV_CLIENT_LIST = 4
    NPH_SRV_EXTERNAL_DEVICE = 5
    NPH_SRV_DEBUG = 6


class NphSrvNavDataTypes(enum.Enum):
    NPH_SND_HISTORY = 100
    NPH_SND_REALTIME = 101


class NphSrvGenericControls(enum.Enum):
    NPH_SGC_RESULT = 0
    NPH_SGC_CONN_REQUEST = 100
    NPH_SGC_CONN_AUTH_STRING = 101
    NPH_SGC_SERVICE_REQUEST = 110
    NPH_SGC_SERVICES_REQUEST = 111
    NPH_SGC_SERVICES = 112
    NPH_SGC_PEER_DESC_REQUEST = 120
    NPH_SGC_PEER_DESC = 121


@dataclass
class AttrType:
    name: str
    code: str
    length: int
    constructor: Callable


@dataclass
class AttrTypes(enum.Enum):
    int16 = AttrType('short', 'h', 2, int)
    u_int16 = AttrType('u_short', 'H', 2, int)
    f_int16 = AttrType('f_short', 'h', 2, to_bin16)
    f_u_int16 = AttrType('f_u_short', 'H', 2, to_bin16)
    int32 = AttrType('integer', 'i', 4, int)
    u_int32 = AttrType('u_integer', 'I', 4, int)
    npl_types = AttrType('npl_types', 'b', 1, NPLTypes)
    nph_service_type = AttrType('nph_service_type', 'H', 2, NPHServiceTypes)
    nph_packet_type = AttrType('nph_packet_type', 'H', 2, int)
    u_int8 = AttrType('unsigned char', 'B', 1, int)
    f_u_int8 = AttrType('f_unsigned byte', 'B', 1, to_bin8)
    time_stamp = AttrType('unsigned int32', 'I', 4, datetime.fromtimestamp)


@dataclass
class NPLHeader:
    signature: AttrTypes.int16  # type: ignore
    data_size: AttrTypes.u_int16  # type: ignore
    flags: AttrTypes.f_int16  # type: ignore
    crc: AttrTypes.u_int16  # type: ignore
    packet_type: AttrTypes.npl_types  # type: ignore
    peer_address: AttrTypes.u_int32  # type: ignore
    request_id: AttrTypes.u_int16  # type: ignore


@dataclass
class NPHHeader:
    service_id: AttrTypes.nph_service_type  # type: ignore
    packet_type: AttrTypes.nph_packet_type  # type: ignore
    flags: AttrTypes.f_u_int16  # type: ignore
    request_id: AttrTypes.u_int32  # type: ignore

    def __len__(self) -> int:
        return 10


@dataclass
class NPHPacket:
    header: NPHHeader
    data: Any

    def __len__(self) -> int:
        return len(self.header) + get_length(type(self.data))


@dataclass
class NphSnd:
    data_type: AttrTypes.u_int8  # type: ignore
    number: AttrTypes.u_int8  # type: ignore


@dataclass
class NphSrvNavData:
    """Type = 1"""
    time_stamp: AttrTypes.time_stamp  # type: ignore
    longitude: AttrTypes.u_int32  # type: ignore
    latitude: AttrTypes.u_int32  # type: ignore
    extra_dop: AttrTypes.f_u_int8  # type: ignore
    bat_voltage: AttrTypes.u_int8  # type: ignore
    speed_avg: AttrTypes.u_int16  # type: ignore
    speed_max: AttrTypes.u_int16  # type: ignore
    course: AttrTypes.u_int16  # type: ignore
    track: AttrTypes.u_int16  # type: ignore
    altitude: AttrTypes.int16  # type: ignore
    nsat: AttrTypes.u_int8  # type: ignore
    pdop: AttrTypes.u_int8  # type: ignore

    @staticmethod
    def get_length() -> int:
        return 26


@dataclass
class NphSndNav(NphSnd):
    data: NphSrvNavData


@dataclass
class InnerDeviceData:
    """Type = 2"""
    an_in0: AttrTypes.u_int16  # type: ignore
    an_in1: AttrTypes.u_int16  # type: ignore
    an_in2: AttrTypes.u_int16  # type: ignore
    an_in3: AttrTypes.u_int16  # type: ignore
    di_in: AttrTypes.u_int8  # type: ignore
    di_out: AttrTypes.u_int8  # type: ignore
    di0_counter: AttrTypes.u_int16  # type: ignore
    di1_counter: AttrTypes.u_int16  # type: ignore
    di2_counter: AttrTypes.u_int16  # type: ignore
    di3_counter: AttrTypes.u_int16  # type: ignore
    odometer: AttrTypes.u_int32  # type: ignore
    CSQ: AttrTypes.u_int8  # type: ignore
    GPRS_State: AttrTypes.u_int8  # type: ignore
    Accel_Energ: AttrTypes.u_int8  # type: ignore
    ext_volt: AttrTypes.u_int8  # type: ignore

    @staticmethod
    def get_length() -> int:
        return 26


@dataclass
class NphSndDev(NphSnd):
    data: InnerDeviceData


@dataclass
class KoronaDeviceData:
    """Type = 3"""
    odometer: AttrTypes.u_int32  # type: ignore
    zone: AttrTypes.u_int16  # type: ignore
    door1_in: AttrTypes.u_int8  # type: ignore
    door2_in: AttrTypes.u_int8  # type: ignore
    door3_in: AttrTypes.u_int8  # type: ignore
    door4_in: AttrTypes.u_int8  # type: ignore
    door1_out: AttrTypes.u_int8  # type: ignore
    door2_out: AttrTypes.u_int8  # type: ignore
    door3_out: AttrTypes.u_int8  # type: ignore
    door4_out: AttrTypes.u_int8  # type: ignore

    @staticmethod
    def get_length() -> int:
        return 14


@dataclass
class NphSndKorona(NphSnd):
    data: KoronaDeviceData


@dataclass
class IrmaDeviceData:
    """Type = 4"""
    odometer: AttrTypes.u_int32  # type: ignore
    zone: AttrTypes.u_int16  # type: ignore
    door1_in: AttrTypes.u_int8  # type: ignore
    door2_in: AttrTypes.u_int8  # type: ignore
    door3_in: AttrTypes.u_int8  # type: ignore
    door4_in: AttrTypes.u_int8  # type: ignore
    door1_out: AttrTypes.u_int8  # type: ignore
    door2_out: AttrTypes.u_int8  # type: ignore
    door3_out: AttrTypes.u_int8  # type: ignore
    door4_out: AttrTypes.u_int8  # type: ignore
    present_door: AttrTypes.f_u_int8  # type: ignore

    @staticmethod
    def get_length() -> int:
        return 15


@dataclass
class NphSndIrma(NphSnd):
    data: IrmaDeviceData


@dataclass
class NphResult:
    error: AttrTypes.u_int32  # type: ignore


@dataclass
class NPLPacket:
    header: NPLHeader
    nph_packet: NPHPacket


Ndtp_Service_Type_dict: dict = {
    NPHServiceTypes.NPH_SRV_NAVDATA: {
        NphSrvNavDataTypes.NPH_SND_HISTORY.value: NphSnd,
        NphSrvNavDataTypes.NPH_SND_REALTIME.value: NphSnd,
    },
    NPHServiceTypes.NPH_SRV_GENERIC_CONTROLS: {
        NphSrvGenericControls.NPH_SGC_RESULT: NphResult,
    }
}
