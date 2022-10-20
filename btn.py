import tkinter


class Btn(tkinter.Button):
    # Creating a button class, which is a subclass of the tkinter Button class
    def __init__(self, field, **kwargs):
        super().__init__(field, **kwargs)
        # initializing self.image:
        self.image = ""

    def default_button(self, row, column):
        # default button properties
        button_image = tkinter.PhotoImage(file="sea_pattern.png")
        self.grid(row=row+1, column=column+1)
        self.configure(image=button_image)
        # Keeping a reference of the image, otherwise Python doesn't display it:
        self.image = button_image
        # TODO Ask - how does self.btn['image'] work "under the hood"?
        # TODO Ask - what exactly is btn.image ? Is it an attribute of the button class?

    def hit_target(self, row, column):
        # button when a ship is hit
        button_image = tkinter.PhotoImage(file="explosion.png")
        self.grid(row=row+1, column=column+1)
        self.configure(image=button_image)
        # Keeping a reference of the image, otherwise Python doesn't display it:
        self.image = button_image

    def miss_target(self, row, column):
        # button when no ship is hit
        button_image = tkinter.PhotoImage(file="miss_target.png")
        self.grid(row=row+1, column=column+1)
        self.configure(image=button_image)
        # Keeping a reference of the image, otherwise Python doesn't display it:
        self.image = button_image

    def ship_display(self, row, column, picture):
        # button displaying a ship
        button_image = tkinter.PhotoImage(file=picture+".png")
        self.grid(row=row+1, column=column+1)
        self.configure(image=button_image)
        # Keeping a reference of the image, otherwise Python doesn't display it:
        self.image = button_image
