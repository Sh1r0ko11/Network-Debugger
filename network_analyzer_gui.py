import tkinter as tk
from tkinter import ttk
import struct
from datetime import datetime
import threading
import socket
import webbrowser
import os
from scapy.all import sniff, IP, TCP, UDP, DNS, ICMP, Raw
from scapy.config import conf
import pandas as pd
from collections import defaultdict
import re
import psutil  # Add this import at the top

# Disable Wireshark warnings
conf.manufdb = ""
conf.nospace_pkg = True

class NetworkAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Network Traffic Analyzer")
        self.root.geometry("1500x800")
        
        # Traffic statistics
        self.packet_count = 0
        self.connections = defaultdict(int)
        self.protocols = defaultdict(int)
        
        # Additional analysis data
        self.suspicious_dns = defaultdict(int)
        self.data_exfil_stats = defaultdict(int)
        self.encrypted_streams = set()
        
        self.is_live_mode = True  # We'll keep this but it will always be true
        self.packet_queue = []
        
        self.port_to_process = {}  # Add this to track port-process mapping
        self.known_services = {
            20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP",
            137: "NetBIOS", 138: "NetBIOS", 139: "NetBIOS", 445: "SMB",
            5432: "PostgreSQL", 27017: "MongoDB", 6379: "Redis"
        }
        self.known_services.update({
            8080: "HTTP-Alt", 5432: "PostgreSQL", 3306: "MySQL",
            1433: "MSSQL", 5672: "AMQP", 6379: "Redis",
            27017: "MongoDB", 1521: "Oracle", 9092: "Kafka",
            6443: "Kubernetes", 2375: "Docker", 9200: "Elasticsearch",
            5601: "Kibana", 8443: "HTTPS-Alt", 1883: "MQTT",
            5222: "XMPP", 389: "LDAP", 636: "LDAPS"
        })
        
        self.last_scroll_position = 0
        self.last_proto_scroll = 0.0  # Add this line with other initializations
        self.setup_gui()
        self.running = True
        
        # Open HTML file - Flexible path handling
        try:
            # Get the web_debuggerIDE1 directory path
            current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
            if current_dir != 'web_debuggerIDE1':
                print("Warning: Script not running from web_debuggerIDE1 directory")
            
            html_file = "WEb-IDE_Debugger1.html"
            html_path = os.path.join(os.path.dirname(__file__), html_file)
            html_url = 'file:///' + os.path.abspath(html_path).replace('\\', '/')
            
            if os.path.exists(html_path):
                webbrowser.open(html_url)
            else:
                print(f"HTML file not found. Make sure {html_file} is in the same directory as this script.")
        except Exception as e:
            print(f"Error opening HTML file: {e}")
        
        # Start packet capture
        threading.Thread(target=self.capture_packets, daemon=True).start()

    def setup_gui(self):
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Packet List Tab
        packet_frame = ttk.Frame(notebook)
        notebook.add(packet_frame, text='Packet Analysis')
        
        # Control frame with Live Display Mode and Auto-scroll
        speed_frame = ttk.Frame(packet_frame)
        speed_frame.pack(fill=tk.X, pady=5)
        ttk.Label(speed_frame, text="Live Display Mode", 
                 font=('Courier', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Add auto-scroll checkbox
        self.auto_scroll_var = tk.BooleanVar(value=True)
        auto_scroll_cb = ttk.Checkbutton(
            speed_frame, 
            text="Auto-scroll", 
            variable=self.auto_scroll_var
        )
        auto_scroll_cb.pack(side=tk.LEFT, padx=5)

        # Enhanced tree with columns
        # Add scrollbar for the tree
        tree_scroll = ttk.Scrollbar(packet_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(packet_frame, columns=(
            'Time', 'Source', 'Destination', 'Protocol', 
            'Length', 'Info'
        ), yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree.yview)
        
        # Bind scroll events to track position
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Statistics Tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text='Network Statistics')
        self.stats_text = tk.Text(stats_frame, font=('Courier', 10), state='disabled')
        self.stats_text.pack(fill=tk.BOTH, expand=True)

        # Network Forensics Tab
        forensics_frame = ttk.Frame(notebook)
        notebook.add(forensics_frame, text='Network Forensics')
        self.forensics_text = tk.Text(forensics_frame, font=('Courier', 10), state='disabled')
        self.forensics_text.pack(fill=tk.BOTH, expand=True)

        # Protocol Analysis Tab with scrollbar
        proto_frame = ttk.Frame(notebook)
        notebook.add(proto_frame, text='Protocol Analysis')
        
        # Add scrollbar to protocol analysis
        proto_scroll = ttk.Scrollbar(proto_frame)
        proto_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.proto_text = tk.Text(proto_frame, font=('Courier', 10), 
                                 state='disabled', yscrollcommand=proto_scroll.set)
        self.proto_text.pack(fill=tk.BOTH, expand=True)
        proto_scroll.config(command=self.proto_text.yview)

    def on_tree_select(self, event):
        """Track the last known scroll position"""
        self.last_scroll_position = self.tree.yview()[0]

    def analyze_packet(self, packet):
        try:
            time = datetime.now().strftime('%H:%M:%S.%f')
            
            # Default values
            src = dst = "Unknown"
            proto_name = "Unknown"
            length = 0
            sport = dport = 0
            info = "No info available"
            
            if IP in packet:
                src = packet[IP].src
                dst = packet[IP].dst
                proto = packet[IP].proto
                length = len(packet)
                
                # Protocol analysis with better error handling
                if TCP in packet:
                    proto_name = "TCP"
                    try:
                        sport = packet[TCP].sport
                        dport = packet[TCP].dport
                        flags = packet[TCP].flags
                        info = f"Port {sport}->{dport} Flags:{flags}"
                    except:
                        info = "Malformed TCP packet"
                
                elif UDP in packet:
                    proto_name = "UDP"
                    try:
                        sport = packet[UDP].sport
                        dport = packet[UDP].dport
                        info = f"Port {sport}->{dport}"
                    except:
                        info = "Malformed UDP packet"
                
                # Only update statistics if we have valid ports
                if sport and dport:
                    self.connections[f"{src}:{sport} -> {dst}:{dport}"] += 1
                else:
                    self.connections[f"{src} -> {dst}"] += 1
                
                self.packet_count += 1
                self.protocols[proto_name] += 1
                
                # Update GUI with mode-based timing
                packet_data = (time, src, dst, proto_name, length, info)
                # Simplified packet display - always live
                # Remember current scroll position
                current_scroll = self.tree.yview()[0]
                
                # Get current scroll position
                current_view = self.tree.yview()
                at_bottom = current_view[1] == 1.0
                
                # Insert packet at END instead of beginning
                self.tree.insert('', 'end', values=(
                    time, src, dst, proto_name, length, info
                ))
                
                # Always scroll to bottom if auto-scroll is enabled
                if self.auto_scroll_var.get():
                    self.tree.yview_moveto(1)
            
                # Update all analysis views
                if self.packet_count % 5 == 0:
                    self.update_forensics()
                    self.update_protocol_analysis()
                
                # Update statistics view every 10 packets
                if self.packet_count % 10 == 0:
                    self.update_statistics()

        except Exception as e:
            print(f"Error analyzing packet: {str(e)}")
            self.tree.insert('', 0, values=(
                datetime.now().strftime('%H:%M:%S.%f'),
                'ERROR', 'ERROR', 'ERROR',
                0, f'Analysis failed: {str(e)}'
            ))

    def analyze_dns(self, packet):
        try:
            qname = packet[DNS].qd.qname.decode()
            # Check for DGA (Domain Generation Algorithm) patterns
            if re.match(r'^[a-z0-9]{10,}\.', qname):
                self.suspicious_dns[qname] += 1
            # Check for DNS tunneling
            if len(qname) > 50:
                self.threats.append(f"Possible DNS tunneling: {qname}")
        except:
            pass

    def analyze_payload(self, packet):
        payload = bytes(packet[Raw])
        
        # Check for known malware patterns
        for pattern_name, pattern in self.known_malware_patterns.items():
            if re.search(pattern, payload):
                self.threats.append(f"Detected {pattern_name} pattern")
                
        # Data exfiltration detection
        if len(payload) > 1000:
            src = packet[IP].src
            self.data_exfil_stats[src] += len(payload)

    def detect_tunnel(self, packet):
        if ICMP in packet and Raw in packet:
            payload = bytes(packet[Raw])
            if len(payload) > 64:  # Suspicious ICMP payload size
                self.threats.append(f"Possible ICMP tunnel from {packet[IP].src}")

    def update_statistics(self):
        stats = "NETWORK STATISTICS:\n"
        stats += "═══════════════════\n\n"
        
        # Packet statistics
        stats += f"Total Packets: {self.packet_count}\n"
        stats += f"Active Connections: {len(self.connections)}\n\n"
        
        # Protocol distribution
        stats += "Protocol Distribution:\n"
        for proto, count in self.protocols.items():
            percentage = (count / self.packet_count) * 100
            stats += f"├─ {proto}: {count} ({percentage:.1f}%)\n"
        
        # Top connections
        stats += "\nTop Active Connections:\n"
        top_conns = sorted(self.connections.items(), key=lambda x: x[1], reverse=True)[:5]
        for conn, count in top_conns:
            stats += f"├─ {conn}: {count} packets\n"
        
        self.update_text_widget(self.stats_text, stats)

    def update_forensics(self):
        forensics = "NETWORK FORENSICS REPORT:\n"
        forensics += "════════════════════════\n\n"
        
        # Connection patterns
        forensics += "Connection Patterns:\n"
        for conn, count in sorted(self.connections.items(), key=lambda x: x[1], reverse=True)[:3]:
            forensics += f"📊 {conn}: {count} packets\n"

        self.update_text_widget(self.forensics_text, forensics)
        
    def update_port_process_map(self):
        """Update the mapping of ports to processes"""
        self.port_to_process.clear()
        try:
            # Get all network connections and their PIDs
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    connections = proc.info['connections']
                    if connections:
                        for conn in connections:
                            if conn.laddr:  # local address exists
                                port = str(conn.laddr.port)
                                self.port_to_process[port] = {
                                    'name': proc.info['name'],
                                    'pid': proc.info['pid']
                                }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"Error updating port map: {e}")

    def update_protocol_analysis(self):
        # Save current scroll position
        self.last_proto_scroll = self.proto_text.yview()[0]
        
        # Update port-process mapping first
        self.update_port_process_map()
        
        analysis = "ACTIVE PROGRAMS AND CONNECTIONS:\n"
        analysis += "═════════════════════════════\n\n"
        
        # Create a dictionary to group connections by process
        process_connections = defaultdict(list)
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    connections = proc.info['connections']
                    if connections:
                        for conn in connections:
                            if conn.status == 'ESTABLISHED':
                                process_connections[proc.info['name']].append({
                                    'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                                    'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                                    'type': conn.type,
                                    'status': conn.status
                                })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                
            # Display the organized information
            for prog_name, connections in process_connections.items():
                analysis += f"📌 {prog_name}\n"
                for conn in connections:
                    proto = "TCP" if conn['type'] == socket.SOCK_STREAM else "UDP"
                    analysis += f"   ├─ {proto} {conn['local']} → {conn['remote']}\n"
                analysis += "\n"
                
            if not process_connections:
                analysis += "No active network connections found.\n"
        
        except Exception as e:
            analysis += f"Error getting process information: {str(e)}\n"

        self.update_text_widget(self.proto_text, analysis)
        
        # Restore scroll position
        self.proto_text.yview_moveto(self.last_proto_scroll)

    def update_text_widget(self, widget, text):
        """Helper to update read-only text widgets"""
        # Save current scroll position
        current_scroll = widget.yview()[0]
        
        # Update text
        widget.config(state='normal')
        widget.delete(1.0, tk.END)
        widget.insert(tk.END, text)
        widget.config(state='disabled')
        
        # Restore scroll position after a small delay to ensure text is rendered
        widget.after(10, lambda: widget.yview_moveto(current_scroll))

    def capture_packets(self):
        """Capture network packets using scapy"""
        try:
            sniff(prn=self.analyze_packet, store=False)
        except Exception as e:
            print(f"Error in packet capture: {e}")
            
    def run(self):
        self.root.mainloop()
        self.running = False

if __name__ == "__main__":
    analyzer = NetworkAnalyzer()
    analyzer.run()
