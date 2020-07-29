from threading import Thread, Lock
from datetime import date
import time
import re

import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor, Chooser
from tkinter.messagebox import askokcancel, askyesno
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames, asksaveasfilename

from PIL import Image, ImageTk

TKINTER_COLOR_DEFAULT = "#f0f0f0"


class Notification(tk.Toplevel):
    def __init__(self, master, frameref=None, width=30, padx=5, pady=5, font=None):
        super(Notification, self).__init__(master)
        self.master = master
        self.frameref = frameref if frameref != None else master
        self.width = width
        self.padx = padx
        self.pady = pady
        if font is None:
            self.font = ("arial", 10, 'bold')
        else:
            self.font = font

        self.master.bind("<Configure>", lambda e: self._position(e))
        self.master.bind("<B1-Motion>", lambda e: self._position(e))
        self.master.bind("<FocusIn>", lambda e: self.lift())
        self.bind("<Configure>", lambda e: self._position(e))

        self._position()

        self.overrideredirect(True)
        self.transient(master)
        
        self.wm_attributes("-alpha", 0.9)
        self.wm_attributes("-transparentcolor", TKINTER_COLOR_DEFAULT)
        
    def _position(self, event=None):
        
        _x = self.frameref.winfo_rootx() + self.frameref.winfo_width() - (self.winfo_width() + self.padx)
        _y = self.frameref.winfo_rooty() + self.pady
        self.geometry()
        self.geometry("+{}+{}".format(_x, _y))
        self.lift()
    
    def _format_message(self, message):
        my_message = ""

        if len(message) > self.width - 5:
            words = message.split()
            words[0] = "    " + words[0]
            line = 0
            for word in words:
                if len(my_message)//25 > line:
                    line += 1
                    my_message = "\n     ".join([my_message, word])
                else:
                    my_message = " ".join([my_message, word])
        else:
            my_message += "    " + message

        return my_message

    def add(self, message, t_message="INFO" or "ERROR" or "WARNING", popout=12):
        """
        Add a new notification  
            Args:
                message (str): message to add 
                t_message (str): the value must be "INFO" or "ERROR" or 
                "WARNING"
                popout (int) : Time to show out the message
        """
        frame = FrameTheme(self)
        frame.pack(fill='x', expand=True, side='top', anchor='n')
        
        

        message = ttk.Label(frame, text=self._format_message(message),
             width=self.width, font=self.font)
        if t_message == "INFO":
            message.config(foreground='white', background='green')
            button = tk.Label(frame, cursor='hand2',
                              bg='green',  bitmap='gray12')
            button.bind("<Button-1>", lambda a: frame.destroy())
        elif t_message == "ERROR":
            message.config(foreground='white', background="red")
            button = tk.Label(frame, cursor='hand2',
                              bg='red',  bitmap='gray12')
            button.bind("<Button-1>", lambda a: frame.destroy())
        elif t_message == "WARNING":
            message.config(foreground='gray', background='yellow')
            button = tk.Label(frame, cursor='hand2',
                              bg='yellow',  bitmap='gray12')
            button.bind("<Button-1>", lambda a: frame.destroy())

        message.pack(fill='both', expand=True, side="left", ipadx=15, pady=3, ipady=10)
        
        #Help text in close button. Comment line below if you dont wanna use it
        HelpTheme(button, text='Close')

        button.pack(fill='y', side='right', ipadx=15, pady=3, ipady=9)
        
        self.lift()
        frame.after(popout*1000, frame.destroy)
    
    def config(self, ibgc='green', ebgc='red', wbgc='yellow'):
        raise NotImplementedError
    
    @staticmethod
    def how_it_works():
        root = tk.Tk()
        root.geometry("400x400")
        label = tk.Label(root, text="Manual Testing for Notification Class")
        label.pack()
        commands = [
            lambda : notification.add("Info Message", "INFO", 7),
            lambda : notification.add("Warning Message", "WARNING", 7),
            lambda : notification.add("Error Message", "ERROR", 7)
        ]
        text = ['Info!', 'Warning!', 'Error!']
        for i in range(3):
            tk.Button(root, command=commands[i], text=text[i]).pack(
                side='left', anchor='s', expand=True, fill='x')

        notification = Notification(root, root)
        root.after(1500, commands[0])
        root.after(2500, commands[1])
        root.after(3500, commands[2])

        root.mainloop()


class ToplevelCentered(tk.Toplevel):
    def __init__(self, master, *args, **kw):
        super(ToplevelCentered, self).__init__(master, *args, **kw)
        self.transient(master)
        self.resizable(0, 0)

    def _set_geometry(self):
        x = (self.winfo_screenwidth() - self.winfo_width())//2
        y = (self.winfo_screenheight() - self.winfo_height())//2 - 30

        self.geometry('+{x}+{y}'.format(x=x, y=y))
    
    def set_geometry(self): self.after(100, self._set_geometry)
        

class ProgressTopMostThetodayme(tk.Toplevel):
    def __init__(self, master, text, *args, **kw):
        super(ProgressTopMostTheme, self).__init__(master, *args, **kw)
        
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", TKINTER_COLOR_DEFAULT)
        self.attributes("-disabled", True)
        
        self.overrideredirect(True)
        self.transient(master)

        self._build(text)
        self._set_geometry()
    
    def _build(self, text):
        LabelTheme(self, font=("arial", 12, "bold"), text=text,width=20,
            justify='left').pack(padx=10,pady=10, anchor='n')

        self.progress = ttk.Progressbar(self)
        self.progress['value'] = 0
        self.progress.pack(fill='x', expand=True, anchor='s')
    
    def _set_geometry(self):
        x, y = self.winfo_screenwidth()//2 , self.winfo_screenheight()//2
        x, y = x - self.winfo_width()//2, y - self.winfo_height()//2

        self.geometry(f'+{x}+{y}')

    def load(self, value):
        """
        Load Progress to given value. If value is greater than 100 
        the widget will be destroyed
        """
        time.sleep(0.5)

        for i in range(self.progress['value'], value):
            self.progress['value'] = i
            self.update_idletasks()            
            time.sleep(0.02)
                    
        if value >= 100:
            self.after(500, self.destroy)
    
    @staticmethod
    def how_it_works():
        def run(root):
            top = ProgressTopMostTheme(root, "Closing...")
            top.after(500, lambda : top.load(12))
            top.after(1000, lambda : top.load(35))
            top.after(1500, lambda : top.load(80))
            top.after(3000, lambda : top.load(100))
            top.after(3500, lambda : top.quit())

        root = tk.Tk()
        LabelTheme(root, text='Close this window to run ProgressTopMost').pack(
            padx=200, pady=200
        )
        root.protocol("WM_DELETE_WINDOW", lambda : run(root))
        root.mainloop()


class HelpTheme(tk.Toplevel):
    """
    Help text will show when mouse over widget.

    Args: 
        widget (tk.Widget)
        static (bool)

    Options:
        text (str) : Text will br showed
        color (str-hex-color)
        background (str-hex-color)
        font (tuple) like ('arial', 9, 'italic')
        padding (int)
    """
    def __init__(self, widget, static = False, *args, **kw):
        self._configs = {
            'text'       : 'This text will be showed when required',
            'color'      : 'black',
            'background' : '#ffffcc',
            'font'       : ('arial', 9, 'italic'),
            'padding'    : 5,
            'delay'      : 1500,
            'widget'     : widget
        }
        self._update_configs(kw)

        super(HelpTheme, self).__init__(widget, *args, **kw)

        self.attributes('-disabled', True)
        self.attributes("-transparentcolor", TKINTER_COLOR_DEFAULT)

        self.overrideredirect(True)
        self.withdraw()
        if static:
            self._build_static()
        else:
            self._build()
            self._configs['widget'].bind('<Enter>', self._show, True)
            self._configs['widget'].bind('<Leave>', self._hide, True)

    
    def _update_configs(self, kw):
        for key in list(kw.keys()):
            if key in self._configs.keys():
                self._configs[key] = kw.pop(key)

    def _build_static(self):
        self.deiconify()

        text = "   " + self._configs['text']

        ttk.Label(self, text=text, foreground=self._configs['color'],
            background=self._configs['background'], font=self._configs['font']).pack(
                ipadx=self._configs['padding'], ipady=self._configs['padding'],
                side='left')
                
        self.bind_all("<Button-1>", lambda e: self.destroy())
        self.after(10, self._set_geometry)
        self.after(7000, self.destroy)
    
    def _build(self):
        text = "   " + self._configs['text']
        ttk.Label(self, text=text, foreground=self._configs['color'],
            background=self._configs['background'], font=self._configs['font']).pack(
                ipadx=self._configs['padding'], ipady=self._configs['padding'],
                side='left')

    def _set_geometry(self):
        w = self._configs['widget']

        x, y = w.winfo_rootx(), w.winfo_rooty() - (self.winfo_height()+2)
        
        if x + self.winfo_width() > w.winfo_screenwidth():
            x = w.winfo_screenwidth() - self.winfo_width()
        elif x < 0:
            x = 0

        self.geometry(f'+{x}+{y}')

    def _show(self, *args):
        self._set_geometry()
        self._call = self.after(self._configs['delay'], self.deiconify)

    def _hide(self, *args):
        self.after_cancel(self._call)
        self.withdraw()
    
    def destroy(self):
        super().destroy()
        
    @staticmethod
    def how_it_works():
        root = tk.Tk()
        ttk.Label(root, text="Mouse over the field below and see the help...").pack(
            padx=200, pady=20
        )
        entry = ttk.Entry(root)
        HelpTheme(entry)
        entry.pack(ipadx=100, pady=100)
        root.mainloop()


