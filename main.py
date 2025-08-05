from auth import LoginWindow
from gui.dashboard import Dashboard

def run_app():
    def launch_dashboard(username):
        Dashboard(username).mainloop()

    app = LoginWindow(on_success=launch_dashboard)
    app.mainloop()

if __name__ == "__main__":
    run_app()

