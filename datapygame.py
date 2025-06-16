import pygame
import sys
import time
import os #for path handling
import random
import PIL


# Get the directory where the current script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media")
BACKGROUND_DIR = os.path.join(MEDIA_DIR, "backgrounds")
TARGET_DIR = os.path.join(MEDIA_DIR, "targets")
STIMULI_DIR = os.path.join(MEDIA_DIR, "stimuli")
MASK_DIR = os.path.join(MEDIA_DIR, "gt")


#initialise pygame
pygame.init()
screen = pygame.display.set_mode((1280, 1080))
pygame.display.set_caption("Object Search Game")
screen_rect = screen.get_rect()

#function to display an image for a set duration
def load_centered_image(path):
    image = pygame.image.load(path)
    rect = image.get_rect()
    rect.center = screen_rect.center
    return image, rect

def show_image_for_ms(image, rect, ms):
    screen.fill((0,0,0)) #clear screen
    screen.blit(image, rect.topleft)
    pygame.display.flip()
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))  # clear screen
        screen.blit(image, rect)
        pygame.display.flip()
        pygame.time.Clock().tick(60)  # limit to ~60 FPS

# # Load images using paths relative to script folder
image1, image1_rect = load_centered_image(os.path.join(BACKGROUND_DIR, "image1.png")) # grayscale
image3, image3_rect = load_centered_image(os.path.join(BACKGROUND_DIR, "image3.png")) # grayscale again

# # center image4
# image4_rect = image4.get_rect()
# image4_rect.center = screen_rect.center


#main game loop (repeat 240 times)
reaction_times = []
NUM_TRIALS = 240

running = True
game_over = False

#shuffling image order
available_indices = list(range(1, NUM_TRIALS + 1))
random.shuffle(available_indices)

for trial_num, idx in enumerate(available_indices, 1):
    print(f"\nStarting trial {trial_num} with image index {idx:03})")
    target_path = os.path.join(TARGET_DIR, f"t{idx:03}.jpg")
    stim_path = os.path.join(STIMULI_DIR, f"img{idx:03}.jpg")
    target_img, target_rect = load_centered_image(target_path)
    stim_img, stim_rect = load_centered_image(stim_path)

    show_image_for_ms(image1, image1_rect, 500)
    show_image_for_ms(target_img, target_rect, 1500)
    show_image_for_ms(image3, image3_rect, 500)
    
    gt_mask = pygame.image.load(os.path.join(MASK_DIR, f"gt{trial_num+1}.jpg")).convert()

    screen.fill((0,0,0))
    screen.blit(stim_img, stim_rect.topleft)
    pygame.display.flip()

# for trial in range(NUM_REPETITIONS):
#     print(f"\nStarting trial {trial + 1}")

#     #show image 1 (grayscale) for 500 ms
#     show_image_for_ms(image1, image1_rect, 500)

#     #show image 2 (grayscale + panda) for 1500 ms
#     show_image_for_ms(image2, image2_rect, 1500)

#     #show image 3 (grayscale) for 500 ms
#     show_image_for_ms(image3, image3_rect, 500)

#     #clear screen before displaying image 4
#     screen.fill((0,0,0))
#     screen.blit(image4,image4_rect.topleft)
#     pygame.display.flip()

    start_time = time.time()
    clicked = False
    timeout = False

    while not clicked and not timeout:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                reaction_time = time.time() - start_time
                reaction_times.append(reaction_time)  # Record reaction time regardless 
                print(f"Trial {trial_num}: Mouse clicked at {click_pos}")
                print(f"Reaction time: {reaction_time:.2f} seconds")

                if 0 <= click_pos[0] < gt_mask.get_width() and 0 <= click_pos[1] < gt_mask.get_height():
                    pixel = gt_mask.get_at(click_pos)  # Returns (R, G, B, A)
                    if pixel[:3] == (255, 255, 255):  # Check if white
                        print("Correct! You clicked on the object.")
                        reaction_times.append(reaction_time)
                        clicked = True
                        game_over = False
                    else:
                        print("Incorrect. Try again.")
                        reaction_times.append(reaction_time)
                        clicked = False

        #timeout after 20000 ms (20 seconds)
        if (time.time() - start_time) > 20.0: #pygame uses ms, python uses s
            print (f"Trial {trial_num + 1}: Timeout! No click registered within 20s.")
            reaction_times.append(20.0) #record max time for timeout
            timeout = True #break loop on timeout

    if game_over:
        break

#after all trials, calculate avg rxn time
avg_rt = sum(reaction_times)/ len(reaction_times)
print (f"\nAll trials completed. Average reaction time: {avg_rt: .2f} seconds")

pygame.quit()
sys.exit()












