import socket
import ast
import sys

class Client:
	
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.addr = []
		self.connected = False
		ip = int(input('IP?\n'))
		port = int(input('Porta?\n'))
	
		self.connect(ip, port)

	def sendMessage(self, m):
		self.sock.sendto(str(m), (self.addr[0], self.addr[1]))

	def toList(self, s):
		l = ast.literal_eval(s)
		return l

	def connect(self, ip, port):
	
		message = 'connect'
		self.sock.sendto(message, (ip, int(port)))
		
		while self.connected == False:
			data, self.addr = self.sock.recvfrom(1024)
			if isinstance(self.addr, tuple) and data == 'conectado':
				if self.addr[0] == ip:
					self.connected = True

		print ('conectado no ' + str(self.addr[0]))
		

		import game
		g = game.Game() #Starts the game
		g.p2 = g.newPlayer(2, g.ships[:], g.p2Field, g.p2BombField)

		self.sendMessage(['done', g.p2.field.field, g.p2.name])

		while data != 'gameDone': #waits for the 'gameDone' message from the correct ip
			print ('Pera...')
			data, self.addr = self.sock.recvfrom(2048) # buffer size is 2048 bytes
			if data != '':
				dataList = self.toList(data)
				if dataList[0] == 'selectCell':
					g.clear()
					g.p2.field.field = dataList[1]
					print ('Teu campo:\n')
					print(g.printfield(g.p2.field.field))
					print ('\nCampo do cara:\n')
					print(g.printfield(g.p2.bombfield.field))
					cell = g.selectCell(g.p2)
					self.sendMessage(['cell', cell])

					while data != 'result': #waits for the 'result' message from the correct ip
						data, self.addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
						if data != '':
							dataList = self.toList(data)
							data = dataList[0]
							if data == 'resultado':
								g.clear()
								if dataList[1] == 'X':
									print ('Boa tigrão!')
								elif dataList[1] == 'O':
									print ('Putz, vacilou!')
								else:
									data = 'gameDone'
									print (dataList[1])
									sys.exit()
								g.p2.bombfield.field[cell[0]][int(cell[1])] = dataList[1]
								print ('Teu campo:\n')
								print(g.printfield(g.p2.field.field))
								print ('\nAs inimiga:\n')
								print (g.printfield(g.p2.bombfield.field))
					data = ''
				
				elif dataList[0] == 'resultado':
					g.clear()
					if dataList[1] == 'X':
						print ('Hit or!')
					elif dataList[1] == 'O':
						print ('Miss, i guess you never miss hã!')
					else:
						data = 'gameDone'
						print (dataList[1])
						sys.exit() #Exit the application





