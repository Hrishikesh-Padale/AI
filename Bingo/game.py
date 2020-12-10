import pygame
import sys
from time import sleep
import random
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
background = pygame.image.load('green_bg.png')
cross = pygame.image.load('cross2.png')

pygame.init()

class cell:
	def __init__(self,value=0,status='unmarked'):
		self.value = value
		self.status = status
	def __str__(self):
		return '%d %s'%(self.value,self.status)

grid = []
for row in range(5):
    grid.append([])
    for column in range(11):
        grid[row].append(cell()) 

grid[0][5]=None
grid[1][5]=None
grid[2][5]=None
grid[3][5]=None
grid[4][5]=None
 
screen = pygame.display.set_mode((1094,700))
WIDTH = 94
HEIGHT = 94
MARGIN = 5

pygame.display.set_caption("BINGO")
 
done = False
font = pygame.font.SysFont('Arial', 25)
largefont = pygame.font.SysFont('Comic Sans MS', 45)
clock = pygame.time.Clock()


user_grid = []
for i in range(5):
	user_grid.append([])
	for j in range(5):
		user_grid[i].append(cell())

bot_grid = []
for i in range(5):
	bot_grid.append([])
	for j in range(5):
		bot_grid[i].append(cell())		

#print(bot_grid,user_grid)

user_marked_rows =[]
user_marked_cols = []
bot_marked_rows = []
bot_marked_cols =[]
user_marked_diagonals = []
bot_marked_diagonals = []

user_all_marked_cells = []
bot_all_marked_cells = []

user_marked_rows_by_number = []
user_marked_cols_by_number = []
user_marked_diags_by_number = []

bot_marked_rows_by_number = []
bot_marked_cols_by_number = []
bot_marked_diags_by_number = []

user_recent_move = '_'
bot_recent_move = '_'

font = pygame.font.Font('freesansbold.ttf', 25)
text1 = font.render("RESET", True, (255,255,0))  
textRect1 = text1.get_rect()
textRect1.center = (200,590)

quit = font.render("QUIT",True,(255,255,0))
quit_rect = quit.get_rect()
quit_rect.center = (450,590)

winner = None
Turn = random.choice([0,1])

def start():
	available = [i for i in range(1,26)]
	assigned = []
	for i in range(5):
		for j in range(5):
			grid[i][j] = cell(random.choice(available))
			user_grid[i][j] = cell(grid[i][j].value)
			available.remove(grid[i][j].value)

	available = [i for i in range(1,26)]
	assigned = []
	for i in range(5):
		for j in range(6,11):
			grid[i][j] = cell(random.choice(available))
			bot_grid[i-5][j-6] = cell(grid[i][j].value)
			available.remove(grid[i][j].value)

	Turn = 0
	user_marked_rows =[]
	user_marked_cols = []
	bot_marked_rows = []
	bot_marked_cols =[]
	user_marked_diagonals = []
	bot_marked_diagonals = []

	user_all_marked_cells = []
	bot_all_marked_cells = []

	user_marked_rows_by_number = []
	user_marked_cols_by_number = []
	user_marked_diags_by_number = []

	bot_marked_rows_by_number = []
	bot_marked_cols_by_number = []
	bot_marked_diags_by_number = []

	Turn = random.choice([0,1])

	print('Started new game')
	return (user_marked_rows,user_marked_cols,user_marked_diagonals,user_all_marked_cells,
		bot_marked_rows,bot_marked_cols,bot_marked_diagonals,bot_all_marked_cells,
		user_marked_rows_by_number,user_marked_cols_by_number,user_marked_diags_by_number,
		bot_marked_rows_by_number,bot_marked_cols_by_number,bot_marked_diags_by_number,Turn)


