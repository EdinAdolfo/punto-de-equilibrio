import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para calcular el punto de equilibrio
def calcular_punto_equilibrio():
    try:
        precio_venta = float(entry_precio_venta.get())
        costo_variable = float(entry_costo_variable.get())
        gastos_fijos = float(entry_gastos_fijos.get())

        if precio_venta <= costo_variable:
            messagebox.showerror("Error", "El precio de venta debe ser mayor al costo variable")
            return

        # Cálculo del punto de equilibrio
        punto_equilibrio_unidades = gastos_fijos / (precio_venta - costo_variable)
        punto_equilibrio_quetzales = punto_equilibrio_unidades * precio_venta

        # Mostrar los resultados en celdas de entrada
        entry_resultado_unidades.config(state='normal')
        entry_resultado_quetzales.config(state='normal')
        entry_resultado_unidades.delete(0, tk.END)
        entry_resultado_unidades.insert(0, f"{punto_equilibrio_unidades:.2f}")
        entry_resultado_quetzales.delete(0, tk.END)
        entry_resultado_quetzales.insert(0, f"Q{punto_equilibrio_quetzales:.2f}")
        entry_resultado_unidades.config(state='readonly')
        entry_resultado_quetzales.config(state='readonly')

        # Llenar la tabla de datos
        tabla.delete(*tabla.get_children())  # Limpiar la tabla antes de llenarla
        niveles_unidades = [3000, 4000, 5000, 6000, 7000]  # Niveles de producción que vamos a mostrar

        for unidades in niveles_unidades:
            ventas = precio_venta * unidades
            costos_variables = costo_variable * unidades
            margen_contribucion = ventas - costos_variables
            utilidad_perdida = margen_contribucion - gastos_fijos

            # Insertar la fila en la tabla
            if unidades % 2 == 0:
                tabla.insert("", "end", values=(unidades, f"Q{ventas:.2f}", f"Q{costos_variables:.2f}", 
                                                f"Q{margen_contribucion:.2f}", f"Q{gastos_fijos:.2f}", 
                                                f"Q{utilidad_perdida:.2f}"), tags=('evenrow',))
            else:
                tabla.insert("", "end", values=(unidades, f"Q{ventas:.2f}", f"Q{costos_variables:.2f}", 
                                                f"Q{margen_contribucion:.2f}", f"Q{gastos_fijos:.2f}", 
                                                f"Q{utilidad_perdida:.2f}"), tags=('oddrow',))

        return punto_equilibrio_unidades, punto_equilibrio_quetzales

    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese valores válidos.")
        return None, None

# Función para mostrar la gráfica del punto de equilibrio
def mostrar_grafica():
    try:
        precio_venta = float(entry_precio_venta.get())
        costo_variable = float(entry_costo_variable.get())
        gastos_fijos = float(entry_gastos_fijos.get())

        # Cambiamos las unidades a los valores reales que estamos manejando
        unidades = [3000, 4000, 5000, 6000, 7000]  # Unidades desde 3000 hasta 7000
        ingresos = [precio_venta * u for u in unidades]
        costos_totales = [gastos_fijos + (costo_variable * u) for u in unidades]

        # Obtener el punto de equilibrio
        punto_equilibrio_unidades, punto_equilibrio_quetzales = calcular_punto_equilibrio()

        fig, ax = plt.subplots()
        ax.plot(unidades, ingresos, label="Ingresos Totales", color='green')
        ax.plot(unidades, costos_totales, label="Costos Totales", color='red')

        # Anotación del punto de equilibrio exacto
        if punto_equilibrio_unidades is not None:
            ax.axvline(x=punto_equilibrio_unidades, color='orange', linestyle='--', label=f'Punto de Equilibrio ({punto_equilibrio_unidades:.2f} unidades)')
            ax.axhline(y=punto_equilibrio_quetzales, color='blue', linestyle='--', label=f'Punto de Equilibrio (Q{punto_equilibrio_quetzales:.2f})')
            ax.scatter([punto_equilibrio_unidades], [punto_equilibrio_quetzales], color='orange')  # Marcar el punto exacto

        # Ajustar el rango del eje x para reflejar las unidades correctamente
        ax.set_xlim([min(unidades) - 1000, max(unidades) + 1000])  # Expandir un poco los márgenes

        ax.set_xlabel("Unidades")
        ax.set_ylabel("Quetzales")
        ax.set_title("Gráfico del Punto de Equilibrio")
        ax.legend()
        ax.grid(True)

        # Ajuste de la gráfica para que esté en la parte superior derecha
        for widget in graph_frame.winfo_children():
            widget.destroy()  # Limpiar cualquier gráfica anterior

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese valores válidos.")

# Interfaz gráfica
root = tk.Tk()
root.title("Calculadora del Punto de Equilibrio")

