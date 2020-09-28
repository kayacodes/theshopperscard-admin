import tkinter as tk       
import time

import mysql.connector
from mysql.connector import Error


try:
    conn = mysql.connector.connect(host='localhost', user='root', passwd='', database ='user_registration', port='3308')
    if conn.is_connected():
        print ('Database Connected')

except Error as e:
    print(e)

mycursor = conn.cursor()

class TSCApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {
            "customerID": tk.IntVar(),
            "calculatedPoints": tk.DoubleVar(),
            "companyName": tk.StringVar(),
            "storedPoints": tk.IntVar(),
            "points_label":  tk.StringVar()
        }

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("800x750")

        self.frames = {}
        for F in (StartPage, MenuPage, Purchase, PurchaseWithPoints):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#A4BAC0")
        self.controller = controller
        
        self.controller.title("The Shopper's Card - Admin")
       
        self.controller.iconphoto(False, 
                        tk.PhotoImage(file='C:/Users/rooks/Documents/Websites/TheShoppersCard-Admin/card.png'))
                        
        headingLabel = tk.Label(self,
                                text = "THE SHOPPER'S CARD",
                                font = ('arial', 50, 'bold'),
                                foreground ='white',
                                background ='#A4BAC0')

        headingLabel.pack(pady=25)

        subLabel = tk.Label(self,
                                text = "ADMIN",
                                font = ('arial', 35),
                                foreground ='white',
                                background ='#A4BAC0')

        subLabel.pack()

        space_label = tk.Label(self, height = 4, bg = '#A4BAC0') 
        space_label.pack()

        idLabel = tk.Label(self,
                            text ='Enter Customer ID',
                            font =('arial', 15, 'bold'),
                            foreground ='white',
                            background ='#A4BAC0')
        idLabel.pack(pady = 10)

        
        self.controller.shared_data["customerID"].set("")
        id_entry_box = tk.Entry(self,
                                textvariable=self.controller.shared_data["customerID"],
                                font = ('arial', 13),
                                width = 24,
                                bg = 'white')
        id_entry_box.focus_set()
        id_entry_box.pack(ipady = 7)  

        def checkID():
            enteredID = (self.controller.shared_data["customerID"].get(),)
            
            if len(str(self.controller.shared_data["customerID"].get())) == 13:
                sql_query = """SELECT id FROM signup WHERE id = %s"""
                mycursor.execute(sql_query, enteredID)
                record = mycursor.fetchone()
                
                if record == None :
                    incorrect_id_label['text'] = 'Incorrect ID'
                
                elif record[0] == self.controller.shared_data["customerID"].get():
                    incorrect_id_label['text'] = ''
                    controller.show_frame('MenuPage')

            else:
                incorrect_id_label['text'] = 'Incorrect ID Length'
            

        enter_button = tk.Button(self,
                                text = 'Enter',
                                command = checkID,
                                relief = 'raised',
                                borderwidth = 3,
                                width = 30,
                                height = 3,
                                bg = 'white')
        enter_button.pack(pady = 10)    
        

        incorrect_id_label = tk.Label(self,
                            text ='',
                            font =('arial', 13, 'bold'),
                            foreground ='white',
                            background ='#5e7e87',
                            anchor = 'n')
        incorrect_id_label.pack(fill='both', expand = True)     

        bottom_frame = tk.Frame(self, relief = 'raised', borderwidth = 3)     
        bottom_frame.pack(fill = 'x', side = 'bottom')      

        def tick():
            current_time = time.strftime('%I:%M %p')
            time_label.config(text = current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font = ('arial', 12))
        time_label.pack(side = 'right')
        
        tick()


