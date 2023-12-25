import socket


def obtener_ip_local():
    try:
        # Obtiene el nombre de host de la máquina local
        nombre_host = socket.gethostname()

        # Obtiene todas las direcciones IP asociadas al nombre de host
        direcciones_ips = socket.gethostbyname_ex(nombre_host)[2]

        return direcciones_ips

    except socket.error as e:
        print(f"Error al obtener la dirección IP: {e}")
        return None


# Ejemplo de uso
ip_local = obtener_ip_local()

if ip_local:
    print(f"La dirección IP local es: {ip_local}")
else:
    print("No se pudo obtener la dirección IP local.")