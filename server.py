from __future__ import print_function
import pygame
from pygame.locals import *
import socket
import select
import sys

def main(): #サーバー側
  (w,h)=(600,600)   #ゲーム画面の大きさ(幅600px,高さ600px)
  pygame.init()     #pygameを初期化
  pygame.display.set_mode((w,h),0,32)   #ディスプレイ設定
  screen = pygame.display.get_surface() #作成したディスプレイ情報をscreenが取得
  bg = pygame.image.load("svstr.jpg").convert_alpha() #背景画像設定   
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.update() #ディスプレイ更新

  running = True #while続行bool

  while running: #初期画面(server起動画面)
    pygame.time.wait(50) #20fps(50ms(0.05秒間)に一回に入出力を制限)

    for event in pygame.event.get(): #何か入力があった場合、その入力に対して処理を行う。
      if event.type == QUIT: #ウィンドウ右上の×がクリックされた時、pygameを閉じ、プログラムそのものも終了。
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN: #キー入力
        if event.key == K_ESCAPE: #escapeキーが押された場合も上記と同様の終了。
          pygame.quit()
          sys.exit()
        if event.key == K_RETURN: #Enterキーが押された場合、whileを抜け、次のページへ
          running = False
      if event.type == MOUSEBUTTONDOWN and event.button == 1: #マウス入力、右クリック
        x, y = event.pos
        if 110 <= x and x <= 490 and 330 <= y and y <= 485: #枠内左クリックでwhileを抜け、次のページへ
          running = False

  bg = pygame.image.load("svstr2.jpg").convert_alpha() #背景画像設定   
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.flip() #ディスプレイ更新

  backlog = 0  #接続可能クライアント数(初期値0)

  running = True #while続行bool

  while running: #プレイヤー数選択画面
    pygame.time.wait(50) #20fps

    for event in pygame.event.get(): #上記同様↓
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
          sys.exit()                 #ここまで↑
        if event.key == K_3: #キーボード3が押されたとき、3playerとしてゲーム開始
          backlog = 3
          running = False
        if event.key == K_4: #キーボード4が押されたとき、4playerとしてゲーム開始
          backlog = 4
          running = False
      if event.type == MOUSEBUTTONDOWN and event.button == 1: #右クリ
        x, y = event.pos
        if 50 <= x and x <= 280 and 190 <= y and y <= 435: #3player枠内判定
          backlog = 3
          running = False
        if 320 <= x and x <= 550 and 190 <= y and y <= 435: #4player枠内判定
          backlog = 4
          running = False

  bg = pygame.image.load("setting.jpg").convert_alpha() #背景画像設定
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.flip() #ディスプレイ更新

  backlogs = str(backlog)      
  #backlog(int型)をstr型にしたものbacklogsを作成。backlog = プレイヤー数なので、そのデータを後々clientアカウントに送りつける。
  #そのためにstr化したものを作成。

  host = "LAPTOP-4AFJAG80"     #ホスト(server)のIPアドレス、今回は俺のPC、状況によって変更可能
  port = 1236                  #ポート番号 今回は1236に設定
  bufsize = 4096               #デフォルト4096

  server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPアドレスと通信プロトコルはIPv4,TCPを採択                                    #処理候補にサーバーソケットを追加
  clients_socks = []                   #人数分のクライアントを格納するためのリスト
  readfds = set([server_sock])         #処理候補(socket)を格納したset、後々select関数にぶち込む為だけに作成
  server_sock.bind((host, port))       #ソケットをアドレスに結び付ける(IPアドレス = host , ポート番号 = port)
  server_sock.listen(backlog)          #入力された接続可能クライアント数を設定(今回は3or4)

  pygame.time.wait(500)                #意味のない0.5秒間、それっぽさ演出。

  if backlog == 3: #3playerの時、それ用の待機画面画像をセット
    bg = pygame.image.load("0-3.jpg").convert_alpha() #背景画像設定
  else:            #4playerの時も、それ用の待機画面画像をセット
    bg = pygame.image.load("0-4.jpg").convert_alpha() #背景画像設定
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.update() #ディスプレイ更新

  running = True #while続行bool

  while running: #プレイヤー待機画面
    pygame.display.update() #ディスプレイ更新
    pygame.time.wait(50)
    for event in pygame.event.get():
      if event.type == QUIT:
        for receiver in clients_socks:
          receiver.send("serverdown".encode('utf-8'))
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          for receiver in clients_socks:
            receiver.send("serverdown".encode('utf-8'))
          pygame.quit()
          sys.exit()
    rready, wready, xready = select.select(readfds, [], [],0.05) #処理を可能な物から順に選択
    for sock in rready:                                   #選択された処理を順次遂行
      if sock is server_sock: #サーバー(ホスト)に対する処理の時
        conn, address = server_sock.accept() #サーバーがクライアントの情報を受け取る(connは新しいソケットオブジェクト、addressはクライアントのアドレス)
        readfds.add(conn)                    #新しく処理候補にクライアントのソケットを登録する
        clients_socks.append(conn)
        conn.send(backlogs.encode('utf-8'))
        connections = len(clients_socks)
        c = str(connections)
        for receiver in clients_socks:
          receiver.send("plwt".encode('utf-8'))
          pygame.time.wait(200)
          receiver.send(c.encode('utf-8'))
          pygame.time.wait(200)

        if backlog == 3:
          if connections == 0:
            bg = pygame.image.load("0-3.jpg").convert_alpha() #背景画像設定
          elif connections == 1:
            print("ok")
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
      else:
        msg = sock.recv(bufsize).decode('utf-8')
        if msg == "QUIT":
          sock.close()
          readfds.remove(sock)

  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.flip() #ディスプレイ更新
  pygame.time.wait(500)
  for receiver in clients_socks:
    receiver.send("STRT".encode('utf-8'))
    pygame.time.wait(200)
  if backlog == 3:
    bg = pygame.image.load("start3.jpg").convert_alpha() #背景画像設定
  else:
    bg = pygame.image.load("start4.jpg").convert_alpha() #背景画像設定
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.flip() #ディスプレイ更新
  pygame.time.wait(2000)
  for receiver in clients_socks:
    receiver.send("MAPSTART".encode('utf-8'))
    pygame.time.wait(200)
  bg = pygame.image.load("catanmap.jpg").convert_alpha() #背景画像設定
  rect_bg = bg.get_rect() #背景画像の大きさを取得
  screen.blit(bg,rect_bg) #背景描画
  pygame.display.flip() #ディスプレイ更新

  running = True

  while running:
    pygame.display.update()
    pygame.time.wait(50)
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