def update(grid):
    screen.blit(background,(0,0))
    for row in range(5):
        for column in range(11):
            color = WHITE
            try:
            	if grid[row][column].status == 'marked':
            	    color = BLACK
            except:
            	pass
            if column != 5:
                pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

            if column != 5:
            	if int(grid[row][column].value/10) == 0:
            		if grid[row][column].status == 'marked':
            			x = (MARGIN + WIDTH)*column+MARGIN
            			y =	(MARGIN + HEIGHT)*row+MARGIN
            			screen.blit(cross,(x,y))	
            		screen.blit(font.render(str(grid[row][column].value),True, (0,0,0)),((MARGIN + WIDTH) * column + MARGIN + 40,(MARGIN + HEIGHT) * row + MARGIN + 35))
            	else:
            		if grid[row][column].status == 'marked':
            			x = (MARGIN + WIDTH)*column+MARGIN
            			y =	(MARGIN + HEIGHT)*row+MARGIN
            			screen.blit(cross,(x,y))
            		screen.blit(font.render(str(grid[row][column].value),True, (0,0,0)),((MARGIN + WIDTH) * column + MARGIN + 30,(MARGIN + HEIGHT) * row + MARGIN + 35))
    
    pygame.draw.rect(screen,(120,120,120),(100,550,200,80))
    pygame.draw.rect(screen,(120,120,120),(350,550,200,80))
    screen.blit(quit,quit_rect)
    screen.blit(text1,textRect1)
    #print(user_recent_move)
    for i in user_marked_rows_by_number:
    	pygame.draw.line(screen,(255,0,0),(5,50+(i*100)),(493,50+(i*100)),3)
    for i in user_marked_cols_by_number:
    	pygame.draw.line(screen,(255,0,0),(50+(i*100),5),(50+(i*100),493),3)
    for i in user_marked_diags_by_number:
    	if i == 0:
    		pygame.draw.line(screen,(255,0,0),(5,5),(493,493),3)
    	if i == 1:
    		pygame.draw.line(screen,(255,0,0),(493,5),(5,493),3)

    for i in bot_marked_rows_by_number:
    	pygame.draw.line(screen,(255,0,0),(599,50+(i*100)),(1089,50+(i*100)),3)
    for i in bot_marked_cols_by_number:
    	pygame.draw.line(screen,(255,0,0),(651+(i*100),5),(651+(i*100),493),3)
    for i in bot_marked_diags_by_number:
    	if i == 0:
    		pygame.draw.line(screen,(255,0,0),(599,5),(1089,493),3)
    	if i == 1:
    		pygame.draw.line(screen,(255,0,0),(1089,5),(599,493),3)

    user_move = font.render(f"User chose : {user_recent_move}",True,(0,0,0))
    user_move_rect = user_move.get_rect()
    user_move_rect.center = (850,540)
    screen.blit(user_move,user_move_rect)
    bot_move = font.render(f"Bot  chose  : {bot_recent_move}",True,(0,0,0))
    bot_move_rect = bot_move.get_rect()
    bot_move_rect.center = (850,580)
    screen.blit(bot_move,bot_move_rect)
    if winner:
    	bingo = largefont.render("BINGO!",True,(255,0,0))
    	bingo_rect = bingo.get_rect()
    	bingo_rect.center = (460,660)
    	win = font.render(f"({winner} won)",True,(255,0,0))
    	win_rect = win.get_rect()
    	win_rect.center = (630,665)
    	screen.blit(win,win_rect)
    	screen.blit(bingo,bingo_rect)

#function to manage user's moves
def user_plays(user_grid):
	progress = len(user_marked_rows) + len(user_marked_diagonals) + len(user_marked_cols)
	for i in user_grid:
		count = 0
		for j in i:
			if j.status == 'marked':
				count += 1
		if count == 5 and i not in user_marked_rows and progress <= 5:
			user_marked_rows.append(i)
			user_marked_rows_by_number.append(user_grid.index(i))

	for i in range(5):
		count = 0
		col = []
		for j in range(5):
			if user_grid[j][i].status == 'marked':
				col.append(user_grid[j][i])	
				count += 1
		if count == 5 and col not in user_marked_cols and progress <= 5:
			user_marked_cols.append(col)
			user_marked_cols_by_number.append(i)

	count = 0
	diagonal = []
	for i in range(5):
		if user_grid[i][i].status == 'marked':
			diagonal.append(user_grid[i][i])
			count += 1

		if count == 5 and diagonal not in user_marked_diagonals and progress <= 5:
			user_marked_diagonals.append(diagonal)
			user_marked_diags_by_number.append(0)

	i = 0
	j = 4
	count = 0
	diagonal = []
	while i <= 4 and j >= 0 :
		if user_grid[i][j].status == 'marked':
			diagonal.append(user_grid[i][j])
			count += 1
		i += 1
		j -= 1
	if count == 5 and diagonal not in user_marked_diagonals and progress <= 5:
		user_marked_diagonals.append(diagonal)
		user_marked_diags_by_number.append(1)

	#print(user_marked_rows_by_number,user_marked_cols_by_number,user_marked_diags_by_number)

