import tkinter as tk
import cv2
from PIL import ImageTk,Image
LARGE_FONT = ("Courier", 24)

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self,width=640,height=480)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_propagate(0)


        self.frames = {}

        for F in (StartPage, PageOne, PageTwo,PageTransaction):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent,bg = "#C2185B")
        def exit_button():
            self.quitAll()
        #exit_button = tk.PhotoImage(file="close.png")
        label = tk.Label(self, text="Face Reconition based ATM System", font=LARGE_FONT,fg="#BDBDBD",bg="#C2185B")



        label.pack(pady=20, padx=10)

        button = tk.Button(self, text="Create New User",borderwidth=1,font = ("Courier",30),
                           command=lambda: controller.show_frame(PageOne))
        button.configure(background = "#757575")
        button.pack(pady=50, padx=10)

        button2 = tk.Button(self, text="Login User",font=("Courier",30),
                            command=lambda: controller.show_frame(PageTwo))
        button2.configure(background = "#757575")
        button2.pack()
        button_qwer = tk.Button(self, text="close", command=self.quit)
        button_qwer.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        ment = tk.StringVar()

        def get_name():
            mtext = ment.get()
            import capture_face
            if mtext!="":
                capture_face.start_capture(mtext)
                label.configure(text = "Done")
            else:
                label.configure(text="Enter Name")
        tk.Frame.__init__(self, parent,bg = "#C2185B")
        label = tk.Label(self, text="Create New User", font=LARGE_FONT,fg="#BDBDBD",bg="#C2185B")
        label.pack(pady=20, padx=10)

        button1 = tk.Button(self, text="Back to Home",borderwidth=1,font = ("Courier",30),
                            command=lambda: controller.show_frame(StartPage))
        button1.configure(background="#757575")
        button1.pack()
        mNameButton = tk.Button(self, text="Enter Name Details", borderwidth=1, font=("Courier", 30),background="#757575",
                                command=get_name).pack(side="top",pady=20, padx=10)

        text_label = tk.Label(self, text="Enter User Name", font=LARGE_FONT,fg="#BDBDBD",bg="#C2185B",bd=-2).pack(padx=45,side="left")
        entry = tk.Entry(self, textvariable=ment,bg = "#E91E63").pack(ipady=5,side="left")
        button_qwer = tk.Button(self, text="close", command=self.quit)
        button_qwer.place(relx=0.5, anchor=tk.CENTER)
        button_qwer.pack(side="left",padx=20,pady=50)

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):

        def authentication():
            import authenticate
            n = authenticate.authen()
            if type(n)!=None:
                label.configure(text = "Welcome "+str(n))
                button2.configure(text="Proceed to Transactions",command=lambda: controller.show_frame(PageTransaction))

            else:
                label.configure(text="Retry")
        tk.Frame.__init__(self, parent,bg = "#C2185B")
        label = tk.Label(self, text="Open Camera to login", font=LARGE_FONT,fg="#BDBDBD",bg="#C2185B")
        label.pack(pady=20, padx=10)

        button1 = tk.Button(self, text="Back to Home",font = ("Courier",30),background="#757575",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=20)

        button2 = tk.Button(self, text="Click to open camera",font = ("Courier",30),background="#757575",
                            command=authentication)
        button2.pack(pady=20)
        button_qwer = tk.Button(self, text="close", command=self.quit)
        button_qwer.place(relx=0.5, anchor=tk.CENTER)
        button_qwer.pack(side="left", padx=20, pady=50)

class PageTransaction(tk.Frame):

    def __init__(self, parent, controller):
        ment = tk.StringVar()
        import random
        self.number = random.randint(1000, 1000000)
        def withdraw():
            if self.number>=int(ment.get()):
                self.number = self.number-int(ment.get())
                label_balance.configure(text="Transaction Succesful. \nBalance: " +str(self.number))

            else:
                label_balance.configure(text="Insuffecient Balance")

        tk.Frame.__init__(self, parent,bg = "#C2185B")
        label = tk.Label(self, text="Account Summary", font=LARGE_FONT,fg="#BDBDBD",bg="#C2185B")
        label.pack(pady=20, padx=10)

        label_balance = tk.Label(self, text="Current Balance:" + str(self.number), font=LARGE_FONT, fg="#BDBDBD", bg="#C2185B")
        label_balance.pack(pady=20, padx=10)
        button1 = tk.Button(self, text="Withdraw Amount", font=("Courier", 30), background="#757575",
                            command=lambda: withdraw())
        button1.pack(pady=20, side="left")
        entry = tk.Entry(self, textvariable=ment, bg="#E91E63").pack(ipady=5, side="left")


        button_qwer = tk.Button(self, text="close", command=self.quit)
        button_qwer.place(relx=0.5, anchor=tk.CENTER)
        button_qwer.pack(side="left", padx=20, pady=50)

app = SeaofBTCapp()
app.resizable(0,0)
app.mainloop()