import pygame


class Gamestate():
        def __init__(this):
            #tao ban co de quan co vao vi tri
            
            this.board =[
                ["bR","bN","bB","bK","bQ","bB","bN","bR"],
                ["bP","bP","bP","bP","bP","bP","bP","bP"],
                ["--","--","--","--","--","--","--","--"],
                ["--","--","--","--","--","--","--","--"],
                ["--","--","--","--","--","--","--","--"],
                ["--","--","--","--","--","--","--","--"],
                ["wP","wP","wP","wP","wP","wP","wP","wP"],
                ["wR","wN","wB","wQ","wK","wB","wN","wR"]
                ]
            this.MoveUnit = {"P":this.PawnMove,"R":this.RookMove,"N":this.KnightMove,
                             "B":this.BishopMove,"Q":this.QueenMove,"K":this.KingMove}
            this.Wturn= True #xac dinh dang den luot cua ai, trang hay den
            this.Movelog=[] #dung de luu cac nuoc di
            this.WKlocation = (7,4)
            this.BKlocation = (0,4)
            this.CheckMate = False #dang chieu tuong
            this.StaleMate = False #vua het nuoc di
            this.enpassant = ()
            
        def MakeMove(this,move):
            this.board[move.startRow][move.startCol] = "--"
            this.board[move.endRow][move.endCol] = move.pieceMove
            this.Movelog.append(move)#luu vao movelog 
            this.Wturn = not this.Wturn #doi luot
            #update vi tri cua king neu di chuyen
            if move.pieceMove == "wK":
                this.WKlocation = (move.endRow,move.endCol)
            elif move.pieceMove == "bK":
                this.BKlocation = (move.endRow,move.endCol)
            #phong cap
            if move.pawnPromotion:
                this.board[move.endRow][move.endCol] = move.pieceMove[0] + "Q"
                
            if move.enpassantMove:
                this.board[move.startRow][move.endCol] = "--"
                
            if move.pieceMove[1] == "P" and abs(move.startRow-move.endRow) == 2:
                this.enpassant = ((move.startRow + move.endRow)//2, move.startCol)
            else:
                this.enpassant = ()
            
        def UndoMove(this): #undo 
            if len(this.Movelog) != 0: #neu movelog co phan tu
                move = this.Movelog.pop() #ham pop xoa phan tu cuoi cung cua danh sach
                this.board[move.startRow][move.startCol]= move.pieceMove #vi tri bat dau
                this.board[move.endRow][move.endCol] = move.pieceCaptured #vi tri ket thuc 
                this.Wturn = not this.Wturn #swap
                
                if move.pieceMove == "wK":
                    this.WKlocation = (move.startRow,move.startCol)
                elif move.pieceMove == "bK":
                    this.BKlocation = (move.startRow,move.startCol)
                    
                if move.enpassantMove:
                    this.board[move.endRow][move.endCol] == "--"
                    this.board[move.startRow][move.endCol] == move.pieceCaptured
                    this.enpassant = (move.endRow,move.endCol)
                    
                if move.pieceMove[1]== "P" and abs(move.startRow - move.endRow) == 2:
                    this.enpassant = ()
                
        def GetValidMove(this): #ham nay se xem co nuoc di nao chieu tuong ko
            tempEnpassant = this.enpassant
            moves = this.GetAllMove()
            for i in range(len(moves)-1,-1,-1):
                this.MakeMove(moves[i])
                this.Wturn = not this.Wturn
                if this.InCheck():
                    moves.remove(moves[i])
                this.Wturn = not this.Wturn
                this.UndoMove()
            if len(moves) == 0:
                if this.InCheck():
                    this.CheckMate = True
                else:
                    this.StaleMate = True
            else:
                this.CheckMate = False
                this.StaleMate = False
                
            this.enpassant = tempEnpassant
            
            return moves
        
        #xem co dang bi chieu tuong ko?
        def InCheck(this):
            if this.Wturn:
                return this.SqUnderAtk(this.WKlocation[0], this.WKlocation[1])
            else:
                return this.SqUnderAtk(this.BKlocation[0], this.BKlocation[1])
        
        #du doan xem doi phuong co the an quan nao
        def SqUnderAtk(this,r,c):
            this.Wturn = not this.Wturn #swap turn
            oppMove = this.GetAllMove()
            this.Wturn = not this.Wturn #swap lai
            for move in oppMove:
                if move.endRow == r and move.endCol == c: #dang cb an o nay
                    return True
            return False
        
        #khi ta chon 1 quan co, ham nay se nhan dien day la quan gi, trang hay den, co dang dung luot ko, sau do tra ve nuoc di cua quan do 
        def GetAllMove(this):
            moves = [] 
            for r in range(len(this.board)): #su dung vong lap de do tren ma tran 2 chieu
                for c in range(len(this.board)):
                    turn = this.board[r][c][0] #[row][col][chu cai dau tien] tham chieu nhu tren phan tu board
                    if(turn == 'w' and this.Wturn) or (turn == 'b' and not this.Wturn):
                        piece = this.board[r][c][1]#loai quan co
                        this.MoveUnit[piece](r,c,moves)
            return moves
        
        def PawnMove(this,r,c,moves):
            if this.Wturn: #tot trang
                if this.board[r-1][c] == "--": #kiem tra xem o truoc mat la o trong hay ko    
                    moves.append(Move((r,c),(r-1,c),this.board))
                    if r == 6 and this.board[r-2][c] == "--":
                        moves.append(Move((r,c),(r-2,c),this.board)) 
                #an quan
                if c-1 >= 0: #an quan ben trai
                    if this.board[r-1][c-1][0] == "b":
                        moves.append(Move((r,c),(r-1,c-1),this.board))
                    elif (r-1,c-1) == this.enpassant:
                        moves.append(Move((r,c),(r-1,c-1),this.board,enpassantMove=True))
                        
                if c+1 <= 7: #an quan ben phai
                    if this.board[r-1][c+1][0] == "b":
                        moves.append(Move((r,c),(r-1,c+1),this.board))
                    elif (r-1,c+1) == this.enpassant:
                        moves.append(Move((r,c),(r-1,c+1),this.board,enpassantMove=True))
            else: #den
                if this.board[r+1][c] == "--": #kiem tra xem o truoc mat la o trong hay ko    
                    moves.append(Move((r,c),(r+1,c),this.board))
                    if r == 1 and this.board[r+2][c] == "--":
                        moves.append(Move((r,c),(r+2,c),this.board)) 
                #an quan
                if c+1 <= 7: #an quan ben phai
                    if this.board[r+1][c-1][0] == "w":
                        moves.append(Move((r,c),(r+1,c+1),this.board))
                    elif (r+1,c+1) == this.enpassant:
                        moves.append(Move((r,c),(r+1,c+1),this.board,enpassantMove=True))
                        
                if c-1 >= 0: #an quan ben trai
                    if this.board[r+1][c-1][0] == "w":
                        moves.append(Move((r,c),(r+1,c-1),this.board))
                    elif (r+1,c-1) == this.enpassant:
                        moves.append(Move((r,c),(r+1,c-1),this.board,enpassantMove=True))
                
        def RookMove(this,r,c,moves):
            direction = ((-1,0),(1,0),(0,-1),(0,1)) #tren trai duoi phai
            EnemyColor = "b" if this.Wturn else "w"
            for d in direction:
                for i in range(1,8):
                    endRow = r + d[0]*i
                    endCol = c + d[1]*i
                    if 0<=endRow<8 and 0<=endCol<8: #tren ban co
                        endPiece=this.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),this.board))
                        elif endPiece[0]==EnemyColor: #khi co quan doi phuong
                            moves.append(Move((r,c),(endRow,endCol),this.board))
                            break
                        else: #khi gap quan cung mau
                            break
                    else: 
                        break
          
        def BishopMove(this,r,c,moves):
            direction = ((-1,1),(1,-1),(-1,-1),(1,1)) #tren trai duoi phai
            EnemyColor = "b" if this.Wturn else "w"
            for d in direction:
                for i in range(1,8):
                    endRow = r + d[0]*i
                    endCol = c + d[1]*i
                    if 0<=endRow<8 and 0<=endCol<8: #tren ban co
                        endPiece=this.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),this.board))
                        elif endPiece[0]==EnemyColor: #khi co quan doi phuong
                            moves.append(Move((r,c),(endRow,endCol),this.board))
                            break
                        else: #khi gap quan cung mau
                            break
                    else: 
                        break
                    
        def KnightMove(this,r,c,moves):
            direction =((2,-1),(-2,1),(1,-2),(-1,2),(-1,-2),(1,2),(2,1),(-2,-1))
            allycolor ="w" if this.Wturn else "b"
            for m in direction:
                endRow = r + m[0]
                endCol = c + m[1]
                if 0 <= endRow <8 and 0 <= endCol <8:
                    endPiece = this.board[endRow][endCol]
                    if endPiece[0]!= allycolor:
                        moves.append(Move((r,c),(endRow,endCol),this.board))
       
        def QueenMove(this,r,c,moves):
            this.BishopMove(r,c,moves)
            this.RookMove(r,c,moves)
        
        def KingMove(this,r,c,moves):
            direction = ((-1,-1),(1,1),(1,-1),(-1,1),(1,0),(-1,0),(0,1),(0,-1))
            allycolor = "w" if this.Wturn else "b"
            for i in range(8):
                endRow = r + direction[i][0]
                endCol = c + direction[i][1]
                if 0<= endRow <8 and 0<= endCol <8:
                    endPiece = this.board[endRow][endCol]
                    if endPiece[0] != allycolor:
                        moves.append(Move((r,c),(endRow,endCol),this.board))
           
