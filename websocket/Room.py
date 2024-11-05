class Room:
    def __init__(self, name: str, creator):
        self.name = name
        self.participants = [creator]
    

    def add_participant(self, participant):
        self.participants.append(participant)
        

    def remove_participant(self, participant) -> bool:
        for part in self.participants:
            if part == participant:
                self.participants.remove(participant)
        if self.participants == []:
            return True
        else:
            return False
    

    def sendmsg(self, msg, frm, server):
        reply = [frm.name, msg, [frm.color[0], frm.color[1], frm.color[2]]]
        self.sendall(reply, server)
    

    def sysmsg(self, msg, server):
        self.sendall(msg, server, 'sys')


    def sendall(self, msg, server, header: str = 'msg'):
        for cl in self.participants:
            cl.send(server, msg, header)


    def get_pos(self) -> dict:
        r = {}
        for cl in self.participants:
            r[cl.name] = [cl.x, cl.y]
        return r
    

    def move(self, server):
        play = []
        poss = self.get_pos()
        for player in list(poss.keys()):
            for cli in self.participants:
                if cli.name == player:
                    cl_color = cli.color
            play.append([player, [poss[f'{player}'][0], poss[f'{player}'][1]], [cl_color[0], cl_color[1], cl_color[2]]])
        self.sendall(play, server, 'move')
    

    def get_usernames(self) -> list:
        r = []
        for cl in self.participants:
            r.append(cl.name)
        return r
    