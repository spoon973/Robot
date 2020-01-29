import win32gui
import win32con
import win32clipboard as w
import time

class sendMessage:
    # 复制文字到剪贴板
    def setText(self,uname,info):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, info)
        w.CloseClipboard()
        self.sendByUser(uname)

    #定位QQ窗口，进行昵称备注的搜索，再回车弹出此好友窗口
    def searchByUser(self,uname,info):
        hwnd = win32gui.FindWindow('TXGuiFoundation', 'QQ')
        # hwnd = win32gui.FindWindow('ChatWnd', uname)
        send_info = info
        self.setText(uname,send_info)
        win32gui.SendMessage(hwnd, 258, 22, 2080193)
        win32gui.SendMessage(hwnd, 770, 0, 0)
        time.sleep(0.5)
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        self.setText(uname,send_info)


    # 定位好友窗口，昵称备注
    def sendByUser(self,uname):
        hwnd = win32gui.FindWindow('TXGuiFoundation', uname)
        # hwnd = win32gui.FindWindow('ChatWnd', uname)
        win32gui.SendMessage(hwnd, 258, 22, 2080193)
        win32gui.SendMessage(hwnd, 770, 0, 0)
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        time.sleep(3)

        self.closeByUser(uname)


    # 发送完信息之后关闭窗口（新的窗口的标题将不是昵称）
    def closeByUser(self,uname):
        hwnd = win32gui.FindWindow('TXGuiFoundation', uname)
        win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def main(self):
        with open('./reault_data/information.txt','r',encoding="utf-8") as f:
            conetent = f.readlines()
            # conetent = f.read().splitlines()
        conetent = ' '.join(conetent)
        self.searchByUser('小潘',conetent)

if __name__ == "__main__":
    send = sendMessage()
    send.main()