class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = "#A4BAC0")
        self.controller = controller

        headingLabel = tk.Label(self,
                                text = "THE SHOPPER'S CARD",
                                font = ('arial', 50, 'bold'),
                                foreground ='white',
                                background ='#A4BAC0')
        headingLabel.pack(pady=25)

        main_menu_label = tk.Label(self,
                                    text = "Main Menu",
                                    font = ('arial', 20, 'bold'),
                                    foreground ='white',
                                    background ='#A4BAC0')
        main_menu_label.pack(pady=15)

        selection_label = tk.Label(self,
                                    text = "Please Make A Selection",
                                    font = ('arial', 15, 'bold'),
                                    foreground ='white',
                                    background ='#A4BAC0'
                                    )
        selection_label.pack(fill = 'x')
        
        
        def displayPoints(*args):
            
            points = (self.controller.shared_data["customerID"].get(), )

            company = var.get()
            if company == "Woolworths":
                self.controller.shared_data["companyName"].set("woolworths")
                
            elif company == "H&M":
                self.controller.shared_data["companyName"].set("hm")

            elif company == "M&S":
                self.controller.shared_data["companyName"].set("ms")

            elif company == "CNA":
                self.controller.shared_data["companyName"].set("cna")

            elif company == "Amazon":
                self.controller.shared_data["companyName"].set("amazon")


            sql_query = """SELECT {0} FROM points WHERE points.id = %s""".format(self.controller.shared_data["companyName"].get())
            mycursor.execute(sql_query, points)
            record = mycursor.fetchone()

            self.controller.shared_data["calculatedPoints"].set(record[0]/10)
            self.controller.shared_data["storedPoints"].set(record[0])

            self.controller.shared_data["points_label"].set('You Have R{0} Worth Of Points'.format(self.controller.shared_data["calculatedPoints"].get()))
            points_label['text'] = self.controller.shared_data["points_label"].get()
            

        OPTIONS = [
            "Woolworths",
            "H&M",
            "M&S",
            "CNA",
            "Amazon"
        ]

        var = tk.StringVar(self)
        var.set(OPTIONS[0])
        var.trace("w", displayPoints)
 
        dropDownMenu = tk.OptionMenu(self, var, OPTIONS[0], OPTIONS[1], OPTIONS[2], OPTIONS[3], OPTIONS[4])
        dropDownMenu.config(width = 15, bg = 'white')
        dropDownMenu.pack()
        
        self.controller.shared_data["points_label"].set("")
        points_label = tk.Label(self,
                            textvariable = self.controller.shared_data["points_label"],
                            font = ('arial', 13, 'bold'),
                            foreground ='white',
                            background ='#A4BAC0',
                            anchor = 'n')
                           
        points_label.pack(pady = 10) 

        button_frame = tk.Frame(self, bg = '#5e7e87')
        button_frame.pack(fill = 'both', expand = True)

        def purchase():
            controller.show_frame('Purchase')

        purchase_button = tk.Button(button_frame,
                                    text = 'Purchase',
                                    command = purchase,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 50,
                                    height = 5,
                                    bg = 'white')
        purchase_button.grid(row = 1, column = 0, padx = 220, pady =30)                            


        def purchaseWithPoints():
            controller.show_frame('PurchaseWithPoints')

        purchaseWithPoints_button = tk.Button(button_frame,
                                    text = 'Purchase With Points',
                                    command = purchaseWithPoints,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 50,
                                    height = 5,
                                    bg = 'white')
        purchaseWithPoints_button.grid(row = 2, column = 0)       

        def exit():
            self.controller.shared_data["customerID"].set("")
            self.controller.shared_data["points_label"].set("")
            
            controller.show_frame('StartPage')

        exit_button = tk.Button(button_frame,
                                    text = 'New Customer',
                                    command = exit,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 50,
                                    height = 5,
                                    bg = 'white')
        exit_button.grid(row = 3, column = 0,  pady =30)                     


        bottom_frame = tk.Frame(self, relief = 'raised', borderwidth = 3)     
        bottom_frame.pack(fill = 'x', side = 'bottom')      

        def tick():
            current_time = time.strftime('%I:%M %p')
            time_label.config(text = current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font = ('arial', 12))
        time_label.pack(side = 'right')
        
        tick()
     


class Purchase(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background ='#A4BAC0')
        self.controller = controller

        headingLabel = tk.Label(self,
                                text = "THE SHOPPER'S CARD",
                                font = ('arial', 50, 'bold'),
                                foreground ='white',
                                background ='#A4BAC0')
        headingLabel.pack(pady=25)

        purchase_amount_label = tk.Label(self,
                                    text = "Enter The Amount Of Purchase",
                                    font = ('arial', 20, 'bold'),
                                    foreground ='white',
                                    background ='#A4BAC0')
        purchase_amount_label.pack(pady=15)

        button_frame = tk.Frame(self, bg = '#5e7e87')
        button_frame.pack(fill = 'both', expand = True)

        amount_label = tk.Label(button_frame,
                                text = "Total Amount",
                                font = ('arial', 20, 'bold'),
                                foreground ='white',
                                background ='#5e7e87')
        amount_label.grid(row = 0, column = 1, pady=20, padx = 260)

        cash = tk.DoubleVar()
        cash.set("")
        amount_entry = tk.Entry(button_frame,
                                textvariable = cash,
                                width = 45)
        amount_entry.grid(row = 2, column = 1, ipady = 15 , padx = 260)

        
        def addPoints():
            newPoints = cash.get() + self.controller.shared_data["storedPoints"].get()

            points = (newPoints, self.controller.shared_data["customerID"].get(), )

            sql_query = """UPDATE points SET {0} = %s WHERE points.id = %s""".format(self.controller.shared_data["companyName"].get())
            mycursor.execute(sql_query, points)
            
            pointsAdded_label['text'] = str(cash.get()) + ' points were added.'
            

        addPoints_button = tk.Button(button_frame,
                                text = 'Enter',
                                command = addPoints,
                                relief = 'raised',
                                borderwidth = 3,
                                width = 38,
                                height = 2,
                                bg = 'white')
        addPoints_button.grid(row = 3, column = 1, pady = 15)  

        pointsAdded_label = tk.Label(button_frame,
                            text ='',
                            font =('arial', 13, 'bold'),
                            foreground ='white',
                            background ='#5e7e87')
        pointsAdded_label.grid(row = 1, column = 1, padx = 50, pady = 10)     

        def back():
            controller.show_frame('MenuPage')

        back_button = tk.Button(button_frame,
                                    text = 'Menu',
                                    command = back,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 38,
                                    height = 2,
                                    bg = 'white')
        back_button.grid(row = 4, column = 1, padx = 5 )     

        def exit():
            self.controller.shared_data["customerID"].set("")
            self.controller.shared_data["points_label"].set("")
            controller.show_frame('StartPage')

        exit_button = tk.Button(button_frame,
                                    text = 'New Customer',
                                    command = exit,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 38,
                                    height = 2,
                                    bg = 'white')
        exit_button.grid(row = 5, column = 1, padx = 5, pady = 15 )    


        bottom_frame = tk.Frame(self, relief = 'raised', borderwidth = 3)     
        bottom_frame.pack(fill = 'x', side = 'bottom')      

        def tick():
            current_time = time.strftime('%I:%M %p')
            time_label.config(text = current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font = ('arial', 12))
        time_label.pack(side = 'right')
        
        tick()

