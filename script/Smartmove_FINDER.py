import random

piece_score = { "K": 0, "Q" : 10, "R" : 5, "B" : 3,"N" : 3, "P" : 1}
CHECKMATE = 1000    #Điểm số với tình huống chiếu tướng
STALEMATE = 0       #Điểm số với tình huống hết nước đi
DEPTH = 2


#Những nước đi bừa
def findRandomMove(vaildMoves):
    return vaildMoves[random.randint(0, len(vaildMoves)-1)]


#Những nước đi dựa thuần vào giá trị
def findBestMove(Gs, vaildMoves):
    
    """Greedy
    Đặt checkmate 1000 điểm, giả sư AI là đen
    AI(đen player_move tiến tới điểm âm -1000) sẽ có điểm xấu nhất là 1000,
    như vậy AI sẽ phải liên tục tìm hướng đi để tiến tới điểm lý tưởng của nó
    
    Đặt checkmate 1000 điểm, giả sư AI là trắng
    AI(trắng oppents tiến tới điểm âm 1000) sẽ có điểm xấu nhất là -1000,
    như vậy AI sẽ phải liên tục tìm hướng đi để tiến tới điểm lý tưởng của nó
    """
    turn_multiplier = 1 if Gs.Wturn else -1
    opponentMinMaxScore = CHECKMATE 
    bestPlayerMove = None
    random.shuffle(vaildMoves)
    for player_move in vaildMoves:
        Gs.MakeMove(player_move)    #thực hiện lịch di chuyển
        opponentsMoves = Gs.GetValidMove()
        if Gs.STALEMATE:
            opponentMaxScore = STALEMATE
        elif Gs.CHECKMATE:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                Gs.MakeMove(opponentsMove)
                Gs.GetValidMove()
                if Gs.CheckMate:
                    score = CHECKMATE
                elif Gs.StaleMate:
                    score = STALEMATE
                else:
                    score = -turn_multiplier * score_material(Gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                Gs.UndoMove()
        if opponentMaxScore < opponentMinMaxScore:
            print("max= ",opponentMaxScore,"Minmax= ",opponentMinMaxScore) 
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = player_move
        Gs.UndoMove()               #Undo lệnh di chuyển thừa
    return bestPlayerMove


#Phương thức helper giúp gọi đệ quy
def findBestMoveMinMax(Gs,validMoves):
    global nextMove
    nextMove = None
    findMoveMinMax(Gs, validMoves, DEPTH, Gs.Wturn)
    return nextMove

def findMoveMinMax(Gs, validMoves, depth, WhiteTurn):
    global nextMove
    if depth == 0:
        return score_material(Gs.board)
    
    if WhiteTurn:
        random.shuffle(validMoves)
        maxScore = -CHECKMATE
        for move in validMoves:
            Gs.MakeMove(move)
            nextMoves = Gs.GetValidMove()
            score = findMoveMinMax(Gs, nextMoves, depth -1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            Gs.UndoMove()
        return maxScore
            
    else:
        random.shuffle(validMoves)
        minScore = CHECKMATE
        for move in validMoves:
            Gs.MakeMove(move)
            nextMoves = Gs.GetValidMove()
            score = findMoveMinMax(Gs, nextMoves, depth -1 , True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            Gs.UndoMove()
        return minScore
                    
                

#A postive score is good for white, a negative is good for black
def scoreBoard(Gs):
    if Gs.CheckMate:
        if Gs.Wturn:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif Gs.Stalemate:
        return STALEMATE
    
    score = 0 
    for row in Gs.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] =='b':
                score -= piece_score[square[1]]
    
    return score
            
            
#Đánh giá trị bàn cơ dựa trên trên quân cờ
def score_material(board):
    score = 0 
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] =='b':
                score -= piece_score[square[1]]
    
    return score
