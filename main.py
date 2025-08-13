import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import wmi
import ctypes
import time

c = wmi.WMI()
vistos = set()
res = "N"
commando = "irm https://get.activated.win | iex"
commando2 = 'powershell -Command "Install-Module -Name PSWindowsUpdate -Force; Import-Module PSWindowsUpdate; Get-WindowsUpdate -Install -AcceptAll -IgnoreReboot"'

main = ctk.CTk(fg_color="#1A1A1A")
main.title("Hardware Checker by Morningstar")
main.iconbitmap(r"icon.ico")
main.geometry("900x600")
main.resizable(False, False)

main.grid_columnconfigure(0, weight=1)
main.grid_columnconfigure(1, weight=1)
main.grid_columnconfigure(2, weight=1)

main.grid_rowconfigure(0, weight=1)
main.grid_rowconfigure(1, weight=1)
main.grid_rowconfigure(2, weight=1)
main.grid_rowconfigure(3, weight=1)
main.grid_rowconfigure(4, weight=1)
main.grid_rowconfigure(5, weight=1)
main.grid_rowconfigure(6, weight=1)

frame1 = ctk.CTkFrame(main, bg_color="transparent", fg_color="transparent")
frame1.grid(row=1, column=1, sticky="n")

widget = ctk.CTkLabel(master=frame1, text="Hardware Checker", width=700, fg_color="#ffd700", bg_color="transparent", height=30, text_color="#1A1A1A", corner_radius=20)
widget.pack()

frame2 = ctk.CTkFrame(main, bg_color="transparent", fg_color="transparent")
frame2.grid(row=3, column=1)

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
text.configure(state="disabled")
text.pack()

frame3 = ctk.CTkFrame(main, bg_color="transparent", fg_color="transparent")
frame3.grid(row=5, column=1)

def write(event=None):
    tempo = time.strftime('%d.%m.%Y.%H_%M_%S')
    with open(f'drivers_{tempo}.txt', 'w') as file:
        for driver in c.Win32_PnPSignedDriver():
            chave = (driver.DeviceName, driver.DriverVersion)
            if chave not in vistos:
                file.write(f"{driver.DeviceName} - {driver.DriverVersion}\n")
                vistos.add(chave)
        file.close()
        CTkMessagebox(main, fg_color="#000000", bg_color="#000000", text_color="#F2F2F2", title="Arquivo gerado", message="Arquivo gerado com sucesso", button_color="#FFD700", button_hover_color="#FFD966", button_text_color="#1A1A1A")

def opcao(event=None):
    ans = entry.get()
    entry.delete(0, "end")
    text.configure(state="normal")
    text.delete(0.0, "end")
    try:
        ans = int(ans)
        match ans:
            case 1:
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
                
            case 2:
                text.delete(1.0, "end")
                for driver in c.Win32_PnPSignedDriver():
                    chave = (driver.DeviceName, driver.DriverVersion)
                    if chave not in vistos:
                        text.insert("end",f"{driver.DeviceName} - {driver.DriverVersion}\n")
                        vistos.add(chave)
            case 3:
                text.delete(0.0, "end")
                text.insert("end", "\n...CARREGANDO SCRIPT DE ATIVAÇÃO...\n")
                ctypes.windll.shell32.ShellExecuteW(
                    None,           
                    "runas",
                    "powershell.exe",
                    commando,
                    None,
                    1
                )
            case 4:
                write()
            case 5:
                ctypes.windll.shell32.ShellExecuteW(
                    None,           
                    "runas",
                    "powershell.exe",
                    commando2,
                    None,
                    1
                )
            case 6:
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

entry = ctk.CTkEntry(frame3, placeholder_text="Selecione uma opção acima...", fg_color="#333333", width=620, height=40, text_color="#F2F2F2", border_color=None,bg_color="transparent", corner_radius=10, border_width=0, placeholder_text_color="#F2F2F2")
entry.bind("<Return>", command=opcao)
entry.grid(row=0, padx=5)

button = ctk.CTkButton(frame3,75,40,text="Enviar",text_color="#1A1A1A",bg_color="transparent",fg_color="#FFD700", command=opcao, hover_color="#FFD966",border_width=0, corner_radius=10)
button.grid(row=0, column=2)

main.mainloop()