class MenuTheme(tk.Menu):
    def __init__(self, master, labes, commands, separator=[3,]):
        menu = ttk.Menubutton(master)
        super(MenuTheme, self).__init__(menu,  tearoff=0)
        for i in range(len(labes)):
            if i in separator:
                self.add_separator()
            self._add_command(self._format_name(labes[i]),
                              commands[i]
                              )

    def _add_command(self, label, command):

        self.add_command(label=label,command=command, compound="left")

    def _format_name(self, name):
        """
        Format the name for len
        """
        name += " "*(30 - len(name))
        name = "     " + name
        return name


class EntryTheme(ttk.Entry):
    """
    A custom ttk.Entry widget with pre implemented actions like upper, placeholder 
    and validate option

    Args:
        master (tk.Widget) A master widget;

    Options:
        type : 'text', 'password', 'email', 'number';
        font : a tuple ('name', size, 'format') or tkinter font object see tkinter fonts documentation
        upper : bool that define how to show caracteres
        placeholder : Text in back
        pattern : A regex for validate the entry
        mask : Mask to write in entry. Use '9' for numerical ,'a' for alpha,
        '*' for alphanumerical. Exemplo : 99/99/9999. 
        callback : A function to run and format entry content
    """
    def __init__(self, master,  *args, **kw):
        self._configs = {
            'type'        : 'text',
            'font'        : ("arial", 10, "normal"),
            'upper'       : False,
            'placeholder' : None,
            'pattern'     : None,
            'mask'        : None,
            'callback'    : None
        }
        self._configs_update(kw)

        vcmd = (master.register(self._on_validate), '%d', '%i', '%P', '%s', '%S')
        
        #Constructor of super class
        super(EntryTheme, self).__init__(
            master, font=self._configs['font'], validate="key",
            validatecommand=vcmd,
            *args, **kw)
        
        if self._configs['placeholder'] is not None:
            self.bind("<FocusIn>", self._foc_in)
            self.bind("<KeyPress>", self._foc_in)
            self.bind("<FocusOut>", self._foc_out)
            self._put_placeholder()
        
        if self._configs['pattern'] is not None:
            self._by_char = False
            self.bind("<FocusOut>", self._validate_pattern)
        
        if self._configs['type'] == 'password':
            self.config(show="●")
        
        self.bind("<KeyRelease>", self._all_upper)

    def _configs_update(self, kw):
        #attributes
        self._index = 0
        self._indexes = {}
        self._caracteres = set()
        self._should_validate = True
        self._has_placeholder = False

        #Configs update
        for key in list(kw.keys()):
            if key in self._configs.keys():
                if key is 'type' and kw[key] not in ['text', 'password', 
                    'email', 'number', 'currency']:
                    #currency not implemented
                    raise(AttributeError('type -{} not valid'.format(kw[key])))
                self._configs[key] = kw.pop(key)
        
        #Autoconfigs
        if self._configs['type'] is 'password':
            self._configs['upper'] = False
        elif self._configs['type'] is 'email' and self._configs['pattern'] is None:
            self._configs['pattern'] = r'^(|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]*)$'
        elif self._configs['type'] is 'number':
            self._configs['upper'] = False
        elif self._configs['type'] is 'currency' and self._configs['mask'] is None:
            self._configs['mask'] = '$ '
            self._configs['upper'] = False
        elif self._configs['type'] is 'currency':
            self._configs['upper'] = False

        if self._configs['mask'] is not None:
            self._list_index()
        
    def _list_index(self):
        for i in range(0, len(self._configs['mask'])):
            temp = {}
            if self._configs['mask'][i] == '9':
                temp.update(input=True, pattern= r'[0-9]', caractere = None)
                self._indexes[i] = temp
            elif self._configs['mask'][i] == 'a':
                temp.update(input=True, pattern= r'[a-z,A-Z]', caractere = None)
                self._indexes[i] = temp
            elif self._configs['mask'][i] == '*':
                temp.update(input=True, pattern= r'[a-z,A-Z,0-9]', caractere = None)
                self._indexes[i] = temp  
            else:
                temp.update(input=False, pattern= None, caractere = self._configs['mask'][i])
                self._indexes[i] = temp
                self._caracteres.add(self._configs['mask'][i])

    def _on_validate(self, d, i, P, s, S, *args):
        #%d = Type of command (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if an4
        
        #If there is a callback
        if self._configs['callback'] != None:
            self.after(500, lambda: self._configs['callback'](self))

        #If not should be validate
        if not self._should_validate:
            self._should_validate = True
            return True

        # If insert
        if d == '1' or d == 1:
            if self._configs['type'] is 'number' and not S.isnumeric():
                self.bell()
                return False

            if self._configs['mask'] is not None and not self._has_placeholder:
                if len(P) > len(self._configs['mask']): 
                    self.bell()
                    return False
                self._mask(int(i), S)
                return False
            
            #When there is a placeholder to remove and text to be inserted
            if s == self._configs['placeholder']:
                self._remove_placeholder()
                self.after(100, lambda : self.insert(0, S))

        # If delete
        elif d == '0' or d == 0:
            if (P == '' and self._configs['placeholder'] != None) or \
                s == self._configs['placeholder']:
                self._put_placeholder()
            
            if self._configs['mask'] is not None and self._index > 0:
                self._index = int(i)

        # If not delete and insert
        else:
            self.bell()
            return False

        self._should_validate = True
        return True

    def _all_upper(self, *args):
        if self._configs['upper']:
            self.update_idletasks()
            position = self.index(tk.INSERT)
            text = self.get().upper()
            self.delete(0, 'end')
            self.insert('end', text)
            self.icursor(position)

    def _mask(self, index, text=None):
        if len(text) > 1:
            index = self._index
            for c in self._caracteres:
                text = text.replace(c, '')
            for i in range(self._index,  index + len(text)):
                self._mask(self._index, text[i - index])

        else:
            if not self._indexes[self._index]['input']:
                while (not self._indexes[self._index]['input'] and
                    len(self.get()) <= len(self._configs['mask'])):
                    self.insert(self._index, self._indexes[self._index]['caractere'])
                    self._index += 1
                
            if re.match(self._indexes[self._index]['pattern'], text) is not None:
                self.insert(self._index, text)
            else:
                self.bell()
                return
        
            self._index += 1

    def _put_placeholder(self, *args):
        self._has_placeholder = True
        self.delete('0', 'end')
        self.insert(0, self._configs['placeholder'], False)
        self.config(foreground='gray', show="")
        self.icursor(0)

    def _remove_placeholder(self, *args):
        self._has_placeholder = False
        self.delete('0', 'end', False)
        self.config(foreground='')
        if self._configs['type'] == 'password':
            self.config(show="●")

    def _foc_in(self, *args):
        """Run when widget take focus"""
        if self.get() == self._configs['placeholder']:
            self.select_clear()
            self.icursor(0)

    def _foc_out(self, *args):
        if self.get() == '' and self._configs['placeholder'] != None:
            self._put_placeholder()

    def _validate_pattern(self, *args):
        if self._configs['pattern'] is not None:
            if re.match(self._configs['pattern'], self.get()) is None:
                self.config(foreground='red')
                if not self._by_char and self.get() is not '':
                    self._by_char = True
                    self.bind("<KeyRelease>", self._validate_pattern)
            else:
                self.config(foreground='')

    def insert(self, index, text, validate=True):
        "Insert text at index validating when required"
        self._should_validate = validate
        if text is not None: super().insert(index, text)
        
    def delete(self, first, last=None, validate=True):
        self._should_validate = validate
        super().delete(first, last)
    
    def configs_update(self, **kw): self._configs_update(kw)

    def active(self): self.configure(state= tk.NORMAL, cursor= 'xterm')
    def disable(self): self.configure(state= tk.DISABLED, cursor= 'arrow')
    def get_value(self): return self.get() if not self._has_placeholder else ''
    def set_value(self, value): self.delete(0, 'end'); self.insert('0', value)
    def get_config(self, config): return self._configs[config]

    @staticmethod
    def how_it_works():
        root = tk.Tk()
        entry = EntryTheme(root, mask='+ 99 (99) 99999-9999')
        entry.pack(padx=100, pady=100)
        entry.after(2000, lambda : entry.insert(0, '5531996469999'))
        entry.after(4000, lambda : entry.delete(0, 'end', True))
        entry.after(6000, lambda : entry.insert(0, '+ 55 (31) 99646-9999'))

        root.mainloop()


