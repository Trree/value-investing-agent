import gradio as gr
import time
from app import orchestrator_worker

def greet(name, history):
    history.append((name, ""))
    for chunk in orchestrator_worker.stream(name):
        response += chunk
        yield response


demo = gr.ChatInterface(
    greet,
    chatbot=gr.Chatbot(
        render_markdown=True,  # 关键设置！
        bubble_full_width=False,
        avatar_images=(None, "🖥️")
    ),
    textbox=gr.Textbox(placeholder="输入股票/行业..."),
    #title="💼 智能投研助手 (Markdown版)"
)

# 优化 Markdown 显示样式
css = """
.message.bot pre {
    background: #f8f9fa !important;
    padding: 10px !important;
    border-radius: 8px !important;
}
.message.bot table {
    border-collapse: collapse;
    margin: 10px 0;
}
.message.bot th, .message.bot td {
    border: 1px solid #ddd;
    padding: 8px;
}
"""

demo.css = css
demo.launch()
