from math import *
from os import *
#--------------------------------------------------------------------------------global vars
visual_assist=True
legend_toggle=help_toggle=False
ai=ai_turn=0
player=1
p1_start=p2_start=p1_current=p2_current=((0,0),(0,0))
number_of_blocks=w=h=0
board=[]
possible_moves=list()
possible_blocks=list()
messages={
		0:"play with human (0) or AI (1) [ai vs ai (2)]> ",
		1:"input board dimensions (w h)> ",
		2:"input number of blockades (n)> ",
		3:"input player start positions (x1 y1 x2 y2 x3 y3 x4 y4)> ",
		4:"input player{} move (x1 y1 x2 y2 x3 y3)> ",
		5:"input player{} move (x1 y1 x2 y2)> ",
		6:"player{} wins! \x1b[38;2;250;215;0m🏆\x1b[0m \nplay again? (y/n)> ",
		7:"human plays first (0) or AI (1)> ",
		8:"load manual (0) or default (1) values> "
		}
colors={
		"YF":"\x1B[1;33m",
		"RF":"\x1B[1;31m",
		"MF":"\x1B[1;35m",
		"BMF":"\x1B[5;35m",
		"CF":"\x1B[1;36m",
		"GF":"\x1B[1;32m",
		"BF":"\x1B[1;34m",
		"YB":"\x1B[1;33;43m",
		"RB":"\x1B[1;31;41m",
		"MB":"\x1B[1;45m",
		"CB":"\x1B[1;46m",
		"GB":"\x1B[1;42m",
		"BB":"\x1B[1;44m",
		"CLR":"\x1B[0m",
		"F":"\x1B[2m",
		"B":"\x1B[5m",
		"WHITE":"\x1B[38;2;250;250;250m",
		"GRAY":"\x1B[38;2;30;30;30m",
		"GRAY2":"\x1B[38;2;70;70;70m",
		"YF2":"\x1B[38;2;240;160;40m",
		"RF2":"\x1B[38;2;250;95;90m"
		}

legend={
		0:"\x1b[1;33m♟︎ \x1b[0m - player1",
		1:"  \x1b[1;31m♟︎ \x1b[0m - player2",
		2:"\x1b[1;32m║ \x1b[0m - player1 block",
		3:"  \x1b[1;34m═ \x1b[0m - player2 block ",
		4:"\x1b[1;35m⬚ \x1b[0m - possible moves",
		5:"  \x1b[38;2;70;70;70m+ \x1b[0m - possible blocks",
		6:"\x1b[1;35m+ \x1b[0m - possible move/block",
		7:"  \x1b[1;33m⚐ \x1b[0m - player1 start",
		8:"\x1b[1;31m⚐ \x1b[0m - player2 start"
		}
_help={
		0:"\n\x1B[1;33mformat poteza: trenutne x y pesaka, x y poteza, x y bloka.",
		1:"svaka komanda se odvaja razmakom, nigde nema zareza.\x1b[0m"
		}
logo=r"""
██████╗ ██╗      ██████╗  ██████╗██╗  ██╗ █████╗ ██████╗ ███████╗
██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔══██╗██╔══██╗██╔════╝
██████╔╝██║     ██║   ██║██║     █████╔╝ ███████║██║  ██║█████╗  
██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ██╔══██║██║  ██║██╔══╝  
██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗██║  ██║██████╔╝███████╗
╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝"""+"\n"
#---------------------------------------------------------------------------------------misc
def get_message(n):
	global messages
	if n!=4 and n!=5 and n!=6:
		return logo+"\n"+messages[n]
	else:
		return messages[n]

def restart_game():
	global visual_assist,help_toggle,legend_toggle,ai,ai_turn,player,p1_current,p2_current,p1_start,p2_start,number_of_blocks,w,h,board,possible_moves,possible_blocks
	visual_assist=True
	color_logo()
	legend_toggle=help_toggle=False
	ai=ai_turn=0
	player=1
	p1_start=p2_start=p1_current=p2_current=((0,0),(0,0))
	number_of_blocks=w=h=0
	board=[]
	possible_moves=list()
	possible_blocks=list()

def switch_player():
	global player
	if player==1:
		player=2
	else:
		player=1

def default_values():
	clear()
	try:
		x=int(input(get_message(8)))
		if x==0:
			return 0
		elif x==1:
			return 1
		else:
			return default_values()
	except ValueError:
		return default_values()

def color_logo():
	global logo
	logo=logo.replace("█",str(colors["RF2"]+"█"+colors["CLR"]))
	logo=logo.replace("╗",str(colors["YF2"]+"╗"+colors["CLR"]))
	logo=logo.replace("╔",str(colors["YF2"]+"╔"+colors["CLR"]))
	logo=logo.replace("═",str(colors["YF2"]+"═"+colors["CLR"]))
	logo=logo.replace("╚",str(colors["YF2"]+"╚"+colors["CLR"]))
	logo=logo.replace("║",str(colors["YF2"]+"║"+colors["CLR"]))
	logo=logo.replace("╝",str(colors["YF2"]+"╝"+colors["CLR"]))

