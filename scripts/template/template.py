from touchpi.appbase.app import App
from PySimpleGUI import VPush, Push, Text


class ${CLASSNAME}(App):
    def __init__(self):
        super().__init__()

    @staticmethod
    def layout():
        layout = [[VPush()]]
        layout += [[Push(), Text('Hello world'), Push()]]
        layout += [[VPush()]]
        return layout


if __name__ == '__main__':
    app = ${CLASSNAME}()
    app.run()
