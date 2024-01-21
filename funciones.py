import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import wave
from scipy.fft import fftfreq, fft
from scipy.io import wavfile
from pydub import AudioSegment
from scipy.signal import windows
#Banda de Subgraves (20 Hz - 200 Hz)
#Banda de Graves (200 Hz - 1 kHz)
#Banda de Medios (1 kHz - 5 kHz)
#Banda de Agudos (5 kHz - 20 kHz)

def ecualizar(señal, sample_rate,lista_tuplas_freq, list_gain):
    # Aplica el cambio en la banda específica con el aumento o reducción de amplitud
    
    señal_fft = np.fft.fft(señal)
    señalCopy = np.fft.fft(señal)
    # obtenemos los rangos de frecuencias a modificar
    freq_range1 = lista_tuplas_freq[0]
    freq_range2 = lista_tuplas_freq[1]
    freq_range3 = lista_tuplas_freq[2]
    freq_range4 = lista_tuplas_freq[3]
    
    # Obtener las frecuencias disponibles en la señal
    freq_bins = np.fft.fftfreq(len(señal), 1 / sample_rate)

    # Identificar los índices de las frecuencias dentro del rango especificado
    # 1
    indices_range = np.where((abs(freq_bins) >= freq_range1[0]) &(abs(freq_bins) <= freq_range1[1]))[0]
    # Aplicar la ganancia en los índices de frecuencias seleccionados
    señal_fft[indices_range] *= list_gain[0]

    #2
    indices_range = np.where((abs(freq_bins) >= freq_range2[0]) &(abs(freq_bins) <= freq_range2[1]))[0]
    # Aplicar la ganancia en los índices de frecuencias seleccionados
    señal_fft[indices_range] *= list_gain[1]
    # Regresar al dominio del tiempo con las frecuencias ya modificadas

    #3
    indices_range = np.where((abs(freq_bins) >= freq_range3[0]) &(abs(freq_bins) <= freq_range3[1]))[0]
    # Aplicar la ganancia en los índices de frecuencias seleccionados
    señal_fft[indices_range] *= list_gain[2]
    # Regresar al dominio del tiempo con las frecuencias ya modificadas

    #4
    indices_range = np.where((abs(freq_bins) >= freq_range4[0]) &(abs(freq_bins) <= freq_range4[1]))[0]
    # Aplicar la ganancia en los índices de frecuencias seleccionados
    señal_fft[indices_range] *= list_gain[3]

    # Regresar al dominio del tiempo con las frecuencias ya modificadas
    señal_ecualizada = np.fft.ifft(señal_fft)
    print("Diferencia máxima entre señal original y ecualizada:", np.max(np.abs(señal - señal_ecualizada.real)))
    #imprimir_numeros_complejos(señal_ecualizada)
    # Devolvemos la señal sin modificar y la señal modificada y las frecuencias que vamos a utilizar para modificar 
    return np.abs(señalCopy),np.abs(señal_fft), señal_ecualizada.real, freq_bins



def graficar(señal_fft,frecuencias):
    plt.figure(figsize=(10, 6))
    #plt.subplot(2, 1, 1)
    plt.title('Señal original')
    #plt.plot(frecuencias, señalCopy)
    #plt.subplot(2, 1, 2)
    #plt.title('Señal despues de la ganancia')
    # Creamos una mascara para eliminar los ceros cuando cortamos esas frecuencias
    mask = np.ma.masked_where(señal_fft == 0, señal_fft)
    frecuencias = np.abs(frecuencias)
    mask = np.abs(mask)

    frecuencias_espejadas = np.concatenate([-frecuencias[::-1], frecuencias])
    mask_espejado = np.concatenate([mask[::-1], mask])
    
    plt.plot(frecuencias_espejadas, mask_espejado)
    plt.show()


def mp3aWav(ruta_mp3):
    # Ruta donde se guardará el archivo WAV
    ruta_wav = 'Audios/Entradas/audioWav.wav'  
    # Cargar el archivo MP3 y convertirlo a WAV
    audio, samplerate = sf.read(ruta_mp3)
    sf.write(ruta_wav, audio, samplerate, format='WAV', endian='LITTLE', subtype='PCM_16')
    return ruta_wav



def guardarWav(audio_ecualizado, sample_rate):
     # Configuración de parámetros del archivo WAV
    sample_width = 2  # Tamaño en bytes de cada muestra (16 bits)
    channels = 2       # Número de canales (2 para estéreo)
    frame_rate = sample_rate # Tasa de muestreo en Hz
    duration = 2      # Duración del audio en segundos
    # Crear un arreglo de dos dimensiones para los datos estéreo
    stereo_data = np.column_stack((audio_ecualizado,audio_ecualizado))

    # Crear objeto de archivo WAV
    wave_file = wave.open("Audios/Salidas/audioEcualizado_DosCanales.wav", "w")
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(frame_rate)
    wave_file.setnframes(int(frame_rate * duration))
    wave_file.setcomptype("NONE", "not compressed")

    # Escribir los datos estéreo en el archivo WAV
    wave_file.writeframes(stereo_data.tobytes())
    # Cerrar el archivo WAV
    wave_file.close()


def convertir_a_mono(archivo_entrada):
    # Leer el archivo de audio WAV
    sample_rate, data_stereo = wavfile.read(archivo_entrada)

    # Verificar si ya es mono (un solo canal)
    if len(data_stereo.shape) == 1:
        print("El archivo ya es mono. No se requiere conversión.")
        return

    # Encontramos el audio
    audio = AudioSegment.from_wav(archivo_entrada)
    # Seleccionamos solo un canal
    audio_mono = audio.set_channels(1)
    # guardamos el archivo ya de un solo canal
    # Guardar el archivo de audio mono
    audio_mono.export("Audios/Entradas/audio_mono.wav", format="wav")

    return "Audios/Entradas/audio_mono.wav"


def guardarMp3(rutaWav):
    wavs =  AudioSegment.from_wav(rutaWav)
    wavs.export("Audios/Salidas/audioFinalMP3.mp3", format="mp3")