#------------------------------------------------------------------------------------display
def clear():
	if name=="nt":
		system("cls")
	elif name=="posix":
		system("clear")
	print("\x1b[0m",end="")

def printf():
	global number_of_blocks,visual_assist,logo,p1_start,p2_start,board,w,h,possible_moves,possible_blocks,colors,legend,legend_toggle,_help,help_toggle
	clear()
	print(logo)
	print("      ",end="")
	for i in range(w):
		s=str(hex(i))[2:].upper()
		if len(s)==1:
			print(s+"   ",end="")
		else:
			print(s+"  ",end="")
	print("\n    ╔",end="")
	for i in range(w*2-1):
		if i%2==0:
			print("══",end="")
		if i%2!=0:
			print("═╦",end="")
	print("═╗\n",end="")
	for i in range(h*2-1):
		print("  ",end="")
		s=str(hex(int(i/2)))[2:].upper()
		if len(s)==1 and i%2==0 and (board[i][0]!=1 and board[i][0]!=2):
			print(s+" ║ ",end="")
		elif len(s)==2 and i%2==0 and (board[i][0]!=1 and board[i][0]!=2):
			print(s+"║ ",end="")
		elif len(s)==1 and i%2==0 and (board[i][0]==1 or board[i][0]==2):
			print(s+" ║",end="")
		elif len(s)==2 and i%2==0 and (board[i][0]==1 or board[i][0]==2):
			print(s+"║",end="")
		else: 
			print("  ╠"+colors["GRAY"]+"─",end="")
		for j in range(w*2-1):
			if board[i][j]==1:
				print(colors["YF"],end="")
				print(" ♟︎ ",end="")
				print(colors["CLR"],end="")
			elif board[i][j]==2:
				print(colors["RF"],end="")
				print(" ♟︎ ",end="")
				print(colors["CLR"],end="")
			elif (i,j)==(p1_start[0][0]*2,p1_start[0][1]*2) or (i,j)==(p1_start[1][0]*2,p1_start[1][1]*2) and (i,j) not in possible_moves:
				print(colors["YF"],end="")
				print("⚐ ",end="")
				print(colors["CLR"],end="")
			elif (i,j)==(p2_start[0][0]*2,p2_start[0][1]*2) or (i,j)==(p2_start[1][0]*2,p2_start[1][1]*2) and (i,j) not in possible_moves:
				print(colors["RF"],end="")
				print("⚐ ",end="")
				print(colors["CLR"],end="")
			elif visual_assist==True and (i,j) in possible_moves and (i,j) in possible_blocks and  board[i][j]==0:
				print(colors["MF"],end="")
				print("+ ",end="") 
				print(colors["CLR"],end="")
			elif visual_assist==True and (i,j) in possible_moves and (i,j) not in possible_blocks and board[i][j]==0:
				print(colors["MF"],end="")
				print("⬚ ",end="") 
				print(colors["CLR"],end="")
			elif visual_assist==True and (i,j) in possible_blocks and board[i][j]==0:
				print(colors["GRAY2"],end="")
				print("+ ",end="")
				print(colors["CLR"],end="")
			elif board[i][j]==-1 and i%2!=0:
				print(colors["GF"],end="")
				print("║",end="")
				print(colors["CLR"],end="")
				print(colors["GRAY"],end="")
				print("─",end="")
				print(colors["CLR"],end="")
			elif board[i][j]==-1 and i%2==0 and board[i][j+1]!=1 and board[i][j+1]!=2:
				print(colors["GF"],end="")
				print("║ ",end="")
				print(colors["CLR"],end="")
			elif board[i][j]==-1 and i%2==0 and (board[i][j+1]==1 or board[i][j+1]==2):
				print(colors["GF"],end="")
				print("║",end="")
				print(colors["CLR"],end="")
			elif board[i][j]==-2:
				print(colors["BF"],end="")
				print("══",end="")
				print(colors["CLR"],end="")
			elif i%2!=0 and j%2==0:	
				print(colors["GRAY"],end="")
				print("──",end="")
				print(colors["CLR"],end="")
			elif i%2!=0 and j%2!=0:	
				print(colors["GRAY"],end="")
				print("┼─",end="")
				print(colors["CLR"],end="")
			elif j%2!=0 and board[i][j+1]!=1 and board[i][j+1]!=2:
				print(colors["GRAY"],end="")
				print("│ ",end="")
				print(colors["CLR"],end="")
			elif j%2!=0 and (board[i][j+1]==1 or board[i][j+1]==2):
				print(colors["GRAY"],end="")
				print("│",end="")
				print(colors["CLR"],end="")
			else:
				print("  ",end="")
		s=str(hex(int(i/2)))[2:].upper()
		if len(s)==1 and i%2==0:
			print("║ "+s,end="")
		elif len(s)==2 and i%2==0:
			print("║"+s,end="")
		else: 
			print("╣",end="")
		if legend_toggle==True and i<len(legend):
			print(" ",legend[i],end="")
		print("\n",end="")
	print("    ╚═",end="")
	for i in range(w*2-1):
		if i%2==0:
			print("══",end="")
		if i%2!=0:
			print("╩═",end="")
	print("╝\n      ",end="")
	for i in range(w):
		s=str(hex(i))[2:].upper()
		if len(s)==1:
			print(s+"   ",end="")
		else:
			print(s+"  ",end="")
	print("\n",end="")
	if help_toggle==True:
		for i in range(len(_help)):
			print(_help[i])
	if player==1:
		print("\n    ",colors["YB"],colors["WHITE"],"BLOCKS LEFT: ",int(number_of_blocks/2),colors["CLR"])
	elif player==2:
		print("\n    ",colors["RB"],colors["WHITE"],"BLOCKS LEFT: ",int(number_of_blocks/2),colors["CLR"])
	
	print("\nv - visual assist on\off\nl - toggle legend on\off\nh - toggle help on\off\nq - quit\n")
