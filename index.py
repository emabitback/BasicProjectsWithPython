from tkinter import ttk
from tkinter import *

import sqlite3


class Product:

    db_name='database.db'

    def __init__(self, window):
        self.window= window
        self.window.title('Products App')

        # Creating a Frame Container
        frame = LabelFrame(self.window, text='Register a new Product')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Name Input
        Label(frame, text='Name: ').grid(row=0,column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=0, column=1)

        # Price Input
        Label(frame, text='Price: ').grid(row=1, column=0)
        self.price = Entry(frame)
        self.price.grid(row=1, column=1)

        # Button Add Product
        ttk.Button(frame, text='Save Product', command=self.add_product).grid(row=2, columnspan=2, sticky=W+E)

        # Output Messages
        self.messages = Label(text='', fg='red')
        self.messages.grid(row=3, columnspan=2, sticky=W+E)

        # Table
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Name', anchor=CENTER)
        self.tree.heading('#1', text='Price', anchor=CENTER)

        # bButtons
        ttk.Button(text='DELETE', command=self.delete_product).grid(row=5, column=0, sticky=W+E)
        ttk.Button(text='EDIT', command=self.edit_product).grid(row=5, column=1, sticky=W + E)

        self.get_products()

    def run_query(self, query, parameters=()):

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        # cleanning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Quering Data
        query = 'SELECT * FROM products ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling Data
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO products VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.messages['text'] = 'Product {0} added Successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
            self.get_products()
        else:
            self.messages['text'] = 'Name and Price is required'

    def validation(self):
        return len(self.name.get()) !=0 and len(self.price.get()) !=0

    def delete_product(self):
        self.messages['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.messages['text'] = 'Please Select A Record'
            return
        self.messages['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM products WHERE name = ?'
        self.run_query(query, (name, ))
        self.messages['text'] = 'Record {0} deleted Successfully'.format(name)
        self.get_products()

    def edit_product(self):
        self.messages['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.messages['text'] = 'Please Select A Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_window = Toplevel()
        self.edit_window.title = 'Edit Product'
        # Old Name
        Label(self.edit_window, text='Old Name:').grid(row=0, column=1)
        Entry(self.edit_window, textvariable=StringVar(self.edit_window, value=name), state='readonly').grid(row=0,
                                                                                                         column=2)
        # New Name
        Label(self.edit_window, text='New Price:').grid(row=1, column=1)
        new_name = Entry(self.edit_window)
        new_name.grid(row=1, column=2)

        # Old Price
        Label(self.edit_window, text='Old Price:').grid(row=2, column=1)
        Entry(self.edit_window, textvariable=StringVar(self.edit_window, value=old_price), state='readonly').grid(row=2,
                                                                                                              column=2)
        # New Price
        Label(self.edit_window, text='New Name:').grid(row=3, column=1)
        new_price = Entry(self.edit_window)
        new_price.grid(row=3, column=2)

        Button(self.edit_window, text='Update',
           command=lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2,
                                                                                                     sticky=W)
        # name = self.tree.item(self.tree.selection())['text']
        # old_price = self.tree.item(self.tree.selection())['values'][0]
        # self.edit_window= Toplevel()
        # self.edit_window.title('EDIT PRODUCT')


        # # Old  Data
        # Label(self.edit_window, text='Old Name').grid(row=1, column=0)
        # Entry(self.edit_window, textvariable=StringVar(self.edit_window, name), state='readonly').grid(row=1, column=1)
        # Label(self.edit_window, text='Old Price: ').grid(row=2, column=0)
        # Entry(self.edit_window, textvariable=StringVar(self.edit_window, old_price), state='readonly').grid(row=2, column=1)


        # # New Data
        # Label(self.edit_window, text='New Name').grid(row=3, column=0)
        # new_name = Entry(self.edit_window)
        # new_name.grid(row=3, column=1)
        #
        # Label(self.edit_window, text='New Price: ').grid(row=4, column=0)
        # new_price = Entry(self.edit_window)
        # new_price.grid(row=4, column=1)
        #
        # # Button SAVE Changes
        # ttk.Button(self.edit_window, text='SAVE CHANGES',
        #            command=lambda: self.edit_records(new_name.get(), name, new_price.get(),
        #                                              old_price)).grid(row=5, column=0, sticky=W + E)

    # def edit_records(self, name, old_price, new_name, new_price):
    #     query = 'UPDATE products SET name = ?, price = ? WHERE name = ? AND price = ?'
    #     parameters = (new_name, new_price, name, old_price)
    #     self.run_query(query, parameters)
    #     self.edit_window.destroy()
    #     self.messages['text'] = 'Record {0} updated Succesfully '.format(name)
    #     self.get_products()
    #     self.edit_window.destroy()

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE products SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_window.destroy()
        self.messages['text'] = 'Record {} updated Successfully'.format(name)
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()



























