import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import wmi
import ctypes
import time

# Cria uma variavél importando a biblioteca wmi para checagem do hardware
c = wmi.WMI()
# Cria uma variável a ser usada na listagem de drivers
vistos = set() 
# Cria uma variável com o comando do massgravedev
commando = "irm https://get.activated.win | iex" 
# Cria uma variável com comando de powershell para atualizar drivers
commando2 = 'powershell -Command "Install-Module -Name PSWindowsUpdate -Force; Import-Module PSWindowsUpdate; Get-WindowsUpdate -Install -AcceptAll -IgnoreReboot"'

main = ctk.CTk(fg_color="#1A1A1A") # Cria a janela principal com cor de fundo
main.title("Hardware Checker by Morningstar") # Define o título da janela
main.iconbitmap(r"icon.ico") # Define o ícone da janela
main.geometry("900x600") # Define o tamanho da janela
main.resizable(False, False) # Define que o tamanho é estático

main.grid_columnconfigure(0, weight=1) # Configura a coluna 0 para ter peso 1, ela fica responsiva com o que tiver dentro dela
main.grid_columnconfigure(1, weight=1)
main.grid_columnconfigure(2, weight=1)

main.grid_rowconfigure(0, weight=1) # Configura a linha 0 para ter peso 1, ela fica responsiva com o que tiver dentro dela
main.grid_rowconfigure(1, weight=1)
main.grid_rowconfigure(2, weight=1)
main.grid_rowconfigure(3, weight=1)
main.grid_rowconfigure(4, weight=1)
main.grid_rowconfigure(5, weight=1)
main.grid_rowconfigure(6, weight=1)

frame1 = ctk.CTkFrame(main, bg_color="transparent", fg_color="transparent") # Faz o primeiro frame da janela
frame1.grid(row=1, column=1, sticky="n") # Define ele da linha 1, coluna 1 e com orientação ao norte

# Cria uma label com o título do app, com tamanho fixo e cor de fundo nos padrões
widget = ctk.CTkLabel(master=frame1, text="Hardware Checker", width=700, fg_color="#ffd700", bg_color="transparent", height=30, text_color="#1A1A1A", corner_radius=20)
widget.pack()

frame2 = ctk.CTkFrame(main, bg_color="transparent", fg_color="transparent") # Cria o segundo frame do app
frame2.grid(row=3, column=1)

# Faz um textbox para que as mensagens do app sejam mostradas em tela
text = ctk.CTkTextbox(master=frame2, fg_color="#333333", width=700, height=400, text_color="#F2F2F2", border_color="#000000", bg_color="transparent")
text.insert(0.0,"""
Selecione sua opção abaixo:\n\n
1. Visualizar especificações de hardware
2. Visualizar versões de drivers
3. Rodar script de ativação
4. Salvar versões de drivers em .txt
5. Atualizar drivers
6. Sair
""")
text.configure(state="disabled") # Configura para que o textbox não seja editável
text.pack()

frame3 = ctk.CTkFrame(main, bg_color="transparent", fg_color="transparent") # Cria o terceiro frame do app para colocar o input e o botão
frame3.grid(row=5, column=1)

def write(event=None):
    tempo = time.strftime('%d.%m.%Y.%H_%M_%S') # Define a data atual com horário em uma variável
    with open(f'drivers_{tempo}.txt', 'w') as file: # Abre um arquivo e escreve dentro dele os drivers atuais do pc
        for driver in c.Win32_PnPSignedDriver(): # Seleciona todos os drivers atuais do computador
            chave = (driver.DeviceName, driver.DriverVersion) # Define a variavel com o driver e a versão
            if chave not in vistos: # Se a chave não tiver na variavel vistos ele escreve o driver no arquivo
                file.write(f"{driver.DeviceName} - {driver.DriverVersion}\n")
                vistos.add(chave) # Adiciona a chave no vistos
        file.close()
        # Aciona uma janela informando a conclusão do arquivo
        CTkMessagebox(main, fg_color="#000000", bg_color="#000000", text_color="#F2F2F2", title="Arquivo gerado", message="Arquivo gerado com sucesso", button_color="#FFD700", button_hover_color="#FFD966", button_text_color="#1A1A1A")

