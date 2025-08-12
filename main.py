import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import wmi
import ctypes
from time import sleep
import time

c = wmi.WMI()
vistos = set()
res = "N"
command = "irm https://get.activated.win | iex"

main = ctk.CTk(fg_color="#1A1A1A")
main.iconbitmap(r"Hardware_Checker\icon.ico")
main.title("Hardware Checker")
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
5. Sair
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
                text.delete(1.0, "end")
                for placa in c.Win32_Baseboard():
                    text.insert(1.0,f"Placa Mãe: {placa.Manufacturer, placa.Product}\n")

                for cpu in c.Win32_Processor():
                    text.insert(1.0,f'CPU: {cpu.Name}\nNúcleos: {cpu.NumberOfCores}\nThreads: {cpu.NumberOfLogicalProcessors}\n')

                for mem in c.Win32_PhysicalMemory():
                    tamanho_gb = int(mem.Capacity) / (1024**3)
                    text.insert(1.0,f"Memória: {tamanho_gb:.0f} GB | Frequência: {mem.Speed} MHz | Fabricante: {mem.Manufacturer}\n")

                for gpu in c.Win32_VideoController():
                    text.insert(1.0,f"GPU: {gpu.Name} | Memória de vídeo (MB): {int(gpu.AdapterRAM) / (1024**2)}\n")
                
            case 2:
                text.delete(1.0, "end")
                for driver in c.Win32_PnPSignedDriver():
                    chave = (driver.DeviceName, driver.DriverVersion)
                    if chave not in vistos:
                        text.insert(1.0,f"{driver.DeviceName} - {driver.DriverVersion}\n")
                        vistos.add(chave)
                text.insert(1.0,f"Deseja")
            case 3:
                text.delete(1.0, "end")
                text.insert(1.0, "Carregando script de ativação massgrave...")
                sleep(2)
                ctypes.windll.shell32.ShellExecuteW(
                    None,           
                    "runas",
                    "powershell.exe",
                    command,
                    None,
                    1
                )
            case 4:
                write()
            case 5:
                main.destroy()
    except:
        text.insert(1.0,"""
===========ENTRADA NÃO ACEITA===========\n
============TENTE  NOVAMENTE============\n\n
1. Visualizar especificações de hardware
2. Visualizar versões de drivers
3. Rodar script de ativação
4. Sair
""")
        text.configure(state="disabled")
    text.configure(state="disabled")

entry = ctk.CTkEntry( master=frame3, placeholder_text="Selecione uma opção acima...", fg_color="#333333", width=620, height=40, text_color="#F2F2F2", border_color=None,bg_color="transparent", corner_radius=10, border_width=0)
entry.bind("<Return>", command=opcao)
entry.grid(row=0, padx=5)

button = ctk.CTkButton(frame3,75,36,text="Enviar",text_color="#1A1A1A",bg_color="transparent",fg_color="#FFD700", command=opcao, hover_color="#FFD966",border_width=0, corner_radius=10)
button.grid(row=0, column=2)

main.mainloop()