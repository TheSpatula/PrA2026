import pygame
from Z_checkpoint import Checkpoint


class Track:
    def __init__(self, image_path, checkpoints, start_pos=(50, 479), start_angle=0):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.checkpoints = checkpoints
        self.start_pos = start_pos
        self.start_angle = start_angle

    def draw(self, screen, show_checkpoints=False):
        if show_checkpoints:
            for checkpoint in self.checkpoints:
                checkpoint.draw(screen)
        screen.blit(self.image, (0, 0))


def load_track_1():
    checkpoints = [
        Checkpoint(15, 381, 120, 20, 1), Checkpoint(4, 229, 120, 20, 2),
        Checkpoint(204, 20, 20, 120, 3), Checkpoint(437, 14, 20, 120, 4),
        Checkpoint(684, 24, 20, 120, 5), Checkpoint(878, 21, 20, 130, 6),
        Checkpoint(901, 167, 130, 20, 7), Checkpoint(847, 187, 20, 120, 8),
        Checkpoint(719, 197, 20, 100, 9), Checkpoint(585, 195, 20, 100, 10),
        Checkpoint(484, 198, 20, 100, 11), Checkpoint(351, 200, 20, 100, 12),
        Checkpoint(183, 326, 160, 20, 13), Checkpoint(359, 349, 20, 120, 14),
        Checkpoint(472, 360, 20, 120, 15), Checkpoint(609, 355, 20, 120, 16),
        Checkpoint(771, 356, 20, 120, 17), Checkpoint(933, 373, 20, 130, 18),
        Checkpoint(962, 540, 100, 20, 19), Checkpoint(893, 585, 20, 100, 20),
        Checkpoint(755, 510, 20, 120, 21), Checkpoint(650, 560, 20, 120, 22),
        Checkpoint(532, 498, 20, 120, 23), Checkpoint(415, 572, 20, 120, 24),
        Checkpoint(194, 613, 20, 100, 25), Checkpoint(10, 591, 130, 20, 26),
    ]
    return Track("assets/Z_RaceTrack1.png", checkpoints, start_pos=(50, 479), start_angle=0)