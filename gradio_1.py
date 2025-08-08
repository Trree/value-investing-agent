import gradio as gr
import time
from app import orchestrator_worker

def greet(name):
    for chunk in orchestrator_worker.stream(name):
        yield chunk 


with gr.Blocks() as demo:
    # 输出区域（Markdown 格式）
    output = gr.Textbox(label="输出", interactive=False)

    # 输入区域（输入框 + 内嵌箭头按钮）
    with gr.Row():
        input_box = gr.Textbox(
            placeholder="输入消息...",
            show_label=False,
            container=False,
            elem_classes="input-box"
        )
        submit_btn = gr.Button("➜", elem_classes="arrow-btn")

    # 交互逻辑
    input_box.submit(greet, inputs=input_box, outputs=output)
    submit_btn.click(greet, inputs=input_box, outputs=output)

# 自定义 CSS（让箭头按钮嵌入输入框）
css = """
.output-area {
    min-height: 300px;
    border: none !important;
    padding: 20px;
    margin-bottom: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
}

.input-box {
    flex-grow: 1;
    padding-right: 50px !important;  /* 给箭头留空间 */
}

.arrow-btn {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    min-width: 30px !important;
    height: 30px !important;
}

/* 输入框容器相对定位，方便箭头绝对定位 */
.gr-box {
    position: relative !important;
}
"""

demo.css = css

if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=7860
    )
