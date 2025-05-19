import serial
import time
import os
from colorama import init, Fore, Style
import readline  # or pyreadline3 on Windows

COMMANDS = ['recraw', 'playraw', 'record', 'sniffing', 'jamming', 'exit', 'help']

def completer(text, state):
    matches = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    if state < len(matches):
        return matches[state]
    return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

init(autoreset=True)

def select_esp32_port():
    ports = list(serial.tools.list_ports.comports())
    esp_keywords = ['cp210', 'ch340', 'silicon labs', 'usb serial', 'esp32']

    esp_ports = [
        port for port in ports
        if any(keyword in port.description.lower() or keyword in port.manufacturer.lower()
               for keyword in esp_keywords if port.manufacturer)
    ]

    if not esp_ports:
        print(Fore.RED + "❌ No ESP32 devices found.")
        exit(1)

    if len(esp_ports) == 1:
        print(Fore.YELLOW + f"✅ ESP32 Detected: {esp_ports[0].device}")
        return esp_ports[0].device

    print(Fore.CYAN + "Multiple possible ESP32 devices found:")
    for i, port in enumerate(esp_ports):
        print(f"[{i}] {port.device} - {port.description}")

    choice = input(Fore.GREEN + "Select port number: ").strip()
    if choice.isdigit() and int(choice) < len(esp_ports):
        return esp_ports[int(choice)].device
    else:
        print(Fore.RED + "Invalid selection.")
        exit(1)

BAUD_RATE = 115200

commands = {
    "recraw": "Record raw data",
    "playraw": "Play raw data",
    "record": "Record decoded signal",
    "sniffing": "Sniff packets",
    "jamming": "Start jamming"
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + """
  _________.__                .___            _________ .__       .__
 /   _____/|  |__ _____     __| _/______  _  _\\_   ___ \\|__|_____ |  |__   ___________
 \\_____  \\ |  |  \\\\__  \\   / __ |/  _ \\ \\/ \\/ /    \\  \\/|  \\____ \\|  |  \\_/ __ \\_  __ \\
 /        \\|   Y  \\/ __ \\_/ /_/ (  <_> )     /\\     \\___|  |  |_> >   Y  \\  ___/|  | \\/
/_______  /|___|  (____  /\\____ |\\____/ \\/\\_/  \\______  /__|   __/|___|  /\\___  >__|
        \\/      \\/     \\/      \\/                     \\/   |__|        \\/     \\/
    """)
    print(Fore.YELLOW + "                       SHcipher - Atmega based subghz tool\n")

def help_menu():
    print(Fore.CYAN + Style.BRIGHT + "{:<12}{}".format("Command", "Description"))
    print(Fore.CYAN + Style.BRIGHT + "-"*30)
    for cmd, desc in commands.items():
        print("{:<12}{}".format(cmd, desc))
    print("{:<12}{}".format("exit", "Exit the console"))
    print("{:<12}{}".format("clear", "Clear the screen"))
    print("{:<12}{}".format("help", "Show this menu"))

def interactive_console(ser):
    banner()    


    while True:
        try:
            cmd = input(Style.BRIGHT + Fore.YELLOW + "shciphr1 > ").strip()


            if cmd == "exit":
                print(Fore.YELLOW + "Exiting...")
                break
            elif cmd == "clear":
                clear()
                banner()
                help_menu()
                continue
            elif cmd == "help":
                help_menu()
                continue
            elif cmd[0:6] == "recraw":
                ser.reset_input_buffer()
                ser.write((cmd + "\n").encode())
                time.sleep(0.5)

                # Read for a fixed time or line count
                read_start = time.time()
                while time.time() - read_start < 2:
                    if ser.in_waiting:
                        line = ser.readline().decode(errors='replace').strip()
                        print(line)
                    else:
                        time.sleep(0.1)
            elif cmd[0:3] == "jam":
                print(Fore.LIGHTBLUE_EX + "[*] Jammer started. Press Ctrl+C to stop.")
                ser.reset_input_buffer()
                ser.write((cmd + "\n").encode())
                time.sleep(0.5)

                try:
                    while True:
                        if ser.in_waiting:
                            line = ser.readline().decode(errors='replace').strip()
                            print(line)
                        else:
                            time.sleep(0.05)  # Avoid CPU overuse
                except KeyboardInterrupt:
                    print(Fore.YELLOW + "\n[*] Jamming stopped.")
                    ser.write(("jam_stop"+"\n").encode())  # Optional: tell ESP to stop
 
            elif cmd == "analyzer":
                print(Fore.LIGHTBLUE_EX + "[*] Analyzer started. Press Ctrl+C to stop.")
                ser.reset_input_buffer()
                ser.write(b"analyzer\n")  # This tells the ESP to start sending data

                try:
                    while True:
                        if ser.in_waiting:
                            line = ser.readline().decode(errors='replace').strip()
                            print(line)
                        else:
                            time.sleep(0.05)  # Avoid CPU overuse
                except KeyboardInterrupt:
                    print(Fore.YELLOW + "\n[*] Analyzer stopped.")
                    ser.write(b"analyzer_stop\n")  # Optional: tell ESP to stop


            else:
                print(Fore.RED + f"Unknown command: {cmd}")

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nExiting on user interrupt.")
            break
        except Exception as e:
            print(Fore.RED + f"[-] " + Fore.RESET + f"Error: {e}")
            break

def main():
    try:

        ser = serial.Serial("COM7", BAUD_RATE, timeout=1)
        time.sleep(2)
        clear()
        interactive_console(ser)

    except serial.SerialException as e:
        print(Fore.RED + f"[-] " + Fore.RESET +f"Serial error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
if __name__=="__main__":
    main()