#--------------------------------------------------------------------------------------input
def input_board_dimensions():
	try:
		clear()
		x,y=map(int,input(get_message(1)).split())
		return x,y
	except ValueError:
		return input_board_dimensions()

def input_number_of_blocks(d):
	global number_of_blocks
	try:
		clear()
		if d==1:
			x=9
		else:
			x=int(input(get_message(2)))
		if x<9 or x>18:
			input_number_of_blocks(d)
		number_of_blocks=x*2
	except ValueError:
		input_number_of_blocks(d)

def input_positions(d):
	try:
		clear()
		if d==1:
			return 3,3,3,7,10,3,10,7
		x1,y1,x2,y2,x3,y3,x4,y4=map(int,input(get_message(3)).split())
		return x1,y1,x2,y2,x3,y3,x4,y4
	except ValueError:
		return input_positions(d)

def input_player_move():
	global player,legend_toggle,help_toggle,visual_assist
	printf()
	try:
		s=input(get_message(4).format(player))
		if s=='v':
			visual_assist=not visual_assist
			printf()
			return input_player_move()
		elif s=='l':
			legend_toggle=not legend_toggle
			printf()
			return input_player_move()
		elif s=='h':
			help_toggle=not help_toggle
			printf()
			return input_player_move()
		elif s=='q':
			exit()
		else:
			x1,y1,x2,y2,x3,y3=map(int,s.split())
			return x1,y1,x2,y2,x3,y3
	except ValueError:
		return input_player_move()

def input_player_move_no_blocks():
	global player
	printf()
	try:
		x1,y1,x2,y2=map(int,input(get_message(5).format(player)).split())
		return x1,y1,x2,y2
	except ValueError:
		return input_player_move_no_blocks()

def who_plays_first():
	global ai_turn
	clear()
	try:
		c=int(input(get_message(7)))
		if c==0:
			ai_turn=0
		elif c==1:
			ai_turn=1
		else:
			who_plays_first()
	except ValueError:
		who_plays_first()	

def ai_or_human():
	global ai
	clear()
	try:
		c=int(input(get_message(0)))
		if c==0:
			ai=c
		elif c==1:
			ai=c
			who_plays_first()
		elif c==2:
			ai=c
		else:
			ai_or_human()
	except ValueError:
		ai_or_human()	
#--------------------------------------------------------------------------------------setup
def create_board(d):
	global w,h,board,number_of_blocks
	if d==1:
		w=14
		h=11
	else:
		w,h=input_board_dimensions()
	if w<14 or h<11 or w>28 or h>23 or w%2!=0 or h%2==0:
		create_board(d)
	board=[[0 for x in range(w*2)]for y in range(h*2)]

def add_players(d):
	global w,h,board,p1_current,p2_current,p1_start,p2_start
	try:
		y1,x1,y2,x2,y3,x3,y4,x4=input_positions(d)
		if (x1==x2 and y1==y2) or (x1==x3 and y1==y3) or (x1==x4 and y1==y4) or (x2==x3 and y2==y3) or (x2==x4 and y2==y4) or (x3==x4 and y3==y4):
			add_players()
		else:
			board[x1*2][y1*2]=1
			board[x2*2][y2*2]=1
			board[x3*2][y3*2]=2
			board[x4*2][y4*2]=2
			p1_current=p1_start=((x1,y1),(x2,y2))
			p2_current=p2_start=((x3,y3),(x4,y4))
	except IndexError:
		add_players(d)
