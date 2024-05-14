!pip install scapy

from scapy.all import sniff, IP, TCP, wrpcap
import datetime
from collections import defaultdict

# Global variables to store packet counts and last seen timestamps for each source IP
packet_counts = defaultdict(int)
last_seen = defaultdict(datetime.datetime)

# Function to log packet information to a file
def log_packet(packet):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {packet.summary()}\n"
    with open("packet_log.txt", "a") as log_file:
        log_file.write(log_entry)

# Function to analyze packets and detect suspicious activity
def analyze_packet(packet):
    global packet_counts, last_seen

    # Log the packet
    log_packet(packet)

    # Detect port scanning (large number of SYN packets to different ports from the same source)
    if TCP in packet and packet[TCP].flags == "S":
        src_ip = packet[IP].src
        if packet_counts[src_ip] > 10:  # Threshold for number of SYN packets
            print(f"Suspicious activity detected - possible port scanning from {src_ip}")
        packet_counts[src_ip] += 1

    # Detect a large number of packets from a single source (possible DoS attack)
    if IP in packet:
        src_ip = packet[IP].src
        if (datetime.datetime.now() - last_seen[src_ip]).total_seconds() < 10:  # Threshold for time window (e.g., 10 seconds)
            packet_counts[src_ip] += 1
            if packet_counts[src_ip] > 50:  # Threshold for number of packets
                print(f"Suspicious activity detected - large number of packets from {src_ip}")
        else:
            packet_counts[src_ip] = 1
        last_seen[src_ip] = datetime.datetime.now()

# Sniff packets and call the analyze_packet function for each packet
def sniff_packets():
    sniff(prn=analyze_packet, store=0)

# Main function
if __name__ == "__main__":
    print("Packet sniffer started...")
    # Sniff packets in a separate thread
    sniff_packets()
