#!/usr/bin/env python3

import logging
from .eonnext import EonNext
from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)

DOMAIN = "eon_next"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"

PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_setup_entry(hass, entry):
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})

    api = EonNext()
    success = await api.login_with_username_and_password(entry.data[CONF_EMAIL], entry.data[CONF_PASSWORD])

    if success == True:

        hass.data[DOMAIN][entry.entry_id] = api

        #hass.async_create_task(
        #    hass.config_entries.async_forward_entry_setup(entry, "sensor")
        #)
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        return True
    
    else:
        return False

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
