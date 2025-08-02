import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import psutil
import time
import numpy as np  # เพิ่ม numpy เข้ามา

# --- ตั้งค่าโปรแกรมหลัก (GLFW) ---
if not glfw.init():
    raise SystemExit("Could not initialize GLFW")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

window = glfw.create_window(1024, 768, "System Monitor", None, None)
if not window:
    glfw.terminate()
    raise SystemExit("Could not create GLFW window")

glfw.make_context_current(window)

imgui.create_context()
imgui_renderer = GlfwRenderer(window)

# --- ตัวแปรสำหรับเก็บข้อมูลระบบ ---
cpu_history = [0.0] * 60  # ใช้ float เพื่อความเข้ากันได้กับ numpy
last_update_time = time.time()
ram_info = psutil.virtual_memory()

# --- Main loop ---
while not glfw.window_should_close(window):
    # จัดการ input
    glfw.poll_events()
    imgui_renderer.process_inputs()

    # อัปเดตข้อมูลระบบทุกๆ 1 วินาที
    if time.time() - last_update_time >= 1.0:
        cpu_percent = psutil.cpu_percent()
        cpu_history.pop(0)
        cpu_history.append(float(cpu_percent))  # แปลงเป็น float ก่อน

        ram_info = psutil.virtual_memory()

        last_update_time = time.time()

    # เริ่มต้น Imgui Frame
    imgui.new_frame()

    # วาด UI ของ System Monitor
    imgui.begin("System Monitor", True)

    imgui.text("CPU Usage:")

    # --- ส่วนที่แก้ไข ---
    # แปลง list เป็น numpy array ก่อนส่งให้ Imgui
    cpu_history_np = np.array(cpu_history, dtype=np.float32)
    imgui.plot_lines("##cpu_graph", cpu_history_np)
    # --- สิ้นสุดส่วนที่แก้ไข ---

    imgui.text(f"Current: {cpu_history[-1]:.2f}%")

    imgui.separator()

    imgui.text("RAM Usage:")
    ram_used_gb = ram_info.used / (1024 ** 3)
    ram_total_gb = ram_info.total / (1024 ** 3)
    ram_percent = ram_info.percent

    imgui.text(f"Used: {ram_used_gb:.2f} GB / Total: {ram_total_gb:.2f} GB")
    imgui.text(f"Percent: {ram_percent:.2f}%")

    imgui.end()

    # แสดงผล
    gl.glClearColor(0.2, 0.2, 0.2, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    imgui.render()
    imgui_renderer.render(imgui.get_draw_data())

    glfw.swap_buffers(window)

# ปิดโปรแกรม
imgui_renderer.shutdown()
glfw.terminate()