#--------------------------------------------------------------------------------------logic
def validmove(x1,y1,x2,y2):
	global board,player
	printf()
	try:
		if board[x1*2][y1*2]==1 and (p2_start[0]==(x2,y2) or p2_start[1]==(x2,y2)):
			if x2==x1-1 and y1==y2:
				return True
			if x2==x1+1 and y1==y2:
				return True
			if x2==x1 and y1+1==y2:
				return True
			if x2==x1 and y1-1==y2:
				return True
		if board[x1*2][y1*2]==2 and (p1_start[0]==(x2,y2) or p1_start[1]==(x2,y2)):
			if x2==x1-1 and y1==y2:
				return True
			if x2==x1+1 and y1==y2:
				return True
			if x2==x1 and y1+1==y2:
				return True
			if x2==x1 and y1-1==y2:
				return True
	#ako novo polje nije prazno i nisu iste
		if board[x2*2][y2*2]!=0:
			return False
		#levo desno gore dole
		if y2>=0 and x2>=0 and x2<w*2 and y2<h*2:
			if y2==y1:
				if x2==x1+2 and board[x1*2+1][y1*2]==0 and board[x1*2+3][y1*2]==0:
					return True
				if x2==x1-2 and board[x1*2-1][y1*2]==0 and board[x1*2-3][y1*2]==0:
					return True
			if x2==x1:
				if y2==y1+2 and board[x1*2][y1*2+1]==0 and board[x1*2][y1*2+3]==0:
					return True
				if y2==y1-2 and board[x1*2][y1*2-1]==0 and board[x1*2][y1*2-3]==0:
					return True
			#dijagonale
			if x2==x1-1 and y2==y1-1 and board[x1*2][y1*2-1]==0 and board[x1*2-1][y1*2]==0 and board[x1*2-1][y1*2-1]==0:
				return True
			if x2==x1-1 and y2==y1+1 and board[x1*2][y1*2+1]==0  and board[x1*2-1][y1*2]==0 and board[x1*2-1][y1*2+1]==0:
				return True
			if x2==x1+1 and y2==y1-1 and board[x1*2][y1*2-1]==0 and board[x1*2+1][y1*2]==0 and board[x1*2+1][y1*2-1]==0:
				return True
			if x2==x1+1 and y2==y1+1 and board[x1*2+1][y1*2]==0 and board[x1*2+1][y1*2]==0 and board[x1*2+1][y1*2+1]==0:
				return True
		return False
	except IndexError:
		return False 

def validblock(x,y):
	printf()
	try:
		global board,player,number_of_blocks
		#dodavanje bloka
		if player==1: #vertikalni
			if x*2<w*2-4 and y*2<h*2+4: #granice su dobre
				return True
		elif player==2: #horizontalno
			if x*2<w*2-8 and y*2<h*2+4: #granice su dobre 
				return True
		return False
	except IndexError:
		return False 

def update_player_location(x1,y1,x2,y2):
	global player,p1_current,p2_current
	if player==1:
		if p1_current[0]==(x1,y1):
			t=list(p1_current)
			t[0]=(x2,y2)
			p1_current=tuple(t)
		else:
			t=list(p1_current)
			t[1]=(x2,y2)
			p1_current=tuple(t)
	else:
		if p2_current[0]==(x1,y1):
			t=list(p2_current)
			t[0]=(x2,y2)
			p2_current=tuple(t)
		else:
			t=list(p2_current)
			t[1]=(x2,y2)
			p2_current=tuple(t)

def play_move(x1,y1,x2,y2):
	global board,player
	board[x2*2][y2*2]=player
	board[x1*2][y1*2]=0
	update_player_location(x1,y1,x2,y2)

def set_block(x,y):
	global board,player,number_of_blocks
	if player==1: #vertikalni
		board[x*2][y*2+1]=-1
		board[x*2+1][y*2+1]=-1
		board[x*2+2][y*2+1]=-1
		number_of_blocks-=1
		return True
	elif player==2: #horizontalno
		board[x*2+1][y*2]=-2
		board[x*2+1][y*2+1]=-2
		board[x*2+1][y*2+2]=-2
		number_of_blocks-=1
		return True	
	return False

def move():
	global board,player,possible_moves,possible_blocks
	state_operator_set()
	if number_of_blocks>0:
		y1,x1,y2,x2,y3,x3=input_player_move()
		if (x2*2,y2*2) in possible_moves and (x3*2,y3*2) in possible_blocks:
			play_move(x1,y1,x2,y2)
			set_block(x3,y3)
		else:
			move()
	else:
		y1,x1,y2,x2=input_player_move_no_blocks()
		if (x2*2,y2*2) in possible_moves:
			play_move(x1,y1,x2,y2)
		else:
			move()
	state_operator_remove()