class Move():
        #ki hieu o hang doc va hang ngang cua ban co
        #gia tri cua no trong ma tran 2 chieu    
        #trong co vua rank la hang va file la cot
        RanktoRow={"1":7,"2":6,"3":5,"4":4,
                   "5":3,"6":2,"7":1,"8":0} 
        RowtoRank={v:k for k, v in RanktoRow.items()}
        
        FiletoCol={"a":0,"b":1,"c":2,"d":3,
                   "e":4,"f":5,"g":6,"h":7}
        ColtoFile={v:k for k, v in FiletoCol.items()}
        

        def __init__(this,StartSq,EndSq,board,enpassantMove = False):  
            #quan co di chuyen tu vi tri 
            this.startRow=StartSq[0]
            this.startCol=StartSq[1]
            #den vi tri nay
            this.endRow=EndSq[0]
            this.endCol=EndSq[1]
            #cho biet quan co nao dang duoc chon
            this.pieceMove=board[this.startRow][this.startCol]
            #cho biet quan co nao da bi an
            this.pieceCaptured=board[this.endRow][this.endCol]
            #phong cap
            this.pawnPromotion = (this.pieceMove == "wP" and this.endRow == 0) or (this.pieceMove == "bP" and this.endRow == 7)
            #an tot qua song
            this.enpassantMove = enpassantMove
            if this.enpassantMove:
                this.pieceCaptured = "wP" if this.pieceMove == "bP" else "bP"
                
            
            #sau do luu vao Movelog de co the undo
            this.MoveID = this.startRow*1000 + this.startCol*100 + this.endRow*10 + this.endCol
            
        def __eq__(this,other):
            if isinstance(other,Move):
                return this.MoveID == other.MoveID
            return False

            #cho phep ta co the xem duoc nuoc di nhu nao 
        def GetChessNotation(this): #notaion la ki hieu nuoc di, kieu g5->g7
            return this.GetRankFile(this.startRow,this.startRow)+"-"+this.GetRankFile(this.endRow,this.endCol)  
            
        def GetRankFile(this,r,c): 
            return this.ColtoFile[c]+this.RowtoRank[r]  
            
        
