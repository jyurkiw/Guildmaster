import py_cui


class UI(object):
    def enable(self):
        pass


class TitleUI(UI):
    title = """
  ________      .__.__       .___                       __                
 /  _____/ __ __|__|  |    __| _/_____ _____    _______/  |_  ___________ 
/   \\  ___|  |  \\  |  |   / __ |/     \\\\__  \\  /  ___/\\   __\\/ __ \\_  __ \\
\\    \\_\\  \\  |  /  |  |__/ /_/ |  Y Y  \\/ __ \\_\\___ \\  |  | \\  ___/|  | \\/
 \\______  /____/|__|____/\\____ |__|_|  (____  /____  > |__|  \\___  >__|   
        \\/                    \\/     \\/     \\/     \\/            \\/"""

    def __init__(self, parent: py_cui.PyCUI):
        self.parent = parent
        self.ui = self.parent.create_new_widget_set(8, 5)
        self.title = self.ui.add_text_block("Arandmoor's", 0, 1, column_span=3, initial_text=TitleUI.title)

    def enable(self):
        self.parent.apply_widget_set(self.ui)


class GameUI(object):
    def __init__(self):
        self.ui = py_cui.PyCUI(8, 5)

        self.title_ui = TitleUI(self.ui)
        self.title_ui.enable()

        self.ui.start()