def check_win():
	global board,player,p1_current,p1_start,p2_current,p2_start
	printf()
	if p1_current[0]==p2_start[0]:
		p1_current=((-1,-1),(p1_current[1]))
		p2_start=((-1,-1),(p2_start[1]))
	if p1_current[0]==p2_start[1]:
		p1_current=((-1,-1),(p1_current[1]))
		p2_start=((p2_start[0]),(-1,-1))
	if p1_current[1]==p2_start[0]:
		p1_current=((p1_current[0]),(-1,-1))
		p2_start=((-1,-1),(p2_start[1]))
	if p1_current[1]==p2_start[1]:
		p1_current=((p1_current[0]),(-1,-1))
		p2_start=((p2_start[0]),(-1,-1))
	if p2_current[0]==p1_start[0]:
		p2_current=((-1,-1),(p2_current[1]))
		p1_start=((-1,-1),(p1_start[1]))
	if p2_current[0]==p1_start[1]:
		p2_current=((-1,-1),(p2_current[1]))
		p1_start=((p1_start[0]),(-1,-1))
	if p2_current[1]==p1_start[0]:
		p2_current=((p2_current[0]),(-1,-1))
		p1_start=((-1,-1),(p1_start[1]))
	if p2_current[1]==p1_start[1]:
		p2_current=((p2_current[0]),(-1,-1))
		p1_start=((p1_start[0]),(-1,-1))
	#p1 win
	if p1_current==((-1,-1),(-1,-1)):
		s=str(input(get_message(6).format(player)))
		if s=='y':
			game_setup()	
		if s=='n':
			exit()
		else:
			check_win()
	#p2 win
	if p2_current==((-1,-1),(-1,-1)):
		s=str(input(get_message(6).format(player)))
		if s=='y':
			game_setup()	
		if s=='n':
			exit()
		else:
			check_win()

def state_operator_remove():
	global possible_moves,possible_blocks
	possible_moves.clear()
	possible_blocks.clear()

def state_operator_set():
	global w,h,board,player,p1_current,p1_start,p2_current,p2_start,possible_moves,possible_blocks,number_of_blocks
	#da li je 1 player stigo
	if player==1:
		x1=p1_current[0][0]
		y1=p1_current[0][1]
		x2=p1_current[1][0]
		y2=p1_current[1][1]
		x3=p2_start[0][0]
		y3=p2_start[0][1]
		x4=p2_start[1][0]
		y4=p2_start[1][1]
	if player==2:
		x1=p2_current[0][0]
		y1=p2_current[0][1]
		x2=p2_current[1][0]
		y2=p2_current[1][1]
		x3=p1_start[0][0]
		y3=p1_start[0][1]
		x4=p1_start[1][0]
		y4=p1_start[1][1]
	#cords
	cords1=[(x1,y1),(x2,y2)]
	cords2=[(x3,y3),(x4,y4)]
	for i in range(2):#ovde prolazi 2 puta za oba pesaka igraca koji je trenutno na potezu
		t1=cords1[i][0]
		t2=cords1[i][1]
		if t1==-1:
			continue
		for j in range(2):
			t3=cords2[i][0]
			t4=cords2[i][1]
			if t3==-1:
				continue
#			if board[t3*2][t4*2]==0:
			ps=0
			if player==1:
				ps=p2_start
			else:
				ps=p1_start
			#ako je cilj na 1 polje
			if t2+1<w and t1==t3 and t2+1==t4:
				if ((t1,t2+1)==ps[0] and board[ps[0][0]*2][ps[0][1]*2]==0) or ((t1,t2+1)==ps[1] and board[ps[1][0]*2][ps[1][1]*2]==0):
					possible_moves.append((t3*2,t4*2))
			if t2-1>=0 and t1==t3 and t2-1==t4:
				if ((t1,t2-1)==ps[0] and board[ps[0][0]*2][ps[0][1]*2]==0) or ((t1,t2-1)==ps[1] and board[ps[1][0]*2][ps[1][1]*2]==0):
					possible_moves.append((t3*2,t4*2))
			if t1+1<h and t2==t4 and t1+1==t3:
				if ((t1+1,t2)==ps[0] and board[ps[0][0]*2][ps[0][1]*2]==0) or ((t1+1,t2)==ps[1] and board[ps[1][0]*2][ps[1][1]*2]==0):
					possible_moves.append((t3*2,t4*2))
			if t1-1>=0 and t2==t4 and t1-1==t3: 
				if ((t1-1,t2)==ps[0] and board[ps[0][0]*2][ps[0][1]*2]==0) or ((t1-1,t2)==ps[1] and board[ps[1][0]*2][ps[1][1]*2]==0):
					possible_moves.append((t3*2,t4*2))
		#normalno 2 polja
		if t1*2+4<h*2 and board[t1*2+1][t2*2]==0 and board[t1*2+3][t2*2]==0 and board[t1*2+4][t2*2]==0:
			possible_moves.append((t1*2+4,t2*2))
		if t1*2-4>=0 and board[t1*2-1][t2*2]==0 and board[t1*2-3][t2*2]==0 and board[t1*2-4][t2*2]==0:
			possible_moves.append((t1*2-4,t2*2))
		if t2*2+4<w*2 and board[t1*2][t2*2+1]==0 and board[t1*2][t2*2+3]==0 and board[t1*2][t2*2+4]==0:
			possible_moves.append((t1*2,t2*2+4))
		if t2*2-4>=0 and board[t1*2][t2*2-1]==0 and board[t1*2][t2*2-3]==0 and board[t1*2][t2*2-4]==0:
			possible_moves.append((t1*2,t2*2-4))
		#dijag
		if t1*2-2>=0 and t1*2+2<h*2 and t2*2-2>=0 and t2*2+2<w*2:
 			if board[t1*2][t2*2-1]!=0 and board[t1*2-1][t2*2]!=0 and board[t1*2-1][t2*2-2]!=0 and board[t1*2-2][t2*2-1]!=0:
 				pass
 			else:
 				if board[t1*2-1][t2*2-1]==0:
 					possible_moves.append((t1*2-2,t2*2-2))
 			if board[t1*2][t2*2+1]!=0 and board[t1*2-1][t2*2]!=0 and board[t1*2-1][t2*2+2]!=0 and board[t1*2-2][t2*2+1]!=0:
 				pass
 			else:
 				if board[t1*2-1][t2*2+1]==0:
 					possible_moves.append((t1*2-2,t2*2+2))
 			if board[t1*2][t2*2-1]!=0 and board[t1*2+1][t2*2]!=0 and board[t1*2+1][t2*2-2]!=0 and board[t1*2+2][t2*2-1]!=0:
 				pass
 			else:
 				if board[t1*2+1][t2*2-1]==0:
 					possible_moves.append((t1*2+2,t2*2-2))
 			if board[t1*2][t2*2+1]!=0 and board[t1*2+1][t2*2]!=0 and board[t1*2+1][t2*2+2]!=0 and board[t1*2+2][t2*2+1]!=0:
 				pass
 			else:
 				if board[t1*2+1][t2*2+1]==0:
 					possible_moves.append((t1*2+2,t2*2+2))
 #
