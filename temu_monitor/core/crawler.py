#src/temu_monitor/core/crawler.py
from playwright.async_api import Page
import logging

# 设置日志记录
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TemuCrawler:
    def __init__(self, page: Page, country_code: str, time_range: str):
        self.page = page
        self.country_code = country_code
        self.time_range = time_range
        self.time_ranges = {
            "30": ".splide__slide[data-uniqid='1']",
            "14": ".splide__slide[data-uniqid='2']",
            "7": ".splide__slide[data-uniqid='3']"
        }

    async def navigate_to_new_arrivals(self):
        try:
            logging.debug("等待 New Arrivals 元素出现...")
            new_arrivals_element = await self.page.query_selector('div._3-CLYVT9._3KPReHFH a._2Tl9qLr1')
            
            if new_arrivals_element:
                href = await new_arrivals_element.get_attribute('href')
                if href:
                    base_url = self.page.url.split('/channel')[0]  # 提取基础 URL
                    full_url = f"{base_url}{href}"
                    logging.debug(f"导航到: {full_url}")
                    await self.page.goto(full_url, wait_until="networkidle", timeout=120000)
                    print(f"🌍 导航到: {full_url}")
                else:
                    logging.error("无法获取 New Arrivals 的 href 属性")
                    raise ValueError("无法获取 New Arrivals 的 href 属性")
            else:
                logging.error("找不到 New Arrivals 元素")
                raise ValueError("找不到 New Arrivals 元素")
        except Exception as e:
            logging.exception(f"导航到 New Arrivals 时出错: {str(e)}")
            print(f"🔥 导航到 New Arrivals 时出错: {str(e)}")

    async def select_time_range(self):
        try:
            # 点击对应的时间范围按钮
            selector = self.time_ranges.get(self.time_range)
            if not selector:
                logging.error(f"无效的时间范围: {self.time_range}. 请选择 '30', '14', 或 '7'.")
                raise ValueError(f"无效的时间范围: {self.time_range}. 请选择 '30', '14', 或 '7'.")
            
            logging.debug(f"点击时间范围按钮: {selector}")
            await self.page.click(selector)
            print(f"📅 已选择时间范围: 过去 {self.time_range} 天内")
        except Exception as e:
            logging.exception(f"选择时间范围时出错: {str(e)}")
            print(f"🔥 选择时间范围时出错: {str(e)}")



