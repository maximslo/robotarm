from pywinauto import Desktop, Application # Imports pywinauto
import time

program_path = r"C:\Program Files (x86)\Microsoft Office\Office16\EXCEL.exe"  # Excel application path
file_path = r"C:\Users\mslobodchikov\Desktop\mysample.xlsx"  # .xlsx file location

app = Application(backend="uia").start(r'{} "{}"'.format(program_path, file_path)) 
# print(app.windows())
dlg = app['mysample.xlsx-Excel'] # Selects Excel window
# time.sleep(3)
# dlg.child_window().click_input()
# ein = dlg.child_window(chr(65))
# ein.click_input()
# app.print_control_identifiers()

# text = ""
# for n in range(65, 65 + 5):
#     ex_id = str(chr(n)) + str(1) #A, B, C, D, etc.
#     dlg.child_window(auto_id = ex_id).click_input()
#     ein = dlg.child_window(auto_id = ex_id)
#     ein.click_input()
#     text+=(ein.legacy_properties()['Value'])
#     text+=" "
# print("Text read from mysample.xlsx is:",(text))


# Works
# app = Application(backend="uia")
# app.start(r"C:\Program Files (x86)\Microsoft Office\Office16\EXCEL.exe")