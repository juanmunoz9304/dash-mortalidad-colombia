# dash-mortalidad-colombia
Repo de dash python para trabajo de analisis de mortalidad en Colombia correspondiente al año 2019.

# Trabajo:
Aplicaciones 1 - Actividad 4: Aplicación web interactiva para el análisis de mortalidad en Colombia - UniSalle - Maestría en IA - Semestre 1

# Autores:

### Juan Sebastian Muñoz
### Jonatán Sebastián Villalba
### Juan David Salazar Rios


# Instrucciones:

```pip install requirements.txt```

### > Punto de partida: app.py

```python app.py```

### > Abrir en:
http://localhost:8050/


### Los datos fueron probados y limpiados usando Colab antes de construirse cada función:
https://colab.research.google.com/drive/1wHvnr58nzpBm8iQgOoc4-SM6y_r0rOcc?usp=sharing


content = """# Análisis de Mortalidad en Colombia - Aplicación Web Interactiva

## Introducción
Dash en Python permite trabajar una aplicación web visual para análisis de datos y estadística. Se diferencia con aplicaciones como Power BI y Tableau por permitir personalización desde el primer momento, dado que cada registro se crea desde cero exactamente como el ingeniero de datos pretende mostrar la información. Dash utiliza por debajo Flask como servidor de aplicaciones y permite encapsular etiquetas HTML para renderizar una página web. Usa Plotly como estándar de visión de datos y es capaz de renderizar figuras, gráficas, tablas entre otros como un conjunto completo de datos. Al ser un sistema servidor web, permite convertir el aplicativo en un servidor web aprovechando la velocidad de montaje de Flask como servidor web.

El proyecto propuesto corresponde a una aplicación web interactiva para el análisis de mortalidad en Colombia, específicamente del año 2019. Se proveen 3 datos para la consolidación de la información:

1. **Datos de mortalidad**: Este dataset en Excel contiene la información cruda de los decesos por diversas causas de la población colombiana clasificada por diferentes parámetros entre los que se destacan principalmente ubicación del deceso, sexo, rango de edades, código muerte, entre otros.
2. **División Político-Administrativa de Colombia**: Permite determinar mediante cruce de códigos la ubicación del deceso e información regional.
3. **Nombres de los códigos de las causas de muerte**: Contiene la información detallada de las múltiples clasificaciones de decesos de la población colombiana, cruzada contra los códigos de muerte.

Con la información mencionada se proponen 10 casos:

1. **Mapa**: Visualización de la distribución total de muertes por departamento en Colombia para el año 2019.
2. **Gráfico de líneas**: Representación del total de muertes por mes en Colombia, mostrando variaciones a lo largo del año.
3. **Gráfico de barras**: Visualización de las 5 ciudades más violentas de Colombia, considerando homicidios (códigos X95, agresión con disparo de armas de fuego y casos no especificados).
4. **Gráfico circular**: Muestra las 10 ciudades con menor índice de mortalidad.
5. **Tabla**: Listado de las 10 principales causas de muerte en Colombia, incluyendo su código, nombre y total de casos (ordenadas de mayor a menor).
6. **Gráfico de barras apiladas**: Comparación del total de muertes por sexo en cada departamento, para analizar diferencias significativas entre géneros.
7. **Histograma**: Distribución de muertes, agrupando los valores de la variable GRUPO EDAD 1 según los rangos definidos en la tabla de referencia para identificar patrones de mortalidad a lo largo del ciclo de vida.

Cada caso debe ser representado como un componente visual en el aplicativo Dash y debe cumplir con los parámetros solicitados. Finalmente, una vez preparado el aplicativo web, se requiere que sea publicado en un servicio de tipo (PaaS) generando un enlace público accesible así como un enlace del repositorio trabajado durante el desarrollo.

## Objetivo
El desarrollo de este aplicativo tiene 3 objetivos principales:

1. Introducir a los estudiantes a Dash y el uso de aplicaciones interactivas web para el análisis de datos.
2. Proponer a los estudiantes resolver un reto de análisis de datos usando un set de información real.
3. Proponer una solución de análisis en la práctica que requiere el ejercicio de publicar la información para un usuario final.

## Estructura del proyecto
Para solucionar el proyecto, hemos optado por empaquetar el proyecto en un venv para instalar de forma aislada los paquetes necesarios. El punto de partida o entrypoint es `app.py`. Se empaquetan los archivos de dataset dentro de una carpeta `/data` y se utiliza una estructura básica basada en patrón repositorio. Se utiliza un DAO para extraer y formatear datos usando `openpyxl` y `pandas`. Un `service` se encarga de la lógica de negocio y tratado de datos. La información retornada se usa para renderizar componentes HTML y figuras de Plotly mediante `dcc.Graph` de Dash.

![Estructura del proyecto en VS Code](screenshots_imgs/estructura_vscode.png)

La carpeta `styles` contiene estilos de tipo clase objeto para inyectar estilos compartidos. Se incluye un `.gitignore`, un `readme.md` y un `requirements.txt` con las librerías principales (`dash`, `openpyxl`, `Flask`, `plotly`, `pandas`). Por último, un `Dockerfile` permite la ejecución mediante contenedores Docker/Podman y facilita el despliegue web.

## Un vistazo a los Requisitos
Esta aplicación está corriendo bajo Python 3 (3.11++). A continuación se muestran todas las librerías instaladas:

![Librerías](screenshots_imgs/librerias.png)

Las librerías resaltadas corresponden a la instalación básica oficial de Dash. Se ha generado una imagen de tipo OCI (Open Container Initiative) capaz de ejecutarse usando Docker o Podman.

## Despliegue
Para el despliegue se utiliza ACA (Azure Container Apps) bajo la nube Azure.

![Diagrama general de despliegue](screenshots_imgs/Diagrama-ACA.png)

El `Dockerfile` provee una máquina Linux ligera con Python. Se exponen el puerto 8050. Puede hacer pull de la imagen: `monolith394/mortalidad-dane:v1`. Azure Container Apps permite ejecutar el servidor con un funcionamiento similar a un lambda (mínimo cero réplicas).

**Pasos para el despliegue:**
1. Buscar **Container Apps** en el portal de Azure.
![Ventana principal ACA](screenshots_imgs/ACA-main.png)
2. Configurar detalles básicos (Resource Group, Región).
![Creando un ACA - Details](screenshots_imgs/creating-aca-1.png)
3. Seleccionar la imagen desde **Docker Hub** (`monolith394/mortalidad-dane:v1`).
![Creando un ACA - Container](screenshots_imgs/creating-aca-2.png)
4. Configurar el **Ingress** (Habilitado, tráfico desde Anywhere, Target Port 8050).
![Creando un ACA - Ingress](screenshots_imgs/creating-aca-3.png)
5. Revisar y Crear. Azure realizará el pull y construcción (aprox. 5 min).
![Creando un ACA - Create](screenshots_imgs/creating-aca-4.png)
6. Acceder a la URL pública en estado Running.
![Creando un ACA - Creado](screenshots_imgs/aca-created.png)

> **Nota sobre el rendimiento:** Debido a la arquitectura de escalado a cero (*Scale-to-Zero*) implementada para optimizar el consumo de recursos, la aplicación puede experimentar una latencia inicial de aprovisionamiento (*Cold Start*). Este proceso implica la instanciación del contenedor y el levantamiento del servidor Flask, lo cual puede tomar entre 1 y 3 minutos en la primera petición.

URL del aplicativo: [https://mortalidad-analisis-app.calmrock-baf448cd.eastus.azurecontainerapps.io](https://mortalidad-analisis-app.calmrock-baf448cd.eastus.azurecontainerapps.io)

## Software
Se utilizó **Google Colab** para desarrollar la parte analítica inicial y **Only Office** para el análisis de hojas de cálculo.
Enlace al Colab: [Análisis Mortalidad Colab](https://colab.research.google.com/drive/1wHvnr58nzpBm8iQgOoc4-SM6y_r0rOcc?usp=sharing)

## Instalación
Repositorio: [https://github.com/juanmunoz9304/dash-mortalidad-colombia.git](https://github.com/juanmunoz9304/dash-mortalidad-colombia.git)

**Ejecución local con Docker:**
```bash
docker pull monolith394/mortalidad-dane:v1
docker run -d -p 8050:8050 --name dashboard-mortalidad monolith394/mortalidad-dane:v1
