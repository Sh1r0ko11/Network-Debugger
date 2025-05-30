# 🔍 Network Traffic Analyzer for Windows

Hey there! 👋 This is my fun little project that I created to make network analysis less boring and more accessible. It's a Windows-based GUI tool that lets you see what's happening on your network in real-time - perfect for curious minds who want to understand their network traffic!

## ✨ What's Cool About It?

- 🚀 Watch packets fly by in real-time
- 📊 See pretty statistics about your network usage
- 🔍 Find out which apps are talking to the internet
- 🎯 Track suspicious network behavior
- 🎮 User-friendly interface (because command line isn't always fun!)
- 📱 Support for all common protocols you'll need

## 🖥️ System Requirements

- Windows 10 or 11 (Sorry Linux/Mac folks!)
- Python 3.8 or newer
- Admin rights on your Windows machine
- Npcap (required for packet capture)
- A modern web browser (Chrome, Firefox, or Edge)
- A curious mind! 🧠

## 🚀 Getting Started

1. First, grab the code:
   - Download this repo as ZIP or clone it
   - Put it somewhere you can easily find it (like Documents folder)

2. Install Python stuff (open PowerShell as admin):
```powershell
pip install scapy==2.5.0
pip install psutil==5.9.0
pip install pandas
pip install tkinter
```

3. Install Npcap (REQUIRED for packet capture):
   - Download Npcap from [https://npcap.com/](https://npcap.com/)
   - Select "WinPcap API-compatible Mode" during installation
   - Just click next-next-finish (default settings are perfect!)

4. Additional Components (auto-installed with pip):
   - struct (built into Python)
   - datetime (built into Python)
   - threading (built into Python)
   - socket (built into Python)
   - webbrowser (built into Python)
   - os (built into Python)
   - re (built into Python)
   - collections (built into Python)

## 🎮 Fire It Up!

1. Right-click on PowerShell and "Run as Administrator"
2. Navigate to where you saved the project:
```powershell
cd "C:\Path\To\web_debuggerIDE1"
```
3. Launch it:
```powershell
python network_analyzer_gui.py
```

## 🎯 What You'll See

- **Main Window**: Your live traffic feed (it's like Matrix, but makes sense!)
- **Stats Tab**: Numbers that tell stories about your network
- **Forensics**: For your inner detective 🕵️
- **Protocol Analysis**: See which apps are doing what

## 🆘 Help! Something's Wrong!

- Getting access denied? Right-click → Run as Administrator is your friend
- No packets showing up? Make sure Npcap is installed properly
- Windows Defender freaking out? Add an exception for the analyzer
- Still stuck? That's what Google is for! 😉

## 💡 Why I Made This

I created this tool just for fun while learning about network analysis. It started as a weekend project and grew into something actually useful! Feel free to use it, break it, fix it, or make it better!

## 📝 License

This is free to use! If you make something cool with it, I'd love to hear about it. Built with ❤️ and lots of ☕

> **Note**: This is a learning tool! Be responsible with network analysis tools. Don't be that person who uses it for uncool stuff! 😉
