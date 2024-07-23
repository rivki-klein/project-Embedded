import socket
import io


def handle_client_data(client_data):
    return client_data


if __name__ == "__main__":
    host = '192.168.1.107'
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host} : {port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        data_buffer = io.BytesIO()

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                data_buffer.write(data)
                print(f"Received {len(data)} bytes of data")  # Debug message
                import camera
                num = camera.get_from_camera()
                # שליחת הערך num ללקוח כתשובה
                client_socket.send(str(num).encode('utf-8'))
        except Exception as e:
            print(f"Error receiving data: {e}")

        client_socket.close()

        data_buffer.seek(0)
        client_data = data_buffer.read().decode('utf-8')

        processed_data = handle_client_data(client_data)
        print("Client data:", processed_data)

        client_socket.close()
