import random

piece_score = { "K": 0, "Q" : 10, "R" : 5, "B" : 3,"N" : 3, "P" : 1}
CheckMate = 1000    #Điểm số với tình huống chiếu hết
StaleMate = 0       #Điểm số với tình huống hết nước đi
DEPTH = 2

#gắn giá trị lên bàn cờ để quân cờ ưu tiên di chuyển tới đó
KnightScore =  [[1, 1, 1, 1 ,1, 1 ,1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1 ,1, 2 ,3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores =  [[1, 1, 1, 3, 1, 1, 1, 1],
                [1, 2, 3, 3, 3, 1, 1, 1], 
                [1, 4, 3, 3, 3, 4, 2, 1], 
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 1, 2, 3, 3, 1, 1, 1],
                [1, 1, 1, 3, 1, 1, 1, 1]]

rockScores = [[4, 3, 4, 4, 4, 4, 3, 4], 
              [4, 4, 4, 4, 4, 4, 4, 4], 
              [1, 1, 2, 3, 3, 2, 1, 1], 
              [1, 2, 3, 4, 4, 3, 2, 1], 
              [1, 2, 3, 4, 4, 3, 2, 1], 
              [1, 1, 2, 2, 2, 2, 1, 1], 
              [4, 4, 4, 4, 4, 4, 4, 4], 
              [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores =  [[8, 8, 8, 8, 8, 8, 8, 8], 
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores =  [[0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [5, 6, 6, 7, 7, 6, 6, 5], 
                    [8, 8, 8, 8, 8, 8, 8, 8], 
                    [8, 8, 8, 8, 8, 8, 8, 8]]


piecePositionScores = {"N":KnightScore, "Q":queenScores, "B": bishopScores, "R": rockScores, "bP":blackPawnScores, "wP":whitePawnScores}

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
def findBestMove(Gs,validMoves,returnQueue):
    global nextMove, counter, count
    nextMove = None
    counter = 0
    count = 0
    #findBestMoveMinMaxNoRescursion(Gs, validMoves)
    #findMoveMinMax(Gs, validMoves, DEPTH, Gs.Wturn)
    findMoveMinMaxAlphaBeta(Gs, validMoves, DEPTH, -CheckMate, CheckMate, Gs.Wturn)
    #findMoveNegaMax(Gs, validMoves, DEPTH, 1 if Gs.Wturn else -1)
    #findMoveNegaMaxAlphaBeta(Gs,validMoves, DEPTH, -CheckMate, CheckMate, 1 if Gs.Wturn else -1)
    print(counter)
    returnQueue.put(nextMove) 

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
                    print(move, score)
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
                    print(move, score)
            Gs.UndoMove()
        return minScore
    
    
def findMoveMinMaxAlphaBeta(Gs, validMoves, depth, alpha, beta, WhiteTurn):
    global nextMove, counter
    counter += 1
    if depth == 0:
        #return score_material(Gs.board)
        return scoreBoard(Gs)
    
    if WhiteTurn:
        random.shuffle(validMoves)
        maxScore = -CheckMate
        for move in validMoves:
            Gs.MakeMove(move)
            nextMoves = Gs.GetValidMove()
            score = findMoveMinMaxAlphaBeta(Gs, nextMoves, depth -1, alpha, beta, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                    print(move.pieceMove[1]+move.GetChessNotation() , score)
            #puring happen
            alpha = max(alpha, maxScore)
            if alpha >= beta:
                break    
            Gs.UndoMove()
        return maxScore
            
    else:
        random.shuffle(validMoves)
        minScore = CheckMate
        for move in validMoves:
            Gs.MakeMove(move)
            nextMoves = Gs.GetValidMove()
            score = findMoveMinMaxAlphaBeta(Gs, nextMoves, depth -1 , alpha, beta, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
                    print(move.pieceMove[1]+move.GetChessNotation() , score)
            #puring happen
            beta = min(beta, minScore)
            if alpha >= beta:
                break
            Gs.UndoMove()
        return minScore

def findMoveNegaMax(Gs,validMoves, depth, turnMutiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMutiplier * scoreBoard(Gs)
    maxScore = -CheckMate
    random.shuffle(validMoves)
    for move in validMoves:
        Gs.MakeMove(move)
        nextMoves = Gs.GetValidMove()
        score = -findMoveNegaMax(Gs, nextMoves, depth -1 , -turnMutiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        Gs.UndoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(Gs,validMoves, depth, alpha, beta, turnMutiplier):
    global nextMove, counter, count
    counter += 1
    if depth == 0:
        return turnMutiplier * scoreBoard(Gs)
    #move odering - implement later
    maxScore = -CheckMate
    random.shuffle(validMoves)
    for move in validMoves:
        count +=1
        #print(count)
        Gs.MakeMove(move)
        nextMoves = Gs.GetValidMove()
        score = -findMoveNegaMaxAlphaBeta(Gs, nextMoves, depth-1 , -beta, -alpha, -turnMutiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move.pieceMove[1]+move.GetChessNotation() , score)
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
    for row in range(len(Gs.board)):
        for col in range(len(Gs.board[row])):
            square = Gs.board[row][col]
            if square != "--":
                #score it positionally
                piecePositionScore = 0
                
                if square[1] != "K":    #no position table for king
                    if square[1]=="P":  #for pawns
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:   #for other pieces
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                
                if square[0] == 'w':
                    score += piece_score[square[1]] + piecePositionScore
                elif square[0] =='b':
                    score -= piece_score[square[1]] + piecePositionScore
        
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
