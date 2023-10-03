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
            this.Wturn= True #xac dinh dang den luot cua ai, trang hay den
            this.Movelog=[] #dung de luu cac nuoc di
            
        def MakeMove(this,move):
            this.board[move.startRow][move.startCol]="--"
            this.board[move.endRow][move.endCol]= move.pieceMove
            this.Movelog.append(move)#luu vao movelog 
            this.WhiteToMove = not this.Wturn #doi luot
            
        def UndoMove(this):
            if len(this.Movelog) != 0:
                move = this.Movelog.pop()
                this.board[move.startRow][move.startCol]= move.pieceMove
                this.board[move.endRow][move.endCol] = move.pieceCaptured
                this.Wturn = not this.Wturn
           
class Move():
        #ki hieu o hang doc va hang ngang cua ban co
        #gia tri cua no trong ma tran 2 chieu    
        #trong co vua rank la hang va file la cot
        RanktoRow={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0} 
        RowtoRank={v:k for k, v in RanktoRow.items()}
        FiletoCol={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
        ColtoFile={v:k for k, v in FiletoCol.items()}
        

        def __init__(this,StartSq,EndSq,board):  
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
            #sau do luu vao Movelog de co the undo

            #cho phep ta co the xem duoc nuoc di nhu nao 
        def GetChessNotation(this): #notaion la ki hieu nuoc di, kieu g5->g7
            return this.GetRankFile(this.startRow,this.startRow)+"->"+this.GetRankFile(this.endRow,this.endCol)  
            
        def GetRankFile(this,r,c): 
            return this.ColtoFile[c]+this.RowtoRank[r]  
            
        