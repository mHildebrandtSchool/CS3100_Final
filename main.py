# Created By Michael Jospeh Hildebrandt. Started 10/27/2023 -> Finished
from LoginGui import LoginGui
from SessionVariables import SessionVariables
from MainGui import MainGui

if __name__ == "__main__":
    #intialize login page
    session = SessionVariables() 
    login_page = LoginGui(session)
    #build page adds all Tkinter elements. Base class parameters are screen size (str) in pixle format i.e 300x100, is there a menu(bool), padding x(int), padding y(int)
    login_page.build_page("300x100", 10, 5)
    #starts the login proccess
    login_page.gui.mainloop()
    print(f"Username: {session.active_username}, Full Name: {session.active_full_name}, id: {session.active_user_id}")
    main_page = MainGui(session)
    session.main_gui = main_page
    main_page.build_page("500x500", 10, 5)
    main_page.gui.mainloop()