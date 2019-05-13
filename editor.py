#Editor z webu ITNetwork
#!/usr/bin/env python3
import copy
import tkinter
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
from subprocess import Popen
import time

class MainWindow(ttk.tkinter.Frame): 

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row = 0, column = 0)
        self.text = ""
        self.text_old = ""
        self.file_name = ""
        self.color_background = "#ffffff"
        self.color_foreground = "#000000"
        self.color_highlight_b = "#c0c0c0"
        self.color_highlight_f = "#000000"
        self.wrap_on = False
        self.createFileMenu()
        self.createWidgets()
        self.parent.minsize(500, 400)
        self.parent.resizable(width = "True", height = "True")
        self.parent.title("EasyScript IDE")
        self.parent.protocol("WM_DELETE_WINDOW", lambda *ignore: self.quitApp())
        
        self.parent.bind("<Control-n>", lambda *ignore: self.newFile())
        self.parent.bind("<Control-o>", lambda *ignore: self.openFile())
        self.parent.bind("<Control-s>", lambda *ignore: self.saveFile())
        self.parent.bind("<Control-q>", lambda *ignore: self.quitApp())
        self.parent.bind("<Control-z>", lambda *ignore: self.undoEvent())
        self.parent.bind("<Control-Z>", lambda *ignore: self.redoEvent())
        self.parent.bind("<Control-a>", lambda *ignore: self.selectAll())
        self.parent.bind("<Control-w>", lambda *ignore: self.wrapSwitch())
        self.parent.bind("<Control-b>", lambda *ignore: self.chooseBackground())
        self.parent.bind("<Control-B>", lambda *ignore: self.chooseForeground())
        self.parent.bind("<Control-i>", lambda *ignore: self.chooseHighlightB())
        self.parent.bind("<Control-I>", lambda *ignore: self.chooseHighlightF())
        self.parent.bind("<Control-R>", lambda *ignore: self.CompileScript())
		
        self.parent.rowconfigure(0, weight=999)
        self.parent.rowconfigure(1, weight=1)
        self.parent.columnconfigure(0, weight=999)
        self.parent.columnconfigure(1, weight=1)
        
    def createWidgets(self):
        self.scroll_bar_y = ttk.Scrollbar(orient = tkinter.VERTICAL)
        self.scroll_bar_x = ttk.Scrollbar(orient = tkinter.HORIZONTAL)
        self.notepad = tkinter.Text(undo = True,
                                    wrap = tkinter.NONE,
                                    yscrollcommand = self.scroll_bar_y.set,
                                    xscrollcommand = self.scroll_bar_x.set,
                                    bg = self.color_background,
                                    fg = self.color_foreground,
                                    selectbackground = self.color_highlight_b,
                                    selectforeground = self.color_highlight_f
                                    )
        self.scroll_bar_y["command"] = self.notepad.yview
        self.scroll_bar_x["command"] = self.notepad.xview

        self.notepad.grid(row = 0, column = 0, sticky = tkinter.NSEW, padx = 1, pady = 1)
        self.scroll_bar_y.grid(row = 0, column = 1, sticky = tkinter.NS)
        self.scroll_bar_x.grid(row = 1, column = 0, sticky = tkinter.EW)

    def createFileMenu(self):
        self.main_menu = tkinter.Menu(self.parent)
        self.file_menu = tkinter.Menu(self.main_menu, tearoff = 0)
        self.edit_menu = tkinter.Menu(self.main_menu, tearoff = 0)
        self.format_menu = tkinter.Menu(self.main_menu, tearoff = 0)
        self.option_menu = tkinter.Menu(self.main_menu, tearoff = 0)
        
        self.main_menu.add_cascade(label="File", menu = self.file_menu, underline = 1)
        self.file_menu.add_command(label="New", command = lambda : self.newFile(), underline = 0, accelerator = "Ctrl+N")
        self.file_menu.add_command(label="Open", command = lambda : self.openFile(), underline = 0, accelerator = "Ctrl+O")
        self.file_menu.add_command(label="Save", command = lambda : self.saveFile(), underline = 0, accelerator = "Ctrl+S")
        self.file_menu.add_command(label="Save as...", command = lambda : self.saveFileAs())
        self.file_menu.add_command(label="Quit", command = lambda : self.quitApp(), underline = 0, accelerator = "Ctrl+Q")
        
        self.main_menu.add_cascade(label="Edit", menu = self.edit_menu, underline = 0)
        self.edit_menu.add_command(label="Undo", command = lambda : self.undoEvent(), underline = 0, accelerator = "Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command = lambda : self.redoEvent(), underline = 0, accelerator = "Ctrl+Shift+Z")
        self.edit_menu.add_command(label="Select All", command = lambda : self.selectAll(), underline = 7, accelerator = "Ctrl+A")

        self.main_menu.add_cascade(label="Format", menu = self.format_menu, underline = 0)
        self.format_menu.add_command(label="Wrap Off/On", command = lambda : self.wrapSwitch(), underline = 0, accelerator = "Ctrl+W")

        self.main_menu.add_cascade(label="Build", menu = self.option_menu, underline = 0)
        self.option_menu.add_command(label="Compile", command = lambda : self.CompileScript(), underline = 0, accelerator = "Ctrl+R")
		
        self.parent["menu"] = self.main_menu
		# Menu piča usínám .... Pičovina píše se to uplně napiču

		
		
		
    def CompileScript(self):
        try:
            os.system("C:/EasyScript/main.bat")
			
        except Exception:
            e = "ERROR SYNTAXED EDITOR BY Itagochi 2017"
            print (e)

            
    def askSave(self):
        reply = messagebox.askyesnocancel(message = "Do you want save changes?", title = "Info")
        if reply is None:
            return None
        if reply:
            return True
        return False

    def invertColor(self, color):
        color = color.replace("#", "0x")
        invert_color = hex(16777215 - int(color, 16)).replace("0x", "")
        invert_color = "#" + "0"*(6 - len(invert_color)) + invert_color
        return invert_color
        

    def newFile(self):
        self.text = self.notepad.get(1.0, "end-1c")
        if self.text != self.text_old:
            answer = self.askSave()
            if answer is None:
                pass
            elif answer:
                self.saveFileAs()
            else:
                self.notepad.edit_reset()
                self.notepad.delete(1.0, tkinter.END)
                self.text = ""
                self.text_old = ""
                self.file_name = ""
        else:
                self.notepad.edit_reset()
                self.notepad.delete(1.0, tkinter.END)
                self.text = ""
                self.text_old = ""
                self.file_name = ""

    def openFile(self):
        self.text = self.notepad.get(1.0, "end-1c")
        if self.text != self.text_old:
            answer = self.askSave()
            if answer is None:
                pass
            elif answer:
                self.saveFileAs()
            else:
                self.file_name = filedialog.askopenfilename(filetypes = (("Text files", "*.es"), ("All files", "*.*")))
                if self.file_name:
                    try:
                        with open(self.file_name, mode="r") as fin:
                            self.text = fin.read()
                            self.notepad.delete(1.0, tkinter.END)
                            self.notepad.insert(1.0, self.text)
                            self.notepad.edit_reset()
                            self.text_old = copy.deepcopy(self.text)
                    except FileExistsError:
                        pass
                    except PermissionError:
                        messagebox.showinfo(message = "You haven´t permission!", title = "Info")
                    except UnicodeDecodeError:
                        messagebox.showinfo(message = "Failed file decoding!", title = "Info")
                else:
                    pass
        else:
            self.file_name = filedialog.askopenfilename(filetypes = (("Text files", "*.es"), ("All files", "*.*")))
            if self.file_name:
                try:
                    with open(self.file_name, mode="r") as fin:
                        self.text = fin.read()
                        self.notepad.delete(1.0, tkinter.END)
                        self.notepad.insert(1.0, self.text)
                        self.notepad.edit_reset()
                        self.text_old = copy.deepcopy(self.text)
                except FileExistsError:
                    pass
                except PermissionError:
                    messagebox.showinfo(message = "You haven´t permission!", title = "Info")
                except UnicodeDecodeError:
                    messagebox.showinfo(message = "Failed file decoding!", title = "Info")
            else:
                pass
		
		# I havent got idea about live

    def saveFile(self):
        if self.file_name != "":
            self.text_old = copy.deepcopy(self.text) 
            self.text = self.notepad.get(1.0, "end-1c")
            try:
                with open(self.file_name, mode="w") as fout:
                    fout.write(self.text)
            except FileExistsError:
                pass
            except PermissionError:
                messagebox.showinfo(message = "You haven´t permission!", title = "Info")
        else:
            self.saveFileAs()
    
    def saveFileAs(self):
        self.file_name = filedialog.asksaveasfilename()
        if self.file_name:
            self.text_old = copy.deepcopy(self.text)
            self.text = self.notepad.get(1.0, "end-1c")
            try:
                with open(self.file_name, mode="w") as fout:
                    fout.write(self.text)
            except FileExistsError:
                pass
            except PermissionError:
                reply = messagebox.info(message = "You haven´t permission!", title = "Info")
        else:
            pass

    def quitApp(self):
        self.text = self.notepad.get(1.0, "end-1c")
        if (self.file_name != "" and self.text == "") or (self.text != self.text_old): #or self.text != "": maybe it´s wrong
            answer = self.askSave()
            if answer is None:
                pass
            elif answer:
                self.saveFileAs()
            else:
                self.parent.destroy()
        else:
            self.parent.destroy()
            
    def undoEvent(self):
        try:
            self.notepad.edit_undo()
        except tkinter.TclError:
            pass

    def redoEvent(self):
        try:
            self.notepad.edit_redo()
        except tkinter.TclError:
            pass        

    def selectAll(self):
        self.notepad.tag_add(tkinter.SEL, "1.0", "end-1c")
        self.notepad.mark_set(tkinter.INSERT, "end-1c")
        self.notepad.see(tkinter.INSERT)

    def wrapSwitch(self):
        if self.wrap_on:
            self.wrap_on = False
            self.notepad["wrap"] = tkinter.NONE
        else:
            self.wrap_on = True
            self.notepad["wrap"] = tkinter.CHAR

    def chooseBackground(self):
        result = colorchooser.askcolor()
        if result[1] is None:
            pass
        else:
            self.color_background = result[1]
            self.notepad["bg"] = self.color_background
            self.notepad["insertbackground"] = self.invertColor(self.color_background)

    def chooseForeground(self):
        result = colorchooser.askcolor()
        if result[1] is None:
            pass
        else:
            self.color_foreground = result[1]
            self.notepad["fg"] = self.color_foreground

    def chooseHighlightB(self):
        result = colorchooser.askcolor()
        if result[1] is None:
            pass
        else:
            self.color_foreground = result[1]
            self.notepad["selectbackground"] = result[1]

    def chooseHighlightF(self):
        result = colorchooser.askcolor()
        if result[1] is None:
            pass
        else:
            self.color_foreground = result[1]
            self.notepad["selectforeground"] = result[1]

    
#Piča jestli to nebude fungovat jebnu sa... 
root = tkinter.Tk()
app = MainWindow(parent = root)
app.mainloop()
