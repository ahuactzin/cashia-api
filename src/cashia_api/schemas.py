from pydantic import BaseModel, Field
from typing import Optional

from cashia_core.common_tools.configuration.cashiaconstants import *
from cashia_core.common_tools.configuration.resource_keys import get_model_path
from cashia_core.common_tools.storage import get_storage

import cashia_model.pm_model_rebuilder as pmmr
from cashia_api.models import *

COMPLETE_MODEL_KEYS = {
    NV_AGT: get_model_path("nv_agt"),
    NV_CC: get_model_path("nv_cc"),
    RNV_AGT: get_model_path("rnv_agt"),
    RNV_CC: get_model_path("rnv_cc"),
}

COLD_START_MODEL_KEYS = {
    NV_AGT: get_model_path("cs_nv_agt"),
    NV_CC: get_model_path("cs_nv_cc"),
    RNV_AGT: get_model_path("cs_rnv_agt"),
    RNV_CC: get_model_path("cs_rnv_cc"),
}

storage = get_storage()

complete_models_container = pmmr.ModelsContainer(
    "Complete",
    COMPLETE_MODEL_KEYS,
    storage=storage,
)

cold_start_models_container = pmmr.ModelsContainer(
    "Cold Start",
    COLD_START_MODEL_KEYS,
    storage=storage,
)

min_plazo = complete_models_container.model["NV_Agt"].min_value("Plazo")
max_plazo = complete_models_container.model["NV_Agt"].max_value("Plazo")

min_edad = complete_models_container.model["NV_Agt"].min_value("Edad Solicitud")
max_edad = complete_models_container.model["NV_Agt"].max_value("Edad Solicitud")

min_dependientes = complete_models_container.model["NV_Agt"].min_value("Dependientes")
max_dependientes = complete_models_container.model["NV_Agt"].max_value("Dependientes")

min_estudios = complete_models_container.model["NV_Agt"].min_value("Estudios")
max_estudios = complete_models_container.model["NV_Agt"].max_value("Estudios")

min_cp = complete_models_container.model["NV_Agt"].min_value("CP")
max_cp = complete_models_container.model["NV_Agt"].max_value("CP")

min_a_resid = complete_models_container.model["NV_Agt"].min_value("Años Residencia")
max_a_resid = complete_models_container.model["NV_Agt"].max_value("Años Residencia")

min_antiguedad = complete_models_container.model["NV_Agt"].min_value("Antigüedad")
max_antiguedad = complete_models_container.model["NV_Agt"].max_value("Antigüedad")

min_ingresos = complete_models_container.model["NV_Agt"].min_value("Ingresos")
max_ingresos = complete_models_container.model["NV_Agt"].max_value("Ingresos")

min_egresos = complete_models_container.model["NV_Agt"].min_value("Egresos")
max_egresos = complete_models_container.model["NV_Agt"].max_value("Egresos")

min_cp_aval = complete_models_container.model["NV_Agt"].min_value("CP Aval")
max_cp_aval = complete_models_container.model["NV_Agt"].max_value("CP Aval")

min_score_agt = complete_models_container.model["NV_Agt"].min_value("Score Agt")
max_score_agt = complete_models_container.model["NV_Agt"].max_value("Score Agt")

min_score_cc = complete_models_container.model["NV_Agt"].min_value("Score CC")
max_score_cc = complete_models_container.model["NV_Agt"].max_value("Score CC")

min_monto = complete_models_container.model["NV_Agt"].min_value("Monto")
max_monto = complete_models_container.model["NV_Agt"].max_value("Monto")

min_ciclo = complete_models_container.model["NV_Agt"].min_value("Ciclo")
max_ciclo = complete_models_container.model["NV_Agt"].max_value("Ciclo")

min_score_ant = complete_models_container.model["NV_Agt"].min_value("Score_Ant")
max_score_ant = complete_models_container.model["NV_Agt"].max_value("Score_Ant")

min_monto_ant = complete_models_container.model["NV_Agt"].min_value("Monto_Ant")
max_monto_ant = complete_models_container.model["NV_Agt"].max_value("Monto_Ant")

min_frecuencia_ant = complete_models_container.model["NV_Agt"].min_value("Frecuencia_Ant")
max_frecuencia_ant = complete_models_container.model["NV_Agt"].max_value("Frecuencia_Ant")

min_capacidad_ant = complete_models_container.model["NV_Agt"].min_value("Capacidad_Ant")
max_capacidad_ant = complete_models_container.model["NV_Agt"].max_value("Capacidad_Ant")




