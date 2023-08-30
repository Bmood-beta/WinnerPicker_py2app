from setuptools import setup

setup(
    app=["WinnerPicker.py"],
    options={
        "py2app": {
            "packages": ["pandas", "openpyxl", "tkinter"],
            "includes": ["tkinter", "tkinter.filedialog", "tkinter.messagebox"],
        }
    }
)
