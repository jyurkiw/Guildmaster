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

        self.title = self.ui.add_text_block("Arandmoor's", 0, 0, column_span=5, initial_text=TitleUI.title)

        self.menu_options = ['New Game', 'Load Game', 'Help', 'Settings', 'Quit']

        self.menu = self.ui.add_scroll_menu('Main Menu', 1, 2, row_span=2)
        self.menu.add_item_list(self.menu_options)
        self.menu.add_key_command(py_cui.keys.KEY_ENTER, self.main_menu_handler)
        self.menu.set_selected(True)

    def main_menu_handler(self):
        option = self.menu.get()

        if option == 'New Game':
            pass
        elif option == 'Load Game':
            pass
        elif option == 'Help':
            self.parent.show_message_popup(
                title='Help',
                text='github.com/jyurkiw/Guildmaster/docs/toc.md',
                color=py_cui.WHITE_ON_BLACK)
        elif option == 'Settings':
            pass
        elif option == 'Quit':
            exit()

    def enable(self):
        self.parent.apply_widget_set(self.ui)


class GameUI(object):
    def __init__(self):
        self.ui = py_cui.PyCUI(8, 5)

        self.title_ui = TitleUI(self.ui)
        self.title_ui.enable()

        self.ui.start()
