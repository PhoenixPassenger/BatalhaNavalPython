import socket
import ast
import sys
import threading
import player
import pickle

class Server:

	def __init__(self):
		self.threads = []

		self.ip = socket.gethostbyname(socket.gethostname())
		self.port = 12345
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.bind((self.ip, self.port))
		self.addr = []
		self.connected =  False
		self.serverDone = False
		self.clientDone = False

		print("Seu IP: " + self.ip + " e porta: " + str(self.port))

	def sendMessage(self, m):
		self.sock.sendto(pickle.dumps(m), (self.addr[0], self.addr[1]))

	def waitForClient(self):

		data = ''
		while len(self.addr) == 0 or data != 'done':
			data, self.addr = self.sock.recvfrom(4096)
			data = pickle.loads(data)
			
			if data != '':
				dataList = data
				data = dataList[0]
				self.enemyField = dataList[1]
				self.enemyName = dataList[2]
		
		self.clientDone = True



	def connect(self):

		while len(self.addr) == 0 or data != 'connect':
			data, self.addr = self.sock.recvfrom(1024)
			data = pickle.loads(data)

		print(str(self.addr[0]) + ' conectado')
		self.connected = True

		self.sendMessage('conectado')


		thread = threading.Thread(target=self.waitForClient)
		thread.start()
		self.threads.append(thread)

		import game
		g = game.Game()
		g.p1 = g.newPlayer(1, g.ships[:], g.p1Field, g.p1BombField)
		self.done = True
		
		g.clear()

		self.threads[0] = None
		thread = None
		if self.clientDone == False:
			print('Esperando...')
			self.waitForClient()
		
		print ('Cliente')

		g.p2Field.field = self.enemyField
		g.p2 = player.Player(self.enemyName, g.ships[:], g.p2Field, g.p2BombField)

		while g.anythingLeft(g.p1.field.field) and g.anythingLeft(g.p2.field.field):
			g.clear()
			print('Seu campo:\n')
			print(g.printfield(g.p1.field.field))
			print ('\nCampo do inimigo:\n')
			print(g.printfield(g.p1.bombfield.field))
			cell = g.selectCell(g.p1)
			g.bomb(g.p1, g.p2, cell[0], cell[1])
			g.clear()

			if g.result == 'X':
				print ('Acertou, mizeravi!')
			elif g.result == 'O':
				print ('Erroooooou!')
			else:
				print (g.result)
				self.sendMessage(['resultado', g.result])
				sys.exit()

			print('Seu campo:\n')
			print(g.printfield(g.p1.field.field))
			print('\nCampo do inimigo :\n')
			print(g.printfield(g.p1.bombfield.field))

			if g.anythingLeft(g.p1.field.field) and g.anythingLeft(g.p2.field.field):
				self.sendMessage(['selectCell', g.p2.field.field])
				data = ''
				print('Esperando...')
				while len(self.addr) == 0 or data != 'cell':
					data, self.addr = self.sock.recvfrom(2048)
					data=pickle.loads(data)
					if data != '':
						dataList = data
						data = dataList[0]
						cell = dataList[1]

				g.bomb(g.p2, g.p1, cell[0], cell[1])
				
				if g.result == 'X' or g.result == 'O':
					self.sendMessage(['resultado', g.result])
				else:
					print (g.result)
					self.sendMessage(['resultado', g.result])
					sys.exit()


