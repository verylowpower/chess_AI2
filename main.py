#file nay se nhan input vao hien thi len
import pygame


from script import chess_engine, Smartmove_FINDER #truy cap module
from multiprocessing import Process, Queue


Width = Height = 512 #kich thuoc ban co 
Dimesion =8 #ti le 8x8
Sq_size= Height//Dimesion #// chia lam tron xuong
Max_fps=15 #dung de tao animation
Asset={}

def LoadAsset():
    Pieces=['bB','bK','bN','bP','bQ','bR','wB','wK','wN','wP','wQ','wR'] #ham nay se la ten cua cac quan co trong file asset
    for piece in Pieces: #su dung vong lap de load asset vao trong ham 
        Asset[piece]= pygame.transform.scale(pygame.image.load("asset/"+piece+".png"),(Sq_size,Sq_size)) #scale quan co theo o vuong
        
def main():
    pygame.init()       
    Screen = pygame.display.set_mode((Width,Height)) #hien thi cua so
    Clock = pygame.time.Clock() 
    Screen.fill(pygame.Color("white")) #fill mau
    Gs = chess_engine.Gamestate() #truy cap class gamestate roi gan vao Gs
    
    ValidMove = Gs.GetValidMove()#khi player di chuyen 1 quan co se luu vao list, sau do no se kiem tra xem nuoc di day co chieu tuong ko
    #khi player tao ra 1 nuoc di chieu tuong, doi phuong thay doi nuoc di thi ham nay se dc lam moi, tranh viec goi ham lien tuc lam game cham di
    MoveMade = False #day nhu 1 flag moi khi nuoc di dc tao ra
    Animate = False
    LoadAsset()
    running = True
    Sq_selected = () #tao tuple de track lan click cuoi cung (tuple:(row,col))
    Player_click = [] #track click cua nguoi choi, vd tuple[(7,4);(4,4)] nguoi choi click vao quan co o vi tri (7,4) sau do di chuyen ra vi tri (4,4)
    GameOver = False
    #thoat game 
    player_one = True #đúng khi người chơi quân trắng, sai khi Ai chơi quân trắng
    player_two = False #Như trên nhưng với cho quân đen
    AIthiking = False
    moveFinderProcess = None
    moveUndone = False
    while running:
        human_turn = (Gs.Wturn and player_one) or (not Gs.Wturn and player_two)
        #Kiểm tra người chơi hay máy chơi
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False    
                #track chuot
            elif e.type == pygame.MOUSEBUTTONDOWN:#ghi nhan xem chuot bam xuong(down) nhu nao, trong bao lau, trai hay phai,..
                if not GameOver:
                    Location=pygame.mouse.get_pos()#toa do x, y cua chuot
                    #lam nhu nay ta co the biet duoc chuot dang chon o vuong o vi tri nao
                    col = Location[0]//Sq_size
                    row = Location[1]//Sq_size
                    #print(Location)
                    #print(Sq_size)
                    #print(col,row)
                    #neu nhu player bam vao o vuong 2 lan thi no co the nhan dien la da di 1 nuoc, vay nen ta can tranh truong hop do
                    if Sq_selected == (row,col) or col >=8: #neu player click vao 1 o vuong 2 lan
                        Sq_selected =() #lam cho tuple rong = bo chon
                        Player_click =[] #nhu tren
                    else: #khi nuoc di day hop le
                        Sq_selected=(row,col) #luu 2 bien col, row vao tuple
                        Player_click.append(Sq_selected) #them o vuong duoc chon vao danh sach quan co duoc chon
                    
                    if len(Player_click)==2 and human_turn: 
                        move = chess_engine.Move(Player_click[0],Player_click[1],Gs.board)
                        
                        print(move.pieceMove[1] + move.GetChessNotation())
                        
                        if move in ValidMove:
                            if Gs.Wturn:
                                print("White turn!")
                            else:
                                print("Black Turn!")                 
                            Gs.MakeMove(move) #khi 1 nuoc di dung luat -> tiep tuc move
                            MoveMade = True #True thi cho phep quan co di 
                            Animate = True  
                            Sq_selected =() #reset vung chon cua player
                            Player_click = []
                        else:
                            Player_click = [Sq_selected]
                    
            #gan chuc nang
            elif e.type == pygame.KEYDOWN: #KEYDOWN la nhan phim
                if e.key == pygame.K_z: #gan vao phim z
                    Gs.UndoMove()
                    MoveMade = True
                    Animate = False
                    print("undo")
                    if AIthiking:
                        moveFinderProcess.terminate()
                        AIthiking = False
                    moveUndone = True
                
                if e.key == pygame.K_r: 
                    Gs = chess_engine.Gamestate()
                    ValidMove = Gs.GetValidMove()
                    Sq_selected = ()
                    Player_click = []
                    MoveMade = False
                    Animate = False
                    GameOver = False
                    if AIthiking:
                        moveFinderProcess.terminate()
                        AIthiking = False
                    moveUndone = False
            
        #AI tìm đường
        if not GameOver and not human_turn and not moveUndone:
            if not AIthiking:
                AIthiking = True
                print("thinking...")
                returnQueue = Queue() #used to pass data between threads
                moveFinderProcess = Process(target=Smartmove_FINDER.findBestMove, args=(Gs, ValidMove,returnQueue))
                moveFinderProcess.start() #call findBestMoves(Gs, ValidMove,returnQueue)
              
            if not moveFinderProcess.is_alive():
                print("done thinking")
                AI_move = returnQueue.get()
                if AI_move is None:
                    AI_move = Smartmove_FINDER.findRandomMove(ValidMove)
                Gs.MakeMove(AI_move)
                MoveMade = True
                Animate = True
                AIthiking = False
        
        if MoveMade:
            if Animate:
                Animation(Gs.Movelog[-1], Screen, Gs.board, Clock)
            ValidMove = Gs.GetValidMove()
            MoveMade = False 
            Animate = False
            moveUndone = False
            
        
        drawGamestate(Screen,Gs,ValidMove,Sq_selected)
        
        if Gs.CheckMate or Gs.StaleMate:
            GameOver = True
            drawEndGameText(Screen,text = 'Stalemate!!' if Gs.StaleMate else 'Black win!' if Gs.Wturn else 'White win!')
             
        Clock.tick(Max_fps)
        pygame.display.flip()


