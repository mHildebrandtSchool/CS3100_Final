# Created By Michael Jospeh Hildebrandt. Started 10/27/2023 -> Finished
from LoginGui import LoginGui
from SessionVariables import SessionVariables
from MainGui import MainGui

class IsRunning():
    def __init__(self):
        self.running = True

    def kill_window(self, window):
        self.running = False
        window.close_window()


if __name__ == "__main__":
    #intialize login page
    check = IsRunning()
    while check.running:
        session = SessionVariables()
        login_page = LoginGui(session)
        #build page adds all Tkinter elements. Base class parameters are screen size (str) in pixle format i.e 300x100, is there a menu(bool), padding x(int), padding y(int)
        login_page.build_page("300x110", 10, 5)
        login_page.gui.protocol("WM_DELETE_WINDOW", lambda: check.kill_window(login_page))
        #starts the login proccess
        login_page.gui.mainloop()
        if session.active_user_id is not None:
            main_page = MainGui(session, check)
            session.main_gui = main_page
            main_page.build_page("500x500", 10, 5)
            main_page.gui.protocol("WM_DELETE_WINDOW", lambda: check.kill_window(main_page))
            session.inital_launch = False
            main_page.gui.mainloop()



    