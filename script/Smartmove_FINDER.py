import random

piece_score = { "K": 0, "Q" : 10, "R" : 5, "B" : 3,"N" : 3, "P" : 1}
CheckMate = 1000    #Điểm số với tình huống chiếu hết
StaleMate = 0       #Điểm số với tình huống hết nước đi
DEPTH = 3

#gắn giá trị lên bàn cờ để quân cờ ưu tiên di chuyển tới đó
KnightScore =  [[1,1,1,1,1,1,1,1],
                [1,2,2,2,2,2,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,2,2,2,2,2,1],
                [1,1,1,1,1,1,1,1]]

piecePositionScore = {"N":KnightScore}

#Những nước đi bừa
def findRandomMove(vaildMoves):
    return vaildMoves[random.randint(0, len(vaildMoves)-1)]

#Những nước đi dựa thuần vào giá tri
#find best move without rescursion
def findBestMoveMinMaxNoRescursion(Gs, vaildMoves):
    
    """Greedy
    Đặt CheckMate 1000 điểm, giả sử AI là đen
    AI(đen player_move tiến tới điểm âm -1000) sẽ có điểm xấu nhất là 1000,
    như vậy AI sẽ phải liên tục tìm hướng đi để tiến tới điểm lý tưởng của nó
    
    Đặt CheckMate 1000 điểm, giả sư AI là trắng
    AI(trắng oppents tiến tới điểm âm 1000) sẽ có điểm xấu nhất là -1000,
    như vậy AI sẽ phải liên tục tìm hướng đi để tiến tới điểm lý tưởng của nó
    """
    turn_multiplier = 1 if Gs.Wturn else -1
    opponentMinMaxScore = CheckMate 
    bestPlayerMove = None
    random.shuffle(vaildMoves)
    for player_move in vaildMoves:
        Gs.MakeMove(player_move)    #thực hiện lịch di chuyển
        opponentsMoves = Gs.GetValidMove()
        if Gs.StaleMate:
            opponentMaxScore = StaleMate
        elif Gs.CheckMate:
            opponentMaxScore = -CheckMate
        else:
            opponentMaxScore = -CheckMate
            for opponentsMove in opponentsMoves:
                Gs.MakeMove(opponentsMove)
                Gs.GetValidMove()
                if Gs.CheckMate:
                    score = CheckMate
                elif Gs.StaleMate:
                    score = StaleMate
                else:
                    score = -turn_multiplier * score_material(Gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                Gs.UndoMove()
        if opponentMaxScore < opponentMinMaxScore:
            #print("max = ",opponentMaxScore,"Minmax = ",opponentMinMaxScore) 
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = player_move
        Gs.UndoMove()               #Undo lệnh di chuyển thừa
    return bestPlayerMove


#Phương thức helper giúp gọi đệ quy
def findBestMove(Gs,validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    #findMoveMinMax(Gs, validMoves, DEPTH, Gs.Wturn)
    #findMoveNegaMax(Gs, validMoves, DEPTH, 1 if Gs.Wturn else -1)
    findMoveNegaMaxAlphaBeta(Gs,validMoves, DEPTH, -CheckMate, CheckMate, 1 if Gs.Wturn else -1)
    print(counter)
    return nextMove

def findMoveMinMax(Gs, validMoves, depth, WhiteTurn):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return score_material(Gs.board)
    
    if WhiteTurn:
        random.shuffle(validMoves)
        maxScore = -CheckMate
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
        minScore = CheckMate
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
    
def findMoveNegaMax(Gs,validMoves, depth, turnMutiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMutiplier * scoreBoard(Gs)
    maxScore = -CheckMate
    for move in validMoves:
        Gs.MakeMove(move)
        nextMoves = Gs.GetValidMove()
        score = -findMoveNegaMax(Gs, nextMoves, depth -1 , -turnMutiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        Gs.UndoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(Gs,validMoves, depth, alpha, beta, turnMutiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMutiplier * scoreBoard(Gs)
    #move odering - implement later
    maxScore = -CheckMate
    for move in validMoves:
        Gs.MakeMove(move)
        nextMoves = Gs.GetValidMove()
        score = findMoveNegaMaxAlphaBeta(Gs, nextMoves, depth -1 ,-alpha, -beta, -turnMutiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        Gs.UndoMove()
        if maxScore > alpha: #puring happen
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
                    
                
#A postive score is good for white, a negative is good for black
def scoreBoard(Gs):
    if Gs.CheckMate:
        if Gs.Wturn:
            return -CheckMate #black wins
        else:
            return CheckMate #white wins
    elif Gs.StaleMate:
        return StaleMate
    
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