#		if board[t1*2][t2*2-1]<0:
#			if board[t1*2-1][t2*2]==0:
#				possible_moves.append((t1*2-2,t2*2-2))
#			if board[t1*2+1][t2*2]==0:
#				possible_moves.append((t1*2+2,t2*2-2))
#		if board[t1*2][t2*2+1]<0:
#			if board[t1*2-1][t2*2]==0:
#				possible_moves.append((t1*2-2,t2*2+2))
#			if board[t1*2+1][t2*2]==0:
#				possible_moves.append((t1*2+2,t2*2+2))
#		if board[t1*2-1][t2*2]<0:
#			if board[t1*2][t2*2-1]==0:
#				possible_moves.append((t1*2-2,t2*2-2))
#			if board[t1*2][t2*2+1]==0:
#				possible_moves.append((t1*2+2,t2*2-2))
#		if board[t1*2+1][t2*2]<0:
#			if board[t1*2][t2*2-1]==0:
#				possible_moves.append((t1*2-2,t2*2+2))
#			if board[t1*2][t2*2+1]==0:
#				possible_moves.append((t1*2+2,t2*2+2))
#		if board[t1*2-1][t2*2]==0 and board[t1*2+1][t2*2]==0 and board[t1*2][t2*2-1]==0 and board[t1*2-1][t2*2+1]==0:
#				possible_moves.append((t1*2-2,t2*2+2))
#				possible_moves.append((t1*2+2,t2*2+2))
#				possible_moves.append((t1*2+2,t2*2-2))
#				possible_moves.append((t1*2-2,t2*2-2))
#
#		if t1*2-2>=0 and t2*2-2>=0 and board[t1*2-1][t2*2-1]==0 and board[t1*2-1][t2*2-2]==0 and board[t1*2-2][t2*2-1]==0 and board[t1*2][t2*2-1]==0 and board[t1*2-1][t2*2]==0 and board[t1*2-2][t2*2-2]==0:
#			possible_moves.append((t1*2-2,t2*2-2))
#		if t1*2-2>=0 and t2*2+2<w*2 and board[t1*2-1][t2*2+1]==0  and board[t1*2-2][t2*2+1]==0  and board[t1*2-1][t2*2+2]==0 and board[t1*2-1][t2*2]==0 and board[t1*2][t2*2+1]==0 and board[t1*2-2][t2*2+2]==0:
#			possible_moves.append((t1*2-2,t2*2+2))
#		if t1*2+2<h*2 and t2*2-2>=0 and board[t1*2+1][t2*2-1]==0 and board[t1*2+2][t2*2-1]==0 and board[t1*2+1][t2*2-2]==0 and board[t1*2+1][t2*2]==0 and board[t1*2][t2*2-1]==0 and board[t1*2+2][t2*2-2]==0:
#			possible_moves.append((t1*2+2,t2*2-2))
#		if t1*2+2<h*2 and t2*2+2<w*2 and board[t1*2+1][t2*2+1]==0  and board[t1*2+2][t2*2+1]==0  and board[t1*2+1][t2*2+2]==0 and board[t1*2+1][t2*2]==0 and board[t1*2][t2*2+1]==0 and board[t1*2+2][t2*2+2]==0:
#			possible_moves.append((t1*2+2,t2*2+2))
	if number_of_blocks==0:
		return
	#sve moguce pozicije zida...
	if player==1: #vertikalni
		for x in range(h-1):	
			for y in range(w-1):	
				if x*2<h*2-2 and y*2<w*2+4: #granice su dobre
					if board[x*2][y*2+1]==0 and board[x*2+1][y*2+1]==0 and board[x*2+2][y*2+1]==0:
						if check_blocks(x,y):																				#ovde mora da bude if uvek
							possible_blocks.append((x*2,y*2))
	elif player==2: #horizontalno
		for x in range(h-1):	
			for y in range(w-1):	
				if x*2<h*2-2 and y*2<w*2+4: #granice su dobre 
					if board[x*2+1][y*2]==0 and board[x*2+1][y*2+1]==0 and board[x*2+1][y*2+2]==0:
						if check_blocks(x,y):																				#ovde mora da bude if uvek
							possible_blocks.append((x*2,y*2))
