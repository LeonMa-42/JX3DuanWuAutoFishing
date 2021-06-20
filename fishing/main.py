import logging
import time

import pygetwindow

import fisher

if __name__ == '__main__':
    print('运行前先修改配置文件设置坐标与监测点RGB颜色')
    for i in reversed(range(5)):
        print('等待... ', i)
        time.sleep(1)
    logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(message)s')
    logging.info('start')
    try:
        pygetwindow.getWindowsWithTitle('剑网3')[0].activate()
        time.sleep(0.1)
    except Exception as e:
        logging.info('set activate window error: %s', e)

    # 开始钓鱼
    fisher = fisher.Fisher()
    fisher.hang_up()

