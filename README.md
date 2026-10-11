# simulador-filtro-sinais
Trabalho passado pela professora Karla, que leciona aulas na UDF, sobre tipos de filtro para uma determinada faixa de frequencia e os graficos mostrando a aplicacao do filtro


Simulador de Frequência de Sinal e Filtros
Este projeto é uma aplicação desktop interativa desenvolvida em Python que permite simular sinais senoidais, adicionar ruídos, aplicar diferentes tipos de filtros digitais em tempo real e visualizar os resultados tanto no domínio do tempo quanto no espectro de frequência (FFT), além de alternar para a visualização dos diagramas de circuitos.

📋 Sumário
Visão Geral da Arquitetura
Pontos Principais e Estrutura do Código
Estrutura Gráfica (CustomTkinter)
Suporte a Múltiplos Idiomas (i18n)
Integração e Tratamento das Imagens dos Circuitos (PNG)
Adaptação de Cores (Modo Escuro / Claro)
Base Teórica e Descrição das Imagens dos Circuitos
Explicação e Implementação dos Filtros Digitais
Filtro Passa-Baixas (LPF)
Filtro Passa-Altas (HPF)
Filtro Passa-Faixa (BPF)
Filtro Rejeita-Faixa (BSF)
Processamento de Sinais e Matplotlib
1. Visão Geral da Arquitetura
O código é estruturado de forma orientada a objetos por meio da classe principal Aplicativo(ctk.CTk). Ele integra uma interface moderna em CustomTkinter, manipulação de imagens com Pillow, processamento matemático de sinais com NumPy e renderização gráfica interativa com Matplotlib.

2. Pontos Principais e Estrutura do Código
Estrutura Gráfica (CustomTkinter)
Crédito: A organização geral da interface gráfica (disposição de frames, barra lateral, abas e controles) foi feita inspirada por um vídeo no YouTube. Você pode conferir a referência no link: YouTube - CustomTkinter Tutorial.
Trecho Resumido:
class Aplicativo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Frequência de Sinal e Filtros / Signal Frequency and Filters")
        self.geometry("1100x850")
        
        # Layout principal e Barra lateral
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.barra_lateral = ctk.CTkFrame(self, width=220)
        self.barra_lateral.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Abas principais
        self.janela_das_abas = ctk.CTkTabview(self, width=600)
        self.janela_das_abas.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
Suporte a Múltiplos Idiomas (i18n)
Crédito: A lógica de estruturação e o dicionário de traduções (suportando Português, Inglês e Espanhol) foram feitos pela IA Gemini.
Trecho Resumido:
self.traducoes = {
    "Português": {
        "aba_inicio": "Início",
        "freq_sinal": "Frequência do Sinal (Hz):",
        ...
    },
    "Inglês": { ... }
}
Integração e Tratamento das Imagens dos Circuitos (PNG)
Crédito: O código em Python para buscar arquivos, realizar o recorte automático (cropping baseado em limiar de pixels) e ajustar o tamanho proporcional foi feito pela IA Gemini.
Autoria das Imagens: As imagens PNG dos circuitos utilizadas no projeto foram desenhadas à mão pelo aluno Heitor VB.
Trecho Resumido:
def recortar_e_ampliar_circuito(self, imagem_pil):
    gray = imagem_pil.convert("L")
    np_img = np.array(gray)
    mascara = np_img < 220  # Isola o traçado do desenho
    # Lógica de recorte com margem (padding) e redimensionamento proporcional
    return imagem_pil, (nova_largura, nova_altura)
Adaptação de Cores (Modo Escuro / Claro)
Nota importante: A adaptação de cores para o modo escuro e claro não foi feita pela IA, tendo sido implementada manualmente na lógica junto da estrutura do customTkinter graças ao video do youtube.
3. Base Teórica e Descrição das Imagens do Circuito
As imagens desenhadas à mão pelo aluno Heitor VB representam esquemáticos analógicos clássicos de filtragem:

Filtro Passa-Baixas (LPF): Geralmente construído com um resistor em série e um capacitor em paralelo (
R
C
). Teoricamente, o capacitor apresenta uma reatância inversamente proporcional à frequência (
X
C
=
1
2
π
f
C
). Em frequências elevadas, a reatância cai, desviando o sinal para o terra e deixando passar apenas as baixas frequências.
Filtro Passa-Altas (HPF): Composto por um capacitor em série e um resistor em paralelo. Em baixas frequências, o capacitor bloqueia o sinal (comportando-se como circuito aberto); em altas frequências, sua reatância diminui, permitindo a passagem do sinal para a saída.
Filtro Passa-Faixa (BPF): Formado pela associação em cascata de um circuito passa-altas seguido por um passa-baixas. A teoria baseia-se em permitir apenas uma faixa intermediária delimitada por duas frequências de corte (
f
c
1
 e 
f
c
2
), atenuando tanto as frequências muito baixas quanto as muito altas.
Filtro Rejeita-Faixa (BSF): Também chamado de notch, combina blocos passa-baixas e passa-altas em paralelo. Sua teoria visa eliminar uma faixa específica indesejada de frequências (como ruídos de rede elétrica) e preservar todo o restante do espectro.
4. Explicação e Implementação dos Filtros Digitais
Crédito: As funções matemáticas responsáveis pela filtragem digital dos sinais foram desenvolvidas a partir do código compartilhado pela professora Karla.
1. Filtro Passa-Baixas (LPF)
Implementado como um filtro digital RC de primeira ordem:

def filtro_passa_baixas(self, x, fc, fs=2000):
    dt = 1 / fs
    RC = 1 / (2 * np.pi * fc)
    alpha = dt / (RC + dt)
    y = np.zeros_like(x)
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = y[i - 1] + alpha * (x[i] - y[i - 1])
    return y
2. Filtro Passa-Altas (HPF)
Bloqueia frequências baixas e deixa passar as superiores a 
f
c
:

def filtro_passa_altas(self, x, fc, fs=2000):
    dt = 1 / fs
    RC = 1 / (2 * np.pi * fc)
    alpha = RC / (RC + dt)
    y = np.zeros_like(x)
    for i in range(1, len(x)):
        y[i] = alpha * (y[i - 1] + x[i] - x[i - 1])
    return y
3. Filtro Passa-Faixa (BPF)
Combina em série um passa-altas e um passa-baixas:

def filtro_passa_faixa(self, x, fc1, fc2, fs=2000):
    y = self.filtro_passa_altas(x, fc1, fs)
    y = self.filtro_passa_baixas(y, fc2, fs)
    return y
4. Filtro Rejeita-Faixa (BSF)
Combina em paralelo as respostas de um passa-baixas e um passa-altas:

def filtro_rejeita_faixa(self, x, fc1, fc2, fs=2000):
    baixa = self.filtro_passa_baixas(x, fc1, fs)
    alta = self.filtro_passa_altas(x, fc2, fs)
    return baixa + alta
5. Processamento de Sinais e Matplotlib
O sistema utiliza o NumPy para gerar os sinais no tempo e calcular a Transformada Rápida de Fourier (np.fft.rfft), enquanto o Matplotlib plota os gráficos dinamicamente no painel do CustomTkinter:

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5), dpi=100)
self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
self.canvas.draw()
