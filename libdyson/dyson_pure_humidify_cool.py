"""Dyson Pure Humidify+Cool device."""

from typing import Optional

from .const import HumidifyOscillationMode, WaterHardness
from .dyson_pure_cool import DysonPureCoolBase

WATER_HARDNESS_ENUM_TO_STR = {
    WaterHardness.SOFT: "2025",
    WaterHardness.MEDIUM: "1350",
    WaterHardness.HARD: "0675",
}
WATER_HARDNESS_STR_TO_ENUM = {
    str_: enum for enum, str_ in WATER_HARDNESS_ENUM_TO_STR.items()
}


class DysonPureHumidifyCool(DysonPureCoolBase):
    """Dyson Pure Humidify+Cool device."""

    @property
    def oscillation(self) -> bool | None:
        """Return oscillation status."""
        return self._get_field_value(self._status, "oson", lambda x: x == "ON")

    @property
    def oscillation_mode(self) -> HumidifyOscillationMode | None:
        """Return oscillation mode."""
        return self._get_field_value(self._status, "ancp", HumidifyOscillationMode)

    @property
    def humidification(self) -> bool | None:
        """Return if humidification is on."""
        return self._get_field_value(self._status, "hume", lambda x: x == "HUMD")

    @property
    def humidification_auto_mode(self) -> bool | None:
        """Return if humidification auto mode is on."""
        return self._get_field_value(self._status, "haut", lambda x: x == "ON")

    @property
    def target_humidity(self) -> int | None:
        """Return target humidity in percentage."""
        return self._get_field_value(self._status, "humt", int)

    @property
    def auto_target_humidity(self) -> int | None:
        """Return humidification auto mode target humidity."""
        return self._get_field_value(self._status, "rect", int)

    @property
    def water_hardness(self) -> WaterHardness | None:
        """Return the water hardness setting."""
        return self._get_field_value(self._status, "wath", lambda x: WATER_HARDNESS_STR_TO_ENUM[x])

    @property
    def time_until_next_clean(self) -> int | None:
        """Return the time remaining in hours before the next deep cleaning."""
        return self._get_field_value(self._status, "cltr", int)

    @property
    def clean_time_remaining(self) -> int | None:
        """Return the time remaining in minutes before the cleaning finishes."""
        return self._get_field_value(self._status, "cdrr", int)

    def enable_oscillation(
        self, oscillation_mode: Optional[HumidifyOscillationMode] = None
    ) -> None:
        """Turn on oscillation."""
        if oscillation_mode is None:
            oscillation_mode = self.oscillation_mode or HumidifyOscillationMode.DEGREE_45

        self._set_configuration(oson="ON", fpwr="ON", ancp=oscillation_mode.value)

    def disable_oscillation(self) -> None:
        """Turn off oscillation."""
        self._set_configuration(oson="OFF")

    def enable_humidification(self) -> None:
        """Enable humidification."""
        self._set_configuration(hume="HUMD")

    def disable_humidification(self) -> None:
        """Disable humidification."""
        self._set_configuration(hume="OFF")

    def enable_humidification_auto_mode(self) -> None:
        """Enable humidification auto mode."""
        self._set_configuration(haut="ON")

    def disable_humidification_auto_mode(self) -> None:
        """Disable humidification auto mode."""
        self._set_configuration(haut="OFF")

    def set_target_humidity(self, target_humidity: int) -> None:
        """Set target humidity."""
        self._set_configuration(humt=f"{target_humidity:04d}", haut="OFF")

    def set_water_hardness(self, water_hardness: WaterHardness) -> None:
        """Set water hardness."""
        self._set_configuration(wath=WATER_HARDNESS_ENUM_TO_STR[water_hardness])


class DysonPurifierHumidifyCoolFormaldehyde(DysonPureHumidifyCool):
    """Dyson Purifier Humidify+Cool Formaldehyde device."""

    @property
    def formaldehyde(self):
        """Return formaldehyde reading."""
        return self._get_environmental_field_value("hchr")
