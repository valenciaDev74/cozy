from Xlib import X, display
from Xlib.ext import randr
import sys


class X11DisplayAdapter:
    def __init__(self):
        self.display = display.Display()
        self.display.set_close_down_mode(X.RetainPermanent)
        self.screen = self.display.screen()
        self.root = self.screen.root
        self.crtc_id = self._get_active_crtc()

        if not self.crtc_id:
            print("Error: No active monitor found")
            sys.exit(1)

    def _get_active_crtc(self):
        resources = randr.get_screen_resources(self.root)
        for crtc in resources.crtcs:
            info = randr.get_crtc_info(self.display, crtc, 0)
            if info.mode != 0:
                return crtc
        return resources.crtcs[0] if resources.crtcs else None

    def get_original_gamma(self):
        gamma = randr.get_crtc_gamma(self.display, self.crtc_id)
        return {
            "r": list(gamma.red),
            "g": list(gamma.green),
            "b": list(gamma.blue),
            "size": len(gamma.red),
        }

    def set_gamma(self, size, r, g, b):
        randr.set_crtc_gamma(self.display, self.crtc_id, size, r, g, b)
        self.display.sync()
