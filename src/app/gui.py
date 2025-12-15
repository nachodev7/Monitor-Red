"""
Interfaz gráfica.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog,simpledialog
import csv
from .config import load_config, save_config
from .network import ping_host
from .history import log_event, read_events





class MonitorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Monitor de Red")
        self.root.geometry("600x400")

        self.config = load_config()
        self.hosts = self.config.get("hosts", [])
        self.last_status = {}
        self.simulation_mode = tk.BooleanVar(
            value=self.config.get("mode") == "simulation"
        )

        self.interval = self.config.get("interval_seconds", 5)
        self.monitoring = False
        
        style = ttk.Style()
        style.theme_use("clam")


        self._build_ui()


    def _build_ui(self) -> None:
        self._setup_styles()

        
        title = ttk.Label(
            self.root,
            text="Monitor de Red",
            style="Title.TLabel"
        )
        title.pack(pady=12)

        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=5)

        ttk.Checkbutton(
            top_frame,
            text="Modo simulación",
            variable=self.simulation_mode
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            top_frame,
            text="Iniciar monitoreo",
            command=self.start_monitoring
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            top_frame,
            text="Refrescar",
            command=self.refresh
        ).pack(side=tk.LEFT, padx=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pestaña de Monitoreo
        self.monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monitor_frame, text="Monitoreo")
        
        hosts_controls = ttk.Frame(self.monitor_frame)
        hosts_controls.pack(fill=tk.X, pady=5)

        ttk.Button(
            hosts_controls,
            text="➕ Agregar host",
            style="Small.TButton",
            command=self.add_host
        ).pack(side=tk.LEFT, padx=4)

        ttk.Button(
            hosts_controls,
            text="❌ Quitar host",
            style="Small.TButton",
            command=self.remove_host
        ).pack(side=tk.LEFT, padx=4)


        self.tree = ttk.Treeview(
        self.monitor_frame,
            columns=("host", "status"),
            show="headings",
            height=12
        )
        self.tree.heading("host", text="Host")
        self.tree.heading("status", text="Estado")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.tag_configure(
            "online", foreground="#5fb3a2"
        )
        self.tree.tag_configure(
            "slow", foreground="#c9a227"
        )
        self.tree.tag_configure(
            "offline", foreground="#c45c5c"
        )

# Pestaña de Histórico

        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="Histórico")

# Frame para la tabla
        history_table_frame = ttk.Frame(self.history_frame)
        history_table_frame.pack(fill=tk.BOTH, expand=True)

        self.history_tree = ttk.Treeview(
            history_table_frame,
            columns=("timestamp", "host", "status"),
            show="headings",
            height=12
        )
        self.history_tree.heading("timestamp", text="Fecha y hora")
        self.history_tree.heading("host", text="Host")
        self.history_tree.heading("status", text="Estado")

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            history_table_frame,
            orient="vertical",
            command=self.history_tree.yview
        )
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_tree.tag_configure(
            "online", foreground="#5fb3a2"
        )
        self.history_tree.tag_configure(
            "slow", foreground="#c9a227"
        )
        self.history_tree.tag_configure(
            "offline", foreground="#c45c5c"
        )

        ttk.Separator(self.history_frame).pack(fill=tk.X, pady=5)

# Frame para botones
        history_buttons_frame = ttk.Frame(self.history_frame)
        history_buttons_frame.pack(fill=tk.X, pady=5)

        export_btn = ttk.Button(
            history_buttons_frame,
            text="Exportar histórico a CSV",
            command=self.export_history
        )
        export_btn.pack(pady=5)


        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.status_bar = ttk.Label(self.root, text="Listo", anchor=tk.W, style="Status.TLabel")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)



    def start_monitoring(self) -> None:
        """Inicia el monitoreo periódico."""
        if not self.hosts:
            messagebox.showwarning(
                "Sin hosts",
                "No hay hosts configurados en config.json"
            )
            return

        if not self.monitoring:
            self.monitoring = True
            self.status_bar.config(text="Monitoreo iniciado")
            self._schedule_refresh()


    def _schedule_refresh(self) -> None:
        if self.monitoring:
            self.refresh()
            self.root.after(self.interval * 1000, self._schedule_refresh)


    def refresh(self) -> None:
        """Actualiza el estado de los hosts."""
        self.tree.delete(*self.tree.get_children())

        mode = self.simulation_mode.get()
        mode_text = "SIMULACIÓN" if mode else "REAL"
        
        for host in self.hosts:
            latency = ping_host(host, simulate=mode)

            if latency is None:
                status = "OFFLINE"
                display = "🔴 OFFLINE"
                tag = "offline"
            elif latency >= 80:
                status = "ONLINE"
                display = f"🟡 LENTO ({latency} ms)"
                tag = "slow"
            else:
                status = "ONLINE"
                display = f"🟢 ONLINE ({latency} ms)"
                tag = "online"

# Detectar cambio de estado

            previous = self.last_status.get(host)
            if previous != status:
                log_event(host, status)
                self.last_status[host] = status

            self.tree.insert(
                "",
                tk.END,
                values=(host, display),
                tags=(tag,)
            )

        self.status_bar.config(
            text=f"Modo: {mode_text} | Hosts monitoreados: {len(self.hosts)}"
        )
        self.refresh_history()

    def refresh_history(self) -> None:
#Actualiza la tabla de histórico desde logs.
        self.history_tree.delete(*self.history_tree.get_children())
        events = read_events()  # función de history.py que devuelve lista de eventos
        for timestamp, host, status in events:
            tag = "online" if status == "ONLINE" else "offline"
            if status.startswith("LENTO"):
                tag = "slow"
            self.history_tree.insert("", tk.END, values=(timestamp, host, status), tags=(tag,))

    def export_history(self) -> None:
        events = read_events()

        if not events:
            messagebox.showinfo("Exportar", "No hay eventos para exportar")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return
        

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Fecha", "Host", "Estado"])
            writer.writerows(events)


        messagebox.showinfo(
            "Exportación exitosa",
            f"Archivo guardado en:\n{file_path}"
        )

    def add_host(self) -> None:
        host = simpledialog.askstring(
        "Agregar host",
        "Ingrese IP o dominio:"
    )

        if not host:
            return

        if host in self.hosts:
            messagebox.showwarning(
                "Duplicado",
                "El host ya existe"
            )
            return

        self.hosts.append(host)
        self.config["hosts"] = self.hosts
        save_config(self.config)

        self.status_bar.config(text=f"Host agregado: {host}")
        self.refresh()

    def remove_host(self) -> None:
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Atención",
                "Seleccione un host para eliminar"
            )
            return

        host = self.tree.item(selected[0])["values"][0]

        if not messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar el host {host}?"
        ):
            return

        self.hosts.remove(host)
        self.config["hosts"] = self.hosts
        save_config(self.config)

        self.last_status.pop(host, None)

        self.status_bar.config(text=f"Host eliminado: {host}")
        self.refresh()


    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

# Fondo principal
        style.configure(".", background="#2b2f33")
        self.root.configure(bg="#2b2f33")

        style.configure("TFrame", background="#2b2f33")
        style.configure("TLabel", background="#2b2f33", foreground="#e0e0e0")

# Título
        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground="#6ca0dc",
            background="#2b2f33"
        )

    # Botones
        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=8,
            background="#3a3f44",
            foreground="#e0e0e0"
        )

        style.map(
            "TButton",
            background=[("active", "#4a5056")]
        )

        style.configure(
            "Primary.TButton",
            background="#4a90e2",
            foreground="#ffffff"
        )

        style.map(
            "Primary.TButton",
            background=[("active", "#357abd")]
        )

# Notebook (tabs)
        style.configure(
            "TNotebook",
            background="#2b2f33",
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background="#31363b",
            foreground="#e0e0e0",
            padding=[12, 6]
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", "#3f444a")],
            foreground=[("selected", "#ffffff")]
        )

# Treeview
        style.configure(
            "Treeview",
            background="#363b40",
            foreground="#e0e0e0",
            fieldbackground="#363b40",
            rowheight=26,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#3f444a",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#4a6fa5")],
            foreground=[("selected", "#ffffff")]
        )

# Barra de estado
        style.configure(
            "Status.TLabel",
            background="#31363b",
            foreground="#b0b0b0",
            font=("Segoe UI", 9)
        )

# Checkbutton (Modo simulación)
        style.configure(
            "TCheckbutton",
            background="#2b2f33",
            foreground="#e0e0e0",
            font=("Segoe UI", 10)
        )

        style.map(
            "TCheckbutton",
            foreground=[("active", "#ffffff")],
            background=[("active", "#2b2f33")]
        )

        style.configure(
            "Small.TButton",
            font=("Segoe UI", 9),
            padding=(6, 3),
            background="#252526",
            foreground="#d4d4d4"
        )

        style.map(
            "Small.TButton",
            background=[("active", "#333333")]
        )