class PurchaseWithPoints(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background ='#A4BAC0')
        self.controller = controller

        headingLabel = tk.Label(self,
                                text = "THE SHOPPER'S CARD",
                                font = ('arial', 50, 'bold'),
                                foreground ='white',
                                background ='#A4BAC0')
        headingLabel.pack(pady=25)

        purchase_amount_label = tk.Label(self,
                                    text = "Enter The Amount Of Purchase",
                                    font = ('arial', 20, 'bold'),
                                    foreground ='white',
                                    background ='#A4BAC0')
        purchase_amount_label.pack(pady=15)

        button_frame = tk.Frame(self, bg = '#5e7e87')
        button_frame.pack(fill = 'both', expand = True)

        amount_label = tk.Label(button_frame,
                                text = "Total Amount",
                                font = ('arial', 20, 'bold'),
                                foreground ='white',
                                background ='#5e7e87')
        amount_label.grid(row = 0, column = 1, pady=20, padx = 260)

        cash = tk.DoubleVar()
        cash.set("")
        amount_entry = tk.Entry(button_frame,
                                textvariable = cash,
                                width = 45)
        amount_entry.grid(row = 2, column = 1, ipady = 15 , padx = 260)

        
        def usePoints():
            
            if cash.get() >= self.controller.shared_data["calculatedPoints"].get():
                newPoints = round(cash.get() - self.controller.shared_data["calculatedPoints"].get())
            
            else:
                newPoints = round((self.controller.shared_data["calculatedPoints"].get() - cash.get()) * 10)

            points = (newPoints, self.controller.shared_data["customerID"].get(), )

            sql_query = """UPDATE points SET {0} = %s WHERE points.id = %s""".format(self.controller.shared_data["companyName"].get())
            mycursor.execute(sql_query, points)
            
            pointsAdded_label['text'] = str(newPoints) + ' points were added.'

       

        addPoints_button = tk.Button(button_frame,
                                text = 'Enter',
                                command = usePoints,
                                relief = 'raised',
                                borderwidth = 3,
                                width = 38,
                                height = 2,
                                bg = 'white')
        addPoints_button.grid(row = 3, column = 1, pady = 15)  

        pointsAdded_label = tk.Label(button_frame,
                            text ='',
                            font =('arial', 13, 'bold'),
                            foreground ='white',
                            background ='#5e7e87')
        pointsAdded_label.grid(row = 1, column = 1, padx = 50, pady = 10)     
    

        def back():
            controller.show_frame('MenuPage')

        back_button = tk.Button(button_frame,
                                    text = 'Menu',
                                    command = back,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 38,
                                    height = 2,
                                    bg = 'white')
        back_button.grid(row = 4, column = 1, padx = 5 )     

        def exit():
            self.controller.shared_data["customerID"].set("")
            self.controller.shared_data["points_label"].set("")
            controller.show_frame('StartPage')

        exit_button = tk.Button(button_frame,
                                    text = 'New Customer',
                                    command = exit,
                                    relief = 'raised',
                                    borderwidth = 3,
                                    width = 38,
                                    height = 2,
                                    bg = 'white')
        exit_button.grid(row = 5, column = 1, padx = 5, pady = 15 ) 


        button_frame = tk.Frame(self, bg = '#5e7e87')
        button_frame.pack(fill = 'both', expand = True)

        bottom_frame = tk.Frame(self, relief = 'raised', borderwidth = 3)     
        bottom_frame.pack(fill = 'x', side = 'bottom')      

        def tick():
            current_time = time.strftime('%I:%M %p')
            time_label.config(text = current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font = ('arial', 12))
        time_label.pack(side = 'right')
        
        tick()

if __name__ == "__main__":
    app = TSCApp()
    app.mainloop()