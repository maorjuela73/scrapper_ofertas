# Pasos para configurar la EC2

## Creación y configuración de la máquina

- Crear la máquina EC2 (las credenciales tienen pass qwerty123)
- Descargar la llave .pem
- Convertir la llave .pem en una .ppk
- Conectarse via Putty o cualquier mecanismo con la llave

## Instalación de programas para la ejecución del código

Los siguientes son los pasos necesarios para configurar el ambiente de ejecución del código

- Instalar en la máquina git con `yum install git`
- Clonar el código
- Instalar miniconda, de la página https://docs.conda.io/en/latest/miniconda.html se descarga un .sh y ese se ejecuta en la máquina
- Cerrar la terminal y abrirla de nuevo
- Crear un nuevo entorno en conda
- Ejecutar el archivo de configuración para descargar los paquetes necesarios `conda env update`
- Instalar libxml `pip3 isntal lxml`
- Instalar el chromedriver según este tutorial https://praneeth-kandula.medium.com/running-chromedriver-and-selenium-in-python-on-an-aws-ec2-instance-2fb4ad633bb5

## Ejecución del código

Asegurarse de existe la carpeta vacante en cada una de las páginas de los proyectos

Para ejecutar cada uno de los scrappers, hay que entrar en cada ruta donde se encuentra el código del scrapper y ejecutar el archivo scrapper.py



