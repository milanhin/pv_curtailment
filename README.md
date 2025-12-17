# PV Curtailment
Custom integration for Home Assistant HACS to curtail PV inverter during negative feed-in tarriffs, as well as general power monitoring.

## General working
This integration will curtail a residential PV inverter. Controlling your inverter makes sense for users with a dynamic pricing energy contract (15-minute based). During negative injection tarriffs, it will control the inverter to prevent power injection onto the grid. When the total electricity price (incl network costs) is negative, the inverter will be shut off entirely to exploit the fact that you get reimbursed for using electricity at that moment. The entire curtailing system is only active when the provided switch entity is enabled.

Next to curtailment, this integration can be used to monitor power production of the inverter. 

An overview (Dutch) about this topic and integration is available [here](https://github.com/milanhin/pv_curtailment/blob/main/PV_curtailment_met_HA.pdf).

## Exposed entities
This component adds the following entities to Home Assistant:
- Active power output of the inverter
- Setpoint of active power output that is sent to the inverter
- System switch with which the entire system can be enabled or disabled

If the system switch is disabled, this integration functions as a regular power monitoring tool.
Note: the system switch does not keep its state over reboots of Home Assistant. It will always default to 'off'. So please reactivate the switch after a reboot (update, power loss,...).

## Installation
Installing this custom component can be done with [HACS](https://hacs.xyz) by searching for "PV Curtailment".
OR
It can be installed by manually downloading the [latest release](https://github.com/milanhin/pv_curtailment/releases) and copying the 'pv_curtailment' folder into your Home Assistant 'config/custom_components' folder.

## SunSpec support
This integration solely supports inverters that provide a SunSpec Modbus TCP connection. It supports both the 100 and 700 series of SunSpec models.

## Supported devices
With release 1.0.0, the only officially tested and supported brand of inverters is SMA.
However, the beta feature 'general SunSpec' can be chosen as model during configuration of the integration. Since it is a beta feature, it may not properly work. Watch the logs and sensors from this integration to check whether everything works as intended.
If you would encounter any problems, submit an [issue](https://github.com/milanhin/pv_curtailment/issues) or fix it yourself and submit a pull request.

## Configuration
Configuration is done through the UI by going to settings -> integrations -> add the PV Curtailment integration.
During configuration, the IP adress, port and Modbus slave ID need to be set, and the brand of inverter needs to be chosen from the list.
This integration also depends on a few other entities that are selected during configuration:
- Electricity price and injection tariff based on day-ahead market, to be set in €/MWh. Possible integration for Belgian prices: [SDAC Elia](https://github.com/milanhin/sdac_elia)
  - Electricity price: must be total cost for the user, so including network costs 
  - Injection tariff
- Power import and export from/to the grid, coming from your digital energy meter. Possible integration for DSMR meters: [DSMR Smart Meter](https://www.home-assistant.io/integrations/dsmr/)

For more information, a detailed Dutch guide is available [here](https://github.com/milanhin/pv_curtailment/blob/main/PV_curtailment_handleiding.pdf).