def unset_block(x,y):
	global board,player,number_of_blocks
	if player==1: #vertikalni
		board[x*2][y*2+1]=0
		board[x*2+1][y*2+1]=0
		board[x*2+2][y*2+1]=0
	elif player==2: #horizontalno
		board[x*2+1][y*2]=0
		board[x*2+1][y*2+1]=0
		board[x*2+1][y*2+2]=0
	number_of_blocks+=1

def check_blocks(x,y):
	global p1_current,p2_current,p1_start,p2_start
#	if set_block(x,y):
#		for i in range(2):
#			for j in range(2):
#				if p1_current[i]!=p2_start[j]:
#					if find_path(p1_current[i],p2_start[j])==[]:
#						unset_block(x,y)
#						return False
#		for i in range(2):
#			for j in range(2):
#				if p2_current[i]!=p1_start[j]:
#					if find_path(p2_current[i],p1_start[j])==[]:
#						unset_block(x,y)
#						return False															#uvek zbog -1 -1 upada u false zasto
	set_block(x,y)
	if find_path(p1_current[0],p2_start[0])==[] and p1_current[0]!=p2_start[0] and p1_current[0]!=(-1,-1) and p2_start[0]!=(-1,-1):				#ovde je problem e sad
		unset_block(x,y)
		return False
	if find_path(p1_current[0],p2_start[1])==[] and p1_current[0]!=p2_start[1] and p1_current[0]!=(-1,-1)and p2_start[1]!=(-1,-1):
		unset_block(x,y)
		return False
	if find_path(p1_current[1],p2_start[0])==[] and p1_current[1]!=p2_start[0] and p1_current[1]!=(-1,-1)and p2_start[0]!=(-1,-1):
		unset_block(x,y)
		return False
	if find_path(p1_current[1],p2_start[1])==[] and p1_current[1]!=p2_start[1] and p1_current[1]!=(-1,-1)and p2_start[1]!=(-1,-1):
		unset_block(x,y)
		return False
	if find_path(p2_current[0],p1_start[0])==[] and p2_current[0]!=p1_start[0] and p2_current[0]!=(-1,-1)and p1_start[0]!=(-1,-1):
		unset_block(x,y)
		return False
	if find_path(p2_current[0],p1_start[1])==[] and p2_current[0]!=p1_start[1] and p2_current[0]!=(-1,-1)and p1_start[1]!=(-1,-1):
		unset_block(x,y)
		return False
	if find_path(p2_current[1],p1_start[0])==[] and p2_current[1]!=p1_start[0] and p2_current[1]!=(-1,-1)and p1_start[0]!=(-1,-1):
		unset_block(x,y)
		return False
	if find_path(p2_current[1],p1_start[1])==[] and p2_current[1]!=p1_start[1] and p2_current[1]!=(-1,-1)and p1_start[1]!=(-1,-1):
		unset_block(x,y)
		return False
	unset_block(x,y)	# -> inverzna funkcija od set_block
	return True
 #	return False

def game_loop():
	global ai,ai_turn
	while(True):
		printf()
		if ai==0:
			move()
			check_win()
			switch_player()
		elif ai==1:
			if ai_turn==0:
				move()
				check_win()
				switch_player()
				ai_move()
				check_win()
				switch_player()
			if ai_turn==1:
				ai_move()
				check_win()
				switch_player()
				move()
				check_win()
				switch_player()
		elif ai==2:
			ai_move()
			check_win()
			switch_player()
			ai_move()
			check_win()
			switch_player()
#-----------------------------------------------------------------------------------------ai
def rastojanje(start, end):
	return sqrt(pow(abs(start[0]-end[0]),2)+pow(abs(start[1]-end[1]),2))

def find_path(start, end):
	global board
	path = list()
	if start==end or start==(-1,-1) or end==(-1,-1):
		return path 
	grid=[[0 for x in range(w*2)]for y in range(h*2)]
	for i in range(h*2):
		for j in range(w*2):
			grid[i][j]=board[i][j]
	path_length = 0
