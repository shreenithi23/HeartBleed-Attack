from json import JSONEncoder
import json


#handshake Records

#Hello Request(0,0x00)
#Client Hello(1,0x01)
#server Hello (2, 0x02)
#Certificate(11,0x0B)
#Server Key Exchange (12, 0x0C)
#Certificate Request (13 ,0x0D)
#Server Hello Done (14,0x0E)
#Certificate Verify (15 0x0F)
#Client key Ekexchange (16, 0x10)
#finished (20, 0x14)

H_SHAKE =22
H_BEAT= 24
C_HELLO = 1
S_HELLO =2
CERT=11
S_KEY_EX= 12
CERT_REQ= 13
S_HELLO_FIN =14
CERT_VERIFY = 15
C_KEY_EX =16
FIN =20
END= 21

class SSLPacket(object):
    def __init__(self, type=None, length=None, payload_type=None, payload=None, fin=False, version=1):
        self.type =type
        self.length= length
        self.version = version
        self.fin = fin
        self.payload_type = payload_type
        self.payload =payload

    def encode(self):
        d = {"type": self.type,
            "length": self.length,
            "version": self.version,
            "fin": self.fin,
            "payload_type": self.payload_type,
            "payload": self.payload,}
        return json.dumps(d).encode()

    def decode(self,byte_obj):
        string =byte_obj.decode()
        try:
            d=json.loads(string)
            self.type = d["type"]
            self.length =d["length"]
            self.version= d["version"]
            self.fin =d["fin"]
            self.payload_type= d["payload_type"]
            self.payload = d["payload"]
            return self
        except:
            return self
