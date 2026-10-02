import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import pi

# ----------------------------------------------------------------------
# 1. Funções dos Filtros
# ----------------------------------------------------------------------
def filtro_passa_baixa(x, fc, fs=1000):
    dt = 1 / fs
    RC = 1 / (2 * pi * fc)
    alpha = dt / (RC + dt)
    y = np.zeros_like(x)
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = y[i - 1] + alpha * (x[i] - y[i - 1])
    return y

def filtro_passa_alta(x, fc, fs=1000):
    dt = 1 / fs
    RC = 1 / (2 * pi * fc)
    alpha = RC / (RC + dt)
    y = np.zeros_like(x)
    for i in range(1, len(x)):
        y[i] = alpha * (y[i - 1] + x[i] - x[i - 1])
    return y

def filtro_passa_faixa(x, fc1, fc2, fs=1000):
    y = filtro_passa_alta(x, fc1, fs)
    y = filtro_passa_baixa(y, fc2, fs)
    return y

def filtro_rejeita_faixa(x, fc1, fc2, fs=1000):
    baixa = filtro_passa_baixa(x, fc1, fs)
    alta = filtro_passa_alta(x, fc2, fs)
    return baixa + alta

# ----------------------------------------------------------------------
# 2. Interface Gráfica Tkinter
# ----------------------------------------------------------------------
class AppSimulador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Filtros de Sinais")
        self.root.geometry("1100x650")

        # Container Principal
        frame_controles = ttk.LabelFrame(self.root, text="Parâmetros da Simulação", padding=10)
        frame_controles.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        frame_graficos = ttk.Frame(self.root, padding=10)
        frame_graficos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Campos de entrada
        ttk.Label(frame_controles, text="Frequência do sinal (Hz):").pack(anchor=tk.W, pady=2)
        self.entry_freq_sinal = ttk.Entry(frame_controles)
        self.entry_freq_sinal.insert(0, "5")
        self.entry_freq_sinal.pack(fill=tk.X, pady=2)

        ttk.Label(frame_controles, text="Frequência do ruído (Hz):").pack(anchor=tk.W, pady=2)
        self.entry_freq_ruido = ttk.Entry(frame_controles)
        self.entry_freq_ruido.insert(0, "50")
        self.entry_freq_ruido.pack(fill=tk.X, pady=2)

        ttk.Label(frame_controles, text="Amplitude do ruído:").pack(anchor=tk.W, pady=2)
        self.entry_amp_ruido = ttk.Entry(frame_controles)
        self.entry_amp_ruido.insert(0, "0.4")
        self.entry_amp_ruido.pack(fill=tk.X, pady=2)

        ttk.Label(frame_controles, text="Tipo de filtro:").pack(anchor=tk.W, pady=2)
        self.combo_filtro = ttk.Combobox(
            frame_controles, 
            values=["Passa-baixa", "Passa-alta", "Passa-faixa", "Rejeita-faixa"],
            state="readonly"
        )
        self.combo_filtro.current(0)
        self.combo_filtro.pack(fill=tk.X, pady=2)
        self.combo_filtro.bind("<<ComboboxSelected>>", self.atualizar_interface)

        ttk.Label(frame_controles, text="fc1 (Frequência de corte 1):").pack(anchor=tk.W, pady=2)
        self.entry_fc1 = ttk.Entry(frame_controles)
        self.entry_fc1.insert(0, "10")
        self.entry_fc1.pack(fill=tk.X, pady=2)

        # Container dinâmico para fc2 (atualizar_interface exibe/oculta)
        self.lbl_fc2 = ttk.Label(frame_controles, text="fc2 (Frequência de corte 2):")
        self.entry_fc2 = ttk.Entry(frame_controles)
        self.entry_fc2.insert(0, "40")

        # Botões
        self.btn_executar = ttk.Button(frame_controles, text="APLICAR FILTRO", command=self.executar)
        self.btn_executar.pack(fill=tk.X, pady=10)

        self.btn_limpar = ttk.Button(frame_controles, text="LIMPAR GRÁFICOS", command=self.limpar)
        self.btn_limpar.pack(fill=tk.X, pady=2)

        # Inicialização da figura do Matplotlib
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graficos)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.atualizar_interface()

    # Função atualizar_interface() conforme especificado
    def atualizar_interface(self, event=None):
        filtro = self.combo_filtro.get()
        if filtro in ["Passa-faixa", "Rejeita-faixa"]:
            self.lbl_fc2.pack(anchor=tk.W, pady=2, before=self.btn_executar)
            self.entry_fc2.pack(fill=tk.X, pady=2, before=self.btn_executar)
        else:
            self.lbl_fc2.pack_forget()
            self.entry_fc2.pack_forget()

    # Função executar() conforme especificado
    def executar(self):
        try:
            freq_sinal = float(self.entry_freq_sinal.get())
            freq_ruido = float(self.entry_freq_ruido.get())
            amp_ruido = float(self.entry_amp_ruido.get())
            fc1 = float(self.entry_fc1.get())
            filtro = self.combo_filtro.get()

            # Validação para filtros de duas frequências
            if filtro in ["Passa-faixa", "Rejeita-faixa"]:
                fc2 = float(self.entry_fc2.get())
                if fc1 >= fc2:
                    messagebox.showerror("Erro de Validação", "A condição fc1 < fc2 deve ser obedecida!")
                    return
            else:
                fc2 = None

        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira apenas valores numéricos válidos.")
            return

        # Parâmetros de amostragem
        fs = 1000
        t = np.linspace(0, 1, fs)

        # Construção do sinal ruidoso
        sinal = np.sin(2 * pi * freq_sinal * t)
        ruido = amp_ruido * np.sin(2 * pi * freq_ruido * t)
        sinal_ruidoso = sinal + ruido

        # Aplicação do filtro
        if filtro == "Passa-baixa":
            sinal_filtrado = filtro_passa_baixa(sinal_ruidoso, fc1, fs)
        elif filtro == "Passa-alta":
            sinal_filtrado = filtro_passa_alta(sinal_ruidoso, fc1, fs)
        elif filtro == "Passa-faixa":
            sinal_filtrado = filtro_passa_faixa(sinal_ruidoso, fc1, fc2, fs)
        elif filtro == "Rejeita-faixa":
            sinal_filtrado = filtro_rejeita_faixa(sinal_ruidoso, fc1, fc2, fs)
            

        # Atualização dos gráficos
        self.ax1.clear()
        self.ax2.clear()

        # Gráfico da esquerda: Sinal original vs Sinal com interferência
        self.ax1.plot(t, sinal, label="Sinal desejado", color="blue", alpha=0.7)
        self.ax1.plot(t, sinal_ruidoso, label="Sinal + Ruído", color="orange", alpha=0.6)
        self.ax1.set_title("Sinal de Entrada")
        self.ax1.set_xlabel("Tempo (s)")
        self.ax1.set_ylabel("Amplitude")
        self.ax1.legend(loc="upper right")
        self.ax1.grid(True)

        # Gráfico da direita: Sinal filtrado vs Sinal desejado
        self.ax2.plot(t, sinal, label="Referência", color="blue", linestyle="--", alpha=0.5)
        self.ax2.plot(t, sinal_filtrado, label="Sinal Filtrado", color="green")
        self.ax2.set_title("Sinal de Saída")
        self.ax2.set_xlabel("Tempo (s)")
        self.ax2.set_ylabel("Amplitude")
        self.ax2.legend(loc="upper right")
        self.ax2.grid(True)

        self.fig.tight_layout()
        self.canvas.draw()

    # Função limpar() conforme especificado
    def limpar(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.grid(True)
        self.ax2.grid(True)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = AppSimulador(root)
    root.mainloop()