class PromocashBase(BaseModel):
    Plazo: Optional[int] = Field(
        ge=min_plazo,
        le=max_plazo,
        description=f"term in which the loan will be repaid [{min_plazo},{max_plazo}]",
    )
    Categoria: Optional[PKCategoria] = Field(description="Loan category")
    Unidad: PKUnidad = Field(description="Place where the loan is requested")
    Edad_Solicitud: int = Field(
        ge=min_edad,
        le=max_edad,
        description=f"Age of the client [{min_edad}, {max_edad}]",
    )
    Genero: PKGenero = Field(description="Gender")
    Estado_Civil: Optional[PKEstadoCivil] = Field(description="Marital status")
    Dependientes: int = Field(
        ge=min_dependientes,
        le=max_dependientes,
        description=f"Number of dependents [{min_dependientes}, {max_dependientes}]",
    )
    Estudios: Optional[int] = Field(
        ge=min_estudios,
        le=max_estudios,
        description=f"Customer studies:"
        + "0: 'Sin Estudios',"
        + "1: 'Primaria',"
        + "2: 'Secundaria',"
        + "3: 'Preparatoria',"
        + "4: 'Técnica',"
        + "5: 'Licenciatura',"
        + "6: 'Maestría',"
        + "7: 'Carrera Trunca'",
    )
    Fuente_Ingresos: Optional[PKFuenteDeIngresos] = Field(
        description=f"Source of income"
    )
    CP: int = Field(ge=min_cp, le=max_cp, description="Postal code of the client")
    Anos_Residencia: Optional[int] = Field(
        ge=min_a_resid, le=max_a_resid, description="Years of customer's residence"
    )
    Tipo_Vivienda: Optional[PKTipoVivienda] = Field(description="Type of housing")
    Asentamiento: Optional[PKAsentamiento] = Field(description="Settlement")
    Antiguedad: Optional[int] = Field(
        ge=min_antiguedad, le=max_antiguedad, description="Seniority on the job"
    )
    Ingresos: int = Field(
        ge=min_ingresos, le=max_ingresos, description="Monthtly income without cents"
    )
    Egresos: int = Field(
        ge=min_egresos, le=max_egresos, description="Monthtly outcome without cents"
    )
    Ingreso_Conyuge: Optional[PKIngresoConyuge] = Field(
        description="Type of spouse income"
    )
    CP_Aval: int = Field(
        ge=min_cp_aval, le=max_cp_aval, description="Postal code of the guarantor"
    )
    Monto: int = Field(
        ge=min_monto, le=max_monto, description="Amount requested in loan by the client"
    )
    Ciclo: int = Field(
        ge=min_ciclo, le=max_ciclo, description="current loan cycle, 1 = first loan"
    )
    Score_Ant: float = Field(ge=min_score_ant, le=max_score_ant, description="")
    Monto_Ant: float = Field(ge=min_monto_ant, le=max_monto_ant, description="")
    Frecuencia_Ant: float = Field(
        ge=min_frecuencia_ant, le=max_frecuencia_ant, description=""
    )
    Capacidad_Ant: float = Field(
        ge=min_capacidad_ant, le=max_capacidad_ant, description=""
    )


class PromocashScoreAgt(PromocashBase):
    """Información requerida para calcular la probabilidad de incobrable cuando se tiene la
    información del score del agente.
    """

    Score_Agt: float = Field(g=0.0, le=max_score_agt, description="Agent score")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Plazo": 9,
                    "Categoria": "NV",
                    "Unidad": "Puebla Norte",
                    "Edad_Solicitud": 18,
                    "Genero": "Femenino",
                    "Estado_Civil": "Casado(a)",
                    "Dependientes": 4,
                    "Estudios": 2,
                    "Fuente_Ingresos": "Empleado",
                    "CP": 72820,
                    "Anos_Residencia": 5,
                    "Tipo_Vivienda": "Propia",
                    "Asentamiento": "Casa Sola",
                    "Antiguedad": 1,
                    "Ingresos": 25000,
                    "Egresos": 23000,
                    "Ingreso_Conyuge": "Empleado",
                    "CP_Aval": 72825,
                    "Monto": 10000,
                    "Ciclo": 3,
                    "Score_Ant": 1.01,
                    "Monto_Ant": 7000,
                    "Frecuencia_Ant": 0.08333,
                    "Capacidad_Ant": 556,
                    "Score_Agt": 1.45,
                }
            ]
        }
    }


class PromocashScoreCC(PromocashBase):
    """Información requerida para calcular la probabilidad de incobrable cuando NO se tiene la
    información del score del agente pero si la de Círculo de Crédito.
    """

    Score_CC: int = Field(
        ge=min_score_cc, le=max_score_cc, description="'Círculo de Crédito' score"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Plazo": 9,
                    "Categoria": "NV",
                    "Unidad": "Puebla Norte",
                    "Edad_Solicitud": 18,
                    "Genero": "Femenino",
                    "Estado_Civil": "Casado(a)",
                    "Dependientes": 4,
                    "Estudios": 2,
                    "Fuente_Ingresos": "Empleado",
                    "CP": 72820,
                    "Anos_Residencia": 5,
                    "Tipo_Vivienda": "Propia",
                    "Asentamiento": "Casa Sola",
                    "Antiguedad": 1,
                    "Ingresos": 25000,
                    "Egresos": 23000,
                    "Ingreso_Conyuge": "Empleado",
                    "CP_Aval": 72825,
                    "Monto": 10000,
                    "Ciclo": 1,
                    "Score_Ant": 1.01,
                    "Monto_Ant": 7000,
                    "Frecuencia_Ant": 0.08333,
                    "Capacidad_Ant": 556,
                    "Score_CC": 520,
                }
            ]
        }
    }


class PromocashApprouval(BaseModel):
    approve: int = Field(ge=0, le=1, description="0: Do not approve, 1: Approve")
    default_probability: float = Field(
        ge=0.0, le=1.0, description="Default probability"
    )
    max_amount: int = Field(
        ge=0, le=MAX_AMOUNT, description="Max amount to be approved on credit"
    )
    ponderated: bool = Field(
        description="Indicates if 'max_amount' has been ponderated or not"
    )
    model: str = Field(description="Indicates the used model")