def opcao(event=None): # def para escolher a opção do input do usuario
    ans = entry.get() # define a resposta em uma variavel
    entry.delete(0, "end") # deleta o que estiver escrito na entry
    text.configure(state="normal") # muda o textbox para ser editavel
    text.delete(0.0, "end") # deleta o que estiver no textbox
    try:
        ans = int(ans) # transforma a resposta em inteiro
        match ans:
            case 1: # caso a resposta seja 1, os for loop irão pegar cada informação sobre os dipositivos e escrever no textbox
                text.delete(0.0, "end")
                for placa in c.Win32_Baseboard():
                    text.insert("end",f"""
┌─────────────────────────────────────────────────┐
├Placa Mãe
│    ├─── Nome: {placa.Product}
│    ├─── Fabricante: {placa.Manufacturer}
│    ├─── Serial Number: {placa.SerialNumber}
└─────────────────────────────────────────────────┘
""")
                    
                for cpu in c.Win32_Processor():
                    text.insert("end",f"""
┌─────────────────────────────────────────────────┐
├CPU                                                   
│    ├─── Nome: {cpu.Name}
│    ├─── Núcleos: {cpu.NumberOfCores}
│    ├─── Threads: {cpu.NumberOfLogicalProcessors}
└─────────────────────────────────────────────────┘
""")

                for mem in c.Win32_PhysicalMemory():
                    tamanho_gb = int(mem.Capacity) / (1024**3)
                    text.insert("end",f"""
┌─────────────────────────────────────────────────┐
├Memória RAM
│    ├─── Tamanho: {tamanho_gb:.0f} GB
│    ├─── Frequência: {mem.Speed} MHz
│    ├─── Fabricante: {mem.Manufacturer}
└─────────────────────────────────────────────────┘
""")

                for gpu in c.Win32_VideoController():
                    text.insert("end",f"""
┌─────────────────────────────────────────────────┐
├GPU
│    ├─── Nome: {gpu.Name}
│    ├─── VRAM: {int(gpu.AdapterRAM) / (1024**2)}
└─────────────────────────────────────────────────┘
""")
                
            case 2: # caso escolha 2 vai escrever em tela todos os drivers que tem e suas versões
                text.delete(1.0, "end")
                for driver in c.Win32_PnPSignedDriver():
                    chave = (driver.DeviceName, driver.DriverVersion)
                    if chave not in vistos:
                        text.insert("end",f"{driver.DeviceName} - {driver.DriverVersion}\n")
                        vistos.add(chave)
            case 3: # caso escolha 3 vai executar o script como administrador no powershell
                text.delete(0.0, "end")
                text.insert("end", "\n...CARREGANDO SCRIPT DE ATIVAÇÃO...\n")
                ctypes.windll.shell32.ShellExecuteW(
                    None,           
                    "runas", # executa como adm
                    "powershell.exe",
                    commando,
                    None,
                    1
                )
            case 4: # caso escolha 4 vai executar a função write()
                write()
            case 5: # caso escolha 5 vai executar o comando para atualizar drivers no computador
                ctypes.windll.shell32.ShellExecuteW(
                    None,           
                    "runas",
                    "powershell.exe",
                    commando2,
                    None,
                    1
                )
            case 6: # caso escolha 6 vai abrir um pop-up de janela confirmando a saída do usuario
                msg = CTkMessagebox(main, title="Adeus", option_1="Cancelar", option_3="Sair", fg_color="#000000", bg_color="#000000", text_color="#F2F2F2", title_color="#F2F2F2",message="Obrigado por usar meu script... Até a próxima!", button_color="#FFD700", button_hover_color="#FFD966", button_text_color="#1A1A1A", icon=r"tks.ico")
                response = msg.get()
                
                if response == "Sair":
                    main.destroy()      
                elif response == "Cancelar":
                    msg.destroy() 
                else:
                    print("Click 'Yes' to exit!")
    except:
        text.insert("end","""
\nSelecione sua opção abaixo:\n\n
1. Visualizar especificações de hardware
2. Visualizar versões de drivers
3. Rodar script de ativação
4. Salvar versões de drivers em .txt
5. Atualizar drivers
6. Sair
""")
        text.configure(state="disabled")
    text.insert("end","""
\nSelecione sua opção abaixo:\n\n
1. Visualizar especificações de hardware
2. Visualizar versões de drivers
3. Rodar script de ativação
4. Salvar versões de drivers em .txt
5. Atualizar drivers
6. Sair
""")
    text.configure(state="disabled")

# cria entrada para o input do usuário
entry = ctk.CTkEntry(frame3, placeholder_text="Selecione uma opção acima...", fg_color="#333333", width=620, height=40, text_color="#F2F2F2", border_color=None,bg_color="transparent", corner_radius=10, border_width=0, placeholder_text_color="#F2F2F2")
entry.bind("<Return>", command=opcao) # define que caso o usuario aperte enter vai ser executado a função opcao()
entry.grid(row=0, padx=5)

# cria o botão para executar a função opcao()
button = ctk.CTkButton(frame3,75,40,text="Enviar",text_color="#1A1A1A",bg_color="transparent",fg_color="#FFD700", command=opcao, hover_color="#FFD966",border_width=0, corner_radius=10)
button.grid(row=0, column=2)

main.mainloop() # roda a janela em loop
