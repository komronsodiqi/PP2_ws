import pygame

pygame.init()
pygame.display.set_caption('Music Player')
screen_size = screen_width, screen_height = 600, 150
screen = pygame.display.set_mode(screen_size)

pygame.mixer.init()
path = '/Users/komronsodiqov/Downloads/'
songList = ['ytmp3-convert.com_320kbps-kadamu-kurbon-va-zainab-2018-new.mp3', 'Neizvestnyjj_ONE_DAY_FanaaTV_Remix_l_Shabnam_Surayo_ARASH_feat_Helena.mp3']

crrnt_song_index = 0
crrnt_song = songList[crrnt_song_index]

pygame.mixer.music.load(path + crrnt_song)
pygame.mixer.music.play()

btn_font = pygame.font.Font(None, 32)
btn = btn_font.render('C(Pause)    V(Unpause)    B(Prev)    N(Next)', True, 'royalblue')

song_name_font = pygame.font.Font(None, 32)
song_name = song_name_font.render(crrnt_song.split('.')[0], True, 'black')


def next_song():
    global crrnt_song, crrnt_song_index, song_name

    crrnt_song_index += 1
    if crrnt_song_index >= len(songList):
        crrnt_song_index = 0

    crrnt_song = songList[crrnt_song_index]
    song_name = song_name_font.render(crrnt_song.split('.')[0], True, 'black')

    pygame.mixer.music.load(path + crrnt_song)
    pygame.mixer.music.play()


def prev_song():
    global crrnt_song, crrnt_song_index, song_name

    crrnt_song_index -= 1
    if crrnt_song_index <= 0:
        crrnt_song_index = len(songList) - 1

    crrnt_song = songList[crrnt_song_index]
    song_name = song_name_font.render(crrnt_song.split('.')[0], True, 'black')

    pygame.mixer.music.load(path + crrnt_song)
    pygame.mixer.music.play()



run = True
while run:
    screen.fill('white')
    screen.blit(btn, (75, screen_height - 40))
    screen.blit(song_name, (15, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
            if event.key == pygame.K_v:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
            # if event.key == pygame.K_SPACE:
            #     if pygame.mixer.music.get_busy():
            #         pygame.mixer.music.pause()
            #     else:
            #         pygame.mixer.music.unpause()
            if event.key == pygame.K_n:
                next_song()
            if event.key == pygame.K_b:
                prev_song()
    pygame.display.flip()


pygame.quit()