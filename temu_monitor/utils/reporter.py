from pathlib import Path
import html
from fpdf import FPDF
import matplotlib.pyplot as plt

class ReportGenerator:
    @classmethod
    def generate_html(cls, products, filename="report.html"):
        """生成交互式HTML报告"""
        html_content = cls._build_html(products)
        Path(filename).write_text(html_content, encoding='utf-8')
        print(f"📊 HTML报告已生成：{filename}")
    
    @classmethod
    def generate_pdf(cls, products, filename="report.pdf"):
        """生成专业PDF报告"""
        pdf = FPDF()
        pdf.add_page()
        
        # 添加标题
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Temu新品分析报告", 0, 1, 'C')
        
        # 添加图表
        cls._add_sales_chart(pdf, products)
        
        # 添加数据表
        pdf.set_font("Arial", size=10)
        col_width = pdf.w / 4.5  # 设置列宽
        row_height = 10
        
        # 表头
        pdf.ln(row_height)
        pdf.cell(col_width * 2, row_height, "产品名称", border=1)
        pdf.cell(col_width, row_height, "价格", border=1)
        pdf.ln(row_height)
        
        # 数据行
        for product in products:
            pdf.cell(col_width * 2, row_height, html.escape(product['title']), border=1)
            pdf.cell(col_width, row_height, html.escape(product['price']), border=1)
            pdf.ln(row_height)
        
        pdf.output(filename)
        print(f"📄 PDF报告已生成：{filename}")
    
    @classmethod
    def _build_html(cls, products):
        """构建HTML内容"""
        rows = "\n".join([cls._build_row(p) for p in products])
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Temu新品报告</title>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h1>发现 {len(products)} 款热销新品</h1>
            <table>
                <thead>
                    <tr>
                        <th>产品名称</th>
                        <th>价格</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </body>
        </html>
        """
    
    @classmethod
    def _build_row(cls, product):
        """生成表格行"""
        return f"""
        <tr>
            <td>{html.escape(product['title'])}</td>
            <td>{html.escape(product['price'])}</td>
        </tr>
        """
    
    @classmethod
    def _add_sales_chart(cls, pdf, products):
        """添加销售图表"""
        sales = [float(p['price'].replace('$', '')) for p in products]
        titles = [p['title'] for p in products]
        plt.figure(figsize=(10, 5))
        plt.bar(titles, sales)
        plt.xlabel('产品')
        plt.ylabel('价格 ($)')
        plt.title('新品价格图表')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        chart_path = "temp_chart.png"
        plt.savefig(chart_path)
        pdf.image(chart_path, x=10, y=30, w=190)
        Path(chart_path).unlink()  # 删除临时文件



from pathlib import Path
import html
from fpdf import FPDF
import matplotlib.pyplot as plt

class ReportGenerator:
    @classmethod
    def generate_html(cls, products, filename="report.html"):
        """生成交互式HTML报告"""
        html_content = cls._build_html(products)
        Path(filename).write_text(html_content, encoding='utf-8')
        print(f"📊 HTML报告已生成：{filename}")
    
    @classmethod
    def generate_pdf(cls, products, filename="report.pdf"):
        """生成专业PDF报告"""
        pdf = FPDF()
        pdf.add_page()
        
        # 添加标题
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Temu新品分析报告", 0, 1, 'C')
        
        # 添加图表
        cls._add_sales_chart(pdf, products)
        
        # 添加数据表
        pdf.set_font("Arial", size=10)
        col_width = pdf.w / 4.5  # 设置列宽
        row_height = 10
        
        # 表头
        pdf.ln(row_height)
        pdf.cell(col_width * 2, row_height, "产品名称", border=1)
        pdf.cell(col_width, row_height, "价格", border=1)
        pdf.ln(row_height)
        
        # 数据行
        for product in products:
            pdf.cell(col_width * 2, row_height, html.escape(product['title']), border=1)
            pdf.cell(col_width, row_height, html.escape(product['price']), border=1)
            pdf.ln(row_height)
        
        pdf.output(filename)
        print(f"📄 PDF报告已生成：{filename}")
    
    @classmethod
    def _build_html(cls, products):
        """构建HTML内容"""
        rows = "\n".join([cls._build_row(p) for p in products])
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Temu新品报告</title>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h1>发现 {len(products)} 款热销新品</h1>
            <table>
                <thead>
                    <tr>
                        <th>产品名称</th>
                        <th>价格</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </body>
        </html>
        """
    
    @classmethod
    def _build_row(cls, product):
        """生成表格行"""
        return f"""
        <tr>
            <td>{html.escape(product['title'])}</td>
            <td>{html.escape(product['price'])}</td>
        </tr>
        """
    
    @classmethod
    def _add_sales_chart(cls, pdf, products):
        """添加销售图表"""
        sales = [float(p['price'].replace('$', '')) for p in products]
        titles = [p['title'] for p in products]
        plt.figure(figsize=(10, 5))
        plt.bar(titles, sales)
        plt.xlabel('产品')
        plt.ylabel('价格 ($)')
        plt.title('新品价格图表')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        chart_path = "temp_chart.png"
        plt.savefig(chart_path)
        pdf.image(chart_path, x=10, y=30, w=190)
        Path(chart_path).unlink()  # 删除临时文件