#	if start[0]==end[0] and start[1]==end[1]:	bolje da vraca samo [] za ovaj slucaj
#		path.append((start[0], start[1]))
#		return path
	grid[start[0]][start[1]] = 0
	grid[end[0]][end[1]] = 0
	visited = set()
	to_visit =  set()
	prev_loc = dict()
	g = dict()
	end_found = False
	to_visit.add(start)
	visited.add(start)
	prev_loc[start] = None
	g[start] = rastojanje(start, end)
	while (not end_found) and len(to_visit) > 0:
		node = None
		for next_node in to_visit:
			if node is None or g[next_node] + grid[next_node[0]*2][next_node[1]*2] < g[node] + grid[node[0]*2][node[1]*2]:
				#najmanje rastojanje do kraja + rastojanje do pocetka
				node = next_node
		if node == end:
			end_found = True
			break
		neighbours = find_neighbours(node,grid)
		for neighbour in neighbours: 
			if neighbour not in to_visit and neighbour not in visited:
				prev_loc[neighbour] = node
				to_visit.add(neighbour)
				grid[neighbour[0]*2][neighbour[1]*2] = grid[node[0]*2][node[1]*2] + 1
				g[neighbour] = rastojanje(neighbour, end)
			else:
				if g[neighbour] + grid[neighbour[0]*2][neighbour[1]*2] > g[neighbour] + g[node] + grid[node[0]*2][node[1]*2] + 1:
					grid[neighbour[0]*2][neighbour[1]*2] = grid[node[0]*2][node[1]*2] + 1
					prev_loc[neighbour] = node
					if neighbour in visited:
						visited.remove(neighbour)
						to_visit.add(neighbour)
		to_visit.remove(node)
		visited.add(node)
	if end_found:
		path.append(end)
		node = prev_loc[end]
		while node is not None:
			path.append(node)
			node = prev_loc[node]
			path_length+=1
		path.reverse()            
	return path 

def find_neighbours(node: tuple,grid) -> list[tuple]:
	global w,h
	neighbours = []
	if node[0]-1 >= 0 and grid[node[0]*2-1][node[1]*2]==0:
		neighbours.append((node[0]-1, node[1]))#gore
	if node[0]+1 < h and grid[node[0]*2+1][node[1]*2]==0:
		neighbours.append((node[0]+1, node[1]))#dole
	if node[1]-1 >= 0 and grid[node[0]*2][node[1]*2-1]==0:
		neighbours.append((node[0], node[1]-1))#levo
	if node[1]+1 < w and grid[node[0]*2][node[1]*2+1]==0:
		neighbours.append((node[0], node[1]+1))#desno
	return neighbours

def ai_move():
	global number_of_blocks,player,board,ai_turn,p1_start,p1_current,p2_start,p2_current,possible_moves,possible_blocks
	import time
	time.sleep(.1)
	state_operator_set()
	printf()
	paths=[]
	for i in range(2):
		for j in range(2):
			if player==1:
				if p1_current[i]!=p2_start[j]:
					paths.append(find_path(p1_current[i],p2_start[j]))
			elif player==2:
				if p2_current[i]!=p1_start[j]:
					paths.append(find_path(p2_current[i],p1_start[j]))
	paths=list(filter(lambda x: x, paths)) 	
	p=min(paths,key=len)
	if len(p)==2:
		play_move(p[0][0],p[0][1],p[1][0],p[1][1])
	elif len(p)>2:
		play_move(p[0][0],p[0][1],p[2][0],p[2][1])
#	for i in p:
#		if (i[0]*2,i[1]*2) in possible_moves:
#			play_move(p[0][0],p[0][1],i[0],i[1])
	if number_of_blocks>0:
		ai_block()
	state_operator_remove()
	printf()

def ai_block():
	global number_of_blocks,player,board,ai_turn,p1_start,p1_current,p2_start,p2_current,possible_moves,possible_blocks
	while True:
		state_operator_set()
		paths=[]
		for i in range(2):
			for j in range(2):
				if player==2:
					if p1_current[i]!=p2_start[j]:
						paths.append(find_path(p1_current[i],p2_start[j])) 
				elif player==1:
					if p2_current[i]!=p1_start[j]:
						paths.append(find_path(p2_current[i],p1_start[j]))
		paths=[x for x in paths if x]	
		p=min(paths,key=len)
#		print(number_of_blocks)
#		print(paths)
#		print(p)
		for i in range(len(p)-1):
			if (p[i+1][0]*2,p[i+1][1]*2) in possible_blocks:
				set_block(p[i+1][0],p[i+1][1])
#				print(p[i+1][0],p[i+1][1])
				return
			if len(p)==2 and (p[1][0]*2,p[1][1]*2) in possible_blocks:
				set_block(p[1][0],p[1][1])
#				print(p[1][0],p[1][1])
				return
			else:
#				print(number_of_blocks)
#				print(player)
#				print(possible_blocks)
#				print(p1_current,p2_current,p1_start,p2_start)
				set_block(int(possible_blocks[0][0]/2),int(possible_blocks[0][1]/2))
#				print(int(possible_blocks[r][0]/2),int(possible_blocks[r][1]/2))
				return
		state_operator_remove()
	return
##---------------------------------------------------------------------------------------main
def game_setup():
	restart_game()
	d=default_values()
	ai_or_human()
	create_board(d)
	input_number_of_blocks(d)
	add_players(d)
	game_loop()
try:
	game_setup()
except KeyboardInterrupt:
	#debug
	pass	
