# Created By Michael Jospeh Hildebrandt. Started 10/27/2023 -> Finished
from LoginGui import LoginGui

if __name__ == "__main__":
    #intialize login page 
    login_page = LoginGui()

    #build page adds all Tkinter elements. Base class parameters are screen size (str) in pixle format i.e 300x100, is there a menu(bool), padding x(int), padding y(int)
    login_page.build_page("300x100", False, 10, 5)

    #starts the program
    login_page.gui.mainloop()