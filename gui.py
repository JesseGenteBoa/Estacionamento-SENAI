from pathlib import Path
from time import sleep
from pyautogui import hotkey
from tkinter import Tk, Canvas, Entry, Label, Button, PhotoImage, IntVar, StringVar, Toplevel
from programa import controlar_cancela
import threading
import queue
import veiculo
import conector


acionador = conector.Conector()
veiculos = veiculo.GerenciadorVeiculos()
veiculo_verificado_queue = queue.Queue()
dados_queue = queue.Queue()


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"Assets")


def abrir_tela_cadastro(window, dados_queue):
    nova_janela = Toplevel(window)
    nova_janela.title("Cadastro de Veículo")
    nova_janela.geometry("300x250")

    campos = ["Tipo", "Marca", "Ano", "Cor", "Dono", "placa"]
    entradas = {}

    for i, campo in enumerate(campos):
        label = Label(nova_janela, text=f"{campo}:")
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        entrada = Entry(nova_janela, width=30)
        entrada.grid(row=i, column=2, padx=10, pady=5)
        entradas[campo] = entrada

    def salvar_dados():
        dados = {campo: entrada.get() for campo, entrada in entradas.items()}
        dados_queue.put(dados)
        nova_janela.destroy()
        hotkey("alt", "tab")
            
    botao_salvar = Button(nova_janela, text="Salvar", command=salvar_dados)
    botao_salvar.grid(row=len(campos), column=2, columnspan=2, pady=10)


def verificar_fila(window, dados_queue):
    try:
        dados = dados_queue.get_nowait()
        placa = dados["placa"]
        placa = placa.strip().upper()
        outros_dados = {campo: valor.strip().capitalize() for campo, valor in dados.items() if campo != "Placa"}
        dados_veiculo = list(outros_dados.values())
        dados_veiculo.pop()
        veiculos.cadastrar(placa, dados_veiculo)
    except queue.Empty:
        window.after(500, verificar_fila, window, dados_queue)


def cadastrar_veic(window, dados_queue):
    abrir_tela_cadastro(window, dados_queue)
    verificar_fila(window, dados_queue)


def iniciar_opencv_thread():
    opencv_thread = threading.Thread(target=controlar_cancela, args=(veiculo_verificado_queue, veiculos))
    opencv_thread.daemon = True 
    opencv_thread.start()


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def abrir_manualmente():
    threading.Thread(target=acionador.abrir_cancela).start()
    sleep(4)
    hotkey("alt", "tab")


def fechar_manualmente():
    threading.Thread(target=acionador.fechar_cancela_manualmente).start()
    sleep(4)
    hotkey("alt", "tab")


