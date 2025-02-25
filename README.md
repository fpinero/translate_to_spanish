# Traductor de Audio MP3 (Inglés a Español)

Script en Python que traduce archivos de audio MP3 del inglés al español utilizando servicios de AWS (Amazon Web Services).

## Requisitos Previos

1. **Cuenta AWS**
   - Necesitarás una cuenta activa en AWS
   - Configurar las credenciales de AWS usando uno de estos métodos:
     - AWS CLI (`aws configure`)
     - Variables de entorno:
       ```bash
       export AWS_ACCESS_KEY_ID='tu_access_key'
       export AWS_SECRET_ACCESS_KEY='tu_secret_key'
       export AWS_DEFAULT_REGION='tu_region'
       ```

2. **Python y Dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Bucket S3**
   - Crear un bucket en Amazon S3 donde se almacenarán temporalmente los archivos
   - Tomar nota del nombre del bucket para la configuración

## Configuración

1. Modifica las siguientes variables en el script `translate_audio.py`:
   ```python
   BUCKET_NAME = 'tu-bucket-nombre'    # Nombre de tu bucket en S3
   INPUT_FILE = 'conferencia.mp3'      # Nombre de tu archivo MP3
   OUTPUT_FILE = 'conferencia_espanol.mp3'  # Nombre del archivo traducido
   ```

2. Coloca el archivo MP3 que deseas traducir en el mismo directorio que el script

## Instalación

1. **Crear y activar entorno virtual**
   ```bash
   # Crear entorno virtual con Python 3.12
   python -m venv venv-translator --python=python3.12  # Windows
   python3.12 -m venv venv                 # Linux/Mac

   # Activar entorno virtual
   venv-translator\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el script:
   ```bash
   python translate_audio.py
   ```

2. El script realizará el siguiente proceso:
   - Sube el archivo MP3 a S3
   - Convierte el audio en inglés a texto (Amazon Transcribe)
   - Traduce el texto a español (Amazon Translate)
   - Genera un nuevo archivo de audio en español (Amazon Polly)

## Consideraciones Importantes

- **Formatos Soportados**: 
  - El script está configurado para MP3
  - Amazon Transcribe soporta otros formatos como WAV, FLAC, etc.

- **Calidad de la Traducción**:
  - La precisión dependerá de la calidad del audio original
  - Se recomienda usar audio claro y sin ruido de fondo

- **Limitaciones**:
  - Hay límites en el tamaño de los archivos que pueden procesar los servicios de AWS
  - Consulta la documentación de AWS para conocer los límites específicos

- **Costos**:
  - El uso de los servicios de AWS (Transcribe, Translate, Polly, S3) genera costos
  - Consulta la página de precios de AWS para más detalles

## Servicios AWS Utilizados

- **Amazon S3**: Almacenamiento de archivos
- **Amazon Transcribe**: Conversión de audio a texto
- **Amazon Translate**: Traducción de texto
- **Amazon Polly**: Síntesis de voz

## Solución de Problemas

Si encuentras errores, verifica:
1. Las credenciales de AWS están correctamente configuradas
2. El bucket S3 existe y es accesible
3. El archivo MP3 está en el directorio correcto
4. Tienes permisos suficientes en tu cuenta AWS

## Licencia

Este proyecto está bajo la Licencia MIT.
