import socket
import concurrent.futures
import time

# Define the target host and the range of ports to scan
TARGET_HOST = '127.0.0.1' # The host to scan (e.g., localhost)
PORT_RANGE_START = 7999   # Starting port for the scan
PORT_RANGE_END = 8081     # Ending port for the scan (inclusive)
SCAN_TIMEOUT = 1.0        # Timeout in seconds for each connection attempt

def scan_port(host, port, timeout):
    """
    Attempts to connect to a given port on a host.
    Returns a tuple (port, status_message).
    """
    try:
        # Create a new socket for each connection attempt
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout) # Set a timeout for the connection attempt
            s.connect((host, port)) # Attempt to connect
            
            # If connected, try to receive data (optional, but confirms service)
            try:
                data = s.recv(1024).decode('utf-8').strip()
                return port, f"OPEN (Service: {data})"
            except socket.timeout:
                return port, "OPEN (No immediate response)"
            except socket.error:
                return port, "OPEN (Connected, but error receiving data)"

    except socket.timeout:
        return port, "CLOSED (Timeout)" # Connection attempt timed out
    except socket.error as e:
        # Connection refused, host unreachable, etc.
        # Check if the error indicates "Connection refused" specifically
        if "Connection refused" in str(e):
            return port, "CLOSED (Connection refused)"
        else:
            return port, f"CLOSED (Error: {e})"
    except Exception as e:
        return port, f"CLOSED (Unexpected Error: {e})"

def main():
    print(f"Starting TCP Port Scan on {TARGET_HOST} from port {PORT_RANGE_START} to {PORT_RANGE_END}...")
    
    open_ports = []
    closed_ports = []
    
    # Use ThreadPoolExecutor for concurrent scanning
    # Adjust max_workers based on your system's capabilities and network
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Submit scan tasks for each port in the range
        future_to_port = {executor.submit(scan_port, TARGET_HOST, port, SCAN_TIMEOUT): port 
                          for port in range(PORT_RANGE_START, PORT_RANGE_END + 1)}
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                result_port, status_message = future.result()
                if "OPEN" in status_message:
                    open_ports.append((result_port, status_message))
                else:
                    closed_ports.append((result_port, status_message))
                # print(f"Port {result_port}: {status_message}") # Uncomment for real-time updates
            except Exception as exc:
                print(f"Port {port} generated an exception: {exc}")

    # Sort results for clear output
    open_ports.sort()
    closed_ports.sort()

    print("\n--- Scan Results ---")
    print(f"Target: {TARGET_HOST}")
    print(f"Scanned Ports: {PORT_RANGE_START}-{PORT_RANGE_END}")

    print("\nOpen Ports:")
    if open_ports:
        for port, status in open_ports:
            print(f"  {port}: {status}")
    else:
        print("  No open ports found in the specified range.")

    print("\nClosed/Filtered Ports:")
    if closed_ports:
        for port, status in closed_ports:
            print(f"  {port}: {status}")
    else:
        print("  All ports in the specified range were open (unlikely for a wide range).")

    print("\nScan complete.")

if __name__ == "__main__":
    main()
