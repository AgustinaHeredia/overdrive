import numpy as np
import soundfile as sf
import tkinter as tk
from tkinter import filedialog, messagebox

def emular_overdrive(input_signal, gain, drive):
    # Validar parámetros
    if gain <= 0:
        raise ValueError("El nivel de ganancia debe ser mayor que 0")
    if not 0 <= drive <= 1:
        raise ValueError("El nivel de saturación debe estar entre 0 y 1")

    # Aplicar la etapa de ganancia
    output_signal = input_signal * gain
    
    # Emular la compresión y saturación
    output_signal = np.tanh(output_signal * drive) / np.tanh(drive)
    
    return output_signal

def aplicar_overdrive(input_file, output_file, nivel_de_ganancia, nivel_de_saturacion):
    try:
        # Cargar el archivo de audio de entrada
        input_data, sample_rate = sf.read(input_file)

        # Aplicar la emulación de overdrive al archivo de audio de entrada
        output_data = emular_overdrive(input_data, nivel_de_ganancia, nivel_de_saturacion)

        # Guardar el archivo de audio de salida
        sf.write(output_file, output_data, sample_rate)

        messagebox.showinfo("Éxito", "Emulación de overdrive completada exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def seleccionar_archivo():
    input_file = filedialog.askopenfilename(title="Seleccionar archivo de audio")
    if input_file:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, input_file)

def procesar_audio():
    input_file = entry_input.get()
    output_file = entry_output.get()
    nivel_de_ganancia = float(entry_gain.get())
    nivel_de_saturacion = float(entry_drive.get())
    aplicar_overdrive(input_file, output_file, nivel_de_ganancia, nivel_de_saturacion)

# Crear ventana principal
root = tk.Tk()
root.title("Emulador de Overdrive")

# Crear widgets
label_input = tk.Label(root, text="Archivo de entrada:")
entry_input = tk.Entry(root, width=50)
button_browse = tk.Button(root, text="Examinar", command=seleccionar_archivo)

label_output = tk.Label(root, text="Archivo de salida:")
entry_output = tk.Entry(root, width=50)

label_gain = tk.Label(root, text="Nivel de ganancia:")
entry_gain = tk.Entry(root, width=10)
entry_gain.insert(0, "3.0")

label_drive = tk.Label(root, text="Nivel de saturación:")
entry_drive = tk.Entry(root, width=10)
entry_drive.insert(0, "0.9")

button_process = tk.Button(root, text="Procesar", command=procesar_audio)

# Posicionar widgets en la ventana
label_input.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
entry_input.grid(row=0, column=1, columnspan=2, padx=10, pady=5)
button_browse.grid(row=0, column=3, padx=10, pady=5)

label_output.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
entry_output.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

label_gain.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
entry_gain.grid(row=2, column=1, padx=10, pady=5)

label_drive.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)
entry_drive.grid(row=2, column=3, padx=10, pady=5)

button_process.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