class RadiobuttonTheme(ttk.LabelFrame):
    """
    A field with Radio Buttons

    Args:
        master
        itens (dict) keys will be valeu and value will be text in radio button
        selected (value) value to selecet standard
        callback (function) a function will be call when some radiobutton was clicked
        geometry (tupla) geometry coords (num rows, num colms).
    
    Keys of Frame:
        ['borderwidth', 'padding', 'relief', 'width',
        'height', 'takefocus', 'cursor', 'style', 'class']
    """
    def __init__(self, master, items, selected=None, callback=None, 
            geometry=None, *args, **kw):
        super(RadiobuttonTheme, self).__init__(master, labelanchor='se', *args, **kw)
        
        self.value = tk.StringVar(self, value=selected)
        self.command = callback
        self.geometry = geometry
        self.items = []
        self._build(items)

    def _build(self, items):
        i, j = 0, 0
        for value, text in items.items():
            w = ttk.Radiobutton(self, 
                                text = text,
                                variable = self.value,
                                value = value,
                                takefocus = False,
                                cursor = "hand2",
                                command = self.command)

            self.items.append(w)
            if self.geometry is None:
                w.pack(side='left',fill='x', padx=10)
            else:
                if j >= self.geometry[1]:
                    j = 0
                    i += 1

                if i >= self.geometry[0]:
                    break
                else:
                    w.grid(arow=i, column=j, sticky='we', padx=10)
                    j += 1

    def get_value(self): return self.value.get()
    def set_value(self, value): self.value.set('' if  value is None else value)

    def active(self): 
        for item in self.items:
            item.configure(state= tk.NORMAL, cursor= 'hand2')
            
    def disable(self): 
        for item in self.items:
            item.configure(state= tk.DISABLED, cursor= 'arrow')

    @staticmethod
    def how_it_works():
        root = tk.Tk()
        widget = RadiobuttonTheme(root, 
                items = {1:"Option1", 2:"Option2", 3:"Option3"},
                selected=1,
                callback=lambda : print(widget.get_value()))
        widget.set_value(None)
        widget.disable()
        widget.pack(padx=50, pady=50)
        ButtonTheme(root, "active", command=widget.active).pack()
        ButtonTheme(root, "deactive", command=widget.disable).pack()
        root.mainloop()


class OptionMenuTheme(ttk.OptionMenu):
    """
    
    """
    def __init__(self, master, items, callback=None, *args, **kw):
        self._configs = {
            'font' : ("arial", 10, "normal"),
            'width' : 20,
            'upper' : False,
            'default' : None
        }
        for config in list(kw.keys()):
            if config in self._configs:
                self._configs[config] = kw.pop(config)

        self.value = tk.StringVar(master)

        self._populate(items)
            
        super(OptionMenuTheme, self).__init__(
                master,
                self.value,
                self._configs['default'],
                *self.to_show,
                **kw)

        self.command = callback
        
        ttk.Style(self).configure("MyTheme.TMenubutton", 
                font=self._configs['font'])
        self.configure(style="MyTheme.TMenubutton", cursor='hand2', 
                width=self._configs['width'])
        if self.command is not None:
            self.value.trace_variable('w', self._call)

    def _call(self, *args):
        if self.value.get == '':
            return
        self.command()

    def _populate(self, items):
        if isinstance(items, dict):
            if self._configs['upper']:
                for key in items.keys():
                    items[key] = items[key].upper()

            self.original_keys = items
            self.items = {value: key for key, value in items.items()}
            self.to_show = list(self.items.keys())

        elif isinstance(items, list):
            if self._configs['upper']:
                for i in range(len(items)):
                    items[i] = items[i].upper()

            self.items = items
            self.to_show = items
            
        else:
            self.items = []
            self.to_show = []
            
            
    def populate(self, items):
        '''Reset the values in the Option Menu
        '''
        
        self._populate(items)
        
        menu = self["menu"]
        menu.delete(0, "end")
        
        for item in self.to_show:
            menu.add_command(label=item, 
                             command=lambda value=item: self.set_value(value))
        
        
        if self._configs['default'] is not None:
            self.set_value(self._options['default'])
        else:
            self.set_value('')
            
    def get_value(self): 
        if isinstance(self.items, dict):
            if self.value.get() == '':
                return ''
            return self.items[self.value.get()]

        elif isinstance(self.items, list):
            return self.value.get()

    def set_value(self, value):
        if value is None:
            self.value.set('')
            return
            
        if isinstance(self.items, dict):
            if value not in self.items.values() and value is not '':
                raise(ValueError(f'value -{value} is not valid!'))
            self.value.set(self.original_keys[value])

        elif isinstance(self.items, list):
            if value not in self.items and value is not '':
                raise(ValueError(f'value -{value} is not valid!'))
            self.value.set(value)

    def active(self): self.configure(state= tk.NORMAL, cursor= 'hand2')
    def disable(self): self.configure(state= tk.DISABLED, cursor= 'arrow')

    @staticmethod
    def how_it_works():
        def fun():
            print("OP1 - When 'items' is a Dict get_value return: ", widget.get_value(),
                  "\nOP2 - When 'items' is a List get_value return: ", widget2.get_value(), "\n")
        
        def repo():
            nonlocal start
            widget2.populate([f'{i:03}' for i in range(start, start + 10)])
            start += 10
            
        start = 1
        root = tk.Tk()
        items = {'1':'one', '2':'two', '3':'three'}
        items2 = ['four', 'five', 'six']

        LabelTheme(root, text=f"Variable items is a Dict:\nitens={items}").pack()
        
        widget = OptionMenuTheme(root,items)
        widget.pack()

        LabelTheme(root, text=f"Variable items is a List:\nitens={items2}").pack()
        widget2 = OptionMenuTheme(root, items2)
        widget2.pack()

        LabelTheme(root, text="Running OptionMenuTheme.populate in 10 seconds.").pack()
        
        ButtonTheme(root, "repopulate", command=repo).pack()
        ButtonTheme(root, "submit", command=fun).pack()
        
        root.mainloop()


class CheckButtonTheme(ttk.Checkbutton):
    def __init__(self, master, text, callback=None, *args, **kw):
        if 'textvariable' in kw:
            raise(AttributeError('option -textvariable is not valid for this widget!\
                    please use value attribute insted!'))
        
        self.value = tk.BooleanVar(master)
        self._command = callback
        self.value.trace_variable('w', self._callback)
        
        super(CheckButtonTheme, self).__init__(master, 
                                               variable = self.value,
                                               text = text,
                                               takefocus = False,
                                               *args, **kw)
        self.active()

    def _callback(self, *args):
        if self._command is not None:
            self._command(self)
    
    def set_style(self, bg, fg, name='CBT'):
        """
        Method for configure a basic Style
        """
        style=StyleTheme(self)
        style.configure(f"{name}.TCheckbutton", background = bg, foreground = fg)
        self.configure(style = f"{name}.TCheckbutton")

    def active(self): self.configure(state= tk.NORMAL, cursor= 'hand2')
    def disable(self): self.configure(state= tk.DISABLED, cursor= 'arrow')
    def get_value(self): return self.value.get()
    def set_value(self, value): self.value.set(False if value is None else value)


