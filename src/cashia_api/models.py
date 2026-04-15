from enum import Enum

class PKCategoria(str, Enum):
    """Representa la categoría del prestamo Nuevo (NV) Renovación (RNV)"""

    NV = "NV"
    RNV = "RNV"


class PKUnidad(str, Enum):
    """Representa el tipo de Unidad"""

    cordoba = "Cordoba"
    cuautla = "Cuautla"
    juridico = "Juridico"
    oaxaca = "Oaxaca"
    orizaba = "Orizaba"
    puebla_norte = "Puebla Norte"
    puebla_oriente = "Puebla Oriente"
    puebla_poniente = "Puebla Poniente"
    boca_del_rio = "Boca del Rio"
    pachuca = "Pachuca"
    recuperacion = "Recuperacion"


class PKGenero(str, Enum):
    """Representa el género"""

    femenino = "Femenino"
    masculino = "Masculino"


class PKEstadoCivil(str, Enum):
    """Representa el estado civil"""

    casado = "Casado(a)"
    divorciado = "Divorciado(a)"
    NC = "NC"
    soltero = "Soltero(a)"
    union_libre = "Union Libre"
    viudo = "Viudo(a)"


class PKFuenteDeIngresos(str, Enum):
    """Representa la fuente de ingresos"""

    ambos = "Ambos"
    empleado = "Empleado"
    NC = "NC"
    negocio = "Negocio"


class PKTipoVivienda(str, Enum):
    """Representa el tipo de vivienda"""

    cero = "0"  # TDO Change for correct value
    familia = "Familia"
    pagandola = "Pagandola"
    propia = "Propia"
    rentada = "Rentada"
    nc = "NC"


class PKAsentamiento(str, Enum):
    """Representa el tipo de asentamiento"""

    rural = "Asentamiento Rural"
    urbano = "Asentamiento Urbano"
    casa_sola = "Casa Sola"
    depto_unidad = "Departamento/Unidad Habitacional"


class PKIngresoConyuge(str, Enum):
    """Representa el tipo de ingresos del conyuge"""

    empleado = "Empleado"
    negocio = "Negocio"
    no_aplica = "N/A"
    desconocido = "Desconocido"


