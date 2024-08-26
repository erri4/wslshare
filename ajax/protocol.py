import struct

msg_format = struct.Struct('!I')
server_addr = ('127.0.0.1', 5001)

def pro_wr_msg(s, msg):
    msg_len = len(msg)
    msg = msg_format.pack(msg_len) + msg
    s.sendall(msg)

def pro_rd_msg(s):
    metadata = s.recv(msg_format.size)
    if metadata == b'':
        return b''
    msg_len = msg_format.unpack(metadata)[0]
    msg = s.recv(msg_len)
    return msg