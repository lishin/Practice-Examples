import wx
import wx.lib.plot as plot
import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('crm.db')
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            registration_date TEXT DEFAULT CURRENT_DATE
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

class AddEditDialog(wx.Dialog):
    def __init__(self, parent, customer=None):
        super().__init__(parent, title="Edit Customer" if customer else "Add Customer")
        self.customer = customer
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        fields = [
            ("Name", "name"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Registration Date (YYYY-MM-DD)", "registration_date")
        ]
        
        self.controls = {}
        for label, field in fields:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            hsizer.Add(wx.StaticText(panel, label=label), 0, wx.ALL|wx.CENTER, 5)
            text_ctrl = wx.TextCtrl(panel)
            self.controls[field] = text_ctrl
            if field == "registration_date" and not customer:
                text_ctrl.SetValue(datetime.today().strftime('%Y-%m-%d'))
            hsizer.Add(text_ctrl, 1, wx.EXPAND)
            sizer.Add(hsizer, 0, wx.EXPAND|wx.ALL, 5)
        
        if customer:
            for field, value in customer.items():
                if field in self.controls:
                    self.controls[field].SetValue(str(value))
        
        btn_sizer = wx.StdDialogButtonSizer()
        btn_sizer.AddButton(wx.Button(panel, wx.ID_OK))
        btn_sizer.AddButton(wx.Button(panel, wx.ID_CANCEL))
        btn_sizer.Realize()
        sizer.Add(btn_sizer, 0, wx.EXPAND|wx.ALL, 5)
        
        panel.SetSizer(sizer)
        self.SetSize((400, 300))

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="CRM System", size=(800, 600))
        self.db = Database()
        
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Customer List
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, "ID", width=50)
        self.list_ctrl.InsertColumn(1, "Name", width=150)
        self.list_ctrl.InsertColumn(2, "Email", width=200)
        self.list_ctrl.InsertColumn(3, "Phone", width=150)
        self.list_ctrl.InsertColumn(4, "Registration Date", width=150)
        main_sizer.Add(self.list_ctrl, 1, wx.EXPAND|wx.ALL, 5)
        
        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons = [
            ("Add", self.on_add),
            ("Edit", self.on_edit),
            ("Delete", self.on_delete),
            ("Generate Report", self.on_report)
        ]
        for label, handler in buttons:
            btn = wx.Button(panel, label=label)
            btn.Bind(wx.EVT_BUTTON, handler)
            btn_sizer.Add(btn, 0, wx.ALL, 5)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)
        
        panel.SetSizer(main_sizer)
        self.refresh_customer_list()
        self.Show()

    def refresh_customer_list(self):
        self.list_ctrl.DeleteAllItems()
        cursor = self.db.execute("SELECT * FROM customers")
        for row in cursor.fetchall():
            self.list_ctrl.Append([str(col) for col in row])

    def get_selected_customer(self):
        index = self.list_ctrl.GetFirstSelected()
        if index == -1:
            wx.MessageBox("Please select a customer first!", "Error", wx.OK|wx.ICON_ERROR)
            return None
        return {
            "id": self.list_ctrl.GetItemText(index),
            "name": self.list_ctrl.GetItem(index, 1).GetText(),
            "email": self.list_ctrl.GetItem(index, 2).GetText(),
            "phone": self.list_ctrl.GetItem(index, 3).GetText(),
            "registration_date": self.list_ctrl.GetItem(index, 4).GetText()
        }

    def on_add(self, event):
        dlg = AddEditDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            self.db.execute(
                "INSERT INTO customers (name, email, phone, registration_date) VALUES (?, ?, ?, ?)",
                (dlg.controls['name'].GetValue(),
                 dlg.controls['email'].GetValue(),
                 dlg.controls['phone'].GetValue(),
                 dlg.controls['registration_date'].GetValue())
            )
            self.refresh_customer_list()
        dlg.Destroy()

    def on_edit(self, event):
        customer = self.get_selected_customer()
        if customer:
            dlg = AddEditDialog(self, customer)
            if dlg.ShowModal() == wx.ID_OK:
                self.db.execute(
                    "UPDATE customers SET name=?, email=?, phone=?, registration_date=? WHERE id=?",
                    (dlg.controls['name'].GetValue(),
                     dlg.controls['email'].GetValue(),
                     dlg.controls['phone'].GetValue(),
                     dlg.controls['registration_date'].GetValue(),
                     customer['id'])
                )
                self.refresh_customer_list()
            dlg.Destroy()

    def on_delete(self, event):
        customer = self.get_selected_customer()
        if customer:
            confirm = wx.MessageBox("Delete this customer?", "Confirm", wx.YES_NO|wx.ICON_QUESTION)
            if confirm == wx.YES:
                self.db.execute("DELETE FROM customers WHERE id=?", (customer['id'],))
                self.refresh_customer_list()

    def on_report(self, event):
        cursor = self.db.execute(
            "SELECT registration_date, COUNT(*) FROM customers GROUP BY registration_date ORDER BY registration_date"
        )
        results = cursor.fetchall()
        
        if not results:
            wx.MessageBox("No data to display!", "Info", wx.OK|wx.ICON_INFORMATION)
            return
        
        dates = [row[0] for row in results]
        counts = [row[1] for row in results]
        points = [(i, count) for i, count in enumerate(counts)]
        
        frame = wx.Frame(self, title="Registration Statistics", size=(600, 400))
        plot_canvas = plot.PlotCanvas(frame)
        plot_canvas.Draw(plot.PlotGraphics(
            [plot.PolyLine(points, colour='blue', width=2)],
            title="Registrations per Day",
            xLabel="Day Sequence",
            yLabel="Number of Registrations"
        ))
        frame.Show()

if __name__ == "__main__":
    app = wx.App()
    MainFrame()
    app.MainLoop()