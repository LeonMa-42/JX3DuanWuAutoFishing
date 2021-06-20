import os
import sys
import time
import logging
import pyautogui
import pygetwindow
import win32gui
import configparser


def rgb_to_color_ref(rgb_tuple):
    ref = 0x00
    for value in reversed(rgb_tuple):
        ref = ref + value << 8
    return ref >> 8


def set_activate_window():
    try:
        pygetwindow.getWindowsWithTitle('剑网3')[0].activate()
        time.sleep(0.1)
    except Exception as e:
        logging.info('set activate window error: %s', e)


class Fisher:
    def __init__(self):
        # 读取配置
        logging.info('init')
        config = configparser.ConfigParser()
        config.sections()
        config.read(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'config.ini'), 'UTF-8')
        logging.info('load path:' + os.path.join(os.path.dirname(__file__), 'config.ini'))
        default = config['DEFAULT']
        # 出杆点坐标
        self.skill_3_x = default.getint('skill_3_x')
        self.skill_3_y = default.getint('skill_3_y')
        logging.info('load 出杆点坐标: %s, %s', self.skill_3_x, self.skill_3_y)
        # 收杆点坐标
        self.skill_4_x = default.getint('skill_4_x')
        self.skill_4_y = default.getint('skill_4_y')
        logging.info('load 收杆点坐标: %s, %s', self.skill_4_x, self.skill_4_y)
        # 提示点坐标
        self.alert_x = default.getint('alert_x')
        self.alert_y = default.getint('alert_y')
        logging.info('load 提示点坐标: %s, %s', self.alert_x, self.alert_y)
        # 提示点颜色
        self.alert_rgb = tuple(eval(default.get('alert_rgb')))
        self.alert_rgb_int = rgb_to_color_ref(self.alert_rgb)
        logging.info('load 提示点颜色:%s', self.alert_rgb)
        # HP
        self.hp_x = default.getint('hp_x')
        self.hp_y = default.getint('hp_y')
        logging.info('load HP检测点坐标: %s, %s', self.hp_x, self.hp_y)
        self.hp_rgb = tuple(eval(default.get('hp_rgb')))
        logging.info('load HP检测点颜色: %s', self.hp_rgb)
        self.hp_rgb_int = rgb_to_color_ref(self.hp_rgb)
        self.need_reset_position = False
        # 原地复活坐标
        self.revive_x = default.getint('revive_x')
        self.revive_y = default.getint('revive_y')
        logging.info('load 原地复活坐标: %s, %s', self.revive_x, self.revive_y)
        # 鱼篓坐标
        self.reset_position_x = default.getint('reset_position_x')
        self.reset_position_y = default.getint('reset_position_y')
        logging.info('load 鱼篓坐标: %s, %s', self.reset_position_x, self.reset_position_y)

        # 窗口句柄相关
        self.hwndChild = win32gui.FindWindowEx(0, 0, 'KGWin32App', None)
        self.hwndDC = win32gui.GetWindowDC(self.hwndChild)

    def start(self):
        logging.info('出杆')
        set_activate_window()
        pyautogui.click(self.skill_3_x, self.skill_3_y)
        # 等待5秒
        time.sleep(5)

    def check(self):
        logging.info('等待鱼上钩...')
        num = 0
        while True:
            num = num + 1
            if num % 100 == 0 and not (self.check_health()):
                # 收杆中死亡 跳过等待上钩
                return False
            if num % 1000 == 0:
                # 循环500次大概50秒未捉到鱼 重新出勾
                return False
            color = win32gui.GetPixel(self.hwndDC, self.alert_x, self.alert_y)
            if color == self.alert_rgb_int:
                logging.info('有鱼上钩了')
                return True
            else:
                time.sleep(0.1)

    def finish(self):
        logging.info('收杆')
        set_activate_window()
        pyautogui.click(self.skill_4_x, self.skill_4_y)
        time.sleep(3)

    def hang_up(self):
        while True:
            self.check_health()
            if self.need_reset_position:
                self.reset_position()
            self.start()
            if self.check():
                self.finish()

    def check_health(self):
        logging.info('血量检查')
        color = win32gui.GetPixel(self.hwndDC, self.hp_x, self.hp_y)
        if color == self.hp_rgb_int:
            logging.info('血量检查通过')
            return True
        else:
            logging.info('血量检查未通过，准备原地复活')
            set_activate_window()
            pyautogui.click(self.revive_x, self.revive_y)
            # 需重新进入钓鱼位
            self.need_reset_position = True
            time.sleep(2)
            self.check_health()
            return False

    def reset_position(self):
        self.need_reset_position = False
        x = self.reset_position_x
        y = self.reset_position_y
        logging.info('准备重新进入钓鱼坑')
        logging.info('鱼篓位置: %s, %s', str(x), str(y))
        set_activate_window()
        pyautogui.moveTo(x, y, 2)
        pyautogui.rightClick(x, y)
        time.sleep(2)