#funtion to manage bot's moves
def bot_plays(bot_grid):
	progress = len(bot_marked_rows)+len(bot_marked_cols)+len(bot_marked_diagonals)
	for i in bot_grid:
		count = 0
		for j in i:
			if j.status == 'marked':
				count += 1
		if count == 5 and i not in bot_marked_rows and progress <= 5:
			bot_marked_rows.append(i)
			bot_marked_rows_by_number.append(bot_grid.index(i))

	for i in range(5):
		count = 0
		col = []
		for j in range(5):
			if bot_grid[j][i].status == 'marked':
				col.append(bot_grid[j][i])	
				count += 1
		if count == 5 and col not in bot_marked_cols and progress <= 5:
			bot_marked_cols.append(col)
			bot_marked_cols_by_number.append(i)

	count = 0
	diagonal = []
	for i in range(5):
		if bot_grid[i][i].status == 'marked':
			diagonal.append(bot_grid[i][i])
			count += 1

		if count == 5 and diagonal not in bot_marked_diagonals and progress <= 5:
			bot_marked_diagonals.append(diagonal)
			bot_marked_diags_by_number.append(0)

	i = 0
	j = 4
	count = 0
	diagonal = []
	while i <= 4 and j >= 0 :
		if bot_grid[i][j].status == 'marked':
			diagonal.append(bot_grid[i][j])
			count += 1
		i += 1
		j -= 1
	if count == 5 and diagonal not in bot_marked_diagonals and progress <= 5:
		bot_marked_diagonals.append(diagonal)
		bot_marked_diags_by_number.append(1)

	#print(len(bot_marked_rows),len(bot_marked_cols),len(bot_marked_diagonals))

def find_best_move(bot_grid):
	rows = {}
	cols = {}
	diagonals = {}

	for i in bot_grid:
		row = []
		for j in i:
			row.append(j)
		if row not in bot_marked_rows:
			rows[bot_grid.index(i)] = row

	for i in range(5):
		col = []
		for j in range(5):
			col.append(bot_grid[j][i])
		if col not in bot_marked_cols:
			cols[i] = col

	diag1 = []
	diag2 = []
	for i in range(5):
		diag1.append(bot_grid[i][i])
	if diag1 not in bot_marked_diagonals:
		diagonals[0] = diag1

	i = 0
	j = 4
	while i <= 4 and j >= 0:
		diag2.append(bot_grid[i][j])
		i += 1
		j -= 1
	if diag2 not in bot_marked_diagonals:
		diagonals[1] = diag2

	rows_status = {}
	for i in rows:
		count = 0
		for j in rows[i]:
			if j.status =='unmarked':
				count += 1
		rows_status[i] = count
	
	cols_status = {}
	for i in cols:
		count = 0
		for j in cols[i]:
			if j.status =='unmarked':
				count += 1
		cols_status[i] = count
	

	diags_status = {}
	for i in diagonals:
		count = 0
		for j in diagonals[i]:
			if j.status == 'unmarked':
				count += 1
		diags_status[i] = count

		try:
			temp = min(rows_status.values()) 
			row_with_max_cells_marked = random.choice([key for key in rows_status if rows_status[key] == temp])
	
			temp = min(cols_status.values())
			col_with_max_cells_marked = random.choice([key for key in cols_status if cols_status[key] == temp])

			temp = min(diags_status.values())
			diag_with_max_cells_marked = random.choice([key for key in diags_status if diags_status[key] == temp])
		except:
			pass
	#print(row_with_max_cells_marked,rows_status[row_with_max_cells_marked])
	#print(col_with_max_cells_marked,cols_status[col_with_max_cells_marked])
	#print(diag_with_max_cells_marked,diags_status[diag_with_max_cells_marked],'\n')
	try:
		final_dict = {}
		final_dict[0]=(row_with_max_cells_marked,rows_status[row_with_max_cells_marked])
		final_dict[1]=(col_with_max_cells_marked,cols_status[col_with_max_cells_marked])
		final_dict[2]=(diag_with_max_cells_marked,diags_status[diag_with_max_cells_marked])
		choices = [final_dict[0][1],final_dict[1][1],final_dict[2][1]]

		#print(final_dict)
		optimal_choice = min(choices)
		type_of_choice = choices.index(optimal_choice)
		#print(choices,optimal_choice,type_of_choice)

		#bot choses a row to mark a cell
		if type_of_choice == 0:
			selected_row = final_dict[type_of_choice][0]
			#print(f'row {selected_row}')
			available_values_to_cross = []  
			for i in bot_grid[selected_row]:
				if i.status == 'unmarked':
					available_values_to_cross.append(i.value)

			selected_value = random.choice(available_values_to_cross)
			#print(available_values_to_cross,selected_value)
			return selected_value

		elif type_of_choice == 1:
			selected_col = final_dict[type_of_choice][0]
			#print(f'Col {selected_col}')
			available_values_to_cross = []
			for i in range(5):
				if bot_grid[i][selected_col]:
					if bot_grid[i][selected_col].status == 'unmarked':
						available_values_to_cross.append(bot_grid[i][selected_col].value)
			selected_value = random.choice(available_values_to_cross)
			#print(available_values_to_cross,selected_value)
			return selected_value

		elif type_of_choice == 2:
			selected_diag = final_dict[type_of_choice][0]
			#print(f'Diag {selected_diag}')
			available_values_to_cross = []
			if selected_diag == 0 :
				for i in range(5):
					if bot_grid[i][i].status == 'unmarked':
						available_values_to_cross.append(bot_grid[i][i].value)
				selected_value = random.choice(available_values_to_cross)
				#print(available_values_to_cross,selected_value)
				return selected_value

			elif selected_diag == 1:
				i = 0
				j = 4
				available_values_to_cross = []
				while i <= 4 and j >= 0 :
					if bot_grid[i][j].status == 'unmarked':	
						available_values_to_cross.append(bot_grid[i][j].value)
					i += 1
					j -= 1
				selected_value = random.choice(available_values_to_cross)
				#print(available_values_to_cross,selected_value)
				return selected_value
	except:
		pass
	#if there are all same number of cells avaiable to mark in row,col and diagonal then priority order is row > col > diag



