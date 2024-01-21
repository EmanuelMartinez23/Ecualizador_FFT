import numpy as np
import wave
from pydub  import AudioSegment
from scipy.fft import fftfreq, fft
from scipy.io import wavfile
import scipy.io.wavfile as wav
from funciones import guardarMp3, ecualizar,graficar, mp3aWav, guardarWav, convertir_a_mono
from scipy.io.wavfile import write


############################## Principal ##########################

def main(gan1,gan2,gan3,gan4):
    print("Ecualizadando")
    # Converitmos de mp3 a Wav
    rutaWav = mp3aWav('Audios/Entradas/just-relax-11157.mp3')
    # cpnvertimos el audio de dos canales a uno si es que es de dos
    audio_mono = convertir_a_mono(rutaWav)
    # leemos el audio mono para sacar sus datos
    sample_rate , stereo_audio = wav.read(audio_mono)
    # lista de tuplas para las frecuencias
    lista_tuplas_freq = [(0, 200), (200, 1000), (1000, 5000), (5000, 24000)]
    # lista de ganancias introducidad por el usuario
    gan1 = 10**(gan1/10)
    gan2 = 10**(gan2/10)
    gan3 = 10**(gan3/10)
    gan4 = 10**(gan4/10)
    list_gain = [gan1,gan2,gan3,gan4]
    #list_gain = [1,1,1,1]
    # ecualizamos y devolvemos la señal original, la señal modificada, el audio ecualizado y las frequecuencias 
    señalCopy, señal_fft, audio_ecualizado, freq_bins = ecualizar(stereo_audio, sample_rate, lista_tuplas_freq, list_gain)
    audio_ecualizado =  audio_ecualizado.astype(np.int16)
    # guardamos el audio en este caso en dos canales
    guardarWav(audio_ecualizado, sample_rate)
    # guardamos en un canal o por defult
    rutaWav = "Audios/Salidas/audioEcualizado.wav"
    wavfile.write(rutaWav, sample_rate, audio_ecualizado)
    # guardamos en el mp3
    guardarMp3(rutaWav)

    # Graficamos
    graficar(señal_fft,freq_bins, "Audio modificado")
    graficar(señalCopy,freq_bins, "Audio original")

######

main(1,0,1,1)