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
            
        