#chiu trach nhiem hien thi tat ca do hoa cua class Gamestate
def drawGamestate(Screen,Gs,ValidMove,Sq_selected):
    drawBoard(Screen) #ve o vuong tren ban co
    highlightSq(Screen,Gs,ValidMove,Sq_selected)
    drawPiece(Screen,Gs.board) #ve quan co

#ve o vuong
def drawBoard(Screen):
    global Colors
    #o vuong goc tren ben trai luon la mau sang
    Colors =[pygame.Color("white"),pygame.Color("gray")] #color dau la mau sang, sau la toi
    for r in range(Dimesion):
        for c in range(Dimesion): #su dung vong lap de to mau, neu le thi la sang con chan thi la toi
            Color = Colors[((r+c)%2)]
            pygame.draw.rect(Screen,Color,pygame.Rect(c*Sq_size, r*Sq_size, Sq_size, Sq_size))
        
#ve quan co su dung Gamestate
def drawPiece(Screen,board):
    for r in range(Dimesion): #dung vong lap de chen anh vao board trong class Gamestate
        for c in range(Dimesion):
            piece = board[r][c] #khai bao bien piece bang mang 2 chieu 
            if piece != "--": #neu quan co ko phai khoang trong (tham chieu ham board trong Gamestate)
                Screen.blit(Asset[piece],pygame.Rect(c*Sq_size,r*Sq_size,Sq_size,Sq_size))
                
def highlightSq(Screen,Gs,ValidMove,Sq_selected):
    if Sq_selected  != ():
        r,c = Sq_selected
        if Gs.board[r][c][0] == ("w" if Gs.Wturn else "b"):
            s = pygame.Surface((Sq_size,Sq_size))
            s.set_alpha(100)
            s.fill(pygame.Color('blue'))
            Screen.blit(s,(c*Sq_size,r*Sq_size))
            s.fill(pygame.Color('yellow'))
            for move in ValidMove:
                if move.startRow == r and move.startCol == c:
                    Screen.blit(s,(move.endCol*Sq_size,move.endRow*Sq_size))


def Animation(move, Screen, board, Clock):
    global Colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    Fps = 3
    frameCount = (abs(dR)+abs(dC))*Fps
    for f in range(frameCount+1):
        r,c = (move.startRow +dR*f/frameCount, move.startCol+dC*f/frameCount)
        drawBoard(Screen)
        drawPiece(Screen,board)
        
        Color = Colors[(move.endRow + move.endCol)%2]
        endSq = pygame.Rect(move.endCol*Sq_size,move.endRow*Sq_size,Sq_size,Sq_size)
        pygame.draw.rect(Screen,Color,endSq)
        if move.pieceCaptured != "--" :
            Screen.blit(Asset[move.pieceCaptured],endSq)
            
        if move.pieceMove != "--":
            Screen.blit(Asset[move.pieceMove], pygame.Rect(c*Sq_size,r*Sq_size,Sq_size,Sq_size))
        pygame.display.flip()
        Clock.tick(60)

def drawEndGameText(Screen,text):
    font = pygame.font.SysFont("Helvitca",32,True,False)
    textObject = font.render(text,0, pygame.Color('White'))
    textLocation = pygame.Rect(0,0,Width,Height).move(Width/2-textObject.get_width()/2,Height/2-textObject.get_height()/2)
    Screen.blit(textObject,textLocation)
    textObject = font.render(text,0,pygame.Color('Black')) 
    Screen.blit(textObject,textLocation.move(2,2))


                

if __name__=="__main__":
    main()
