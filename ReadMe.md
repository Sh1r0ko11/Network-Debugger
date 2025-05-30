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

2. Install Python packages (open PowerShell as admin):
```powershell
# Core functionality
pip install scapy        # For packet capture
pip install psutil       # For process monitoring
pip install pandas      # For data analysis

# GUI and system packages (if not included with Python)
pip install tk          # For GUI (tkinter)
pip install ttk         # For themed widgets
```

3. Required Python Built-in Modules:
   These come with Python, no need to install:
   - struct (binary data handling)
   - datetime (time operations)
   - threading (multithreading)
   - socket (network operations)
   - webbrowser (opening web pages)
   - os (file/path operations)
   - re (regular expressions)
   - collections (for defaultdict)

4. Install Npcap (REQUIRED for packet capture):
   - Download Npcap from [https://npcap.com/](https://npcap.com/)
   - Install with default settings
   - Required for Scapy to capture packets

5. Install Node.js for JavaScript support:
   - Download Node.js from [https://nodejs.org/](https://nodejs.org/)
   - Install the LTS (Long Term Support) version
   - Verify installation by opening PowerShell and typing:
```powershell
node --version
npm --version
```

6. Verify JavaScript files:
   Make sure all these files are in your project folder:
   - operation_nomenclature.js
   - cpu_tracker.js
   - assembly_tracker.js
   - ram_debugger.js
   - x86_assembly_monitor.js
   - memory_profiler.js
   - WEb-IDE_Debugger1.html

7. Additional Components (auto-installed):
   - All Python built-in modules (struct, datetime, etc.)
   - JavaScript runs in the browser (no extra installation needed)
   - HTML/CSS comes with the package

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
