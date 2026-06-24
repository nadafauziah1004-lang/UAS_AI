import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# 1. Konfigurasi Environment & API
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

console = Console()

if not API_KEY:
    console.print("[bold red]Error:[/bold red] API Key tidak ditemukan. Pastikan file .env sudah dikonfigurasi.")
    sys.exit()

genai.configure(api_key=API_KEY)

def main():
    # 2. Merancang Persona dan System Prompt
    system_instruction = """
    Kamu adalah Shaffira, seorang tutor bahasa Arab yang ceria, ramah, dan suportif. 
    Tugas utamamu adalah melatih pengguna dalam 'maharah kalam' (kemampuan berbicara/percakapan). 
    Gunakan bahasa Arab sehari-hari yang natural dan berikan terjemahan atau penjelasan bahasa Indonesia jika pengguna kesulitan.
    Selalu ajukan pertanyaan balik untuk menjaga agar percakapan tetap mengalir. 
    Jika pengguna salah tata bahasa (nahwu/sharaf) atau kosakata, puji usaha mereka terlebih dahulu (misal: "Mumtaz!" atau "Jayyid!"), lalu berikan koreksi dengan lembut, sebelum membalas topik utama.
    """
    
    # 3. Inisialisasi Model Gemini
    # Menggunakan Gemini 1.5 Flash yang cepat dan mendukung system instructions
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )
    
    # Memulai sesi percakapan (menyimpan riwayat otomatis)
    chat_session = model.start_chat(history=[])
    
    # 4. Antarmuka Awal (Greeting)
    console.print(Panel.fit("[bold green]Ahlan wa Sahlan![/bold green] Selamat Datang di Shaffira Kalam Arabic.\nTeman percakapan bahasa Arab interaktif untuk melatih Maharah Kalam-mu.", title="✨ Shaffira Bot"))
    
    # 5. Fitur Minimum: 3 Mode Pembelajaran
    console.print("\n[bold cyan]Silakan pilih Mode Pembelajaran hari ini:[/bold cyan]")
    console.print("1. Ta'aruf (Perkenalan Diri Dasar)")
    console.print("2. Maukif (Bermain Peran - Skenario di Restoran)")
    console.print("3. Hiwar Bebas (Bincang Santai)")
    
    while True:
        mode = Prompt.ask("\nMasukkan pilihan Anda (1/2/3)")
        if mode in ['1', '2', '3']:
            break
        console.print("[bold red]Pilihan tidak valid. Silakan pilih 1, 2, atau 3.[/bold red]")
    
    # Menentukan pemicu awal berdasarkan mode yang dipilih
    if mode == '1':
        topik_awal = "Mari kita mulai dengan perkenalan diri (Ta'aruf). Sapa saya dan tanyakan nama, asal, serta hobi saya dalam bahasa Arab."
    elif mode == '2':
        topik_awal = "Mari kita bermain peran. Anggap kita sedang berada di restoran Arab. Kamu sebagai pelayan yang ramah, dan saya sebagai pelanggan yang ingin memesan makanan. Silakan sapa saya terlebih dahulu."
    else:
        topik_awal = "Mari kita ngobrol santai (Hiwar Bebas). Sapa saya dengan ramah dan tanyakan bagaimana hari saya atau topik apa yang ingin saya bicarakan hari ini."

    console.print("\n[bold yellow]Ketik 'exit' atau 'quit' kapan saja untuk keluar dari sesi.[/bold yellow]")
    console.print("-" * 50)
    
    # Mengirim prompt sistem pertama ke AI agar Shaffira memulai percakapan
    try:
        response = chat_session.send_message(topik_awal)
        console.print(f"\n[bold magenta]👩‍🏫 Shaffira:[/bold magenta] {response.text}\n")
    except Exception as e:
        console.print(f"[bold red]Terjadi kesalahan saat memulai sesi:[/bold red] {e}")
        sys.exit()
    
    # 6. Loop Percakapan Utama
    while True:
        user_input = Prompt.ask("[bold blue]👤 Anda[/bold blue]")
        
        # Perintah keluar
        if user_input.lower() in ['exit', 'quit']:
            console.print(Panel.fit("[bold green]Ma'as salama! Terima kasih telah berlatih bersama Shaffira hari ini. Sampai jumpa![/bold green]"))
            break
            
        if user_input.strip() == "":
            continue
            
        # Mengirim pesan pengguna ke AI
        try:
            response = chat_session.send_message(user_input)
            console.print(f"\n[bold magenta]👩‍🏫 Shaffira:[/bold magenta] {response.text}\n")
        except Exception as e:
            console.print(f"[bold red]Terjadi kesalahan koneksi API:[/bold red] {e}")

if __name__ == "__main__":
    main()
    