#function to check if somebody has won the game
def result():
	if len(user_marked_rows) + len(user_marked_diagonals) + len(user_marked_cols) == 5:
		return 1
	elif len(bot_marked_rows) + len(bot_marked_diagonals) + len(bot_marked_cols) == 5:
		return 2

(user_marked_rows,user_marked_cols,user_marked_diagonals,user_all_marked_cells,
	bot_marked_rows,bot_marked_cols,bot_marked_diagonals,bot_all_marked_cells,
	user_marked_rows_by_number,user_marked_cols_by_number,user_marked_diags_by_number,
	bot_marked_rows_by_number,bot_marked_cols_by_number,bot_marked_diags_by_number,Turn) = start()

def gameover():
	crashed = False
	while not crashed:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				column = pos[0] // (WIDTH + MARGIN)
				row = pos[1] // (HEIGHT + MARGIN)
				if (row,column) in [(5,3),(6,3),(5,5),(5,4),(6,4),(6,5)]:
					print('Game ended')
					sys.exit()
		update(grid)
		clock.tick(60)
		pygame.display.flip()
	pygame.quit()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
        	if Turn == 0:
	        	pos = pygame.mouse.get_pos()
	        	column = pos[0] // (WIDTH + MARGIN)
	        	row = pos[1] // (HEIGHT + MARGIN)
	        	#print("Click ", pos, "Grid coordinates: ", row, column)
        	if column < 5 and Turn == 0:
        		try:
        			grid[row][column].status = 'marked'
        			user_grid[row][column].status = 'marked'
        			if (row,column) not in user_all_marked_cells:
        				user_all_marked_cells.append((row,column))
        				user_recent_move = grid[row][column].value 
        				Turn = 1
        				user_plays(user_grid)
        			if result() == 1:
        				winner = 'User'
        				done = True
        				Turn = None
        			elif result() == 2:
        				winner = 'Bot'
        				done = True
        				Turn = None
        			if not winner:
        				for i in range(5):
        					for j in range(6,11):
        						if grid[i][j].value == grid[row][column].value:
        							grid[i][j].status = 'marked'
        							bot_grid[i-5][j-6].status = 'marked'
        							bot_all_marked_cells.append((i,j-6))
        				bot_plays(bot_grid)
        		except:
        			pass
        	if (row,column) in [(5,1),(6,1),(5,2),(6,2)]:
        		(user_marked_rows,user_marked_cols,user_marked_diagonals,user_all_marked_cells,
        			bot_marked_rows,bot_marked_cols,bot_marked_diagonals,bot_all_marked_cells,
        			user_marked_rows_by_number,user_marked_cols_by_number,user_marked_diags_by_number,
        			bot_marked_rows_by_number,bot_marked_cols_by_number,bot_marked_diags_by_number,Turn) = start()		
        	if (row,column) in [(5,3),(6,3),(5,5),(5,4),(6,4),(6,5)]:
        		print('Game ended')
        		sys.exit()

        if result() == 1:
        	winner = 'User'
        	done = True
       		gameover()
        elif result() == 2:
        	winner = 'Bot'
        	done = True
        	gameover()
        
        if Turn == 1 and not winner:
        	move = find_best_move(bot_grid)
        	#print(f'Bot : {move}')
        	bot_recent_move = move
        	for i in range(5):
        		for j in range(6,11):
        			if grid[i][j].value == move:
        				grid[i][j].status = 'marked'
        				bot_grid[i-5][j-6].status = 'marked'
        				bot_all_marked_cells.append((i,j-6))
        	bot_plays(bot_grid) #call some bot function
        	if result() == 1:
        		winner = 'User'
        		done = True
        		gameover()
        	elif result() == 2:
        		winner = 'Bot'
        		done = True
        		gameover()
        	if not winner:
        		for i in range(5):
        			for j in range(5):
        				if grid[i][j].value == move:
        					grid[i][j].status = 'marked'
        					user_grid[i][j].status = 'marked'
        					user_all_marked_cells.append((i,j))
        		user_plays(user_grid)
        	if Turn != None:
        		Turn = 0

    try:
    	update(grid)
    	clock.tick(60)
    	pygame.display.flip()
    except:
    	pass



