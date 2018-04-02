if __name__ == '__main__':
    import sys,platform
    from PyQt5.QtWidgets import QApplication
    from CvPyGui import Main

    if platform.system() == "Windows":
        import ctypes  
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

  
    app = QApplication(sys.argv)
    window = Main.MyApp()
    window.show()
    global update1
    update1 = 0
    global update2
    update2 = 0
    sys.exit(app.exec_())
