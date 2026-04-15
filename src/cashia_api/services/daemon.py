import asyncio
from datetime import datetime
from typing import Optional

import pandas as pd

from cashia_core.common_tools.storage import get_storage
from cashia_core.common_tools.configuration.resource_keys import get_resource_path
from cashia_core.ponderation.initializer import fill_initial_configuration


class ModelsConfigurationDaemon:
    CONFIG_FILE = get_resource_path("configuration")
    CONFIG_LOG_FILE = get_resource_path("configuration_log")

    def __init__(self, check_interval_seconds: int = 900):
        self.storage = get_storage()
        self.check_interval_seconds = check_interval_seconds

        self.last_modified_time: Optional[datetime] = None
        self.models_df: Optional[pd.DataFrame] = None
        self.models_ponderations = None

    def _get_current_modified_time(self):
        return self.storage.get_modified_time(self.CONFIG_FILE)

    def _load_models_df(self) -> pd.DataFrame:
        return self.storage.read_excel(self.CONFIG_FILE, index_col=0)

    def _build_ponderations(self, models_df: pd.DataFrame):
        return fill_initial_configuration(models_df)

    def _ensure_log_file(self) -> pd.DataFrame:
        return self.storage.ensure_csv(
            self.CONFIG_LOG_FILE,
            ["update_date_time", "review_date_time", "changed"]
        )

    def initialize(self):
        """
        Carga inicial de configuración. Llamar una vez al arrancar la API.
        """
        current_modified_time = self._get_current_modified_time()
        models_df = self._load_models_df()
        models_ponderations = self._build_ponderations(models_df)

        self.last_modified_time = current_modified_time
        self.models_df = models_df
        self.models_ponderations = models_ponderations

        print("Configuración inicial cargada correctamente.")

    def reload_if_needed(self) -> bool:
        """
        Revisa si cambió el archivo y recarga si es necesario.
        Regresa True si hubo cambio, False si no.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_modified_time = self._get_current_modified_time()

        if hasattr(current_modified_time, "timestamp"):
            update_date_time_str = current_modified_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            update_date_time_str = datetime.fromtimestamp(
                current_modified_time
            ).strftime("%Y-%m-%d %H:%M:%S")

        conf_changed = (
            self.last_modified_time is None
            or current_modified_time != self.last_modified_time
        )

        if conf_changed:
            print(f"Archivo actualizado. Cargando datos... {datetime.now()}")
            models_df = self._load_models_df()
            models_ponderations = self._build_ponderations(models_df)

            self.models_df = models_df
            self.models_ponderations = models_ponderations
            self.last_modified_time = current_modified_time

            print("Datos cargados.")
        else:
            print(f"El archivo no ha cambiado. Última revisión: {datetime.now()}")

        df_log = self._ensure_log_file()

        new_row = {
            "update_date_time": update_date_time_str,
            "review_date_time": now_str,
            "changed": conf_changed,
        }

        df_log = pd.concat([df_log, pd.DataFrame([new_row])], ignore_index=True)

        self.storage.write_csv(
            self.CONFIG_LOG_FILE,
            df_log,
            index=False,
            encoding="utf-8",
        )

        return conf_changed

    async def run_forever(self):
        """
        Loop async que revisa periódicamente si cambió la configuración.
        """
        while True:
            try:
                self.reload_if_needed()
            except Exception as e:
                print(f"Error revisando cambios de configuración: {e}")

            await asyncio.sleep(self.check_interval_seconds)


