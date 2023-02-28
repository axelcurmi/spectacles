import math

import cv2

class Spectacles:
    window_name = "spectacles"

    def __init__(self, image):
        cv2.namedWindow(self.window_name)
        self.original_image = cv2.imread(image)
        self.working_image = self.original_image.copy()
        self.temp_image = None

        self.lines = []
        self.mouse_position = None

        self.simple_mode = True

        cv2.setMouseCallback(self.window_name,
            self.handle_mouse_events)

    def draw_line(self, start, end, baseline = False):
        color = (12,36,255) if baseline and not self.simple_mode \
            else (36,255,12)

        cv2.line(self.working_image,
            (start[0], start[1]),
            (end[0], end[1]),
            color, 2)

        if self.simple_mode:
            return

        line_length = self.calculate_line_length(start, end)
        proportion = 1
        
        if not baseline:
            main_line_length = self.calculate_line_length(
                self.lines[0][0], self.lines[0][1]
            )
            proportion = round(main_line_length / line_length, 2)

        mid_x = int((start[0] + end[0]) / 2)
        mid_y = int((start[1] + end[1]) / 2)

        cv2.putText(self.working_image,
            f"{line_length} ({proportion})",
            (mid_x + 15, mid_y + 5),
            cv2.FONT_HERSHEY_SIMPLEX, 1,
            color, 2, cv2.LINE_AA)

    def calculate_line_length(self, start, end):
        return round(math.sqrt(
            pow(start[0] + end[0], 2) +
            pow(start[1] + end[1], 2)
        ), 2)

    def handle_mouse_events(self, event, x, y, flags, parameters):
        if self.mouse_position is None and \
            event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_position = (x, y)
            self.temp_image = self.working_image.copy()
        elif self.mouse_position is not None and \
            event == cv2.EVENT_LBUTTONDOWN:
            self.lines.append((self.mouse_position, (x, y)))
            self.mouse_position = None
            self.temp_image = None
        elif self.mouse_position is not None and \
            event == cv2.EVENT_MOUSEMOVE:
            self.working_image = self.temp_image.copy()
            self.draw_line(self.mouse_position, (x, y),
                baseline=len(self.lines) < 1)
            self.show_image()

    def reset(self):
        self.lines.clear()
        self.working_image = self.original_image.copy()

    def redraw_lines(self):
        self.working_image = self.original_image.copy()
        for idx, (start, end) in enumerate(self.lines):
            self.draw_line(start, end, baseline=idx<1)

    def toggle_simple_mode(self):
        self.simple_mode = not self.simple_mode
        self.redraw_lines()

    def show_image(self):
        cv2.imshow(self.window_name, self.working_image)

if __name__ == "__main__":
    import argparse

    argument_parser = argparse.ArgumentParser("Spectacles")
    argument_parser.add_argument("image",
        help="image to open spectacles with")
    args = argument_parser.parse_args()

    app = Spectacles(args.image)

    while True:
        app.show_image()
        key = cv2.waitKey(1)

        if key == ord('r'):
            app.reset()
        if key == ord('s'):
            app.toggle_simple_mode()
        elif key == ord('q'):
            cv2.destroyAllWindows()
            exit()
