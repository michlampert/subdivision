from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from tkinter import messagebox
from tkinter import ttk
import utils 
import mesh

class State:
    def __init__(self):
        self.app = utils.app
        self.app.configure(bg=utils.dark_blue)
        self.filename_input = None
        self.filename_output = None
        self.selected_algorithm = "CathmulClark"
        self.info_frame = Frame(self.app, background=utils.dark_blue)

        self.app.title('Subdivision')
        self.app.geometry(str(utils.window_width) + "x" + str(utils.window_height))

        Label(self.app, text="Enter your output filename:", bg=utils.dark_blue, fg=utils.white).pack()
        self.text_box = Entry(self.app)
        self.text_box.pack(pady = 10)

        self.input_button = Button(self.app, text ="Choose input file:", command = self.import_mesh_from_file)
        self.input_button.pack(pady = 10)

        Label(self.app, text="Choose number of iterations:", bg=utils.dark_blue, fg=utils.white).pack()
        self.iterations_count_entry = Spinbox(self.app, from_ = 1, to = 10) #Entry(self.app)
        self.iterations_count_entry.pack(pady = 10)

        Label(self.app, text="Choose algorithm:", bg=utils.dark_blue, fg=utils.white).pack()
        self.algorithm_menu = ttk.Combobox(self.app, value = utils.algorithm_names)
        self.algorithm_menu.current(0)
        self.algorithm_menu.pack(pady = 10)
        run_button = Button(self.app, text ="Run subdivision", command = self.run_subdivision)

        run_button.pack(pady = 10)

    def actualize_font(self):
        utils.font_size = utils.set_height(1 / 25)
        utils.normal_font = Font(family="Open Sans", size=utils.font_size)
        utils.bigger_font = Font(family="Open Sans", size=utils.set_font(3 / 2))

    def import_mesh_from_file(self):
        self.filename_input = filedialog.askopenfilename(title="Select File",  filetypes=(("text", ".off"), ("all files", "*.*")))

    def run_subdivision(self):
        iterations_count = utils.validate_int(self.iterations_count_entry.get())
        self.filename_output = utils.validate_filename(self.text_box.get())
        if not self.filename_input: messagebox.showinfo("Input file!", "Please specify your input file!") 
        if not iterations_count or not self.filename_output: return None
        mesh.subdivision(self.filename_input, self.filename_output, iterations_count, self.algorithm_menu.get())
        messagebox.showinfo("Success!", "Your mesh has been saved!")

    

def main():
    state = State()
    # App responsiveness:
    while True:
        state.app.update()
        if utils.window_width != state.app.winfo_width() or utils.window_height != state.app.winfo_height():
            if state.app.winfo_width() * 2 / 3 > state.app.winfo_height():
                utils.window_width = int(state.app.winfo_height() * 3 / 2)
                utils.window_height = state.app.winfo_height()
            else:
                utils.window_width = state.app.winfo_width()
                utils.window_height = int(state.app.winfo_width() * 2 / 3)

            state.app.geometry(str(utils.window_width) + "x" + str(utils.window_height))
            state.actualize_font()
            #state.place()

if __name__ == "__main__":
    main()