# Crear un frame para la gráfica
graph_frame = tk.Frame(root)
graph_frame.grid(row=0, column=2, rowspan=8, padx=10, pady=10)

# Crear un frame para los inputs de datos y darle color verde menta
input_frame = tk.Frame(root, bg='#98FF98', bd=5, relief="solid", padx=20, pady=20)  # Verde menta, bordes más gruesos y padding interno
input_frame.grid(row=0, column=0, rowspan=4, columnspan=2, padx=20, pady=20)  # Padding externo aumentado

# Etiquetas y campos de entrada dentro del frame de inputs
label_precio_venta = tk.Label(input_frame, text="Precio por Unidad (Q):", bg='#98FF98', font=("Arial", 12))
label_precio_venta.grid(row=0, column=0, padx=10, pady=10)
entry_precio_venta = tk.Entry(input_frame, font=("Arial", 12), width=15)
entry_precio_venta.grid(row=0, column=1, padx=10, pady=10)

label_costo_variable = tk.Label(input_frame, text="Costo Variable por Unidad (Q):", bg='#98FF98', font=("Arial", 12))
label_costo_variable.grid(row=1, column=0, padx=10, pady=10)
entry_costo_variable = tk.Entry(input_frame, font=("Arial", 12), width=15)
entry_costo_variable.grid(row=1, column=1, padx=10, pady=10)

label_gastos_fijos = tk.Label(input_frame, text="Gastos Fijos Mensuales (Q):", bg='#98FF98', font=("Arial", 12))
label_gastos_fijos.grid(row=2, column=0, padx=10, pady=10)
entry_gastos_fijos = tk.Entry(input_frame, font=("Arial", 12), width=15)
entry_gastos_fijos.grid(row=2, column=1, padx=10, pady=10)

# Botón para calcular el punto de equilibrio
boton_calcular = tk.Button(input_frame, text="Calcular Punto de Equilibrio", command=calcular_punto_equilibrio, font=("Arial", 12), width=25)
boton_calcular.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Botón para mostrar la gráfica
boton_grafica = tk.Button(root, text="Mostrar Gráfica", command=mostrar_grafica, font=("Arial", 12), width=25)
boton_grafica.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Etiquetas y campos de entrada para mostrar el resultado (en celdas)
label_resultado_unidades = tk.Label(root, text="Punto de Equilibrio (Unidades):", font=("Arial", 12))
label_resultado_unidades.grid(row=5, column=0, padx=10, pady=5)
entry_resultado_unidades = tk.Entry(root, font=("Arial", 12), width=15, state='readonly')
entry_resultado_unidades.grid(row=5, column=1, padx=10, pady=5)

label_resultado_quetzales = tk.Label(root, text="Punto de Equilibrio (Quetzales):", font=("Arial", 12))
label_resultado_quetzales.grid(row=6, column=0, padx=10, pady=5)
entry_resultado_quetzales = tk.Entry(root, font=("Arial", 12), width=15, state='readonly')
entry_resultado_quetzales.grid(row=6, column=1, padx=10, pady=5)

# Tabla de resultados de datos (cuadrícula estilo Excel con bordes negros)
tabla = ttk.Treeview(root, columns=("Unidades", "Ventas", "Costos Variables", "Margen de Contribución", "Costos Fijos", "Utilidad/Pérdida"), show="headings", height=10)
tabla.heading("Unidades", text="Unidades")
tabla.heading("Ventas", text="Ventas (Q)")
tabla.heading("Costos Variables", text="Costos Variables (Q)")
tabla.heading("Margen de Contribución", text="Margen de Contribución (Q)")
tabla.heading("Costos Fijos", text="Costos Fijos (Q)")
tabla.heading("Utilidad/Pérdida", text="Utilidad o Pérdida (Q)")
tabla.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Estilo de cuadrícula con bordes simulados de celdas
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="lightgray", borderwidth=1)  # Estilo de encabezado
style.configure("Treeview", font=("Arial", 12), rowheight=25, borderwidth=1, relief="solid")  # Estilo de celdas con borde sólido
style.map('Treeview', background=[('selected', 'lightblue')], foreground=[('selected', 'black')])

# Ajuste del ancho de las columnas y bordes de las celdas
tabla.column("Unidades", width=100, anchor='center')
tabla.column("Ventas", width=150, anchor='center')
tabla.column("Costos Variables", width=150, anchor='center')
tabla.column("Margen de Contribución", width=150, anchor='center')
tabla.column("Costos Fijos", width=150, anchor='center')
tabla.column("Utilidad/Pérdida", width=150, anchor='center')

# Alternar el color de las filas y simular los bordes de las celdas con líneas negras
tabla.tag_configure('oddrow', background="white")
tabla.tag_configure('evenrow', background="lightblue")

# Iniciar la aplicación
root.mainloop()

