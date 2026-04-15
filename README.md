# apipk
Promocash score api

# Como generar la versión para despliegue en windows
1.	Copiar el conjunto de archivos en un nuevo folder con el nombre de la versión por ejemplo apipkV0.7
2.	Colocarse dentro del directorio (en este caso apipkV0.9)
3.	Crear un nuevo ambiente virtual de Python haciendo, por ejemplo:

    python -m venv cashia

4.	Salir del ambiente base (base) haciendo:

    conda deactivate

5.	Activar el nuevo ambiente virtual de Python:

    .\apipkenv\Scripts\activate

6.	Si se tiene el archivo requirements_Windows.txt ejecutar, sino, pasara al paso siguiente: 

    pip install --no-cache-dir -r requirements.txt

1.  Si falta alguna librería instalarla con pip y hacer:

    pip freeze > requirements_Windows.txt

7.	Lanzar el servidor con:

    `uvicorn cashia_api.main:app --reload`

8.	Probar que todo funcione con el notebook test_apipk_from_file

# Como instalar la API en un servidor en windows
1.	Lanzar una consola Anaconda Prompt
2.	Colocarse en el directorio en el que se descomprimió por ejemplo cashia
3.	Crear el ambiente con: `python -m venv apipkenv python=3.11`
4.	Desactivar el ambiente actual: `conda deactivate`
5.	Activar el ambiente venv: `.\apipkenv\Scripts\activate`
6.	Ejecutar: `pip install --no-cache-dir -r requirements.txt`
7.	Lanzar el servidor con:
    a.	En modo pruebas: `uvicorn cashia_api.main:app --reload`
    b.	En modo producción: `uvicorn cashia_api.main:app` 


# Como generar la versión para despliegue en linux

1.  Agregar

        export PYTHONPATH="<mi ruta>/serpicl:$PYTHONPATH"
    
    en el archivvo `.bashrc`

2. hacer source .bashrc

3.	Copiar el conjunto de archivos en un nuevo folder con el nombre de la versión por ejemplo apipkV0.9
4.	Colocarse dentro del directorio (en este caso apipkV0.9)
5.  Desactivar el ambiente python si es necesario haciendo:

    conda deactivate
    
6.	Crear un nuevo ambiente virtual de Python haciendo, por ejemplo:

    conda create -n apipkenv

7.	Activar el nuevo ambiente virtual de Python:

    conda activate apipkenv

8.  instalar pip si es necesario con:

    sudo apt install python3-pip

9.	Ejecutar: 

    pip install --no-cache-dir -r requirements.txt

10.	Lanzar el servidor con:

    `python3 -m uvicorn cashia_api.main:app --reload`


11. Si hace falta alguna o algunas librerías instalarlas hasta que tenga éxito la ejecución del paso anterior

12.	Actualizar el archivo de requerimientos: 

    pip freeze > requirementsLinux.txt

13. Volver a lanzar el servidor si es necesario con

    `python3 -m uvicorn cashia_api.main:app --reload`

11.	Probar que todo funcione con el notebook test_apipk_from_file

# Como instalar la API en un servidor Linux

1.  Colocarse en el directorio en el que se descomprimió por ejemplo cashia
2.  Desactivar el ambiente python si es necesario haciendo:

    `conda deactivate`
    
3.	Crear un nuevo ambiente virtual de Python haciendo, por ejemplo:

    `conda create -n apipkenv python=3.11`

4.	Activar el nuevo ambiente virtual de Python:

    `conda activate apipkenv`

5.	Ejecutar: 

    `pip install --no-cache-dir -r requirements.txt`

6.	Lanzar el servidor con:

    `python3 -m uvicorn cashia_api.main:app`

