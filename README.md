#  Monitor de Red en Python

Aplicación de escritorio desarrollada en **Python + Tkinter (ttk)** para monitorear el estado de múltiples hosts de red (online / lento / offline), registrar cambios de estado y exportar históricos en formato **CSV**.


---

## 🚀 Características principales

* 📡 Monitoreo de hosts mediante *ping*
* 🟢 Estados visuales: ONLINE / LENTO / OFFLINE
* 🧪 Modo simulación (sin tráfico real)
* 🧾 Registro histórico automático de eventos
* 📤 Exportación del histórico a CSV
* ➕ Agregar y quitar hosts desde la interfaz
* 🪟 Aplicación de escritorio (Tkinter)

---



## 🛠️ Tecnologías usadas

* **Python 3.10+**
* **Tkinter / ttk** (GUI)
* **CSV** (exportación de datos)
* **JSON** (configuración)


---

## 📂 Estructura del proyecto

```
monitor_red/
├── src/
│   └── app/
│       ├── __init__
        ├── __main__.py
│       ├── gui.py          
│       ├── monitor.py      
│       ├── history.py      
│       ├── config.py       
        ├── network.py
        ├── logger.py
│       
├── .gitignore           
├── config.json
├── logs.json
├── README.md
└── requirements.txt

```

---



## ▶️ Cómo ejecutar el proyecto

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/nachodev7/monitor-red.git
cd monitor-red
```

### 2️⃣ Crear entorno virtual 

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar la app

```bash
python -m src.app
```

---



---

## 📤 Exportación de datos

Desde la pestaña **Histórico**, podés exportar todos los eventos registrados a un archivo **CSV**.

---



