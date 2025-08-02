import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import psutil
import time
import numpy as np
import wmi  # ใช้ wmi เป็นตัวหลักสำหรับข้อมูล GPU

# --- ตั้งค่าโปรแกรมหลัก (GLFW) ---
if not glfw.init():
    raise SystemExit("Could not initialize GLFW")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

window = glfw.create_window(1024, 768, "System Monitor Final", None, None)
if not window:
    glfw.terminate()
    raise SystemExit("Could not create GLFW window")

glfw.make_context_current(window)

imgui.create_context()
imgui_renderer = GlfwRenderer(window)

# --- ตัวแปรสำหรับเก็บข้อมูลระบบ ---
cpu_history = [0.0] * 60
last_update_time = time.time()
ram_info = psutil.virtual_memory()
gpu_info = None
gpu_name = "N/A"

# พยายามดึงชื่อการ์ดจอด้วย WMI (มักจะสำเร็จ)
try:
    wmi_obj = wmi.WMI()
    video_controllers = wmi_obj.Win32_VideoController()
    if video_controllers:
        gpu_name = video_controllers[0].Name
except Exception as e:
    gpu_name = f"Error: {e}"

# --- Main loop ---
while not glfw.window_should_close(window):
    glfw.poll_events()
    imgui_renderer.process_inputs()

    if time.time() - last_update_time >= 1.0:
        cpu_percent = psutil.cpu_percent()
        cpu_history.pop(0)
        cpu_history.append(float(cpu_percent))
        ram_info = psutil.virtual_memory()
        last_update_time = time.time()

    imgui.new_frame()

    imgui.begin("System Monitor", True)
    imgui.set_window_size(450, 300)

    if imgui.begin_tab_bar("MyTabBar"):
        if imgui.begin_tab_item("CPU")[0]:
            imgui.text("CPU Usage:")
            cpu_history_np = np.array(cpu_history, dtype=np.float32)
            imgui.plot_lines("##cpu_graph", cpu_history_np, overlay_text=f"{cpu_history[-1]:.2f}%")
            imgui.end_tab_item()

        if imgui.begin_tab_item("RAM")[0]:
            imgui.text("RAM Usage:")
            ram_used_gb = ram_info.used / (1024 ** 3)
            ram_total_gb = ram_info.total / (1024 ** 3)
            ram_percent = ram_info.percent
            imgui.text(f"Used: {ram_used_gb:.2f} GB / Total: {ram_total_gb:.2f} GB")
            imgui.text(f"Percent: {ram_percent:.2f}%")
            imgui.progress_bar(ram_percent / 100, (300, 20), f"{ram_percent:.2f}%")
            imgui.end_tab_item()

        if imgui.begin_tab_item("Storage")[0]:
            imgui.text("Disk Usage:")
            partitions = psutil.disk_partitions()
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    imgui.text(f"Drive {partition.device}:")
                    imgui.progress_bar(usage.percent / 100, (300, 20), f"{usage.percent:.2f}%")
                    imgui.text(f"Used: {usage.used / (1024 ** 3):.2f} GB / Total: {usage.total / (1024 ** 3):.2f} GB")
                    imgui.separator()
                except OSError:
                    pass
            imgui.end_tab_item()

        # --- แท็บ GPU (ใช้ WMI เพื่อดึงชื่อ) ---
        if imgui.begin_tab_item("GPU")[0]:
            imgui.text(f"GPU Name: {gpu_name}")
            imgui.text("GPU Utilization: Not available via standard libraries.")
            imgui.text("VRAM Usage: Not available via standard libraries.")
            imgui.text("To get this info, you might need a specialized Intel tool.")
            imgui.end_tab_item()

        imgui.end_tab_bar()

    imgui.end()

    gl.glClearColor(0.2, 0.2, 0.2, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    imgui.render()
    imgui_renderer.render(imgui.get_draw_data())

    glfw.swap_buffers(window)

imgui_renderer.shutdown()
glfw.terminate()