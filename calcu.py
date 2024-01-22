import tkinter as tk
from tkinter import messagebox

LARGE_FONT_STYLE = ("Arial", 30, "bold")
SMALL_FONT_STYLE = ("Arial", 14)
DIGITS_FONT_STYLE = ("Arial", 20, "bold")
DEFAULT_FONT_STYLE = ("Arial", 18)
BACKSPACE_FONT_STYLE = ("Arial", 14)
HISTORY_FONT_STYLE = ("Arial", 25)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("320x500")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        self.image = tk.PhotoImage(file="calc.png")
        self.window.iconphoto(False,self.image)

        self.total_expression = ""
        self.current_expression = ""
        self.calculation_history = []
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits ={
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), ".": (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.total_temp = ""

        self.buttons_frame.rowconfigure(0, weight=1)
        self.display_frame.rowconfigure(0, weight=1)
        for x in range (1,5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
            self.display_frame.rowconfigure(x, weight=1)
            self.display_frame.columnconfigure(x, weight=1)
        self.create_digits_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()
        self.create_history_button()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(str(key), lambda event, operator=key: self.append_operator(operator))
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_backspace_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.grid(row=2, column=4, sticky=tk.E)

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.grid(row=4, column=4, sticky=tk.E)

        return total_label, label
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        if self.current_expression == "Error":
            self.clear()
        self.current_expression += str(value)
        self.update_label()

    def create_digits_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        if self.current_expression == "Error":
            self.clear()
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()
    def create_operator_buttons(self):
        i = 0
        for operator,symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i+=1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="AC", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, columnspan=2, sticky=tk.NSEW)

    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def create_backspace_button(self):
        button = tk.Button(self.buttons_frame, text="\u232B", bg=OFF_WHITE, fg=LABEL_COLOR, font=BACKSPACE_FONT_STYLE,
                           borderwidth=0, command=self.backspace)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def add_history(self):
        self.temp_update = self.update_temp()
        history_entry = f"{self.temp_update} = {self.current_expression}"
        self.calculation_history.append(history_entry)

    def show_history(self):
        messagebox.showinfo("Calculation History", "\n".join(self.calculation_history))


    def create_history_button(self):
        button = tk.Button(self.display_frame, text="\u2331", bg=LIGHT_GRAY, fg=LABEL_COLOR, bd=110, height=0,
                           font=HISTORY_FONT_STYLE, borderwidth=0, command=self.show_history)
        button.grid(row=0, column=4, sticky=tk.NE)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            if self.current_expression == "Error":
                self.clear()
            self.current_expression = str(eval(self.total_expression))
            self.total_temp = self.total_expression
            self.total_expression = ""
            self.add_history()
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_temp(self):
        expression = self.total_temp
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        return expression

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)


    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()
