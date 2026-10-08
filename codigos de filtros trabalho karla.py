import customtkinter as ctk
import numpy as np
import time
import os
from PIL import Image, ImageOps

# Importação para integrar o Matplotlib no CustomTkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Aplicativo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Frequência de Sinal e Filtros / Signal Frequency and Filters")
        self.geometry("1100x850")

        # Descobre a pasta exata onde o arquivo .py está localizado
        self.pasta_script = os.path.dirname(os.path.abspath(__file__))

        # Dicionário de Idiomas (i18n)
        self.idioma_atual = "Português"
        self.traducoes = {
            "Português": {
                "aba_inicio": "Início",
                "aba_pref": "Preferências",
                "aba_dash": "Dashboard",
                "menu_titulo": "Menu Inicial",
                "freq_sinal": "Frequência do Sinal (Hz):",
                "freq_ruido": "Frequência do Ruído (Hz):",
                "amp_ruido": "Amplitude do Ruído:",
                "corte1": "Frequência de Corte 1 (Hz):",
                "corte2": "Frequência de Corte 2 (Hz):",
                "tipo_filtro": "Tipo de Filtro:",
                "filtros": ["Passa-Baixas (LPF)", "Passa-Altas (HPF)", "Passa-Faixa (BPF)", "Rejeita-Faixa (BSF)"],
                "modo_escuro": "Modo Escuro",
                "vis_opcao": "Opção de visualização:",
                "vis_freq": "Frequência / Sinal",
                "vis_circuito": "Circuito",
                "sel_idioma": "Selecione um idioma:",
                "dash_titulo": "Carregar modificações e simular gráficos",
                "btn_iniciar": "Iniciar carregamento",
                "plot_t_title": "Sinal no Domínio do Tempo (Senoides)",
                "plot_t_x": "Tempo (ms)",
                "plot_t_y": "Amplitude",
                "plot_t_in": "Entrada (Sinal + Ruído)",
                "plot_t_out": "Saída (Filtrado)",
                "plot_f_title": "Espectro de Frequência (FFT)",
                "plot_f_x": "Frequência (Hz)",
                "plot_f_y": "Magnitude",
                "plot_f_in": "FFT Entrada",
                "plot_f_out": "FFT Saída (Filtrada)"
            },
            "Inglês": {
                "aba_inicio": "Home",
                "aba_pref": "Preferences",
                "aba_dash": "Dashboard",
                "menu_titulo": "Main Menu",
                "freq_sinal": "Signal Frequency (Hz):",
                "freq_ruido": "Noise Frequency (Hz):",
                "amp_ruido": "Noise Amplitude:",
                "corte1": "Cutoff Frequency 1 (Hz):",
                "corte2": "Cutoff Frequency 2 (Hz):",
                "tipo_filtro": "Filter Type:",
                "filtros": ["Low-Pass (LPF)", "High-Pass (HPF)", "Band-Pass (BPF)", "Band-Stop (BSF)"],
                "modo_escuro": "Dark Mode",
                "vis_opcao": "Display Option:",
                "vis_freq": "Frequency / Signal",
                "vis_circuito": "Circuit",
                "sel_idioma": "Select a language:",
                "dash_titulo": "Load changes and simulate graphs",
                "btn_iniciar": "Start Loading",
                "plot_t_title": "Signal in Time Domain (Sine Waves)",
                "plot_t_x": "Time (ms)",
                "plot_t_y": "Amplitude",
                "plot_t_in": "Input (Signal + Noise)",
                "plot_t_out": "Output (Filtered)",
                "plot_f_title": "Frequency Spectrum (FFT)",
                "plot_f_x": "Frequency (Hz)",
                "plot_f_y": "Magnitude",
                "plot_f_in": "Input FFT",
                "plot_f_out": "Output FFT (Filtered)"
            },
            "Espanhol": {
                "aba_inicio": "Inicio",
                "aba_pref": "Preferencias",
                "aba_dash": "Panel de Control",
                "menu_titulo": "Menú Principal",
                "freq_sinal": "Frecuencia de la Señal (Hz):",
                "freq_ruido": "Frecuencia del Ruido (Hz):",
                "amp_ruido": "Amplitud del Ruido:",
                "corte1": "Frecuencia de Corte 1 (Hz):",
                "corte2": "Frecuencia de Corte 2 (Hz):",
                "tipo_filtro": "Tipo de Filtro:",
                "filtros": ["Paso Bajo (LPF)", "Paso Alto (HPF)", "Paso Banda (BPF)", "Rechazo de Banda (BSF)"],
                "modo_escuro": "Modo Oscuro",
                "vis_opcao": "Opción de visualización:",
                "vis_freq": "Frecuencia / Señal",
                "vis_circuito": "Circuito",
                "sel_idioma": "Seleccione un idioma:",
                "dash_titulo": "Cargar modificaciones y simular gráficos",
                "btn_iniciar": "Iniciar carga",
                "plot_t_title": "Señal en el Dominio del Tiempo (Senoidales)",
                "plot_t_x": "Tiempo (ms)",
                "plot_t_y": "Amplitud",
                "plot_t_in": "Entrada (Señal + Ruido)",
                "plot_t_out": "Salida (Filtrada)",
                "plot_f_title": "Espectro de Frequencia (FFT)",
                "plot_f_x": "Frecuencia (Hz)",
                "plot_f_y": "Magnitud",
                "plot_f_in": "FFT Entrada",
                "plot_f_out": "FFT Salida (Filtrada)"
            }
        }

        # Configuração do Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Barra lateral
        self.barra_lateral = ctk.CTkFrame(self, width=220)
        self.barra_lateral.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Abas principais
        self.janela_das_abas = ctk.CTkTabview(self, width=600)
        self.janela_das_abas.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        self.janela_das_abas.add("Início")
        self.janela_das_abas.add("Preferências")
        self.janela_das_abas.add("Dashboard")

        self.valores_frequencia = [str(i) for i in range(5, 1001, 5)]
        self.valores_amp_ruido = [f"{i/10:.1f}" for i in range(1, 11)]

        self.canvas = None
        self.label_imagem_circuito = None

        # Construção da interface
        self.construir_abalateral()
        self.construir_abaperfil()
        self.construir_abaperferencias()
        self.construir_abasistema()

    def construir_abalateral(self):
        texts = self.traducoes[self.idioma_atual]

        self.titulo = ctk.CTkLabel(self.barra_lateral, text=texts["menu_titulo"], font=ctk.CTkFont(size=22, weight="bold"))
        self.titulo.pack(pady=(20, 10), padx=10)

        # 1. Frequência do Sinal (Padrão: 30 Hz)
        self.label_freq_sinal = ctk.CTkLabel(self.barra_lateral, text=texts["freq_sinal"])
        self.label_freq_sinal.pack(pady=(10, 2), padx=10)
        self.combo_freq_sinal = ctk.CTkComboBox(self.barra_lateral, values=self.valores_frequencia)
        self.combo_freq_sinal.set("30")
        self.combo_freq_sinal.pack(pady=(0, 10), padx=10)

        # 2. Frequência do Ruído (Padrão: 150 Hz)
        self.label_freq_ruido = ctk.CTkLabel(self.barra_lateral, text=texts["freq_ruido"])
        self.label_freq_ruido.pack(pady=(10, 2), padx=10)
        self.combo_freq_ruido = ctk.CTkComboBox(self.barra_lateral, values=self.valores_frequencia)
        self.combo_freq_ruido.set("150")
        self.combo_freq_ruido.pack(pady=(0, 10), padx=10)

        # 3. Amplitude do Ruído (Padrão: 0.4)
        self.label_amp_ruido = ctk.CTkLabel(self.barra_lateral, text=texts["amp_ruido"])
        self.label_amp_ruido.pack(pady=(10, 2), padx=10)
        self.combo_amp_ruido = ctk.CTkComboBox(self.barra_lateral, values=self.valores_amp_ruido)
        self.combo_amp_ruido.set("0.4")
        self.combo_amp_ruido.pack(pady=(0, 10), padx=10)

        # 4. Frequência de Corte 1 (Padrão: 80 Hz)
        self.label_corte1 = ctk.CTkLabel(self.barra_lateral, text=texts["corte1"])
        self.label_corte1.pack(pady=(10, 2), padx=10)
        self.combo_corte1 = ctk.CTkComboBox(self.barra_lateral, values=self.valores_frequencia)
        self.combo_corte1.set("80")
        self.combo_corte1.pack(pady=(0, 10), padx=10)

        # 5. Frequência de Corte 2 (Padrão: 120 Hz)
        self.label_corte2 = ctk.CTkLabel(self.barra_lateral, text=texts["corte2"])
        self.label_corte2.pack(pady=(10, 2), padx=10)
        self.combo_corte2 = ctk.CTkComboBox(self.barra_lateral, values=self.valores_frequencia)
        self.combo_corte2.set("120")
        self.combo_corte2.pack(pady=(0, 10), padx=10)

        # Tipo de Filtro
        self.label_tipo_filtro = ctk.CTkLabel(self.barra_lateral, text=texts["tipo_filtro"], font=ctk.CTkFont(weight="bold"))
        self.label_tipo_filtro.pack(pady=(15, 2), padx=10)
        self.menu_tipo_filtro = ctk.CTkOptionMenu(
            self.barra_lateral, 
            values=texts["filtros"],
            command=self.alterar_tipo_filtro
        )
        self.menu_tipo_filtro.set(texts["filtros"][0])
        self.menu_tipo_filtro.pack(pady=(0, 15), padx=10)

        # Modo Dark/Light
        self.switch_mododark = ctk.CTkSwitch(self.barra_lateral, text=texts["modo_escuro"], command=self.mudar_para_modo_dark)
        self.switch_mododark.pack(pady=(10, 20), padx=10, side="bottom")
        self.switch_mododark.select()

    def construir_abaperfil(self):
        texts = self.traducoes[self.idioma_atual]
        self.aba_inicio = self.janela_das_abas.tab("Início")

        self.frame_topo = ctk.CTkFrame(self.aba_inicio)
        self.frame_topo.pack(fill="x", padx=10, pady=10)

        self.campo_Opcao = ctk.IntVar(value=1)
        self.radio_label = ctk.CTkLabel(self.frame_topo, text=texts["vis_opcao"])
        self.radio_label.pack(side="left", padx=10)
        self.radio_frequencia = ctk.CTkRadioButton(
            self.frame_topo, 
            text=texts["vis_freq"], 
            variable=self.campo_Opcao, 
            value=1,
            command=self.alternar_visualizacao
        )
        self.radio_frequencia.pack(side="left", padx=10)
        self.radio_circuito = ctk.CTkRadioButton(
            self.frame_topo, 
            text=texts["vis_circuito"], 
            variable=self.campo_Opcao, 
            value=2,
            command=self.alternar_visualizacao
        )
        self.radio_circuito.pack(side="left", padx=10)

        # Frame central para os gráficos ou imagem
        self.frame_grafico = ctk.CTkFrame(self.aba_inicio)
        self.frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)

        self.label_imagem_circuito = ctk.CTkLabel(self.frame_grafico, text="")

    def construir_abaperferencias(self):
        texts = self.traducoes[self.idioma_atual]
        self.aba_preferencias = self.janela_das_abas.tab("Preferências")
        self.label_idiomas = ctk.CTkLabel(self.aba_preferencias, text=texts["sel_idioma"])
        self.label_idiomas.pack(pady=(30, 10))
        self.menu_idiomas = ctk.CTkOptionMenu(
            self.aba_preferencias, 
            values=["Português", "Inglês", "Espanhol"],
            command=self.alterar_idioma
        )
        self.menu_idiomas.set(self.idioma_atual)
        self.menu_idiomas.pack()

    def construir_abasistema(self):
        texts = self.traducoes[self.idioma_atual]
        self.aba_sistema = self.janela_das_abas.tab("Dashboard")
        self.label_carregamento = ctk.CTkLabel(self.aba_sistema, text=texts["dash_titulo"], font=ctk.CTkFont(size=18))
        self.label_carregamento.pack(pady=(30, 30))
        self.barra_progresso = ctk.CTkProgressBar(self.aba_sistema, width=400)
        self.barra_progresso.pack(pady=(10, 10)) 
        self.barra_progresso.set(0)
        self.botao_progresso = ctk.CTkButton(self.aba_sistema, text=texts["btn_iniciar"], command=self.carregar)
        self.botao_progresso.pack(pady=(20, 20))

    # --- Busca e Exibição Expandida dos Circuitos ---

    def obter_chave_filtro_atual(self):
        filtros = self.traducoes[self.idioma_atual]["filtros"]
        selecionado = self.menu_tipo_filtro.get()
        if selecionado == filtros[0]: return "lpf"
        if selecionado == filtros[1]: return "hpf"
        if selecionado == filtros[2]: return "bpf"
        if selecionado == filtros[3]: return "bsf"
        return "lpf"

    def encontrar_arquivo_na_pasta(self, chave):
        termos = {
            "lpf": ["passa baixa", "lpf", "passa_baixa"],
            "hpf": ["passa alta", "hpf", "passa_alta"],
            "bpf": ["passa faixa", "bpf", "passa_faixa"],
            "bsf": ["rejeita faixa", "bsf", "rejeita_faixa"]
        }
        
        try:
            arquivos = os.listdir(self.pasta_script)
            for arq in arquivos:
                nome_lower = arq.lower()
                for termo in termos[chave]:
                    if termo in nome_lower and (nome_lower.endswith('.jpg') or nome_lower.endswith('.jpeg') or nome_lower.endswith('.png') or '.' not in arq):
                        caminho_completo = os.path.join(self.pasta_script, arq)
                        if os.path.isfile(caminho_completo):
                            return caminho_completo
        except Exception as e:
            print(f"Erro ao listar pasta: {e}")
        return None

    def recortar_e_ampliar_circuito(self, imagem_pil):
        # Converte para escala de cinzentos para encontrar a área riscada/desenhada
        gray = imagem_pil.convert("L")
        
        # Limiar (threshold) para isolar traços escuros sobre fundo claro
        np_img = np.array(gray)
        mascara = np_img < 220  # Identifica pixels de desenho (não brancos)
        
        if np.any(mascara):
            y_indices, x_indices = np.where(mascara)
            ymin, ymax = y_indices.min(), y_indices.max()
            xmin, xmax = x_indices.min(), x_indices.max()
            
            # Adiciona margem de segurança (padding) de 15px
            padding = 15
            ymin = max(0, ymin - padding)
            ymax = min(np_img.shape[0], ymax + padding)
            xmin = max(0, xmin - padding)
            xmax = min(np_img.shape[1], xmax + padding)
            
            # Recorta exatamente o traçado do circuito
            imagem_pil = imagem_pil.crop((xmin, ymin, xmax, ymax))

        # Calcula o tamanho ideal para preencher a tela mantendo a proporção correta
        largura_orig, altura_orig = imagem_pil.size
        limite_largura, limite_altura = 750, 580
        
        proporcao = min(limite_largura / largura_orig, limite_altura / altura_orig)
        nova_largura = int(largura_orig * proporcao)
        nova_altura = int(altura_orig * proporcao)

        return imagem_pil, (nova_largura, nova_altura)

    def atualizar_imagem_circuito(self):
        chave = self.obter_chave_filtro_atual()
        caminho_arquivo = self.encontrar_arquivo_na_pasta(chave)

        if caminho_arquivo:
            try:
                imagem_orig = Image.open(caminho_arquivo).convert("RGB")

                # Processa o recorte cirúrgico e expansão
                imagem_recortada, tamanho_ampliado = self.recortar_e_ampliar_circuito(imagem_orig)

                # Tratamento para o Modo Escuro vs Modo Claro
                is_dark = self.switch_mododark.get() == 1
                if is_dark:
                    img_light = imagem_recortada
                    img_dark = ImageOps.invert(imagem_recortada)
                else:
                    img_light = imagem_recortada
                    img_dark = imagem_recortada

                imagem_ctk = ctk.CTkImage(
                    light_image=img_light, 
                    dark_image=img_dark, 
                    size=tamanho_ampliado
                )
                self.label_imagem_circuito.configure(image=imagem_ctk, text="")
            except Exception as e:
                self.label_imagem_circuito.configure(image=None, text=f"Erro ao abrir imagem: {e}")
        else:
            self.label_imagem_circuito.configure(image=None, text=f"Imagem do filtro ({chave.upper()}) não encontrada na pasta do projeto.")

    def alternar_visualizacao(self):
        modo = self.campo_Opcao.get()
        if modo == 1:
            self.label_imagem_circuito.pack_forget()
            self.plotar_graficos()
        else:
            if self.canvas is not None:
                self.canvas.get_tk_widget().pack_forget()
            self.atualizar_imagem_circuito()
            self.label_imagem_circuito.pack(expand=True, fill="both", padx=10, pady=10)

    def alterar_tipo_filtro(self, escolha):
        if self.campo_Opcao.get() == 1:
            if self.canvas is not None:
                self.plotar_graficos()
        else:
            self.atualizar_imagem_circuito()

    # --- Filtros Digitais e Matplotlib ---

    def filtro_passa_baixas(self, x, fc, fs=2000):
        dt = 1 / fs
        RC = 1 / (2 * np.pi * fc)
        alpha = dt / (RC + dt)
        y = np.zeros_like(x)
        y[0] = x[0]
        for i in range(1, len(x)):
            y[i] = y[i - 1] + alpha * (x[i] - y[i - 1])
        return y

    def filtro_passa_altas(self, x, fc, fs=2000):
        dt = 1 / fs
        RC = 1 / (2 * np.pi * fc)
        alpha = RC / (RC + dt)
        y = np.zeros_like(x)
        for i in range(1, len(x)):
            y[i] = alpha * (y[i - 1] + x[i] - x[i - 1])
        return y

    def filtro_passa_faixa(self, x, fc1, fc2, fs=2000):
        y = self.filtro_passa_altas(x, fc1, fs)
        y = self.filtro_passa_baixas(y, fc2, fs)
        return y

    def filtro_rejeita_faixa(self, x, fc1, fc2, fs=2000):
        baixa = self.filtro_passa_baixas(x, fc1, fs)
        alta = self.filtro_passa_altas(x, fc2, fs)
        return baixa + alta

    def gerar_e_filtrar_sinais(self):
        try:
            f_sinal = float(self.combo_freq_sinal.get())
            f_ruido = float(self.combo_freq_ruido.get())
            amp_ruido = float(self.combo_amp_ruido.get())
            fc1 = float(self.combo_corte1.get())
            fc2 = float(self.combo_corte2.get())
        except ValueError:
            f_sinal, f_ruido, amp_ruido, fc1, fc2 = 30.0, 150.0, 0.4, 80.0, 120.0

        fs = 2000.0
        duracao = 2.0
        t_total = np.linspace(0, duracao, int(fs * duracao), endpoint=False)

        sinal_puro = np.sin(2 * np.pi * f_sinal * t_total)
        ruido = amp_ruido * np.sin(2 * np.pi * f_ruido * t_total)
        sinal_entrada = sinal_puro + ruido

        tipo_filtro = self.menu_tipo_filtro.get()
        filtros_lista = self.traducoes[self.idioma_atual]["filtros"]

        if tipo_filtro == filtros_lista[0]:
            sinal_saida = self.filtro_passa_baixas(sinal_entrada, fc1, fs)
        elif tipo_filtro == filtros_lista[1]:
            sinal_saida = self.filtro_passa_altas(sinal_entrada, fc1, fs)
        elif tipo_filtro == filtros_lista[2]:
            sinal_saida = self.filtro_passa_faixa(sinal_entrada, fc1, fs)
        elif tipo_filtro == filtros_lista[3]:
            sinal_saida = self.filtro_rejeita_faixa(sinal_entrada, fc1, fc2, fs)
        else:
            sinal_saida = sinal_entrada.copy()

        n = len(t_total)
        freqs_pos = np.fft.rfftfreq(n, d=1/fs)
        fft_entrada = np.abs(np.fft.rfft(sinal_entrada)) * (2.0 / n)
        fft_saida = np.abs(np.fft.rfft(sinal_saida)) * (2.0 / n)

        pontos_vis = int(fs * 0.5)
        return t_total[:pontos_vis], sinal_entrada[:pontos_vis], sinal_saida[:pontos_vis], freqs_pos, fft_entrada, fft_saida

    def plotar_graficos(self):
        t, sinal_in, sinal_out, freqs, fft_in, fft_out = self.gerar_e_filtrar_sinais()
        texts = self.traducoes[self.idioma_atual]

        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        is_dark = self.switch_mododark.get() == 1
        bg_color = "#2b2b2b" if is_dark else "#f0f0f0"
        text_color = "white" if is_dark else "black"
        grid_color = "#555555" if is_dark else "#cccccc"

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5), dpi=100)
        fig.patch.set_facecolor(bg_color)

        ax1.set_facecolor(bg_color)
        ax1.plot(t * 1000, sinal_in, label=texts["plot_t_in"], color="#ff6b6b", alpha=0.7)
        ax1.plot(t * 1000, sinal_out, label=texts["plot_t_out"], color="#4ecdc4", linewidth=2)
        ax1.set_title(texts["plot_t_title"], color=text_color, fontsize=11)
        ax1.set_xlabel(texts["plot_t_x"], color=text_color, fontsize=9)
        ax1.set_ylabel(texts["plot_t_y"], color=text_color, fontsize=9)
        ax1.tick_params(colors=text_color)
        ax1.grid(True, color=grid_color, linestyle="--", alpha=0.5)
        ax1.legend(facecolor=bg_color, edgecolor=grid_color, labelcolor=text_color, fontsize=8)

        ax2.set_facecolor(bg_color)
        ax2.plot(freqs, fft_in, label=texts["plot_f_in"], color="#ff6b6b", alpha=0.7)
        ax2.plot(freqs, fft_out, label=texts["plot_f_out"], color="#1dd1a1", linewidth=2)
        ax2.set_title(texts["plot_f_title"], color=text_color, fontsize=11)
        ax2.set_xlabel(texts["plot_f_x"], color=text_color, fontsize=9)
        ax2.set_ylabel(texts["plot_f_y"], color=text_color, fontsize=9)
        ax2.set_xlim(0, 300)
        ax2.tick_params(colors=text_color)
        ax2.grid(True, color=grid_color, linestyle="--", alpha=0.5)
        ax2.legend(facecolor=bg_color, edgecolor=grid_color, labelcolor=text_color, fontsize=8)

        fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def carregar(self):
        for i in range(100):
            time.sleep(0.015)
            self.barra_progresso.set((i + 1) / 100)
            self.update()

        self.janela_das_abas.set("Início")
        self.alternar_visualizacao()

    def mudar_para_modo_dark(self):
        if self.switch_mododark.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

        if self.campo_Opcao.get() == 1 and self.canvas is not None:
            self.plotar_graficos()
        elif self.campo_Opcao.get() == 2:
            self.atualizar_imagem_circuito()

    def alterar_idioma(self, novo_idioma):
        self.idioma_atual = novo_idioma
        texts = self.traducoes[self.idioma_atual]

        self.titulo.configure(text=texts["menu_titulo"])
        self.label_freq_sinal.configure(text=texts["freq_sinal"])
        self.label_freq_ruido.configure(text=texts["freq_ruido"])
        self.label_amp_ruido.configure(text=texts["amp_ruido"])
        self.label_corte1.configure(text=texts["corte1"])
        self.label_corte2.configure(text=texts["corte2"])
        self.label_tipo_filtro.configure(text=texts["tipo_filtro"])

        idx_filtro = 0
        current_filtro = self.menu_tipo_filtro.get()
        for key, lang_dict in self.traducoes.items():
            if current_filtro in lang_dict["filtros"]:
                idx_filtro = lang_dict["filtros"].index(current_filtro)
                break

        self.menu_tipo_filtro.configure(values=texts["filtros"])
        self.menu_tipo_filtro.set(texts["filtros"][idx_filtro])

        self.switch_mododark.configure(text=texts["modo_escuro"])
        self.radio_label.configure(text=texts["vis_opcao"])
        self.radio_frequencia.configure(text=texts["vis_freq"])
        self.radio_circuito.configure(text=texts["vis_circuito"])
        self.label_idiomas.configure(text=texts["sel_idioma"])
        self.label_carregamento.configure(text=texts["dash_titulo"])
        self.botao_progresso.configure(text=texts["btn_iniciar"])

        if self.campo_Opcao.get() == 1 and self.canvas is not None:
            self.plotar_graficos()

if __name__ == "__main__":
    janela = Aplicativo()
    janela.mainloop()
