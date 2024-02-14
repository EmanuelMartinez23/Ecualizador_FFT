import matplotlib.pyplot as plt
import numpy as np

# Datos del espectro del ecualizador
frequencies = np.linspace(-20000, 20000, 1000)
amplitudes = np.random.rand(1000)  # Puedes reemplazar esto con tus propios datos

# Crear la figura y los ejes
plt.figure(figsize=(10, 6))

# Graficar el espectro del ecualizador
plt.plot(frequencies, amplitudes, label='Espectro del Ecualizador', color='blue')

# Configurar etiquetas y leyenda
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.title('Espectro del Ecualizador')
plt.legend()

# Autoscale en el eje y y ajustar los límites del eje x
plt.autoscale(enable=True, axis='y', tight=True)
plt.xlim(-20000, 20000)

# Mostrar la gráfica
plt.show()
