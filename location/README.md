# Raspberry Pi 2 Model B Setup Guide

## 1. Enable Python 3

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 -y
sudo apt install python3-pip -y
```

To make `python3` the default:

```bash
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
```

Verify installation:

```bash
python --version
pip3 --version
```

---

## 2. Install Git

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git -y
```

Verify:

```bash
git --version
```

(Optional) Configure Git:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 3. Install `pip3` and Required Python Modules

If `pip3 install` fails with an **externally-managed environment** error, use a **virtual environment**:

### **3.1 Create and Activate a Virtual Environment**

```bash
python3 -m venv ~/myenv
source ~/myenv/bin/activate
```

### **3.2 Install Required Modules Inside the Virtual Environment**

```bash
pip install requests gps3 pynmeagps
```

### **3.3 Run Your Python Script Inside the Virtual Environment**

```bash
python your_script.py
```

### **3.4 Exit the Virtual Environment When Done**

```bash
deactivate
```

Alternatively, install system-wide using APT (if available):

```bash
sudo apt install python3-requests python3-gps -y
```

---

## 4. Verify Installations

After all installations, check if the required modules are available:

```bash
python3 -c "import requests, pynmeagps, gps3; print('Modules installed successfully!')"
```

This ensures a clean and properly set up Python environment on your **Raspberry Pi 2 Model B**. 🚀
