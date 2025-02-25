import boto3  # SDK de AWS para Python
import time
from botocore.exceptions import ClientError
import requests  # Necesario añadir este import que faltaba

class AudioTranslator:
    """
    Clase principal que maneja la traducción de audio utilizando servicios de AWS.
    Integra Transcribe (audio a texto), Translate (traducción) y Polly (texto a audio)
    """
    def __init__(self):
        # Inicialización de los clientes de AWS necesarios
        self.transcribe = boto3.client('transcribe')  # Para transcripción de audio
        self.translate = boto3.client('translate')    # Para traducción de texto
        self.polly = boto3.client('polly')           # Para síntesis de voz
        self.s3 = boto3.client('s3')                 # Para almacenamiento de archivos

    def upload_to_s3(self, file_path, bucket_name, object_name):
        """
        Sube el archivo MP3 original a un bucket de S3.
        Amazon Transcribe necesita que el audio esté en S3 para procesarlo.
        
        Args:
            file_path (str): Ruta local del archivo MP3
            bucket_name (str): Nombre del bucket S3
            object_name (str): Nombre que tendrá el archivo en S3
        """
        try:
            self.s3.upload_file(file_path, bucket_name, object_name)
            return f"s3://{bucket_name}/{object_name}"
        except ClientError as e:
            print(f"Error al subir archivo a S3: {e}")
            return None

    def transcribe_audio(self, job_name, s3_uri):
        """
        Convierte el audio en inglés a texto usando Amazon Transcribe.
        El proceso es asíncrono, por lo que se espera hasta que termine.
        
        Args:
            job_name (str): Identificador único para el trabajo de transcripción
            s3_uri (str): URI del archivo en S3 (s3://bucket-name/file-path)
            
        Returns:
            str: Texto transcrito del audio, o None si hay error
        """
        try:
            # Inicia el trabajo de transcripción
            self.transcribe.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': s3_uri},
                MediaFormat='mp3',
                LanguageCode='en-US'  # Especifica que el audio está en inglés
            )

            # Espera y verifica el estado del trabajo cada 5 segundos
            while True:
                status = self.transcribe.get_transcription_job(TranscriptionJobName=job_name)
                if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                    break
                time.sleep(5)

            # Obtiene el resultado de la transcripción
            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
                response = requests.get(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
                text = response.json()['results']['transcripts'][0]['transcript']
                return text
            return None
        except Exception as e:
            print(f"Error en la transcripción: {e}")
            return None

    def translate_text(self, text):
        """
        Traduce el texto de inglés a español usando Amazon Translate.
        
        Args:
            text (str): Texto en inglés a traducir
            
        Returns:
            str: Texto traducido al español, o None si hay error
        """
        try:
            response = self.translate.translate_text(
                Text=text,
                SourceLanguageCode='en',
                TargetLanguageCode='es'
            )
            return response['TranslatedText']
        except Exception as e:
            print(f"Error en la traducción: {e}")
            return None

    def text_to_speech(self, text, output_file):
        """
        Convierte el texto en español a audio usando Amazon Polly.
        Utiliza la voz de Conchita, que es una voz femenina en español.
        
        Args:
            text (str): Texto en español a convertir en audio
            output_file (str): Ruta donde se guardará el archivo MP3
            
        Returns:
            bool: True si la conversión fue exitosa, False en caso contrario
        """
        try:
            response = self.polly.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId='Conchita',  # Voz en español
                LanguageCode='es-ES'
            )

            with open(output_file, 'wb') as file:
                file.write(response['AudioStream'].read())
            return True
        except Exception as e:
            print(f"Error en la síntesis de voz: {e}")
            return False

def main():
    """
    Función principal que ejecuta el proceso completo de traducción:
    1. Sube el archivo MP3 a S3
    2. Transcribe el audio en inglés a texto
    3. Traduce el texto a español
    4. Convierte el texto traducido a audio en español
    """
    # Configuración inicial - Modificar estos valores según necesidad
    BUCKET_NAME = 'tu-bucket-nombre'    # Nombre de tu bucket en S3
    INPUT_FILE = 'conferencia.mp3'      # Nombre del archivo MP3 en inglés
    OUTPUT_FILE = 'conferencia_espanol.mp3'  # Nombre del archivo MP3 traducido
    
    # Crea una instancia del traductor
    translator = AudioTranslator()
    
    # Proceso paso a paso con verificación de errores en cada etapa
    # 1. Subir archivo a S3
    s3_uri = translator.upload_to_s3(INPUT_FILE, BUCKET_NAME, 'input/' + INPUT_FILE)
    if not s3_uri:
        return
    
    # 2. Transcribir audio a texto
    job_name = f"transcription_{int(time.time())}"  # Nombre único para el trabajo
    english_text = translator.transcribe_audio(job_name, s3_uri)
    if not english_text:
        return
    
    # 3. Traducir texto a español
    spanish_text = translator.translate_text(english_text)
    if not spanish_text:
        return
    
    # 4. Convertir texto traducido a audio
    if translator.text_to_speech(spanish_text, OUTPUT_FILE):
        print(f"Traducción completada. Archivo guardado como: {OUTPUT_FILE}")
    else:
        print("Error en el proceso de traducción")

if __name__ == "__main__":
    main() 