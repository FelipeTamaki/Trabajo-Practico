# Read Me
## Estructuras de Datos usadas

* Diccionarios: Se uso esta estructura porque se reconocieron situaciones en donde convenia almacenar los datos en forma clave: valor
* Listas: Se utilizaron debido a su versatilidad y flexibilidad a la hora de manejar datos
* Nodos: Para las ciudades y las conexiones
* Sets: En nodos y conexiones, para obtener datos unicos

## Conceptos usados aprendidos en la materia
* Clases
* Herencia
* Matplotlib
* Tkinter
* DateTime
* Manejo de errores
* Magic 


## Dificultades 
* Nuestra principal dificultad fue encontrar un algoritmo apropiado para encontrar la solucion optima de KPI

* Tuvimos problemas usando el LiveShare, en especial desde nuestras casas porque la conexión no funcionaba correctamente

* Otra dificultad que tuvimos fue como separar los costos en base a las restricciones pedidas, y en que momento aplicar los costos fijos a la sumatoria de costos para que de el resultado correcto

* Tuvimos dificultades a la hora de decidir las estructuras de datos convenient e s



## Soluciones
Para resolver el problema principal, optamos por usar el algoritmo de Dijkstra 

## Diseño
El primer paso que tuvimos como grupo fue buscar y poner en comun diferentes algoritmos para encontrar el camino  optimo en base a lo pedido (menor tiempo y menor costo). Luego de discutirlo, optamos usar el algoritmo de Dijkstra. 
Luego, pensamos la manera de almacenar los datos de las conexiones. Para esto se creo una clase llamado conexion, la cual, recibiendo la informacion del archivo csv, la almacenaba en conjuntos. Esto debido a que no se pueden repeti
Luego, pensamos la manera de almacenar los datos de las conexiones. Para esto se creo una clase llamado conexion, la cual, recibiendo la informacion del archivo csv, la almacenaba en conjuntos. Esto debido a que no se pueden repetir los datos, es decir, hay un solo.
Posteriormente, se busco la manera de diferenciar las conexiones 

## Como Usar
Para utilizar el codigo se debe tener un archivo de nodos ("Ciudades") con el formato presente en el archivo 'nodos.csv'. Se detener también un archivo csv de conexiones ("Caminos") . Para esto se utilizo conexiones, la clase previamente creada.
con el formato presente en el archivo 'conexiones.csv'. Estos archivos pueden utilzarse a modo de prueba. Con estos archivos, puede utilizarse la funcion crear_nodos("nodos.csv") y crear_