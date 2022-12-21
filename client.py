from __future__ import print_function
import socket
import sys
import pygame
from pygame.locals import *
import select
from contextlib import closing
#nyonyonyo-nya-
def main(): #クライアント側
  (w,h)=(600,600)   #ゲーム画面の大きさ(幅600px,高さ600px)
  pygame.init()     #pygameを初期化
  pygame.display.set_mode((w,h),0,32)   #ディスプレイ設定
  screen = pygame.display.get_surface() #作成したディスプレイ情報をscreenが取得
  bg = pygame.image.load("clstr.jpg").convert_alpha() #背景画像設定   
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.update() #ディスプレイ更新

  running = True #event発生までTrue

  while running: #初期画面(server起動画面)
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
          sys.exit()
        if event.key == K_RETURN:
          running = False
      if event.type == MOUSEBUTTONDOWN and event.button == 1:
        x, y = event.pos
        if 145 <= x and x <= 460 and 350 <= y and y <= 510:
          running = False
  bg = pygame.image.load("setting.jpg").convert_alpha() #背景画像設定
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.update() #ディスプレイ更新
  pygame.time.wait(300)
  host = "LAPTOP-4AFJAG80" 
  port = 1236         #ポート番号 今回は1236に設定
  bufsize = 4096      #デフォルト4096

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPアドレスと通信プロトコルはIPv4,TCPを採択
  sock.connect((host, port)) #サーバーに接続(host = ホストのIPアドレス、port = ポート番号)
  backlogs = sock.recv(bufsize).decode('utf-8')
  print("backlogs,",backlogs)
  backlog = int(backlogs)
  readfds = set([sock])

  with closing(sock):
    running = True
    while running:
      pygame.display.update() #ディスプレイ更新
      pygame.time.wait(50)
      for event in pygame.event.get():
        if event.type == QUIT:
          sock.send("QUIT".encode('utf-8'))
          pygame.quit()
          sys.exit()
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            sock.send("QUIT".encode('utf-8'))
            pygame.quit()
            sys.exit()
      rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
      for sock in rready:                                   #選択された処理を順次遂行
        msg1 = sock.recv(bufsize).decode('utf-8')
        print("msg1,",msg1)
        if msg1 == "plwt":
          msg2 = sock.recv(bufsize).decode('utf-8')
          print("msg2,",msg2)
          connections = int(msg2)
          print("connections,",connections)
          if backlog == 3:
            if connections == 0:
              bg = pygame.image.load("0-3.jpg").convert_alpha() #背景画像設定
            elif connections == 1:
              bg = pygame.image.load("1-3.jpg").convert_alpha() #背景画像設定
            elif connections == 2:
              bg = pygame.image.load("2-3.jpg").convert_alpha() #背景画像設定
            else:
              bg = pygame.image.load("3-3.jpg").convert_alpha() #背景画像設定
              running = False
          else:
            if connections == 0:
              bg = pygame.image.load("0-4.jpg").convert_alpha() #背景画像設定
            elif connections == 1:
              bg = pygame.image.load("1-4.jpg").convert_alpha() #背景画像設定
            elif connections == 2:
              bg = pygame.image.load("2-4.jpg").convert_alpha() #背景画像設定
            elif connections == 3:
              bg = pygame.image.load("3-4.jpg").convert_alpha() #背景画像設定
            else:
              bg = pygame.image.load("4-4.jpg").convert_alpha() #背景画像設定
              running = False
          rect_bg = bg.get_rect() #背景画像の大きさを取得
          screen.blit(bg,rect_bg) #背景描画
    rect_bg = bg.get_rect() #背景画像の大きさを取得
    screen.blit(bg,rect_bg) #背景描画
    pygame.display.flip() #ディスプレイ更新
    pygame.time.wait(500)
    startsign = sock.recv(bufsize).decode('utf-8')
    print("startsign,",startsign)
    if startsign == "STRT":
      if backlog == 3:
        bg = pygame.image.load("start3.jpg").convert_alpha() #背景画像設定
      else:
        bg = pygame.image.load("start4.jpg").convert_alpha() #背景画像設定
    rect_bg = bg.get_rect() #背景画像の大きさを取得
    screen.blit(bg,rect_bg) #背景描画
    pygame.display.flip() #ディスプレイ更新
    pygame.time.wait(2000)
    startmap = sock.recv(bufsize).decode('utf-8')
    print("startmap,",startmap)
    if startmap == "MAPSTART":
      bg = pygame.image.load("catanmap.jpg").convert_alpha() #背景画像設定
    rect_bg = bg.get_rect() #背景画像の大きさを取得
    screen.blit(bg,rect_bg) #背景描画
    pygame.display.flip() #ディスプレイ更新

    running = True

    while running:
      pygame.display.update()
      pygame.time.wait(20)
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
  return

if __name__ == '__main__':
  main()
