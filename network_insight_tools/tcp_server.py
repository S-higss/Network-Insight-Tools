import socket
import threading
import sys
import time

# Define the host and a list of ports to listen on
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
LISTEN_PORTS = [8000, 8001, 8002, 8080] # Ports the server will listen on

def handle_client(conn, addr, port):
    """
    Handles an incoming client connection in a separate thread.
    Sends a welcome message and then closes the connection.
    """
    print(f"[Port {port}] Connected by {addr}")
    try:
        message = f"Hello from TCP server on port {port}!\n"
        conn.sendall(message.encode('utf-8')) # Send the message to the client
    except socket.error as e:
        print(f"[Port {port}] Error sending data to {addr}: {e}")
    finally:
        conn.close() # Ensure the connection is closed
        print(f"[Port {port}] Connection with {addr} closed.")

def start_server_on_port(port):
    """
    Starts a TCP server listening on a specific port.
    Accepts incoming connections and hands them off to handle_client.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, port)) # Bind the socket to the host and port
            s.listen() # Enable the server to accept connections
            print(f"Server listening on {HOST}:{port}...")
            
            while True:
                conn, addr = s.accept() # Accept a new connection
                # Start a new thread to handle the client connection
                client_handler = threading.Thread(target=handle_client, args=(conn, addr, port))
                client_handler.daemon = True # Allow main program to exit even if threads are running
                client_handler.start()
        except socket.error as e:
            print(f"Error starting server on port {port}: {e}")
            print(f"Port {port} might be in use or requires elevated privileges.")
        except KeyboardInterrupt:
            print(f"Server on port {port} is shutting down...")
        finally:
            s.close()

if __name__ == "__main__":
    print("Starting TCP/IP Server...")
    server_threads = []
    for port in LISTEN_PORTS:
        # Create and start a thread for each port
        server_thread = threading.Thread(target=start_server_on_port, args=(port,))
        server_thread.daemon = True # Daemon threads will exit when the main program exits
        server_threads.append(server_thread)
        server_thread.start()
        time.sleep(0.1) # Give a small delay for threads to start up

    print(f"All server threads started. Listening on ports: {LISTEN_PORTS}")
    print("Press Ctrl+C to stop the server.")
    
    try:
        # Keep the main thread alive so daemon threads can continue running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMain server process shutting down.")
        # No explicit join needed for daemon threads, they will terminate.
