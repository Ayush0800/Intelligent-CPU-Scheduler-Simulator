# 🧠 CPU Scheduling Visualizer ⏱️

An interactive Flask web app to simulate and visualize classic **CPU Scheduling Algorithms** including FCFS, SJF, Priority, and Round Robin. Perfect for learning OS concepts with ease! 💻📊

---

## 📸 Preview

> Enter processes ➡️ Choose algorithm ➡️ View Gantt Chart and stats!

![Screenshot 2025-04-06 012025](https://github.com/user-attachments/assets/0fc5cbff-48d9-42a8-9ec6-9b3c98e3a885)


---

## 🚀 Features

- ✅ **FCFS**, **SJF (Preemptive & Non-Preemptive)**, **Priority**, **Round Robin**
- ✅ Gantt Chart visualization
- ✅ Waiting Time & Turnaround Time Calculation
- ✅ Simple & clean frontend (HTML/CSS)
- ✅ Built with Flask (Python backend)

---

## 📁 Project Structure

```bash
├── app.py                     # Flask application
├── scheduling_algorithms.py   # Scheduling logic
├── requirements.txt           # Project dependencies
├── templates/
│   └── index.html             # UI page
```


## ⚙️ Setup Instructions

You can either follow manual setup steps below or use the provided setup scripts.

---
### 🛠 Manual Setup
#### 1️⃣ Clone the Repo
```bash
git clone https://github.com/yourusername/cpu-scheduling-visualizer.git
cd cpu-scheduling-visualizer
```
#### 2️⃣ Create Virtual Environment (Recommended)
# Windows
```bash
python -m venv venv
venv\Scripts\activate
```

# macOS/Linux
``` bash 
python3 -m venv venv
source venv/bin/activate
```
#### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
#### 4️⃣ Run the Application
```bash
python app.py
```
App will be running at: 👉 http://127.0.0.1:5000

### 📦 Automatic Setup Scripts (Optional)
#### ▶️ setup.sh (macOS/Linux)
``` bash
#!/bin/bash
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "🚀 Launching the app..."
python app.py
```
Save as setup.sh, make executable:
```bash
chmod +x setup.sh
./setup.sh
```
#### ▶️ setup.bat (Windows)
```bat
@echo off
echo 🔧 Creating virtual environment...
python -m venv venv
call venv\Scripts\activate
echo 📦 Installing dependencies...
pip install -r requirements.txt
echo 🚀 Launching the app...
python app.py
pause
```
Save this as setup.bat and double-click it to run.

# 💡 Future Enhancements
- ### 📱 Responsive UI for mobile

- ### 🌙 Dark mode support

- ### 📈 Show CPU utilization, throughput

- ### 📤 Export Gantt chart as image

- ### 💾 Save/load process session history
---

# 🤝 Contributing
Pull requests are welcome!
Follow these steps:
```bash
git checkout -b feature-name
# Make your changes
git commit -m "Add feature"
git push origin feature-name
# Then open a Pull Request
```

# 📄 License
Licensed under the MIT License – free to use, modify, and distribute.

# 🙌 Acknowledgments
- ### 💡 Inspired by OS course projects

- ### 🐍 Thanks to Flask & Python

- ### 🧠 Conceptual references from Operating System textbooks
