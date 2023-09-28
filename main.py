#file nay se nhan input vao hien thi len
import pygame


from script import chess_engine #truy cap module


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
    Screen=pygame.display.set_mode((Width,Height)) #hien thi cua so
    Clock=pygame.time.Clock() 
    Screen.fill(pygame.Color("white")) #fill mau
    Gs=chess_engine.Gamestate() #truy cap class gamestate roi gan vao Gs
    LoadAsset()
    Sq_selected=() #tao tuple de track lan click cuoi cung (tuple:(row,col))
    Player_click=[] #track click cua nguoi choi, vd tuple[(7,4);(4,4)] nguoi choi click vao quan co o vi tri (7,4) sau do di chuyen ra vi tri (4,4)
    #thoat game 
    running=True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False    
                #track chuot
            elif e.type ==pygame.MOUSEBUTTONDOWN:#ghi nhan xem chuot bam xuong(down) nhu nao, trong bao lau, trai hay phai,..
                Location=pygame.mouse.get_pos()#toa do x, y cua chuot
                #gan toa do x y vao chuot 
                #lam nhu nay ta co the biet duoc chuot dang chon o vuong o vi tri nao
                col= Location[0]//Sq_size
                row = Location[1]//Sq_size
                #neu nhu player bam vao o vuong 2 lan thi no co the nhan dien la da di 1 nuoc, vay nen ta can tranh truong hop do
                if Sq_selected == (row,col): #neu player click vao 1 o vuong 2 lan
                    Sq_selected =() #lam cho tuple rong = bo chon
                    Player_click =[] #nhu tren
                else: #khi nuoc di day hop le
                    Sq_selected=(row,col) #luu 2 bien col, row vao tuple
                    Player_click.append(Sq_selected) #them o vuong duoc chon vao danh sach quan co duoc chon
                if len(Player_click)==2: 
                
            drawGamestate(Screen,Gs)
            Clock.tick(Max_fps)
            pygame.display.flip()

#chiu trach nhiem hien thi tat ca do hoa cua class Gamestate
def drawGamestate(Screen,Gs):
    drawBoard(Screen) #ve o vuong tren ban co
    drawPiece(Screen,Gs.board) #ve quan co
    

#ve o vuong
def drawBoard(Screen):
    #o vuong goc tren ben trai luon la mau sang
    Colors =[pygame.Color("white"),pygame.Color("dark green")] #color dau la mau sang, sau la toi
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
                
            



if __name__=="__main__":
    main()