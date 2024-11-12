import tkinter as tk

def main():
    root = tk.Tk()
    root.title("IdentiTech")
    root.iconbitmap("Logo.ico")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(True, True)

    root.mainloop()


    
main()