def interface_grafica():
    window = Tk()

    vagas_disponiveis = IntVar(value=100)
    vagas_carros = IntVar(value=68)
    vagas_motos = IntVar(value=32)
    tipo = StringVar()
    marca = StringVar()
    cor = StringVar()
    ano = StringVar()
    dono = StringVar()


    def dados_veiculo():
        try:
            veiculo_verificado = veiculo_verificado_queue.get_nowait()
            print(veiculo_verificado)
            if veiculo_verificado:
                vagas_disponiveis.set(vagas_disponiveis.get()-1)
                if veiculo_verificado[0] == "Carro":
                    vagas_carros.set(vagas_carros.get()-1)
                else:
                    vagas_motos.set(vagas_motos.get()-1)
                _tipo, _marca, _cor, _ano, _dono = veiculo_verificado
                tipo.set(_tipo)
                marca.set(_marca)
                cor.set(_cor)
                ano.set(_ano)
                dono.set(_dono)  
                veiculo_verificado.clear()
                window.after(10, dados_veiculo)
        except queue.Empty:
            window.after(10, dados_veiculo)
        

    largura_tela = window.winfo_screenwidth()
    altura_tela = window.winfo_screenheight()

    window.geometry(f"{largura_tela+5}x{altura_tela}+0+0")
    window.configure(bg = "#85B2F5")


    canvas = Canvas(
        window,
        bg = "#85B2F5",
        height = 718,
        width = 1366,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        72.0,
        20.99999999999997,
        322.0,
        101.99999999999997,
        fill="#5B5CB4",
        outline="")

    canvas.create_text(
        88.0,
        27.99999999999997,
        anchor="nw",
        text="Vagas Totais:",
        fill="#FFFFFF",
        font=("Malgun Gothic", 16 * -1)
    )

    canvas.create_text(
        88.0,
        68.99999999999997,
        anchor="nw",
        text="Moto:",
        fill="#FFFFFF",
        font=("Malgun Gothic", 16 * -1)
    )

    canvas.create_text(
        202.0,
        68.99999999999997,
        anchor="nw",
        text="Carro:",
        fill="#FFFFFF",
        font=("Malgun Gothic", 16 * -1)
    )

    canvas.create_text(
        204.0,
        27.99999999999997,
        anchor="nw",
        text="100",
        fill="#FFFFFF",
        font=("Malgun Gothic", 16 * -1)
    )

    canvas.create_text(
        259.0,
        68.99999999999997,
        anchor="nw",
        text="68",
        fill="#FFFFFF",
        font=("Malgun Gothic", 16 * -1)
    )
    canvas.create_text(
        144.0,
        68.99999999999997,
        anchor="nw",
        text="32",
        fill="#FFFFFF",
        font=("Malgun Gothic", 16 * -1)
    )



    canvas.create_text(
        72.0,
        120.99999999999997,
        anchor="nw",
        text="Vagas Disponiveis:",
        fill="#FFFFFF",
        font=("Malgun Gothic", 24 * -1)
    )


    canvas.create_text(
        72.0,
        167.99999999999997,
        anchor="nw",
        text="Moto:",
        fill="#FFFFFF",
        font=("Malgun Gothic", 24 * -1)
    )

    canvas.create_text(
        263.0,
        167.99999999999997,
        anchor="nw",
        text="Carro:",
        fill="#FFFFFF",
        font=("Malgun Gothic", 24 * -1)
    )

    label_vd = Label(
        window,
        textvariable=vagas_disponiveis,
        font=("Malgun Gothic", 24 * -1),
        fg="#FFFFFF",
        anchor="center",
        justify="center",
        bg="#85B2F5",
        relief="flat"
    )
    label_vd.place(
        x = 300.0,
        y = 115.0,
        width=50.0,
        height=40.0
    )

    label_vc = Label(
        window,
        textvariable=vagas_carros,
        font=("Malgun Gothic", 24 * -1),
        fg="#FFFFFF",
        anchor="center",
        justify="center",
        bg="#85B2F5",
        relief="flat"
    )
    label_vc.place(
        x = 360.0,
        y = 165.0,
        width=50.0,
        height=40.0
    )

    label_vm = Label(
        window,
        textvariable=vagas_motos,
        font=("Malgun Gothic", 24 * -1),
        fg="#FFFFFF",
        anchor="center",
        justify="center",
        bg="#85B2F5",
        relief="flat"
    )
    label_vm.place(
        x = 170.0,
        y = 165.0,
        width=50.0,
        height=40.0
    )



    canvas.create_text(
        514.0,
        29.99999999999997,
        anchor="nw",
        text="Cancela:",
        fill="#FFFFFF",
        font=("Malgun Gothic", 28 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=1,
        highlightthickness=0,
        command=lambda: abrir_manualmente(),
        relief="ridge",
        cursor="hand2"
    )
    button_1.place(
        x=511.0,
        y=73.99999999999997,
        width=289.0,
        height=52.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=1,
        highlightthickness=0,
        command=lambda: fechar_manualmente(),
        relief="ridge",
        cursor="hand2"
    )
    button_2.place(
        x=511.0,
        y=140.99999999999997,
        width=289.0,
        height=52.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=2,
        highlightthickness=0,
        command=lambda: cadastrar_veic(window, dados_queue),
        relief="solid",
        cursor="hand2"
    )
    button_3.place(
        x=958.0,
        y=73.99999999999997,
        width=320.0,
        height=101.0
    )

    canvas.create_rectangle(
        689.0,
        232.99999999999997,
        1314.0,
        673.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        1066.0,
        381.0,
        anchor="nw",
        text="Cor:",
        fill="#000000",
        font=("K2D Regular", 24 * -1)
    )

    canvas.create_text(
        750.0,
        549.0,
        anchor="nw",
        text="Ano:",
        fill="#000000",
        font=("K2D Regular", 24 * -1)
    )

    canvas.create_text(
        750.0,
        443.0,
        anchor="nw",
        text="Marca:",
        fill="#000000",
        font=("K2D Regular", 24 * -1)
    )

    canvas.create_text(
        912.0,
        263.0,
        anchor="nw",
        text="Dados do Veículo",
        fill="#000000",
        font=("K2D Regular", 24 * -1)
    )

    canvas.create_text(
        750.0,
        338.0,
        anchor="nw",
        text="Tipo:",
        fill="#000000",
        font=("K2D Regular", 24 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        847.5,
        392.5,
        image=entry_image_1
    )
    entry_1 = Label(
        textvariable=tipo,
        bd=0,
        bg="#E2E2FF",
        fg="#000716",
        highlightthickness=0,
        justify="center",
        relief="groove",
        font=("K2D Regular", 20 * -1)
    )
    entry_1.place(
        x=750.0,
        y=369.0,
        width=195.0,
        height=45.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_2 = canvas.create_image(
        1163.5,
        435.5,
        image=entry_image_2
    )
    entry_2 = Label(
        textvariable=ano,
        bd=0,
        bg="#E2E2FF",
        fg="#000716",
        highlightthickness=0,
        justify="center",
        relief="groove",
        font=("K2D Regular", 20 * -1)
    )
    entry_2.place(
        x=1066.0,
        y=412.0,
        width=195.0,
        height=45.0
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_3 = canvas.create_image(
        1163.5,
        566.5,
        image=entry_image_3
    )
    entry_3 = Label(
        textvariable=dono,
        bd=0,
        bg="#E2E2FF",
        fg="#000716",
        highlightthickness=0,
        justify="center",
        relief="groove",
        font=("K2D Regular", 20 * -1)
    )
    entry_3.place(
        x=1066.0,
        y=543.0,
        width=195.0,
        height=45.0
    )

    canvas.create_text(
        1066.0,
        512.0,
        anchor="nw",
        text="Dono:",
        fill="#000000",
        font=("K2D Regular", 24 * -1)
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_4 = canvas.create_image(
        847.5,
        498.5,
        image=entry_image_4
    )
    entry_4 = Label(
        textvariable=marca,
        bd=0,
        bg="#E2E2FF",
        fg="#000716",
        highlightthickness=0,
        justify="center",
        relief="groove",
        cursor="xterm",
        font=("K2D Regular", 20 * -1)
    )
    entry_4.place(
        x=750.0,
        y=475.0,
        width=195.0,
        height=45.0
    )

    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_5 = canvas.create_image(
        847.5,
        603.5,
        image=entry_image_5
    )
    entry_5 = Label(
        textvariable=cor,
        bd=0,
        bg="#E2E2FF",
        fg="#000716",
        highlightthickness=0,
        justify="center",
        relief="groove",
        cursor="xterm",
        font=("K2D Regular", 20 * -1)
    )
    entry_5.place(
        x=750.0,
        y=580.0,
        width=195.0,
        height=45.0
    )

    dados_veiculo()
    #window.after(2, dados_veiculo)
    window.resizable(False, False)
    window.mainloop()
