import asyncio
from temu_monitor.core.auth import AuthManager         # 导入认证管理器类
from temu_monitor.core.crawler import TemuCrawler     # 导入爬虫类
import logging

# 设置日志记录，将日志级别设置为 DEBUG，并指定日志格式
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def get_public_ip(page):
    try:
        logging.debug("获取公共 IP 地址...")  # 记录日志：正在获取公共 IP 地址
        print("🔍 获取公共 IP 地址...")  # 打印信息：正在获取公共 IP 地址
        response = await page.goto("https://api.ipify.org?format=json", wait_until="networkidle", timeout=120000)  # 导航到获取公共 IP 地址的 API 并等待网络空闲
        ip_info = await response.json()  # 将响应内容解析为 JSON
        public_ip = ip_info.get('ip')  # 提取公共 IP 地址
        if public_ip:
            logging.debug(f"公共 IP 地址: {public_ip}")  # 记录日志：公共 IP 地址
            print(f"🌐 公共 IP 地址: {public_ip}")  # 打印信息：公共 IP 地址
        else:
            logging.warning("无法获取公共 IP 地址")  # 记录警告日志：无法获取公共 IP 地址
            print("⚠️ 无法获取公共 IP 地址")  # 打印警告信息：无法获取公共 IP 地址
    except Exception as e:
        logging.exception(f"获取公共 IP 地址时出错: {str(e)}")  # 记录异常日志
        print(f"🔥 获取公共 IP 地址时出错: {str(e)}")  # 打印异常信息

async def main():
    auth = None  # 初始化认证管理器变量
    browser = None  # 初始化浏览器变量
    context = None  # 初始化浏览器上下文变量
    page = None  # 初始化页面变量
    try:
        logging.debug("启动 Temu 监控系统")  # 记录日志：启动 Temu 监控系统
        print("🚀 启动 Temu 监控系统")  # 打印信息：启动 Temu 监控系统
        
        # 配置代理设置
        proxy_settings = {
            "server": "res.proxy-seller.com",
            "port": 10008,
            "username": "e22e12b999946190",
            "password": "RNW78Fm5"
        }
        
        auth = AuthManager()  # 创建认证管理器实例
        result = await auth.login(proxy_settings)  # 调用登录方法并传入代理设置
        
        if not result:
            logging.error("登录失败")  # 记录错误日志：登录失败
            print("❌ 登录失败")  # 打印错误信息：登录失败
            return
            
        browser, context, page = result  # 解包返回的结果，获取浏览器、上下文和页面对象
        
        # 获取公共 IP 地址
        await get_public_ip(page)
        
        logging.debug("请在浏览器中手动选择国家和地区，完成后输入 yes 继续")  # 记录日志：提示用户手动选择国家和地区
        print("🔑 请在浏览器中手动选择国家和地区，完成后输入 yes 继续")  # 打印信息：提示用户手动选择国家和地区
        user_input = input("🔔 是否已完成手动选择？(输入 yes 继续): ")  # 等待用户输入

        if user_input.lower() != "yes":
            logging.error("手动选择未完成，退出程序")  # 记录错误日志：手动选择未完成
            print("❌ 手动选择未完成，退出程序")  # 打印错误信息：手动选择未完成
            await auth.close(browser, context, page)  # 关闭浏览器资源
            return
        
        # 用户选择时间范围
        logging.debug("请选择时间范围:")  # 记录日志：提示用户选择时间范围
        print("请选择时间范围:")  # 打印信息：提示用户选择时间范围
        print("(1) 过去30天内")  # 打印选项：过去30天内
        print("(2) 过去14天内")  # 打印选项：过去14天内
        print("(3) 过去7天内")  # 打印选项：过去7天内
        
        time_choice = input("请输入选项 (1/2/3): ")  # 等待用户输入时间范围选项
        
        if time_choice == '1':
            time_range = '30'  # 设置时间范围为过去30天
        elif time_choice == '2':
            time_range = '14'  # 设置时间范围为过去14天
        elif time_choice == '3':
            time_range = '7'  # 设置时间范围为过去7天
        else:
            logging.error("无效的选择，请重新运行脚本并输入有效的选项。")  # 记录错误日志：无效的选择
            print("无效的选择，请重新运行脚本并输入有效的选项。")  # 打印错误信息：无效的选择
            await auth.close(browser, context, page)  # 关闭浏览器资源
            return
        
        # 初始化爬虫
        crawler = TemuCrawler(page, "", time_range)  # 国家代码暂时为空
        
        # 根据页面元素导航到 New Arrivals 页面
        await crawler.navigate_to_new_arrivals()
        
        # 选择时间范围
        await crawler.select_time_range()
        
        logging.info("时间范围选择完成！")  # 记录日志：时间范围选择完成
        print("🎉 时间范围选择完成！")  # 打印信息：时间范围选择完成
        
    except Exception as e:
        logging.exception(f"严重错误: {str(e)}")  # 记录异常日志
        print(f"🔥 严重错误: {str(e)}")  # 打印异常信息
        import traceback
        print(traceback.format_exc())  # 打印堆栈跟踪信息
    finally:
        if auth and browser:
            await auth.close(browser, context, page)  # 关闭浏览器资源

if __name__ == "__main__":
    asyncio.run(main())  # 运行主函数



