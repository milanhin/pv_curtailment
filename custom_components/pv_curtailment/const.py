from enum import StrEnum

DOMAIN = "pv_curtailment"
COORDINATOR = "coordinator"
CONFIG = "config"
SERIAL_NUMBER = "serial_number"

CONF_INJ_TARIFF_ENT_ID = "injection_tariff_entity_id"
CONF_PWR_IMP_ENT_ID = "power_import_entity_id"
CONF_PWR_EXP_ENT_ID = "power_export_entity_id"
CONF_INVERTER_BRAND = "inverter_brand"
CONF_IP = "ip_address"
CONF_PORT = "port"
CONF_SLAVE_ID = "slave_id"
CONF_USER_STEP = "user_step"
CONF_CONNECT_STEP = "connect_step"
CONF_ENERGY_METER_STEP = "energy_meter_step"
CONF_INJ_TARIFF_STEP = "inj_tariff_step"

INJ_CUTOFF_TARIFF = 0  # [€/Mwh]
UPDATE_INTERVAL = 15   # [s]

# Supported brands
class Brand(StrEnum):
    """
    All supported brands should be configured here
    """
    SMA = "SMA"
    SOLAREDGE = "SolarEdge"
    GENERAL_SUNSPEC = "General SunSpec (Beta)"

# default slave ID mapping for each Brand:
SLAVE_ID_MAP = {
    Brand.SMA: 126,
    Brand.SOLAREDGE: 1,
    Brand.GENERAL_SUNSPEC: None,
}

# SunSpec model IDs
COMMON_MID = 1
    # 100 series
NAMEPLATE_MID = 120
INVERTER_SINGLE_PHASE_MID = 101
INVERTER_SPLIT_PHASE_MID = 102
INVERTER_THREE_PAHSE_MID = 103
CONTROLS_MID = 123
    # 700 series
DER_MEASURE_AC_MID = 701
DER_CAPACITY_MID = 702
DER_CTL_AC_MID = 704

# SunSpec offsets (See information model reference: https://sunspec.org/specifications/)
SN_OFFSET = 50
    # 100 series
WRTG_OFFSET_1XX = 3
WMAXLIMPCT_OFFSET_1XX = 5
WMAXLIMPCT_WINTMS_OFFSET_1XX = 6
WMAXLIMPCT_RVRTTMS_OFFSET_1XX = 7
WMAXLIMPCT_RMPTMS_OFFSET_1XX = 8
WMAXLIM_ENA_OFFSET_1XX = 9
W_OFFSET_1XX = 14

    # 700 series
WRTG_OFFSET_7XX = 2
W_OFFSET_7XX = 10
WMAXLIMPCTENA_OFFSET_7XX = 14
WMAXLIMPCT_OFFSET_7XX = 15
WMAXLIMPCTRVRT_OFFSET_7XX = 16
WMAXLIMPCTENARVRT_OFFSET_7XX = 17
WMAXLIMPCTRVRTTMS_OFFSET_7XX = 18