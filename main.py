import tkinter as tk
from tkinter import ttk, messagebox, font
import pyperclip
import keyboard
import time
import threading
from deep_translator import GoogleTranslator
import sys
from PIL import Image, ImageTk

class ModernTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Translator")
        self.root.geometry("500x400")  
        self.root.resizable(False, False)
        self.root.configure(bg="#1D1D1D")
        image = Image.open("image.png")
        photo = ImageTk.PhotoImage(image)
        self.root.iconphoto(True, photo)

        
        self.center_window()
        
        self.setup_styles()

        self.popup = None
        self.is_running = False
        self.last_text = ""

        self.languages = {
            "Auto-detect": "auto",
            "Russian": "ru",
            "English": "en", 
            "French": "fr",
            "German": "de",
            "Spanish": "es",
            "Italian": "it",
            "Chinese": "zh",
            "Japanese": "ja",
            "Korean": "ko",
            "Portuguese": "pt",
            "Arabic": "ar"
        }
        
        self.source_lang = tk.StringVar(value="Auto-detect")
        self.target_lang = tk.StringVar(value="Russian")

        self.create_widgets()

        self.update_translator()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        self.root.update_idletasks()
        width = 500
        height = 400
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Modern.TButton",
                       background="#3D3D3D",
                       foreground="white",
                       borderwidth=0,
                       focuscolor="none",
                       font=("Segoe UI", 10, "bold"))
        
        style.map("Modern.TButton",
                 background=[("active", "#777777"),
                           ("pressed", "#777777")])

        style.configure("Modern.TCombobox",
                       fieldbackground="white",
                       background="#ecf0f1",
                       borderwidth=2)
    
    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg="#1D1D1D", height=80)
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        title_frame.pack_propagate(False)
        
        title_font = font.Font(family="Segoe UI", size=24, weight="bold")
        title_label = tk.Label(title_frame, text="🌐 Smart Translator", 
                              font=title_font, bg="#1D1D1D", fg="#ecf0f1")
        
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame, text="Automatic translation on copy", 
                                 font=("Segoe UI", 10), bg="#1D1D1D", fg="#bdc3c7")
        
        subtitle_label.pack()

        lang_frame = tk.LabelFrame(self.root, text="Language Settings", 
                                  font=("Segoe UI", 12, "bold"),
                                  bg="#2E2E2E", fg="#ecf0f1", 
                                  relief="solid", bd=2)
        lang_frame.pack(fill="x", padx=20, pady=10)

        
        source_frame = tk.Frame(lang_frame, bg="#2E2E2E")
        source_frame.pack(fill="x", padx=15, pady=10)

        
        tk.Label(source_frame, text="From language:", font=("Segoe UI", 10, "bold"),
                bg="#2E2E2E", fg="#ecf0f1").pack(side="left")
        
        source_combo = ttk.Combobox(source_frame, textvariable=self.source_lang,
                                   values=list(self.languages.keys()),
                                   state="readonly", style="Modern.TCombobox",
                                   font=("Segoe UI", 10))
        source_combo.pack(side="right", padx=(10, 0))
        source_combo.bind("<<ComboboxSelected>>", lambda e: self.update_translator())
  
        target_frame = tk.Frame(lang_frame, bg="#2E2E2E")
        target_frame.pack(fill="x", padx=15, pady=(0, 10))

        
        tk.Label(target_frame, text="To language:", font=("Segoe UI", 10, "bold"),
                bg="#2E2E2E", fg="#ecf0f1").pack(side="left")
        
        target_combo = ttk.Combobox(target_frame, textvariable=self.target_lang,
                                   values=list(self.languages.keys())[1:],  
                                   state="readonly", style="Modern.TCombobox",
                                   font=("Segoe UI", 10))
        target_combo.pack(side="right", padx=(10, 0))
        target_combo.bind("<<ComboboxSelected>>", lambda e: self.update_translator())

        button_frame = tk.Frame(self.root, bg="#1D1D1D")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="▶️ Start Monitoring",
                                      command=self.toggle_monitoring,
                                      style="Modern.TButton")
        self.start_button.pack(side="left", padx=(0, 10))
        
        test_button = ttk.Button(button_frame, text="🧪 Test",
                               command=self.test_translation,
                               style="Modern.TButton")
        test_button.pack(side="left", padx=(0, 10))

        self.status_label = tk.Label(self.root, text="⏸️ Stopped", 
                                   font=("Segoe UI", 10, "bold"),
                                   bg="#1D1D1D", fg="#e74c3c")
        self.status_label.pack(pady=5)

        info_frame = tk.Frame(self.root, bg="#1D1D1D")
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        info_text = "💡 Tip: Copy any text (Ctrl+C), and the translation will appear in a popup window"
        info_label = tk.Label(info_frame, text=info_text, 
                            font=("Segoe UI", 9), bg="#1D1D1D", fg="#95a5a6",
                            wraplength=460, justify="center")
        info_label.pack()
    
    def update_translator(self):
        source_code = self.languages[self.source_lang.get()]
        target_code = self.languages[self.target_lang.get()]
        
        try:
            self.translator = GoogleTranslator(source=source_code, target=target_code)
        except Exception as e:
            messagebox.showerror("Error", f"Translator initialization error: {e}")
    
    def toggle_monitoring(self):
        if not self.is_running:
            self.start_monitoring()
        else:
            self.stop_monitoring()
    
    def start_monitoring(self):
        try:
            keyboard.add_hotkey("ctrl+c", self.on_copy)
            self.is_running = True
            self.start_button.configure(text="⏸️ Stop Monitoring")
            self.status_label.configure(text="🔄 Running", fg="#27ae60")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {e}")
    
    def stop_monitoring(self):
        try:
            keyboard.unhook_all_hotkeys()
            self.is_running = False
            self.start_button.configure(text="▶️ Start Monitoring")
            self.status_label.configure(text="⏸️ Stopped", fg="#e74c3c")
        except Exception as e:
            messagebox.showerror("Error", f"Stop error: {e}")
    
    def on_copy(self):
        def translate_async():
            time.sleep(0.1) 
            text = pyperclip.paste()
            
            if text.strip() and text != self.last_text:
                self.last_text = text
                try:
                    translated = self.translator.translate(text)
                    self.root.after(0, lambda: self.show_popup(text, translated))
                except Exception as e:
                    error_msg = f"Text length need to be between 0 and 5000 characters, and only text is supported."
                    self.root.after(0, lambda: self.show_popup(text, error_msg, is_error=True))
        
        thread = threading.Thread(target=translate_async, daemon=True)
        thread.start()
    
    def show_popup(self, original_text, translated_text, is_error=False):
        if self.popup:
            self.popup.destroy()
        
        self.popup = tk.Toplevel(self.root)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        max_width = 400
        max_height = 900
        
        bg_color = "#ffebee" if is_error else "#252525"
        border_color = "#f44336" if is_error else "#575757"
        
        self.popup.configure(bg=border_color)

        main_frame = tk.Frame(self.popup, bg=border_color)
        main_frame.pack(fill="both", expand=True)
        
        inner_frame = tk.Frame(main_frame, bg=bg_color, relief="solid", bd=2)
        inner_frame.pack(fill="both", expand=True, padx=3, pady=3)


        header_frame = tk.Frame(inner_frame, bg=bg_color)
        header_frame.pack(fill="x", padx=10, pady=(8, 0))
        
        header_text = "❌ Translation Error" if is_error else "🌐 Translation"
        header_color = "#d32f2f" if is_error else "#2e7d32"
        
        header_label = tk.Label(header_frame, text=header_text,
                               font=("Segoe UI", 10, "bold"),
                               bg=bg_color, fg=header_color)
        header_label.pack(side="left")
        
        close_button = tk.Label(header_frame, text="✕",
                               font=("Segoe UI", 11, "bold"),
                               bg=bg_color, fg="#666",
                               cursor="hand2")
        close_button.pack(side="right")
        close_button.bind("<Button-1>", lambda e: self.close_popup())
        
        separator = tk.Frame(inner_frame, bg="#bdbdbd", height=1)
        separator.pack(fill="x", padx=10, pady=5)
        

        canvas_frame = tk.Frame(inner_frame, bg=bg_color)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        canvas = tk.Canvas(canvas_frame, bg=bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        trans_label = tk.Label(scrollable_frame, text=translated_text,
                              font=("Segoe UI", 11, "bold"), bg=bg_color,
                              fg="#d32f2f" if is_error else "#1976d2",
                              wraplength=max_width-60, justify="left")
        trans_label.pack(pady=(0, 10), padx=5, anchor="w")
        
        if not is_error:
            sep_frame = tk.Frame(scrollable_frame, bg="#bdbdbd", height=1)
            sep_frame.pack(fill="x", pady=(0, 10))
            
            orig_label = tk.Label(scrollable_frame, 
                                 text=f"📝 Original: {original_text}",
                                 font=("Segoe UI", 9), bg=bg_color, fg="#666",
                                 wraplength=max_width-60, justify="left")
            orig_label.pack(pady=(0, 5), padx=5, anchor="w")
        
    
        self.popup.update_idletasks()
        

        canvas.update_idletasks()
        content_height = scrollable_frame.winfo_reqheight()
        header_height = 80
        
        popup_width = max_width
        popup_height = min(content_height + header_height, max_height)
        

        if content_height + header_height > max_height:
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
        else:
            canvas.pack(fill="both", expand=True)
        

        x = screen_width - popup_width - 20 
        y = 100
        

        if y + popup_height > screen_height:
            y = screen_height - popup_height - 20
        
        self.popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel():
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel():
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', lambda e: _bind_mousewheel())
        canvas.bind('<Leave>', lambda e: _unbind_mousewheel())
    
    def close_popup(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None
    
    def test_translation(self):
        test_text = "Hello, world! This is a test translation."
        pyperclip.copy(test_text)
        self.on_copy()

    
    def on_closing(self):
        if self.is_running:
            self.stop_monitoring()
        
        self.root.destroy()
        sys.exit()
    
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()

def main():
    try:
        app = ModernTranslator()
        app.run()
    
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()