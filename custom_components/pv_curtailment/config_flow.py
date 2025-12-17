import voluptuous as vol
import logging

from typing import Any
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import selector, EntitySelector, EntityFilterSelectorConfig
from .const import *

_LOGGER = logging.getLogger(__name__)

def map_default_ID(brand: Brand) -> int | None:
    """Map inverter brand to default slave ID"""
    if brand in SLAVE_ID_MAP:
        return SLAVE_ID_MAP[brand]
    else:
        return None

USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_INVERTER_BRAND): selector({
            "select": {
                "options": [brand.value for brand in Brand]
            }
        })
    }
)

ENERGY_METER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PWR_IMP_ENT_ID): EntitySelector(EntityFilterSelectorConfig(domain=["sensor", "input_number", "number"])),
        vol.Required(CONF_PWR_EXP_ENT_ID): EntitySelector(EntityFilterSelectorConfig(domain=["sensor", "input_number", "number"])),
    }
)

PRICING_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_INJ_TARIFF_ENT_ID): EntitySelector(EntityFilterSelectorConfig(domain=["sensor", "input_number", "number"])),
        vol.Required(CONF_PRICE_ENT_ID): EntitySelector(EntityFilterSelectorConfig(domain=["sensor", "input_number", "number"])),
    }
)

class PvCurtailmentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for the PV Curtailment integration setup"""

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Invoked when a user initiates a config flow via the UI
        In this step, the inverter brand is selected
        """
        errors = {}
        self.data = {}
        if user_input is not None:
            self.brand = Brand(user_input[CONF_INVERTER_BRAND])
            self.data[CONF_USER_STEP] = user_input
            return await self.async_step_connect()
        
        return self.async_show_form(step_id="user", data_schema=USER_SCHEMA, errors=errors)
    
    async def async_step_connect(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Configure IP, port and modbus slave ID"""
        CONNECT_SCHEMA = vol.Schema(
            {
                vol.Required(CONF_IP): str,
                vol.Required(CONF_PORT, default=502): vol.Coerce(int),
                vol.Required(CONF_SLAVE_ID, default=map_default_ID(brand=self.brand)): vol.Coerce(int),
            }
        )
        errors = {}

        if user_input is not None:
            try:
                validated_schema = CONNECT_SCHEMA(user_input)
            except Exception as e:
                errors["base"] = "invalid_input"
            
            if not errors:
                self.data[CONF_CONNECT_STEP] = user_input
                return await self.async_step_energy_meter()
        
        return self.async_show_form(step_id="connect", data_schema=CONNECT_SCHEMA, errors=errors)
    
    async def async_step_energy_meter(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Configure energy meter entity IDs"""
        errors = {}

        if user_input is not None:
            self.data[CONF_ENERGY_METER_STEP] = user_input
            return await self.async_step_pricing()
        
        return self.async_show_form(step_id="energy_meter", data_schema=ENERGY_METER_SCHEMA, errors=errors)
    
    async def async_step_pricing(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Configure SDAC injection tariff entity ID"""
        errors = {}

        if user_input is not None:
            self.data[CONF_PRICING_STEP] = user_input
            return self.async_create_entry(title=DOMAIN, data=self.data)
        
        return self.async_show_form(step_id="pricing", data_schema=PRICING_SCHEMA)
    

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler()
    

class OptionsFlowHandler(config_entries.OptionsFlowWithReload):
    """Handles options flow for the component"""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Invoked when a user initiates a flow via the user interface."""
        old_config = self.hass.data[DOMAIN][CONFIG]
        old_brand = Brand(str(old_config[CONF_USER_STEP][CONF_INVERTER_BRAND]))
        OPTIONS_INIT_SCHEMA = vol.Schema(
            {
                vol.Required(CONF_INVERTER_BRAND, default=old_brand): selector({
                    "select": {
                        "options": [brand.value for brand in Brand]
                    }
                })
            }
        )
        errors = {}
        self.data = {}
        if user_input is not None:
            self.brand = Brand(user_input[CONF_INVERTER_BRAND])
            self.data[CONF_USER_STEP] = user_input
            return await self.async_step_connect()

        return self.async_show_form(step_id="init", data_schema=OPTIONS_INIT_SCHEMA, errors=errors)
    
    async def async_step_connect(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Configure IP, port and modbus slave ID"""
        errors = {}
        old_config = self.hass.data[DOMAIN][CONFIG]
        old_ip = old_config[CONF_CONNECT_STEP][CONF_IP]
        old_port = old_config[CONF_CONNECT_STEP][CONF_PORT]

        OPTIONS_CONNECT_SCHEMA = vol.Schema(
            {
                vol.Required(CONF_IP, default=old_ip): str,
                vol.Required(CONF_PORT, default=old_port): vol.Coerce(int),
                vol.Required(CONF_SLAVE_ID, default=map_default_ID(brand=self.brand)): vol.Coerce(int),
            }
        )

        if user_input is not None:
            try:
                validated_schema = OPTIONS_CONNECT_SCHEMA(user_input)
            except Exception as e:
                errors["base"] = "invalid_input"
            
            if not errors:
                self.data[CONF_CONNECT_STEP] = user_input
                return await self.async_step_energy_meter()
        
        return self.async_show_form(step_id="connect", data_schema=OPTIONS_CONNECT_SCHEMA, errors=errors)
    
    async def async_step_energy_meter(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Configure energy meter entity IDs"""
        errors = {}
        old_config = self.hass.data[DOMAIN][CONFIG]
        old_pwr_imp_ent_id = old_config[CONF_ENERGY_METER_STEP][CONF_PWR_IMP_ENT_ID]
        old_pwr_exp_ent_id = old_config[CONF_ENERGY_METER_STEP][CONF_PWR_EXP_ENT_ID]

        OPTIONS_ENERGY_METER_SCHEMA = vol.Schema(
            {
                vol.Required(CONF_PWR_IMP_ENT_ID, default=old_pwr_imp_ent_id): EntitySelector(EntityFilterSelectorConfig(domain=["sensor", "input_number", "number"])),
                vol.Required(CONF_PWR_EXP_ENT_ID, default=old_pwr_exp_ent_id): EntitySelector(EntityFilterSelectorConfig(domain=["sensor", "input_number", "number"])),
            }
        )
        
        if user_input is not None:
            self.data[CONF_ENERGY_METER_STEP] = user_input
            return await self.async_step_pricing()
        
        return self.async_show_form(step_id="energy_meter", data_schema=OPTIONS_ENERGY_METER_SCHEMA, errors=errors)
    
    async def async_step_pricing(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Configure SDAC injection tariff entity ID"""
        errors = {}
        old_config = self.hass.data[DOMAIN][CONFIG]
        old_inj_tariff_ent_id = old_config[CONF_PRICING_STEP][CONF_INJ_TARIFF_ENT_ID]
        old_price_ent_id = old_config[CONF_PRICING_STEP][CONF_PRICE_ENT_ID]

        OPTIONS_PRICING_SCHEMA = vol.Schema(
            {
                vol.Required(CONF_INJ_TARIFF_ENT_ID, default=old_inj_tariff_ent_id): EntitySelector(EntityFilterSelectorConfig(domain=["sensor", "input_number", "number"])),
                vol.Required(CONF_PRICE_ENT_ID, default=old_price_ent_id): EntitySelector(EntityFilterSelectorConfig(domain=["sensor", "input_number", "number"])),
            }
        )
        
        if user_input is not None:
            self.data[CONF_PRICING_STEP] = user_input
            return self.async_create_entry(data=self.data)
        
        return self.async_show_form(step_id="pricing", data_schema=OPTIONS_PRICING_SCHEMA, errors=errors)