# TP Estructuras de Datos

## Integrantes del grupo
- Lucas Binello  
- Felipe Tamaki  
- Catalina Bachetti  
- Kiara Natale  
- Matías Goldschmidt  

## Librerías necesarias para que funcione el código
- **Matplotlib** – instalar con `pip install matplotlib`  
- **NetworkX** – instalar con `pip install networkx`  

## Cómo utilizar con datos personales
Para utilizar el código se debe tener un archivo de nodos (ciudades) con el formato presente en el archivo `nodos.csv`. También se debe contar con un archivo CSV de conexiones (caminos) con el formato presente en `conexiones.csv`. Ambos archivos pueden utilizarse como ejemplo.  
Una vez obtenidos los archivos con el formato adecuado, se deben modificar los nombres de los archivos a cargar mediante las funciones `crear_nodos()` y `crear_conexiones(). Esto se hace en el archivo `A_main.py`, líneas 79 a 96.
```
try:
    crear_nodos("nodos.csv")
    try:
        crear_conexiones("conexiones.csv")
    except FileNotFoundError:
        print("No se encontro el archivo de conexiones")
        raise
    except ValueError as e:
        print(e)
except FileNotFoundError:
    print("No se encontro el archivo de nodos")
    raise 
except ValueError as e:
    print(e)
else:
    menu = tk.Tk()
    menu.title("Menú interactivo")
    menu.geometry("300x140")
```
Además, si se desea cargar solicitudes automaticas debe cambiarse el archivo de `solicitudes.csv` por uno propio siguiendo su mismo formato. Nuevamente, está cargado un archivo a modo de ejemplo
```
def solicitudes_automaticas(): # Realiza todas las solicitudes que encuentre dentro del archivo solicitudes
    solicitudes = leer_solicitudes("solicitudes.csv")
    KPI_solicitudes(solicitudes)
```


Luego de cargar los archivos nuevos, solo debe ejecutarse el programa. Se abrirán los menús interactivos para el usuario.

## Estructuras de datos usadas
- **Diccionarios**: Se utilizaron para almacenar datos en formato clave:valor, facilitando el acceso eficiente.  
- **Listas**: Por su versatilidad y facilidad para manejar colecciones de datos.  
- **Nodos**: Representan ciudades y conexiones.  
- **Sets**: Se usaron en nodos y conexiones para obtener datos únicos y evitar duplicados.  

## Conceptos usados aprendidos en la materia
- Clases  
- Herencia  
- `Matplotlib`  
- `Tkinter`
- DateTime  
- Manejo de errores  
- Magic Methods  

## Herramientas de Python no vistas en clase y conocimientos previos
- Librería `math` (función `ceil`): Para calcular la cantidad de vehículos necesarios para transportar una carga.  
- Librería `networkx`: Permite graficar los grafos y mostrar visualmente los resultados al usuario.  
- Manejo de archivos CSV: Para lectura y posterior uso de datos externos.

## Diseño
El primer paso fue investigar y discutir distintos algoritmos que permitieran encontrar el camino óptimo según los criterios establecidos (menor tiempo y menor costo). Optamos por implementar el algoritmo de Dijkstra.  
Luego, definimos una estrategia para almacenar la información de las conexiones. Creamos una clase llamada `Conexión`, que recibe los datos desde un archivo CSV y los almacena en conjuntos, evitando duplicados.  
En la clase `Nodo`, implementamos un método que devuelve un diccionario donde cada clave representa un modo de transporte y su valor es un conjunto de objetos `Conexión` correspondientes a ese modo.  
También creamos una clase específica para cada tipo de transporte. Todas heredan de la clase base `Transporte`, que incluye los métodos y atributos comunes. Esta clase calcula tiempo, costos fijos por carga y costos por tramo. Las clases hijas redefinen métodos si requieren lógica particular.  
Con las clases listas, desarrollamos funciones para calcular costos y tiempos totales, el algoritmo de Dijkstra y una función que determina el medio de transporte usado en cada tramo.  
Finalmente, desarrollamos la función `KPI`, que calcula dos caminos: el de menor costo (con su tiempo asociado) y el de menor tiempo (con su costo asociado). Esta función usa herramientas anteriores y una función auxiliar, `datos_acumulados`, que recopila datos en forma de lista para graficarlos.

## Dificultades
- La principal dificultad fue encontrar un algoritmo apropiado para resolver de forma óptima el cálculo de KPI.  
- Problemas con Live Share, especialmente desde nuestras casas por fallas de conexión.  
- Dificultades para separar correctamente los costos y aplicar los costos fijos en el momento adecuado del cálculo.  
- Incertidumbre al decidir qué estructuras de datos eran las más adecuadas.  
- Complejidad al comenzar a armar los gráficos y los menús interactivos, ya que no lo habíamos visto en clase.  

## Soluciones
Para resolver el problema principal, implementamos el algoritmo de Dijkstra. Este analiza un grafo ponderado y permite encontrar el trayecto óptimo desde un nodo origen a un nodo destino, eligiendo siempre el nodo no visitado con el menor costo acumulado. A medida que avanza, actualiza las distancias mínimas conocidas y guarda el nodo anterior más eficiente.  
Frente a los problemas con los cálculos de costos, consultamos con profesores y ayudantes, lo que nos permitió entender bien la consigna y llegar al resultado correcto.  
Para generar los gráficos, utilizamos la biblioteca Matplotlib, que permite crear visualizaciones claras y personalizadas. Esta herramienta requiere construir dos listas con valores para los ejes X e Y, y permite agregar títulos, etiquetas y otras personalizaciones útiles para interpretar los resultados.

## Cierre
Este trabajo práctico nos permitió aplicar múltiples conceptos de programación orientada a objetos, manejo de estructuras de datos, visualización y lectura de archivos. Además, nos ayudó a mejorar nuestras habilidades de trabajo en equipo, investigación de herramientas nuevas y resolución de problemas técnicos concretos. Consideramos que logramos integrar de manera sólida los contenidos de la materia en una solución funcional y extensible.
