# main.py

import pygame
import sys
import os

#os.chdir('C:\\Users\\kanat\\OneDrive\\デスクトップ\\GPT\\PowerBallSimu\\asssets\\character.png')

# ================================
# 🛠️ 初期設定
# ================================
pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🪃ブーメランシミュレーター")

# 色設定
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BROWN = (160, 82, 45)

# キャラクター位置
character_x = 100
character_y = HEIGHT // 2 - 50  # キャラクターの高さを中央寄せ
initial_character_y = character_y  # 初期位置を保存

# キャラクター画像の読み込みとサイズ調整
character_ready_image = pygame.image.load('assets/ready.png')
character_ready_image = pygame.transform.scale(character_ready_image, (100, 150))  # 幅50、高さ100にリサイズ

character_throw_image = pygame.image.load('assets/throw.png')
character_throw_image = pygame.transform.scale(character_throw_image, (100, 150))  # 幅50、高さ100にリサイズ

character_image = character_ready_image  # 初期状態は投げる前の画像

# ブーメラン画像の読み込みとサイズ調整
boomerang_image_path = 'assets/boomerang.png'
if not os.path.exists(boomerang_image_path):
    print(f"Error: File '{boomerang_image_path}' not found.")
    sys.exit(1)
boomerang_image = pygame.image.load(boomerang_image_path)
boomerang_image = pygame.transform.scale(boomerang_image, (60, 40))  # サイズ調整

# ブーメランリスト
boomerangs = []

# パワーゲージの初期設定
power = 0
power_direction = 1  # ゲージの増減方向
power_active = False  # ゲージ操作中かどうか

# キャラクター移動ロック
character_locked = True  # 初期状態ではロック

# フレームレート
clock = pygame.time.Clock()

# ================================
# 🛠️ メインループ
# ================================
running = True
while running:
    clock.tick(60)  # 60FPS

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # スペースキー押下時の処理を修正
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                power_direction = 1  # ゲージ増加開始
                power_active = True  # ゲージ操作中

        # スペースキーを離したらブーメラン発射
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                boomerangs.append([character_x + character_width + 10, character_y + character_height // 2, -10, power / 4])  # 初期位置をキャラクターの右外側に設定
                power = 0  # ゲージをリセット
                power_active = False  # ゲージ操作終了
                character_image = character_throw_image  # 投げた後の画像に切り替え
                character_locked = False  # キャラクターの移動を解除

    # 矢印キーでキャラクターを上下に動かす（長押し対応）
    keys = pygame.key.get_pressed()
    if not character_locked:  # ロックされていない場合のみ移動可能
        if keys[pygame.K_UP]:
            character_y -= 10  # 上に移動
        if keys[pygame.K_DOWN]:
            character_y += 10  # 下に移動

    # ゲージの増減処理（スペースキーが押されている間のみ）
    if power_active:
        power += power_direction * 2
        if power >= 100 or power <= 0:
            power_direction *= -1  # 増減方向を反転

    # 背景を白で塗る
    screen.fill(WHITE)

    # キャラクターを描画
    screen.blit(character_image, (character_x, character_y))

    # キャラクターのコリジョン範囲を画像サイズに同期
    character_width, character_height = character_ready_image.get_size()
    character_rect = pygame.Rect(character_x, character_y, character_width, character_height)

    # パワーゲージを描画
    pygame.draw.rect(screen, (255, 110, 0), (character_x - 35, character_y + 126 - power, 12, power))  # ゲージ本体を上下に伸縮

    # メモリの高さをキャラクターに同期
    for i in range(0, 101, 20):  # 20刻みに変更
        pygame.draw.line(screen, (0, 0, 0), (character_x - 35, character_y + 126 - i), (character_x - 25, character_y + 126 - i))  # メモリ線
        text = pygame.font.Font(None, 20).render(f"{i}%", True, (0, 0, 0))
        screen.blit(text, (character_x - 70, character_y + 120 - i))

    # ブーメランの挙動を更新
    for b in boomerangs:
        b[2] += 0.25  # 重力加速度を適用
        b[0] += b[3]  # x方向の速度で移動
        b[1] += b[2]  # y方向の速度で移動

        # --- ここを追加！ ---
        b[3] += 0.35  # 少しずつ右に曲がる力を加える（0.05は調整できる）
        b[3] -= 0.8  # 少しずつ左に曲がる力を加える（0.05は調整できる）

        # --- 回転描画を先にする！ ---
        rotation_angle = pygame.time.get_ticks() / 2
        rotated_boomerang = pygame.transform.rotate(boomerang_image, rotation_angle)
        new_rect = rotated_boomerang.get_rect(center=(b[0], b[1]))
        screen.blit(rotated_boomerang, new_rect)

        # ブーメランが画面外に出た場合に削除（右側は除外）
        if b[1] > HEIGHT or b[1] < 0:
            boomerangs.remove(b)
            if len(boomerangs) == 0:  # 全てのブーメランが消えたら
                character_image = character_ready_image  # 投げる前の画像に戻す
                character_y = initial_character_y  # 初期位置に戻す
                character_locked = True  # キャラクターの移動を再ロック
            continue

        # キャラクターに触れた場合の判定を厳密化
        if character_rect.collidepoint(b[0], b[1]):
            boomerangs.remove(b)
            if len(boomerangs) == 0:  # 全てのブーメランが消えたら
                character_image = character_ready_image  # 投げる前の画像に戻す
                character_y = initial_character_y  # 初期位置に戻す
                character_locked = True  # キャラクターの移動を再ロック

    # 画面更新
    pygame.display.flip()

# 終了処理
pygame.quit()
sys.exit()
