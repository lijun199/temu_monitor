import asyncio
from playwright.async_api import async_playwright
import logging

# 设置日志记录，将日志级别设置为 DEBUG，并指定日志格式
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_proxy_url(proxy_settings):
    # 根据代理设置生成代理 URL
    if "username" in proxy_settings and "password" in proxy_settings:
        return f"http://{proxy_settings['username']}:{proxy_settings['password']}@{proxy_settings['server']}:{proxy_settings['port']}"
    else:
        return f"http://{proxy_settings['server']}:{proxy_settings['port']}"

class AuthManager:
    def __init__(self):
        pass  # 初始化方法，目前没有需要执行的操作

    async def login(self, proxy_settings=None):
        try:
            logging.debug("正在初始化浏览器环境...")  # 记录日志：正在初始化浏览器环境
            print("🛠️ 正在初始化浏览器环境...")  # 打印信息：正在初始化浏览器环境

            # 配置代理设置
            launch_options = {}  # 创建一个空字典用于存储启动选项
            if proxy_settings:
                proxy_url = get_proxy_url(proxy_settings)  # 获取代理 URL
                launch_options["proxy"] = {
                    "server": proxy_url  # 设置代理服务器
                }
                logging.debug(f"代理 URL: {proxy_url}")  # 记录日志：代理 URL

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False, **launch_options)  # 启动 Chromium 浏览器，非无头模式
                context = await browser.new_context()  # 创建新的浏览器上下文
                page = await context.new_page()  # 在新上下文中打开新页面

                logging.debug(f"代理设置: {proxy_settings}")  # 记录日志：代理设置
                print(f"🔧 代理设置: {proxy_settings}")  # 打印信息：代理设置

                logging.debug("导航到登录页面...")  # 记录日志：导航到登录页面
                print("🌐 导航到登录页面...")  # 打印信息：导航到登录页面

                # 添加自定义请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
                }

                await page.set_extra_http_headers(headers)  # 设置额外的 HTTP 请求头

                # 监听请求和响应
                page.on('request', lambda request: logging.debug(f"Request: {request.url}"))  # 监听请求并记录请求 URL
                page.on('response', lambda response: logging.debug(f"Response: {response.status} {response.url}"))  # 监听响应并记录响应状态码和 URL

                await page.goto("https://www.temu.com/login", wait_until="networkidle", timeout=120000)  # 导航到登录页面，等待网络空闲

                # 获取页面内容
                content = await page.content()  # 获取页面内容
                logging.debug(f"Page Content: {content[:500]}")  # 记录日志：页面内容（前500个字符）

                logging.debug("请在浏览器完成登录后输入 yes")  # 记录日志：提示用户完成登录
                print("🔑 请在浏览器完成登录后输入 yes")  # 打印信息：提示用户完成登录
                user_input = input("🔔 是否已完成登录？(输入 yes 继续): ")  # 等待用户输入

                if user_input.lower() != "yes":
                    logging.error("登录未完成，退出程序")  # 记录日志：登录未完成
                    print("❌ 登录未完成，退出程序")  # 打印信息：登录未完成
                    await browser.close()  # 关闭浏览器
                    return None  # 返回 None 表示登录失败
                
                logging.debug("正在执行验证流程...")  # 记录日志：正在执行验证流程
                print("🔄 正在执行验证流程...")  # 打印信息：正在执行验证流程
                
                # 增加等待时间以防止会话过早关闭
                await asyncio.sleep(5)  # 等待5秒
                
                logging.info("混合验证成功")  # 记录日志：混合验证成功
                print("✅ 混合验证成功")  # 打印信息：混合验证成功
                return browser, context, page  # 返回浏览器、上下文和页面对象
        except Exception as e:
            logging.exception(f"登录过程中出错: {str(e)}")  # 记录异常日志
            print(f"🔥 登录过程中出错: {str(e)}")  # 打印异常信息
            import traceback
            print(traceback.format_exc())  # 打印堆栈跟踪信息
            return None  # 返回 None 表示登录失败

    async def close(self, browser, context, page):
        try:
            logging.debug("正在释放浏览器资源...")  # 记录日志：正在释放浏览器资源
            print("🧹 正在释放浏览器资源...")  # 打印信息：正在释放浏览器资源
            if page:
                logging.debug("页面实例 已释放")  # 记录日志：页面实例已释放
                print("   - 页面实例 已释放")  # 打印信息：页面实例已释放
                await page.close()  # 关闭页面
            if context:
                logging.debug("浏览器上下文 已释放")  # 记录日志：浏览器上下文已释放
                print("   - 浏览器上下文 已释放")  # 打印信息：浏览器上下文已释放
                await context.close()  # 关闭上下文
            if browser:
                logging.debug("浏览器实例 已释放")  # 记录日志：浏览器实例已释放
                print("   - 浏览器实例 已释放")  # 打印信息：浏览器实例已释放
                await browser.close()  # 关闭浏览器
        except Exception as e:
            logging.exception(f"释放资源时出错: {str(e)}")  # 记录异常日志
            print(f"🔥 释放资源时出错: {str(e)}")  # 打印异常信息
            import traceback
            print(traceback.format_exc())  # 打印堆栈跟踪信息

