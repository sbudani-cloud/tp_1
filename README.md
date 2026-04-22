# Luliify
Este proyecto es un reproductor de música, basandose en Spotify para algunas ideas de sus funcionamientos, y prestandole atención a la interfaz. 

***
## Bitácora
8/04
Pensé como queria que se vea la interfaz y empece a organizar los frames y poner las cosas en su lugar, aunque todavia no funcionen.
Después decoré y logré hacer funcionar el botón de play.

***
9/05
Cree una sección para las playlist e hice funcionar los botones de añadir y eliminar canciones a la playlist. Por ahora las canciones en la playlist no se pueden reproducir desde ahí.
Hice funcionar el botón de anterior, siguiente y loop. También hice que cuanto una canción termine la siguiente en la lista funcione automáticamente. Por ahora solo funciona con la lista de canciones, y no con la lista de playlist.
Por último, hice que el botón de ir a la canción anterior reinice la canción si ya esta  empezada (más de 3 segundos sonando), y si no, que si vaya a la anterior. (Funciona como el botón de stop)
Siento que me va a costar lo de el tema de seleccionar de dos treeviews diferentes, pero voy a encargarme de eso la siguiente clase.
Tengo planeado, además, poner las fotos del album de forma decorada, y que sean un gif que vaya girando y que si queres agregar más de una vez una canción a una playlist, te de un aviso antes de que el usuario decida si quiere hacerlo igual o no. También que si haces doble click en una canción se reproduzca como si fuera apretar el botón play.
Otra cosa que quiero hacer es un .json donde se guarde la playlist que hayas creado, y una carpeta para poner las fotos de los albums.

Agregué imagenes para los botones loop y aleatorio, los demas quiero que queden como botones normales porque me parecen lindos asi. El aleatorio solo funciona visualmente pero no hace nada. También ya hice lo del doble click en las canciones.
También quiero agregar en un futuro una configuración que te permita cambiar el estilo y crear estilos de mas colores. Y un botón para "Abrir archivo..." y poder añadir canciones desde ahí.

***
13/04
Cree las imagenes para los albums y los hice funcionar. Estoy considerando no hacer mi idea de los gifs porque mi compu es malisima y no aguanta mucho, entonces prefiero dejar el programa lo mas light posible, pero más adelante me la pienso, por ahora quiero hacer cambios más urgentes como hacer que la playlist funcione y el botón para que las canciones se reproduzcan aleatoriamente (para eso quiero que sea como spotify y que una cancion no se repita hasta que todas se hayan escuchado al menos una vez. probablemente haga una lista y vaya sacando las canciones q suenan, y que se vuelva a llenar cuando se quede vacia).

***
16/04
Hoy planeo hacer las cosas que son mas escenciales que funcionen, que son la playlist y el botón de aleatorio. Quiero agregar una barra de busqueda, aunque hayan pocas canciones. También quiero un cosito para aumentar y bajar el volumen.
El botón de aleatorio funciona. Use mucho ChatGPT porque pense que se entregaba hoy, pero entiendo lo que ChatGPT me dijo, asi que está bien.
Agregué temas e hice que se pueda mover la progress bar a distintas partes de la canción. El único bug que encontré es que cuando activo el loop y muevo la barra y termina la canción hace una cosa rara. Logré arreglar ese bug.
Cosas a hacer: que el botón de anterior funcione bien en el modo aleatorio, cambiar los pngs para que el estilo azul se vea bien, hacer nuevos botones de loop y aleatorio para versión azul.
Hice que funcione la playlist y que se guarde en un json.

Lista de cosas para hacer:
-Cambiar botones de loop y aleatorio cuando cambie el estilo.
-Mejorar botón anterior en modo aleatorio.
-Arrastrar para reordenar canciones en la playlist.
-Barra de búsqueda.
-Botón “Abrir archivo…” para importar canciones.
-Aviso si querés agregar una canción duplicada a la playlist.
-Volumen.
-Crear más estilos.

***
21/04
Hice lo de que cambie el boton de loop y aleatorio con el estilo, y mejoré el botón de anterior en modo aleatorio. También hice que se puedan reordenar las canciones en la playlist.
Agregué un slider para poder cambiar el volumen.

Falta:
-Aviso si querés agregar una canción duplicada a la playlist. 
-Volumen. 
-Foto para album desconocido
-Crear más estilos.