# -*- coding: utf-8 -*-
# ###################################################################################
#
#             Your text
#
#    License:
#    Author:
#
#                    __   .__
#      _____ _____  |  | _|__|_  _  _______ ____________
#     /     \\__  \ |  |/ /  \ \/ \/ /\__  \\_  __ \__  \
#    |  Y Y  \/ __ \|    <|  |\     /  / __ \|  | \// __ \_
#    |__|_|  (____  /__|_ \__| \/\_/  (____  /__|  (____  /
#          \/     \/     \/                \/           \/
#
#    Program walks through a directory (and subs), watch for audio and
#   extract an excerpt save the new file
#
# ######################################################################


# from audio_extract import main
import main
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import filedialog as fd

import sys
from tkinter.scrolledtext import ScrolledText


class PrintLogger(object):  # create file like object
    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
        pass


class Gui:
    root: Tk
    output_folder: Path
    log_widget: ScrolledText
    default = {
        "start": 0,
        "end": 30,
        "fade": True,
        "fade_d": 5,
        "input": Path.cwd().joinpath("input").relative_to(Path.cwd()),
    }

    def __init__(self):
        print("launching_gui..")
        self.gui()

    def launch_extract(self, debug=True, *args):
        """launch the process of extraction in backend"""

        print("Processing")
        variables = ["start", "end", "fade", "fade_d", "input"]

        try:
            # checking data input quality.
            # ---------------------------
            # variables should not be empty
            for v in variables:
                try:  # check string variables
                    if len(self.root.getvar(v)) < 1 or self.root.getvar(v) is None:
                        print(f"{v} is missing")
                        return 1
                except:
                    pass

            # launch backend process
            # ----------------------

            # convert what needs to be convert
            print("fade", self.root.getvar("fade"), bool(self.root.getvar("fade")))
            if bool(int(self.root.getvar("fade"))):
                print("here")
                fade_d = int(self.root.getvar("fade_d"))
            else:
                fade_d = 0

            params = {
                "first_second": int(self.root.getvar("start")),
                "last_second": int(self.root.getvar("end")),
                "input_dir": Path(self.root.getvar("input")).absolute(),
                "output_dir": self.output_folder.absolute(),
                "fade_d": fade_d,
            }
            print(params)

            # launch backend convertion
            # -------------------------
            main.process(input_params=params)

            if debug == True:
                print("processing done")

            return 0

        except ValueError as e:
            print("Value error", e)
            return 1

    def get_folder(self, *args):
        """select a folder and put it into input_folder
        update output part
        """
        print("Getting folder info")

        # filename = fd.askopenfilename()
        folder = fd.askdirectory()
        # folder = ""
        print(folder)

        try:
            input_folder = Path(folder).relative_to(Path.cwd())
        except:
            input_folder = Path(folder)

        self.update_output_folder(input_folder)

        print(f"input: {input_folder}, output: {self.output_folder}")

        self.root.setvar("input", value=input_folder)

    def update_output_folder(self, input_folder):
        """update the output according to the input one"""

        if not isinstance(input_folder, Path):
            input_folder = Path(input_folder)

        try:
            self.output_folder = (
                input_folder.absolute()
                .parents[0]
                .joinpath("output/")
                .relative_to(Path.cwd())
            )
        except:
            self.output_folder = input_folder.absolute().parents[0].joinpath("output/")

        # update data layer
        self.root.setvar("output", value=self.output_folder)

    def switch_control(self, target_widget: ttk.Widget, debug=True):
        """switch on or off the target widget"""

        if debug:
            print(f"(de)activating {target_widget}")
            print(target_widget["state"])  # don't remove ! Only way to work ?

        if target_widget["state"] != "disabled":
            target_widget.config(state="disabled")
        else:
            target_widget.config(state="normal")

        target_widget.update()

    def redirect_logging(self):
        """get stdout and stderr to UI"""

        logger = PrintLogger(self.log_widget)
        sys.stdout = logger
        sys.stderr = logger

    def gui(self):
        """setup GUI"""

        # main setup
        self.root = Tk()
        self.root.title("audio extract")

        title_font = font.Font(size=13, weight="bold", name="title")
        subtitle_font = font.Font(size=11, slant="italic", name="subtitle")
        frame = ttk.Frame(self.root)
        frame.grid(column=0, row=0, sticky=(N, W, E, S))

        # main frame
        title = ttk.Frame(frame)
        title.grid(column=0, row=0, columnspan=2, sticky=(N, W), padx=10, pady=10)
        options = ttk.Frame(frame)
        options.grid(column=0, row=1, sticky=(N, W), padx=5, pady=5)
        folders = ttk.Frame(frame)
        folders.grid(column=1, row=1, sticky=(N, W), padx=5, pady=5)
        process = ttk.Frame(frame)
        process.grid(column=1, row=2, sticky=(N, E), padx=5, pady=5)
        log = ttk.Frame(frame)
        log.grid(column=0, row=4, columnspan=2, sticky=(N, E), padx=5, pady=5)

        ## title frame
        # --------------
        label_title = ttk.Label(title, text="Audio extract", font=title_font)
        label_title.grid(column=0, row=0)

        #  Options frame
        #  -----------------
        options_title = ttk.Label(options, text="Options", font=subtitle_font)
        options_title.grid(column=0, row=0, columnspan=3, sticky=(N, W))

        # duration setting
        start_label = ttk.Label(options, text="Starting second")
        start_label.grid(column=0, row=1, sticky=(W))
        var_start = StringVar(self.root, name="start")
        start_second = ttk.Entry(options, textvariable=var_start)
        start_second.grid(column=1, row=1, columnspan=2)
        end_label = ttk.Label(options, text="Ending second")
        end_label.grid(column=0, row=2, sticky=(W), columnspan=2)
        var_end = StringVar(self.root, name="end")
        end_second = ttk.Entry(options, textvariable=var_end)
        end_second.grid(column=1, row=2, columnspan=2)

        # fade selection
        fade_label = ttk.Label(options, text="fade out")
        fade_label.grid(column=0, row=3, sticky=(W))
        fade_var = BooleanVar(self.root, name="fade")
        fade = ttk.Checkbutton(options, variable=fade_var)

        fade.grid(column=1, row=3, sticky=(W))
        fade_duration_var = IntVar(self.root, name="fade_d")
        fade_duration = ttk.Entry(options, textvariable=fade_duration_var)
        fade_duration.grid(column=2, row=3)
        fade.bind(
            "<1>", lambda *args: self.switch_control(fade_duration)
        )  # deactivate fade duration when fade is False

        ## folders frame
        # ---------------
        folders_title = ttk.Label(folders, text="Folders", font=subtitle_font)
        folders_title.grid(column=0, row=0, columnspan=2, stick=(N, W))

        # input and output folders
        input_label = ttk.Label(folders, text="Input folder")
        input_label.grid(column=0, row=1, sticky=(W))
        var_input = StringVar(self.root, name="input")
        input_folder = ttk.Entry(folders, textvariable=var_input, width=50)
        input_folder.bind(
            "<1>", lambda *args: self.get_folder(var_input, *args)
        )  # callback on click
        input_folder.grid(column=1, row=1)
        output_label = ttk.Label(folders, text="Output folder")
        output_label.grid(column=0, row=2, sticky=(W))
        var_output = StringVar(self.root, name="output")
        output_folder = ttk.Label(folders, textvariable=var_output, width=50)
        output_folder.bind(
            "<1>", lambda *args: self.get_folder(var_output, *args)
        )  # callback on click
        output_folder.grid(column=1, row=2)

        # process frame
        # ---------------
        process_button = ttk.Button(
            process, text="Process", command=lambda: self.launch_extract()
        )
        process_button.grid(column=0, row=0, sticky=(N, E))
        self.root.bind("<Return>", lambda *args: self.launch_extract())

        # process frame
        # ---------------
        self.log_widget = ScrolledText(
            log, height=10, width=120, font=("consolas", "8", "normal")
        )
        self.log_widget.grid(column=0, row=0, sticky=(N, E))
        self.redirect_logging()

        # set default values
        # ------------------
        for k, v in self.default.items():
            self.root.setvar(k, value=v)

        self.update_output_folder(self.root.getvar("input"))

        # launching the main loop
        # ------------------------
        self.root.mainloop()


def launch_gui():
    gui = Gui()


if __name__ == "__main__":
    launch_gui()
