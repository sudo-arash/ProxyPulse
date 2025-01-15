import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import asyncio
from src.proxy_tester import test_proxies
import queue
import logging
import os

def main_gui():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    root = tk.Tk()
    root.title("ProxyPulse")
    root.configure(bg='#f0f0f0')

    # Frame for input section with background color
    input_frame = ttk.Frame(root, padding="10", relief=tk.RIDGE, borderwidth=1, style='Input.TFrame')
    input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Style for input frame background
    style = ttk.Style()
    style.configure('Input.TFrame', background='#e0f0ff')
    style.configure('Control.TFrame', background='#e0ffe0')
    style.configure('Output.TFrame', background='#ffffe0')

    # Label for input section
    ttk.Label(input_frame, text="Select Proxies File:", background='#e0f0ff').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    # Entry to display selected file path
    file_path_var = tk.StringVar()
    file_path_entry = ttk.Entry(input_frame, textvariable=file_path_var, state='readonly', width=40)
    file_path_entry.grid(row=0, column=1, padx=5, pady=5)

    # Button to select file
    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            file_path_var.set(file_path)

    ttk.Button(input_frame, text="Browse", command=select_file).grid(row=0, column=2, padx=5, pady=5)

    # Frame for controls with background color
    control_frame = ttk.Frame(root, padding="10", relief=tk.RIDGE, borderwidth=1, style='Control.TFrame')
    control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Start button
    start_button = ttk.Button(control_frame, text="Start Testing", command=lambda: start_testing(file_path_var.get()))
    start_button.grid(row=0, column=0, padx=5, pady=5)

    # Progress bar
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(control_frame, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

    # Frame for output section with background color
    output_frame = ttk.Frame(root, padding="10", relief=tk.RIDGE, borderwidth=1, style='Output.TFrame')
    output_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Label for output section
    ttk.Label(output_frame, text="Working Proxies:", background='#ffffe0').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    # Listbox to display working proxies
    listbox = tk.Listbox(output_frame, height=15, width=40, font=("Helvetica", 12))
    listbox.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

    # Scrollbar for Listbox
    scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
    listbox.configure(yscrollcommand=scrollbar.set)

    # Clear button
    def clear_results():
        listbox.delete(0, tk.END)
        progress_var.set(0)

    ttk.Button(output_frame, text="Clear Results", command=clear_results).grid(row=2, column=0, padx=5, pady=5)

    # Function to start testing
    def start_testing(file_path):
        if not file_path:
            messagebox.showerror("Error", "Please select a proxies file.")
            return
        if not messagebox.askyesno("Confirm", "Do you want to start testing the proxies?"):
            return
        start_button.config(state=tk.DISABLED)
        progress_var.set(0)
        # Read proxies from file
        try:
            with open(file_path, 'r') as file:
                proxy_list = file.read().splitlines()
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")
            start_button.config(state=tk.NORMAL)
            return
        if not proxy_list:
            messagebox.showwarning("Warning", "No proxies found in the file.")
            start_button.config(state=tk.NORMAL)
            return
        # Queue to communicate between threads
        q = queue.Queue()
        # Thread to run the async test
        thread = threading.Thread(target=run_async_test, args=(q, proxy_list))
        thread.start()
        # After starting the thread, check the queue periodically
        root.after(100, check_queue, q, listbox, start_button, progress_var)

    # Function to run the async test in a thread
    def run_async_test(q, proxy_list):
        try:
            results = asyncio.run(test_proxies(proxy_list))
            q.put(results)
        except Exception as e:
            q.put(f"Error during testing: {e}")
        finally:
            q.put("Testing completed.")

    # Function to check the queue and update GUI
    def check_queue(q, listbox, start_button, progress_var):
        try:
            msg = q.get_nowait()
            if isinstance(msg, list):
                # Display working proxies
                listbox.delete(0, tk.END)
                for proxy in msg:
                    listbox.insert(tk.END, proxy)
            elif msg == "Testing completed.":
                messagebox.showinfo("Info", msg)
                start_button.config(state=tk.NORMAL)
            else:
                # Display error messages
                messagebox.showerror("Error", msg)
        except queue.Empty:
            pass
        # Simulate progress update (replace with actual progress tracking if possible)
        current_progress = progress_var.get()
        if current_progress < 100:
            current_progress += 10
            progress_var.set(current_progress)
        root.after(100, check_queue, q, listbox, start_button, progress_var)

    root.mainloop()
