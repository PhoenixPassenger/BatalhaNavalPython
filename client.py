import socket
import ast
import sys
import pickle
class Client:
	
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.addr = []
		self.connected = False
		ip = str(input('IP?\n'))
		port = int(input('Porta?\n'))
	
		self.connect(ip, port)

	def sendMessage(self, m):
		self.sock.sendto(pickle.dumps(m), (self.addr[0], self.addr[1]))


	def connect(self, ip, port):
	
		message = 'connect'
		self.sock.sendto(pickle.dumps(message), (ip, int(port)))
		
		while self.connected == False:
			data, self.addr = self.sock.recvfrom(1024)
			data =pickle.loads(data)
			if isinstance(self.addr, tuple) and data == 'conectado':
				if self.addr[0] == ip:
					self.connected = True

		print('conectado no ' + str(self.addr[0]))
		

		import game
		g = game.Game()
		g.p2 = g.newPlayer(2, g.ships[:], g.p2Field, g.p2BombField)

		self.sendMessage(['done', g.p2.field.field, g.p2.name])

		while data != 'gameDone':
			print ('Pera...')
			data, self.addr = self.sock.recvfrom(2048)
			data = pickle.loads(data)
			if data != '':
				dataList = data

				if dataList[0] == 'resultado':
					g.clear()
					if dataList[1] == 'X':
						print('Hit!')
					elif dataList[1] == 'O':
						print('Miss!')
					else:
						data = 'gameDone'
						print (dataList[1])
						sys.exit()

				elif dataList[0] == 'selectCell':
					g.clear()
					g.p2.field.field = dataList[1]
					print('Teu campo:\n')
					print(g.printfield(g.p2.field.field))
					print('\nCampo do cara:\n')
					print(g.printfield(g.p2.bombfield.field))
					cell = g.selectCell(g.p2)
					self.sendMessage(['cell', cell])

					while data != 'resultado':
						data, self.addr = self.sock.recvfrom(1024)
						data = pickle.loads(data)
						if data != '':
							dataList = data
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
				