class PickerTheme(ttk.Frame):
    """
    A picker field.

    Args:
        master (tk.Widget)
        picker (str) 'file', 'files', 'directory', 'save_as' or 'color'

    options:
        title (str)', 
        initialdir (str) a path name, 
        filetypes (list) list of tupla [('All', '*'),('Python','*.py')] 
    """
    def __init__(self, master, picker, *args, **kw):
        self._update_configs(kw)

        super(PickerTheme, self).__init__(master, *args, **kw)

        if picker == 'file': self._command = self._button_file
        elif picker == 'files': self._command = self._button_files
        elif picker == 'directory': self._command = self._button_directory
        elif picker == 'save_as': self._command = self._button_save_as
        elif picker == 'color': self._command = self._button_color
        else: 
            raise(AttributeError("picker must be 'file', 'files', 'directory', 'save_as' or 'color'"))
        
        self._build()
    
    def _update_configs(self, kw):
        self._configs = {
            'title' : None,
            'initialdir' : None,
            'filetypes' : []
        }
        for config in list(kw.keys()):
            if config in self._configs:
                self._configs[config] = kw.pop(config)

    def _build(self):
        vcmd = (self.register(self._on_keypress), '%d')
        
        self.value = tk.StringVar(self)

        self.entry = ttk.Entry(master = self,
                               textvariable = self.value,
                               validate="key",
                               validatecommand=vcmd
                               )
        self.entry.pack(fill='x', expand=True, ipady=0, side='left')
        self.entry.bind('<Double-1>', self._command)

        self.button = ttk.Button(master = self, text = '...', 
                   command = self._command,
                   width = 3,
                   takefocus = False
                   )
        self.button.pack(side='left')

    def _button_color(self, *args):
        color = self.value.get()

        value = askcolor(color if color != '' else '#00ff00',
                         title = self._configs['title']
                         )
        if value[1] is not None:
            self.entry.config(foreground=value[1])
            self.value.set(value[1])
            self.entry.icursor(0)
            self.focus_displayof()
    
    def _button_file(self, *args):
        value = askopenfilename(initialdir = self._configs['initialdir'],
                                title = self._configs['title'],
                                filetypes = self._configs['filetypes']
                                )

        if value != '' and value is not None:
            self.value.set(value)
    
    def _button_save_as(self, *args):
        value = asksaveasfilename(initialdir = self._configs['initialdir'],
                                  title = self._configs['title'],
                                  filetypes = self._configs['filetypes']
                                  )

        if value != '' and value is not None:
            self.value.set(value)
    
    def _button_files(self, *args):
        value = ''
        values = askopenfilenames(initialdir = self._configs['initialdir'],
                                title = self._configs['title'],
                                filetypes = self._configs['filetypes']
                                )
        
        for item in values:
            value += f"{item};"

        if value != '':
            self.value.set(value)

    def _button_directory(self, *args):
        value = askdirectory(initialdir = self._configs['initialdir'],
                             title = self._configs['title']
                             )

        if value != '' and value is not None:
            self.value.set(value)

    def _on_keypress(self, *args): return False

    def get_value(self): return self.value.get()
    def set_value(self, value): self.value.set('' if value is None else value)
    def active(self): 
        self.button.configure(state= tk.NORMAL, cursor= 'hand2')
        self.entry.configure(state= tk.NORMAL, cursor= 'xterm')
        self.entry.bind('<Double-1>', self._command)

    def disable(self): 
        self.button.configure(state= tk.DISABLED, cursor= 'arrow')
        self.entry.configure(state= tk.DISABLED, cursor= 'arrow')
        self.entry.unbind('<Double-1>')

    def change_state(self):
        if str(self.entry['state']) == 'normal':
            self.after(100, self.disable)
        elif str(self.entry['state']) == 'disabled':
            self.after(100, self.active)
        else:
            self.after(100, self.disable)

    @staticmethod
    def how_it_works():
        root = tk.Tk()
        
        LabelTheme(root, text='Color: ').pack()
        picker = PickerTheme(root, 'color')
        picker.set_value(None)
        picker.pack(side='top')

        LabelTheme(root, text='Color with title: ').pack()
        picker = PickerTheme(root, 'color', title = 'This is Choose a color')
        picker.pack(side='top')

        LabelTheme(root, text='File: ').pack()
        picker = PickerTheme(root, 'file')
        picker.pack(side='top')
        
        LabelTheme(root, text='File with title: ').pack()
        picker = PickerTheme(root, 'file', title = 'Title is Choose a file', 
                initialdir = '/')
        picker.pack(side='top')
        
        LabelTheme(root, text='Files: ').pack()
        picker = PickerTheme(root, 'files', filetypes=[('Python', '*.py'), ('All', '*')],
                initialdir = '')
        picker.pack(side='top')
        
        LabelTheme(root, text='Directory: ').pack()
        picker = PickerTheme(root, 'directory')
        picker.pack(side='top')

        LabelTheme(root, text='Save as with filetypes: ').pack()
        picker = PickerTheme(root, 'save_as', filetypes=[('Python', '*.py'), ('All', '*')])
        picker.pack(side='top')

        root.mainloop()


class SimpleCalendar(ttk.Entry):
    """Simple calendar

    Args:
        master

    Options:
        'name_buttons' (list) default is ['Ok', 'Cancel']
        'name_head' (list) default is ['Day', 'Month', 'Year']
        'font' (tuple) default is ("arial", 10, "normal") see tkinter fonts
        'format' (str) Use 'yyyy' for year, 'mm' for month and 'dd' for day. Default is 'yyyy-mm-dd'
        'first_year' (int) defaul is 1970
    """
    def __init__(self, master, *args, **kw):
        self._optns = {
            'name_buttons' : ['Ok', 'Cancel'],
            'name_head' : ['Day', 'Month', 'Year'],
            'font' : ("arial", 10, "normal"),
            'format' : 'yyyy-mm-dd',
            'first_year' :  1970
        }
        for key in self._optns.keys():
            if key in kw.keys():
                self._optns[key] = kw.pop(key)

        self.value = tk.StringVar()

        vcmd = (master.register(self._on_keypress), '%d')

        super(SimpleCalendar, self).__init__(master, font=self._optns['font'], 
                textvariable=self.value,
                validatecommand=vcmd,
                validate="key",
                *args, **kw)
        
        self._date = date.today()
        self._calendar = None
        self._calendar_monted = False

        self.bind("<Button>", lambda e: self._build(e))
        self.bind_all("<Configure>", lambda e: self._position(e))
        
    def _on_keypress(self, *args): self.icursor(0); return False

    def _position(self, e=None):
        if self._calendar_monted:
            try:
                self._calendar.geometry("+{}+{}".format(
                    self.winfo_rootx(), 
                    self.winfo_rooty() + self.winfo_height()
                    )
                )
            except:
                pass
    
    def _close_or_not(self, e):
        if not self._calendar_monted:
            return
        else:
            x1 = self._calendar.winfo_rootx()
            y1 = self._calendar.winfo_rooty()
            x2 = x1 + self._calendar.winfo_width()
            y2 = y1 + self._calendar.winfo_height()
            if not ((e.x_root > x1) and (e.x_root < x2) \
                    and (e.y_root > y1) and (e.y_root < y2)):
                self._calendar.destroy()
                self._calendar.unbind_all("<Button>")
                self._calendar_monted = False

        self.icursor(0)
        self.focus_displayof()
            
    def _build(self, e):
        if str(self['state']) == tk.DISABLED:
            return

        if self._calendar_monted:
            self.icursor(0)
            self._calendar.lift()
            return

        self._calendar = tk.Toplevel(self)
        
        self._calendar.overrideredirect(True)
        self._calendar.bind_all("<Button>", lambda e: self._close_or_not(e))
                
        frame_with_border = FrameTheme(self._calendar, relief=tk.RIDGE, borderwidth=2)
        frame_with_border.pack()

        frame_with_border.bind("<Configure>", lambda e: self._position(e))

        frame_top = FrameTheme(frame_with_border)
        frame_top.pack(side='top', fill='x')
        frame_bottom = FrameTheme(frame_with_border)
        frame_bottom.pack(side='bottom', fill='x')

        for i in range(len(self._optns['name_head'])):
            LabelTheme(frame_top, text=self._optns['name_head'][i]).grid(row=0, column=i)

        self.day = tk.Listbox(frame_top, selectmode=tk.SINGLE, 
            exportselection=0, width=15, takefocus=False, 
            selectborderwidth=0, bd=0, relief=tk.FLAT)
        self.month = tk.Listbox(frame_top, selectmode=tk.SINGLE, 
            exportselection=0, width=15, takefocus=False, 
            selectborderwidth=0, bd=0, relief=tk.FLAT)
        self.year = tk.Listbox(frame_top, selectmode=tk.SINGLE, 
            exportselection=0, width=15, takefocus=False, 
            selectborderwidth=0, bd=0, relief=tk.FLAT)

        self.day.grid(row=1, column=0)
        self.month.grid(row=1, column=1)
        self.year.grid(row=1, column=2)

        for i in range(31):
            self.day.insert(i+1, i+1)
        
        for i in range(12):
            self.month.insert(i+1, i+1)

        for i in range(self._optns['first_year'] - 1, date.today().year + 20):
            self.year.insert(i+1, i+1)
        
        self.year.see(date.today().year - self._optns['first_year'])
        
        if self.get() == '':
            self.set_today()
        
        to_activate = [
            self._date.day - 1, 
            self._date.month - 1,
            self._date.year - self._optns['first_year']
        ]
      
        self.day.see(to_activate[0] - 3)
        self.month.see(to_activate[1] - 3)
        self.year.see(to_activate[2] - 3)

        self.day.select_set(to_activate[0])
        self.month.select_set(to_activate[1])
        self.year.select_set(to_activate[2])
        
        self.day.activate(to_activate[0])
        self.month.activate(to_activate[1])
        self.year.activate(to_activate[2])
            
        def confirm():
            date = "{:04}-{:02}-{:02}".format(
                    self.year.get(tk.ACTIVE),
                    self.month.get(tk.ACTIVE),
                    self.day.get(tk.ACTIVE)
                    )
            self.set_value(date)
            self._calendar.unbind_all("<Button>")
            self.focus_displayof()
            self._calendar.destroy()
            self._calendar_monted = False

        def cancel():
            self._calendar.unbind_all("<Button>")
            self._calendar_monted = False
            self.focus_displayof()
            self._calendar.destroy()

        self.button_ok = ttk.Button(frame_bottom, text=self._optns['name_buttons'][0], command=confirm, takefocus=False)
        self.button_cancel = ttk.Button(frame_bottom, text=self._optns['name_buttons'][1], command=cancel, takefocus=False)
        
        self.button_ok.pack(expand=True, fill='x',side='left')
        self.button_cancel.pack(expand=True, fill='x',side='left')

        self._calendar_monted = True
        self._position()
        self.after(100, lambda : self.icursor(0))
        self.active()

    def active(self): self.configure(state= tk.NORMAL, cursor= 'hand2')
    def disable(self): self.configure(state= tk.DISABLED, cursor= 'arrow')
    
    def get(self): 
        "Value in Entry Widget" 
        return self.value.get()
    
    def get_value(self): 
        "Iso date value" 
        return self._date.isoformat()
    
    def get_date(self): 
        "The datetime.date object"
        return date(self._date.year, self._date.month, self._date.day)
    
    def set_value(self, value = None, format_show = None):
        """Set a date value to be showed

        Arguments:
            value (datetime.date, str or dict) -- A date object, dict or a str date 
                formatted according to ISO.
                
                if date object it will be set like format. Default format is ISO 8601 - Date '2012-02-28'.
                if dict it will need have the follow keys: 'day', 'month' and 'year'
                if str date it will be need like ISO 8601 - Date '2012-02-28'
                
            format_show (str) -- Use 'dd' for day 'mm' for month and 'yyyy' for year. (default: None)
        """
                    
        if isinstance(value, date):
            self._date = value
        
        elif isinstance(value, dict):
            self._date = date(value['year'], value['month'], value['day'])
                           
        elif isinstance(value, str):
            if re.match(r'^([0-9]{2}|[0-9]{1})\/([0-9]{2}|[0-9]{1})\/[0-9]{4}$', value) is not None:
                # Exception not documented date input like "yyyy/mm/dd"
                value = value.split('/')
                self._date = date(int(value[2]), int(value[1]), int(value[0]))
                
            elif re.match(r'^[0-9]{4}\-([0-9]{2}|[0-9]{1})\-([0-9]{2}|[0-9]{1})$', value) is not None:
                # ISO Date
                self._date = date.fromisoformat(value)
                
            else:
                #Not Aceptec format
                raise(ValueError('value str not match iso date "yyyy-mm-dd"'))

        elif value is None:
            self._date = date.today()
            
        else:
            raise(ValueError(f"value {type(value)} is not valid!"))
       
        
        if format_show is not None: self._optns['format'] = format_show
        
        to_show = str(self._optns['format'])
        to_show = to_show.replace('dd', f"{self._date.day:02}")
        to_show = to_show.replace('mm', f"{self._date.month:02}")
        to_show = to_show.replace('yyyy', f"{self._date.year:04}")
        self.value.set(to_show)

    def set_today(self): self.set_value()

    @staticmethod
    def how_it_works():
        root = tk.Tk()
        calendar = SimpleCalendar(root, format='mm / yyyy')
        calendar.pack(padx=100, pady=100)
        
        root.after(1*2000, lambda : calendar.set_value('03/01/2019'))
        root.after(2*2000, lambda : calendar.set_value('2016-02-22'))
        root.after(3*2000, lambda : calendar.set_value(date(1995, 7, 5)))
        root.after(4*2000, lambda : calendar.set_value())
        
        root.mainloop()


