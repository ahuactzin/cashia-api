import pandas as pd
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from contextlib import asynccontextmanager

from cashia_core.common_tools.configuration.cashiaconstants import print_version
from cashia_core.common_tools.utils import *

import cashia_model.pm_model_rebuilder as pmmr

from cashia_api.services.daemon import ModelsConfigurationDaemon

from cashia_api.services.daemon import *
from cashia_api.models import *
from cashia_api.schemas import *
from cashia_api.utils import validation_error


import asyncio


config_daemon = ModelsConfigurationDaemon(check_interval_seconds=900)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print_version()

    config_daemon.initialize()
    task = asyncio.create_task(config_daemon.run_forever())

    app.state.config_daemon = config_daemon
    app.state.config_task = task

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

# Server URL
SERVER_URL = "127.0.0.1:8000"
# print_message(f"Current configuration: Ponderation={PONDERATION_MODE}, Ponderation_level={PONDERATION_MODE_LEVEL}, Base_amount={BASE_AMOUNT}",
#               decoration=False, silent=False)
app = FastAPI(lifespan=lifespan)


# Configura los orígenes permitidos (puedes añadir el dominio específico o usar "*" para todos)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://mi-dominio.com",
    # o usa "*" para permitir todos los orígenes
    "*",
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# Permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes, ajusta según sea necesario
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


@app.post("/promocash_score_agt/")
async def promocash_score_agt(item: PromocashScoreAgt, request: Request) -> PromocashApprouval:
    my_item = dict(item)

    now = datetime.now()

    one_entry = {
        "Plazo": [my_item["Plazo"]],
        "Categoria": [my_item["Categoria"]],
        "Unidad": [my_item["Unidad"]],
        "Fecha Inicial": [now],
        "Edad Solicitud": [my_item["Edad_Solicitud"]],
        "Genero": [my_item["Genero"]],
        "Estado Civil": [my_item["Estado_Civil"]],
        "Dependientes": [my_item["Dependientes"]],
        "Estudios": [my_item["Estudios"]],
        "Fuente Ingresos": [my_item["Fuente_Ingresos"]],
        "CP": [my_item["CP"]],
        "Años Residencia": [my_item["Anos_Residencia"]],
        "Tipo Vivienda": [my_item["Tipo_Vivienda"]],
        "Asentamiento": [my_item["Asentamiento"]],
        "Antigüedad": [my_item["Antiguedad"]],
        "Ingresos": [my_item["Ingresos"]],
        "Egresos": [my_item["Egresos"]],
        "Ingreso Conyuge": [my_item["Ingreso_Conyuge"]],
        "CP Aval": [my_item["CP_Aval"]],
        "Monto": [my_item["Monto"]],
        "Ciclo": [my_item["Ciclo"]],
        "Score_Ant": [my_item["Score_Ant"]],
        "Monto_Ant": [my_item["Monto_Ant"]],
        "Frecuencia_Ant": [my_item["Frecuencia_Ant"]],
        "Capacidad_Ant": [my_item["Capacidad_Ant"]],
        "Score Agt": [my_item["Score_Agt"]],
    }

    # Lectura del conjunto de datos de a categorizar
    original_data = pd.DataFrame(one_entry)

    unit = my_item["Unidad"]

    data = original_data.copy()

    # Seleccionar el modelo adecuado
    if my_item["Categoria"] == "NV":
        model_key = NV_AGT
    else:
        model_key = RNV_AGT


    if get_model_regime(unit) == COLD_START_MODEL:
        model_container = cold_start_models_container
    else:
        model_container = complete_models_container

    model = pmmr.ModelRebuilder(
        set(data.columns), model=model_container.model[model_key]
    )

    errors, data = model.prepare_data(data)

    daemon = request.app.state.config_daemon
    models_ponderations = daemon.models_ponderations

    if not errors:
        original_data, returnvalue = model.predict_max_amount(
            data,
            original_data,
            models_ponderations[model_key].copy(),
            model_key,
        )

        print("\n------------- Computation finished --------------")
        return PromocashApprouval(
            approve=returnvalue["approve"],
            default_probability=returnvalue["default_probability"],
            max_amount=returnvalue["max_amount"],
            ponderated=returnvalue["ponderated"],
            model=model_key,
        )
    else:
        return validation_error(errors)


@app.post("/promocash_score_CC/")
async def promocash_score_cc(item: PromocashScoreCC, request: Request) -> PromocashApprouval:
    my_item = dict(item)

    now = datetime.now()

    one_entry = {
        "Plazo": [my_item["Plazo"]],
        "Categoria": [my_item["Categoria"]],
        "Unidad": [my_item["Unidad"]],
        "Fecha Inicial": [now],
        "Edad Solicitud": [my_item["Edad_Solicitud"]],
        "Genero": [my_item["Genero"]],
        "Estado Civil": [my_item["Estado_Civil"]],
        "Dependientes": [my_item["Dependientes"]],
        "Estudios": [my_item["Estudios"]],
        "Fuente Ingresos": [my_item["Fuente_Ingresos"]],
        "CP": [my_item["CP"]],
        "Años Residencia": [my_item["Anos_Residencia"]],
        "Tipo Vivienda": [my_item["Tipo_Vivienda"]],
        "Asentamiento": [my_item["Asentamiento"]],
        "Antigüedad": [my_item["Antiguedad"]],
        "Ingresos": [my_item["Ingresos"]],
        "Egresos": [my_item["Egresos"]],
        "Ingreso Conyuge": [my_item["Ingreso_Conyuge"]],
        "CP Aval": [my_item["CP_Aval"]],
        "Monto": [my_item["Monto"]],
        "Ciclo": [my_item["Ciclo"]],
        "Score_Ant": [my_item["Score_Ant"]],
        "Monto_Ant": [my_item["Monto_Ant"]],
        "Frecuencia_Ant": [my_item["Frecuencia_Ant"]],
        "Capacidad_Ant": [my_item["Capacidad_Ant"]],
        "Score CC": [my_item["Score_CC"]],
    }

    # Lectura del conjunto de datos de a categorizar
    original_data = pd.DataFrame(one_entry)
    data = original_data.copy()

    if my_item["Categoria"] == "NV":
        model_key = "NV_CC"
    else:
        model_key = "RNV_CC"

    unit = my_item["Unidad"]

    if get_model_regime(unit) == COLD_START_MODEL:
        model_container = cold_start_models_container
    else:
        model_container = complete_models_container

    # Leer el modelo disponible
    model = pmmr.ModelRebuilder(
        set(data.columns), model=model_container.model[model_key]
    )

    errors, data = model.prepare_data(data)

    daemon = request.app.state.config_daemon
    models_ponderations = daemon.models_ponderations

    if not errors:
        original_data, returnvalue = model.predict_max_amount(
            data,
            original_data,
            models_ponderations[model_key].copy(),
            model_key,
        )

        print("\n------------- Computation finished --------------")
        return PromocashApprouval(
            approve=returnvalue["approve"],
            default_probability=returnvalue["default_probability"],
            max_amount=returnvalue["max_amount"],
            ponderated=returnvalue["ponderated"],
            model=model_key,
        )
    else:
        return validation_error(errors)




