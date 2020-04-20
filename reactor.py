
import pygame as pg
pg.init()
display_height = 800
display_width = 600
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
gray = (220, 220, 220)
gameDisplay = pg.display.set_mode(
    (display_width, display_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
pg.display.set_caption('chain reaction')
clock = pg.time.Clock()
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
IMAGE_NORMAL = pg.Surface((100, 32))
IMAGE_NORMAL.fill(pg.Color('dodgerblue1'))
IMAGE_HOVER = pg.Surface((100, 32))
IMAGE_HOVER.fill(pg.Color('lightskyblue'))
IMAGE_DOWN = pg.Surface((100, 32))
IMAGE_DOWN.fill(pg.Color('aquamarine1'))

class Button():
    def __init__(self, x, y, w, h, callback, img = None):
        self.x=x
        self.y=y