class StyleTheme(ttk.Style):
    def __init__(self, master):
        super(StyleTheme, self).__init__(master)
    
    @staticmethod
    def how_it_works():
        root = tk.Tk()
        StyleTheme(root)

        root.mainloop()


class LabelTheme(ttk.Label):
    """
    Clase para Manipulação Mais Simplificada da Classe LabelTheme

    Chaves do Widget:
        ['background', 'foreground', 'font', 'borderwidth',
        'relief', 'anchor', 'justify', 'wraplength', 'takefocus',
        'text', 'textvariable', 'underline', 'width', 'image',
        'compound', 'padding', 'state', 'cursor', 'style', 'class']
    """

    def __init__(self, master, *args, **kw):
        """
        Constructor of Class
        """
        super(LabelTheme, self).__init__(master, *args, **kw)

    def set_font(self, font=('Arial', 10, 'normal')):
        self.configure(font=font)

    def set_image(self, image, size=(70, 70)):
        """
        Method for add a image a Label
        """
        image = Image.open(image).convert("RGBA")
        image.thumbnail(size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self.configure(image=self.image)

    def set_style(self, bg, fg):
        """
        Method for configure a basic Style
        """
        style = StyleTheme(self)
        style.configure("LabelTheme.TLabel", background=bg, foreground=fg)

        self.configure(style="LabelTheme.TLabel")


class FrameTheme(ttk.Frame):
    """
    A ttk.Frame more easy to use in this code

    Keys of Frame:
        ['borderwidth', 'padding', 'relief', 'width',
        'height', 'takefocus', 'cursor', 'style', 'class']
    """

    def __init__(self, master, *args, **kw):
        """"
        Construcctor of Class
        """
        super(FrameTheme, self).__init__(master, *args, **kw)
        #self.set_style(COLORS['bg'])

    def set_style(self, bg):
        """
        Method for configure a basic Style
        """
        style = StyleTheme(self)
        style.configure("FrameTheme.TFrame", background=bg)
        self.configure(style="FrameTheme.TFrame")
    
    def is_inside(self):
        """Return True if pointer is inside Frame
        """
        p_x, p_y = self.winfo_pointerxy()
        x, y, w, h= self.winfo_rootx(), self.winfo_rooty(), \
                self.winfo_width(), self.winfo_height()
        
        if p_x > x and p_x < x + w and p_y > y and p_y < y + h and self.winfo_viewable():
            return True
        else:
            return False


class LabelFrameTheme(ttk.Labelframe):
    """
    A LabelThemeFrame more easy to use and learn

    LabelFrame's keys:
        ['labelanchor', 'text', 'underline', 'labelwidget',
        'borderwidth', 'padding', 'relief', 'width', 'height',
        'takefocus', 'cursor', 'style', 'class']
    """

    def __init__(self, master, *args, **kw):
        super(LabelFrameTheme, self).__init__(master, *args, **kw)
        #self.set_style(bg='white', fg='white')

    def set_style(self, bg=None, fg=None):
        style = StyleTheme(self)
        style.configure("LabelFrameTheme.TLabelframe",
                        background=bg, foreground=fg)
        self.configure(style="FrameTheme.TFrame")
    
    def is_inside(self):
        """Return True if pointer is inside Frame
        """
        p_x, p_y = self.winfo_pointerxy()
        x, y, w, h= self.winfo_rootx(), self.winfo_rooty(), \
                self.winfo_width(), self.winfo_height()
        
        if p_x > x and p_x < x + w and p_y > y and p_y < y + h and self.winfo_viewable():
            return True
        else:
            return False
     

class ButtonTheme(ttk.Button): 
    """
        A more easy way to manipulate Buttons in Aplication

        With this Class set a icon (size, what, format) can be did directly.
        It process image inside the class using the Pillow Class
        
        Args:
            master (tk.Widget)
            text (str) txt in button
            command (class function) This one is substitute for -command key
        
        options :
            icon (str) This one is substitute for -image key
            size (tuple) Size of image in pixels
            width (int) Width of button
    """
    def __init__(self, master, text, *args, **kw):
        self._configs = {
            'text' : text,
            'size' : (45, 45),
            'icon' : None,
            'command' : None,
            'width' : 20,
            'align' : 'left',
            'compound' : 'left'
        }

        for key in list(kw.keys()):
            if key in self._configs:
                self._configs[key] = kw.pop(key)

        self._format_name()
        self._format_icon()

        super(ButtonTheme, self).__init__(
            master, 
            text = self._configs['text'], 
            command = self._configs['command'],
            image = self.icon, 
            width = self._configs['width'],  
            compound = self._configs['compound'], 
            cursor = 'hand2',
            *args, **kw)

        self.config(takefocus=False)

    def _format_name(self):
        """
        Format the name for len
        """
        text = self._configs['text']
        if self._configs['align'] == 'left':
            text = "   " + text.ljust(self._configs['width']+20)
        elif self._configs['align'] == 'center':
            text = text
        elif self._configs['align'] == 'right':
            text = "   " + text.rjust(self._configs['width']+20)
        
        self._configs['text'] = text

    def _format_icon(self):
        if self._configs['icon'] is not None:
            image = Image.open(self._configs['icon']).convert("RGBA")
            image.thumbnail(self._configs['size'], Image.ANTIALIAS)

            self.icon = ImageTk.PhotoImage(image)
        else:
            self.icon = None

    def disable(self): self.config(state = tk.DISABLED, cursor = 'arrow')
    def active(self): self.config(state = tk.NORMAL, cursor = 'hand2')


class ScrollFrameTheme(FrameTheme):
    """
    This widget make a frame with a Scroolbar

    How it does'nt possible set a scrollbar here we create a canvas and set in canvas a frame.
    This frame is viewPort atributte. THIS SHOULD SET LIKE MASTER FOR WIDGETS IN FRAME
    
    scroll = ScrollFrameTheme(master)
    
    label = Label(scroll.viewPort, text='scroll.viewPort is the frame with scroll')
    
    """
    
    def __init__(self, master, *args, **kw):
        super(ScrollFrameTheme, self).__init__(master, *args, **kw)  # create a frame (self)

        self._canvas = tk.Canvas(self)
        
        self._vsb = ttk.Scrollbar(self, orient="vertical",
                                 command=self._canvas.yview)
        
        self.viewPort = FrameTheme(self._canvas)
        
        self._canvas.configure(yscrollcommand=self._vsb.set)
        self._canvas.configure(highlightcolor=TKINTER_COLOR_DEFAULT)

        self._canvas_frame = self._canvas.create_window(
            (0, 0), window=self.viewPort)

        # pack canvas to left of self and expand to fill
        self._canvas.pack(side='left', anchor=tk.NW, fill="both", expand=True)
        
        # bind an event whenever the size of the viewPort frame changes.
        self.viewPort.bind("<Configure>", self._resize_window)
        self._canvas.bind('<Configure>', self._resize_canvas)
        self.bind("<Map>", self._bind_scroll)
        self.bind("<Unmap>", self._unbind_scroll)

    def _bind_scroll(self, *argv):
        # with Windows OS
        self.viewPort.bind_all("<MouseWheel>", self.mouse_wheel)
        # with Linux OS
        self.viewPort.bind_all("<Button-4>", self.mouse_wheel)
        self.viewPort.bind_all("<Button-5>", self.mouse_wheel)
    
    def _unbind_scroll(self, *argv):
        # with Windows OS
        self.viewPort.unbind_all("<MouseWheel>")
        
        # with Linux OS
        self.viewPort.unbind_all("<Button-4>")
        self.viewPort.unbind_all("<Button-5>")
            
    def _resize_canvas(self, event):
        canvas_width = self._canvas.winfo_width()
        self._canvas.itemconfig(self._canvas_frame, width=canvas_width)

    def _resize_window(self, *argv):
        '''Reset the scroll region to encompass the inner frame'''
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        
        if self.winfo_height() <= self.viewPort.winfo_height():
            # pack scrollbar to right of self
            self._vsb.pack(side="right", fill="y")
            self._bind_scroll()
        else:
            self._vsb.pack_forget()
            self._unbind_scroll()
            
        # whenever the size of the frame changes, alter the scroll region respectively

    def mouse_wheel(self, event):
        if self.winfo_height() <= self.viewPort.winfo_height() and self.is_inside():
            self._canvas.yview_scroll(int(-1*(event.delta/120)), "units")


class PreLoadAplication(tk.Tk):
    
    def __init__(self, image=None, position=None, transparent_color=TKINTER_COLOR_DEFAULT):
        """Load a Top Level Frame without border and with an image

        Args:
            master (Tt): A Tk element to set focus when this widget to be destroyed
            image (str): Image file path
            position (tuple, optional): (x, y) position. Defaults to None that will center image.
            transparent_color (str, optional): A compatible tkinter color. Defaults to TKINTER_COLOR_DEFAULT. 
            Avaliable just in windows os.           
        """
        super(PreLoadAplication, self).__init__()
        # The image must be stored to Tk or it will be garbage collected.
        self._images_loaded = False
        self._photo = Image.open(image)
        self._transparent_color = transparent_color
        
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-disabled", True)
        self.wm_attributes("-transparentcolor", self._transparent_color)
        
        self.config(bg=self._transparent_color)
        
        width, height = self._photo.size
        
        if position is None:
            x = (self.winfo_screenwidth()-width)//2
            y = (self.winfo_screenheight()-height)//2
        
        else:
            x, y = position
            
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def _load_frames(self, photo):
        """Inicia loop de animação
        """
        self._frameIndex = 0
        self._frames = []
        
        try:
            while True:
                image = ImageTk.PhotoImage(photo.convert("RGBA"))
                self._frames.append(image)
                photo.seek(len(self._frames))
        except EOFError:
            pass

        self.label = tk.Label(self, image=self._frames[0], bg=self._transparent_color)
        self.label.pack()
        
        self._images_loaded = True
        self.after(self._delay, self._animate)

    def _animate(self):
        self._frameIndex += 1
        if self._frameIndex < len(self._frames):
            self.label.config(image=self._frames[self._frameIndex])
        else:
            self._frameIndex = 0
            self.after(self._delay, self.destroy)
            
        if self._frameIndex != 0:
            self.label.after(self._delay, self._animate)

    def destroy(self):
        return super().destroy()
    
    def show(self, delay=50):
        """Show

        Args:
            delay (int, optional): delay (int, optional): Time in ms to load frames. If image is not a gif time to show image.
            Defaults to 100.
            destroy (bool, optional): Decide if will be destroyed after show
        """
        self._delay = delay
        self._loaded = False
        
        if self._photo.format == 'GIF':
            if not self._images_loaded:
                self._load_frames(self._photo)
            else: 
                self._animate()
            
        else:
            self.image = ImageTk.PhotoImage(self._photo)
            label = tk.Label(self, image=self.image, bg=self._transparent_color)
            label.pack()
            self.after(delay, self.destroy)
        
        self.after(10, self.lift)
        self.mainloop()
        
        
class FormTheme(object):
    """
    self._options = {
            #'color' : '',
            #'color_title' : '',
            #'color_subtitle' : '',
            #'color_info' : '',
            #'color_button' : '',

            'font_label' : ('arial', 10, 'normal'),
            'font_entry' : ('arial', 10, 'normal'),
            'font_title' : ('arial', 36, 'bold'),
            'font_subtitle' : ('arial', 14, 'bold'),
            'font_info' : ('arial', 9, 'italic'),
            'font_button' : ('arial', 10, 'normal'),
            'font_link' : ('Arial', 9, 'bold', 'underline'),

            'upper' : True,
            
            'btn_size' : (15, 15),
            'btn_in_field' : True,
            'btn_in_line' : True,
            'btn_width' : 50,
            
            'width_label' : 15,
            'width_entry' : 15,

            'message_require' : "Fill this field!",
            'padding' : 2
        }
    """
    def __init__(self, master, *args, **kw):
        self._options = {
            #'color' : '',
            #'color_title' : '',
            #'color_subtitle' : '',
            #'color_info' : '',
            #'color_button' : '',

            'font_label' : ('arial', 10, 'normal'),
            'font_entry' : ('arial', 10, 'normal'),
            'font_title' : ('arial', 36, 'bold'),
            'font_subtitle' : ('arial', 14, 'bold'),
            'font_info' : ('arial', 9, 'italic'),
            'font_button' : ('arial', 10, 'normal'),
            'font_link' : ('Arial', 9, 'bold', 'underline'),

            'upper' : True,
            
            'btn_size' : (15, 15),
            'btn_in_field' : True,
            'btn_in_line' : True,
            'btn_width' : 20,
            'btn_padding' : 0,
            
            'width_label' : 15,
            'width_entry' : 15,

            'message_require' : "Fill this field!",
            'padding' : 2
        }
        self._update(self._options, kw)
        
        self._master = master
        self._sections = {} 
        self._elements = {}
        self._buttons = {}
        self._states = {}
        
        self._frame_form = FrameTheme(
                master = self._master,
                padding = 10,
                *args, **kw)

        self._field = False
        self._frame_field = None

    def __getitem__(self, key):
        try:
            return self._elements[key]
        except KeyError:
            raise(KeyError("Element -" + key + "not found!"))
        except Exception as e:
            raise(e)

    def _configs(self, **kw):
        pass

    def _update(self, options, kw):
        """
        Update options with keys in kw

        Args:
            options (dict):
            kw (dict):
        return:
            options, kw
        """
        for key in list(kw.keys()):
            if key in options.keys():
                options[key] = kw.pop(key)

        return options, kw

    def _append_element(self, name, required, help_text, value, widget):
        "Append element in form's elements."
        element = {
            'required' : required,
            'help_text' : help_text,
            'value' : value,
            'widget' : widget
        }

        assert name not in self._elements, f"Element -{name} already created!"
        
        if element['help_text'] is not None:
            HelpTheme(widget, text=element['help_text'])
        
        self._elements[name] = element
    
    def _append_button(self, name, widget):
        "Append button in form's buttons."

        assert name not in self._buttons, f"Button -{name} already created!"

        self._buttons[name] = widget

    def _require_value(self, name):
        "If value in name input is empty"
        message = self._options['message_require']
        if self._elements[name]['help_text'] is not None:
            message +=  "\n  " + self._elements[name]['help_text']

        HelpTheme(self._elements[name]['widget'],
                  static = True,
                  text = message,
                  background = 'cornsilk2')

    def _add_label(self, label, options, *args):
        if options['new_line']: self.add_line()

        if options['required']:
            LabelTheme(self._line, text='*', width=1, foreground='red').pack(side='left')
        else: 
            LabelTheme(self._line, text=' ', width=1).pack(side='left')
        
        if label is not None:
            LabelTheme(self._line, 
                    text = label,
                    width = self._options['width_label'],
                    font = self._options['font_label']
                    ).pack(side='left')

    def add_line(self, *args, **kw):
        """
        Add a new line to form
        Options are the same as ttk.Frame

        Return:
            A frame object (FrameTheme)
        """
        options = {
        }
        self._update(options, kw)
        
        self._line = FrameTheme(
            master = self._frame_field if self._field else self._frame_form,
            padding = self._options['padding'],
            *args, **kw
        )
        self._line.pack(fill='x', side='top')

        return self._line
    
    def add_spacer(self, plane, padding, expand=True,*args, **kw):
        """Add a spacer arround widgets.

        Args:
            plane (str): 'vertical' or 'horizontal'
            padding (int): spacer measure
        """
        if plane == 'vertical':
            self.add_line()
            widget = LabelTheme(self._line, text=' ')
            widget.pack(pady=padding, side='left', fill='y', expand = expand)
        elif plane == 'horizontal':
            widget = LabelTheme(self._line, text=' ')
            widget.pack(padx=padding, side='left', fill='x', expand = expand)
        else:
            raise(AttributeError('plane -' + plane + ' not valid!'))
        
        return widget

    def add_line_buttons(self, *args, **kw):
        """
        Add a line for buttons.

        Args:
            in_field (bool)
            
        Return:
            A FrameTheme where buttons will be pack.
        """
        options = {
            'in_field' : self._options['btn_in_field'],
        }
        self._update(options, kw)
        
        self._line_buttons = FrameTheme(
            master = self._frame_field if options['in_field'] and self._field else self._frame_form,
            padding = self._options['padding'],
            *args, **kw)
        
        self._line_buttons.pack(fill='x', side='top')

        return self._line_buttons

    def start_field(self, text, *args, **kw):
        """
        Start a Field.
        Args:
            text (str) Text to show in field
        Return
            A LabelFrameTheme 
        """
        self.add_line()
        self._field = True
        self._frame_field = LabelFrameTheme(
            master = self._line, 
            text = text, 
            padding = self._options['padding'],
            *args, **kw)
        self._frame_field.pack(fill='x', side='top')
        return self._field
    
    def close_field(self):
        self._field = False
        self._frame_field = None
        self.add_line()
        
    def add_title(self, text, *args, **kw):
        """
        Add a Label with a text.

        Args:
            text (str)
        Return:
            A LabelTheme Widget (ttk.Label)
        Options:
            ['background', 'foreground', 'font', 'borderwidth',  
            'relief', 'anchor', 'justify', 'wraplength', 'takefocus',  
            'text', 'textvariable', 'underline', 'width', 'image',  
            'compound', 'padding', 'state', 'cursor', 'style', 'class']
        """
        options = {
            'new_line' : True,
            'font' : self._options['font_title'],
            'align' : 'left'
        }
        self._update(options, kw)
        if options['new_line']: self.add_line()
        widget = LabelTheme(
            master = self._line,
            text = text, 
            font = options['font'],
            padding = self._options['padding']
            *args, **kw
        )
        widget.pack(fill='x', side='left')
        return widget

    def add_subtitle(self, text, *args, **kw):
        """
        Add a Label with a text.
        Args:
            text (str)
        Return:
            A LabelTheme Widget (ttk.Label)
        Options:
            ['background', 'foreground', 'font', 'borderwidth',  
            'relief', 'anchor', 'justify', 'wraplength', 'takefocus',  
            'text', 'textvariable', 'underline', 'width', 'image',  
            'compound', 'padding', 'state', 'cursor', 'style', 'class']
        """
        options = {
            'new_line' : True
        }

        self._update(options, kw)
        if options['new_line']: self.add_line()
        LabelTheme(self._line, text=text,
                   font=("Marsek Demi", 12, "bold")).pack(fill='x', 
                   padx=self._options['padding'])
    
    def add_info(self, text, *args, **kw):
        """
        Add a Label with a text.
        Args:
            text (str)
        Return:
            A LabelTheme Widget (ttk.Label)
        Options:
            ['background', 'foreground', 'font', 'borderwidth',  
            'relief', 'anchor', 'justify', 'wraplength', 'takefocus',  
            'text', 'textvariable', 'underline', 'width', 'image',  
            'compound', 'padding', 'state', 'cursor', 'style', 'class']
        """
        options = {
            'new_line' : True,
            'inButtonLine' : False,
            'label' : True,
            'side' : 'left',
            'font' : self._options['font_info']
        }
        
        self._update(options, kw)

        if options['new_line']: self.add_line()

        widget = LabelTheme(
            master = self._line, 
            text = text, 
            font = options['font'],
            *args, **kw
        
        )
        widget.pack(fill='x', padx=self._options['padding'])
        
    def add_image(self, image, size, *args, **kw):
        "Add a image with size (width, height) dimensions on side."
        options = {
            'new_line' : True,
            'side' : 'right'
        }
        self._update(options, kw)

        if options['new_line']: self.add_line()

        widget = LabelTheme(self._line, padding=5)
        widget.set_image(image, size)
        widget.pack(side='left', expand=True)

        return widget

    def add_entry(self, name, label=None, *args, **kw):
        """
        Add a Entry field with a label left.

        Args:
            name (str)
            label (str) text in label. If none label will not create.
        
        Options:
            add_entry: 
                'new_line', 'expand', 'required', 'help_text', 'font', 'width'

            EntryTheme:

                'type', 'upper', 'placeholder', 'pattern', 'mask', 'callback'

            ttk.Entry (availables):
                'exportselection', 'justify', 'state', 'textvariable', 
                'xscrollcommand', 'foreground', 'background', 'takefocus', 
                'cursor', 'style', 'class'
        """
        options = {
            'new_line' : True,
            'expand' : True,
            'required' : False,
            'help_text' : None,
            'value' : None,
            'font' : self._options['font_entry'],
            'width': self._options['width_entry']
            }
        self._update(options, kw)

        self._add_label(label=label, options=options)

        widget = EntryTheme(master = self._line, 
                            width = options['width'],
                            font =  options['font'],
                            *args, **kw)
        widget.pack(fill='x', expand=options['expand'], ipady=1, side='left')

        if options['value'] is not None: widget.set_value(options['value'])

        self._append_element(name = name,
                             required = options['required'],
                             help_text = options['help_text'],
                             value = options['value'],
                             widget = widget)
        
        return widget

    def add_textarea(self, name, label=None, *args, **kw):
        raise(NotImplementedError)

    def add_calendar(self, name, label=None, *args, **kw):
        options = {
            'new_line' : True,
            'expand' : True,
            'required' : False,
            'help_text' : None,
            'value' : None,
            'font' : self._options['font_entry'],
            'width': self._options['width_entry'],
            'name_buttons' : ['Ok', 'Cancel'],
            'name_head' : ['Day', 'Month', 'Year']
            }
        self._update(options, kw)

        self._add_label(label=label, options=options)

        widget = SimpleCalendar(master = self._line,
                                name_buttons = options['name_buttons'],
                                name_head = options['name_head'],
                                width = options['width'],
                                font =  options['font'],
                                *args, **kw
                                )
        widget.pack(fill='x', expand=options['expand'], ipady=1, side='left')

        if options['value'] is not None: widget.set_value(options['value'])

        self._append_element(name = name, 
                             required = options['required'],
                             help_text = options['help_text'],
                             value = options['value'],
                             widget = widget)
        
        return widget

    def add_picker(self, name, label=None, picker='color', *args, **kw):
        options = {
            'new_line' : True,
            'expand' : True,
            'required' : False,
            'help_text' : None,
            'value' : None
            }
        self._update(options, kw)

        self._add_label(label=label, options=options)

        widget = PickerTheme(master = self._line,
                        picker = picker,
                        width = self._options['width_entry'],
                        title = label,
                        *args, **kw)

        widget.pack(fill='x', expand=options['expand'], side='left')
        if options['value'] is not None: widget.set_value(options['value'])
        
        self._append_element(name = name, 
                             required = options['required'],
                             help_text = options['help_text'],
                             value = options['value'],
                             widget = widget)
        
        return widget

    def add_check(self, name, label, callback=None, *args, **kw):
        options = {
            'new_line' : True,
            'expand' : True,
            'required' : False,
            'help_text' : None,
            'font': self._options['font_label'],
            'value' : None
            }
        self._update(options, kw)

        if options['new_line']: self.add_line()

        LabelTheme(self._line, text=' ', width=1).pack(side='left')

        widget = CheckButtonTheme(master = self._line,
                                  text = label,
                                  callback = callback,
                                  *args, **kw)
        widget.pack(fill='x', expand=options['expand'], side='left')

        if options['value'] is not None: widget.set_value(options['value'])
        
        self._append_element(name = name, 
                             required = options['required'],
                             help_text = options['help_text'],
                             value = options['value'],
                             widget = widget)

        if options['value'] is not None: widget.set_value(options['value']) 

        return widget           

    def add_option(self, name, label, items=None, callback=None, *args, **kw):
        options = {
            'new_line' : True,
            'expand' : True,
            'required' : False,
            'help_text' : None,
            'value' : None,
            'upper' : self._options['upper'],
            'font' : self._options['font_entry'],
            'width': self._options['width_entry']
            }
        self._update(options, kw)

        self._add_label(label=label, options=options)

        widget = OptionMenuTheme(master = self._line,
                                 items = items,
                                 callback = callback,
                                 font = options['font'],
                                 upper = options['upper'],
                                 width = options['width'],
                                 *args, **kw)

        widget.pack(fill='x', expand=options['expand'], ipady=1, side='left')

        if options['value'] is not None: widget.set_value(options['value'])
        
        self._append_element(name = name,
                             required = options['required'],
                             help_text = options['help_text'],
                             value = options['value'],
                             widget = widget)
        
        return widget 

    def add_radio(self, name, label=None, items=None, callback=None, *args, **kw):
        options = {
            'new_line' : True,
            'expand' : True,
            'required' : False,
            'help_text' : None,
            'value' : None,
            'geometry' : None,
            'font' : self._options['font_entry'],
            'width': self._options['width_entry']
            }
        self._update(options, kw)

        self._add_label(label=label, options=options)

        widget = RadiobuttonTheme(self._line,
                                  items = items,
                                  callback = callback,
                                  geometry = options['geometry'],
                                  *args, **kw)
        widget.pack(fill='x', expand=options['expand'], side='left')

        if options['value'] is not None: widget.set_value(options['value'])
        
        self._append_element(name = name, 
                             required = options['required'],
                             help_text = options['help_text'],
                             value = options['value'],
                             widget = widget)
        
        return widget 

    def add_separator(self, *args, **kw):
        "Add a Separator in form."
        self.add_line()

        widget = ttk.Separator(self._line, orient="horizontal", *args, **kw)
        widget.pack(fill='x', expand=True, padx=self._options['padding'])
        self.add_line()


        return widget

    def add_button(self, name, text, command, *args, **kw):
        options = {
            'name': name,
            'text': text,
            'icon': None,
            'side': 'right',
            'width': self._options['btn_width'],
            'size': self._options['btn_size'],
            'padding': self._options['btn_padding']
        }
        self._update(options, kw)
        
        try: self._line_buttons
        except AttributeError: self.add_line_buttons()
        
        widget = ButtonTheme(master = self._line_buttons,
                             text = text,
                             command = command,
                             icon = options['icon'],
                             size = options['size'],
                             width = options['width'],
                             *args, **kw
                             )

        widget.pack(side=options['side'], padx=options['padding'], 
                pady=options['padding'])

        self._append_button(name, widget)

        return widget

    def add_link(self, text, command = None,  *args, **kw):
        """
        Add a Label with a link.
        Args:
            text (str)
        Return:
            A LabelTheme Widget (ttk.Label)
        Options:
            ['background', 'foreground', 'font', 'borderwidth',  
            'relief', 'anchor', 'justify', 'wraplength', 'takefocus',  
            'text', 'textvariable', 'underline', 'width', 'image',  
            'compound', 'padding', 'state', 'cursor', 'style', 'class']
        """
        options = {
            'new_line' : True,
            'font' : self._options['font_link'],
            'expand': True,
            'align' : 'left'
        }

        self._update(options, kw)

        if options['new_line']: self.add_line()

        widget = LabelTheme(master = self._line,
                            text = text,
                            font = options['font'],
                            justify = options['align'],
                            cursor='hand2'
                            )
        widget.pack(fill='x', expand=options['expand'])

        if command is not None: widget.bind("<Button-1>", lambda e: command())

        return widget

    def new_state(self, state_name, state_map):
        """
        Create a map state for form.

        args:
            state_name (str)
            #how it has to be
            state_map = {
                'elements' : {
                    'name' : 'active',
                    'email': 'disabled'
                },
                'buttons' : {
                    'submit' : 'active',
                    'reset' : 'active'
                }
            }
        """
        for item in state_map.keys():
            assert item in ['elements', 'buttons'], \
                f"-{item} is not valid! Use 'elements' or 'buttons'"
            for subitem in state_map[item].keys():
                assert subitem in self._elements.keys() \
                    or subitem in self._buttons.keys(), f"item -{subitem} is not defined!"

        self._states[state_name] = state_map
    
    def set_state(self, state_name):
        """
        Set a predefined state or one created. 
        
        predefineds are: 'all_active', 'all_disabled', 'only_buttons', 
        'only_elements'
        """
        if state_name not in ['all_active', 'all_disabled', \
                'only_buttons', 'only_elements']:
            try: elements = self._states[state_name]['elements']
            except KeyError: elements = {}
            try: buttons = self._states[state_name]['buttons']
            except KeyError: buttons = {}
            
            for name, state in elements.items():
                widget = self._elements[name]['widget']
                if state == 'active': widget.active()
                elif state == 'disabled': widget.disable()
                else: raise(AttributeError(f"state -{state} set for -{name} is wrong!"))
            
            for name, state in buttons.items():
                widget = self._buttons[name]
                if state == 'active': widget.active()
                elif state == 'disabled': widget.disable()
                else: raise(AttributeError(f"state -{state} set for button -{name} is wrong!"))
        else:
            #Disable all
            if state_name == 'all_disabled' or state_name == 'only_elements' \
                    or state_name == 'only_buttons':
                for name in self._elements.keys():
                    widget = self._elements[name]['widget']
                    widget.disable()
            
                for name in self._buttons.keys():
                    widget = self._buttons[name]
                    widget.disable()

            #Active all elements
            if state_name == 'all_active' or state_name == 'only_elements':
                for name in self._elements.keys():
                    widget = self._elements[name]['widget']
                    widget.active()

            #Active all buttons
            if state_name == 'all_active' or state_name == 'only_buttons':
                for name in self._buttons.keys():
                    widget = self._buttons[name]
                    widget.active()

        self._frame_form.focus_force()
            
    def reset(self, default_values=True):
        for name, element in self._elements.items():
            widget = element['widget']
            if default_values: widget.set_value(element['value'])
            else: widget.set_value(None)

    def get_default_values(self):
        """returns the default values ​​of the form
        
        Returns:
            dict -- default values ​​from the input items of the form
        """
        default = {}
        for name, elements in self._elements.items():
            default[name] = elements['value']
        
        return default

    def set_default_values(self, name=None, value=None):
        if name is not None and value is not None:
            self._elements[name]['widget'].set_value(value)
        elif name is not None and value is None:
            raise(ValueError('value cannot be none!'))
        elif name is None and value is not None:
            raise(ValueError('name cannot be none!'))
        elif name is None and value is None:
            values = self.get()
            for name, value in values.items():
                self._elements[name]['widget'].set_value(value)
        else:
            raise(Exception(f'Error!'))

    def get(self):
        """Return values from form like {'element_name':'element_value'}
        """
        submit = {}
        for name, element in self._elements.items():
            if element['widget'].get_value() == '' and element['required']:
                self._require_value(name)
                return {}
            else:
                submit[name] = element['widget'].get_value()
        
        return submit
    
    def pack_widget(self, **kw): self._frame_form.pack(fill='both', expand=True)
    def unpack_widget(self): self._frame_form.pack_forget()
    def elements(self): return list(self._elements.keys())
    def element(self, name) : return self._elements[name]
    def buttons(self): return list(self._buttons.keys())
    def button(self, name) : return self._buttons[name]
    def changed(self): return self.values() == self.get()
    def keys(self): return list(self._options.keys())

    @staticmethod
    def how_it_works():
        root = tk.Tk()

        form = FormTheme(root, )
        form.add_title("Add Title")
        form.add_subtitle("Add Subtitle")
        form.add_info("Add Info")

        form.add_line()

        form.add_entry('name', 'Your Name: ', expand=False)
        form.add_line()
        form.add_entry('phone', 'Your Phone: ', type='number', 
                required = False, mask='+ 999 (99) 99999-9999')
        widget = form.add_entry('ex', placeholder='An Exemple')
        widget.disable()
        form.add_separator()
        form.add_entry('email', 'Your email: ', type='email', 
                help_text="Type your email, Guy!")
        widget = form.add_separator()
        widget.pack_configure(padx=100) 
        form.add_picker('color', 'Choose a color: ', help_text='hello')

        form.add_line_buttons()
        form.add_line_buttons()
        fun = lambda : print(form.get())
        form.add_button('submit', 'Submit', fun, align='center')

        form.pack_widget()
        print(form.get())

        root.mainloop()


class HowWidgetsThemeWorks(tk.Tk):
    """Show how the defined widgets work

    """
    def __init__(self):
        pass
    
    def __call__(self):
        pass
    
    def run(self):
        pass
    
    
if __name__ == "__main__":
    PickerTheme.how_it_works()