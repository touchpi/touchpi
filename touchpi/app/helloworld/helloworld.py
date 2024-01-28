from touchpi.appbase.app import App
from PySimpleGUI import Text, VPush, Push


class HelloWorld(App):
    def __init__(self):
        super().__init__()

    @staticmethod
    def layout():
        layout = [[VPush()]]
        layout += [[Push(), Text('Hello World'), Push()]]
        layout += [[VPush()]]
        return layout


if __name__ == '__main__':
    app = HelloWorld()
    app.run()
