import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer

# เริ่มต้น GLFW
if not glfw.init():
    raise SystemExit("Could not initialize GLFW")

# สร้างหน้าต่าง
window = glfw.create_window(1280, 720, "ImGui By Alip", None, None)
if not window:
    glfw.terminate()
    raise SystemExit("Could not create GLFW window")

glfw.make_context_current(window)

# สร้าง ImGui context และ renderer
imgui.create_context()
imgui_renderer = GlfwRenderer(window)

# --- ส่วนนี้สำหรับปรับขนาด UI และตัวอักษร ---
io = imgui.get_io()
io.font_global_scale = 1.5  # ปรับขนาด UI ทั้งหมดให้ใหญ่ขึ้น 1.2 เท่า

# --- ตัวแปรสำหรับ Mod Menu ---
show_menu = True
toggle_feature = False
speed_value = 1.0
message_text = "Welcome to the mod menu!"

# Main loop
while not glfw.window_should_close(window):
    # จัดการ input ของ GLFW
    glfw.poll_events()
    imgui_renderer.process_inputs()

    # เริ่มต้น frame ใหม่ของ ImGui
    imgui.new_frame()

    # --- วาด UI ของเรา ---
    if show_menu:
        imgui.begin("My Mod Menu", True)

        # ตั้งค่าขนาดหน้าต่าง
        imgui.set_window_size(400, 250)

        # ข้อความต้อนรับ
        imgui.text(message_text)

        # Checkbox สำหรับเปิด/ปิดฟีเจอร์
        _, toggle_feature = imgui.checkbox("Enable Hack", toggle_feature)
        if toggle_feature:
            imgui.text("Hack is ON!")

        # Slider สำหรับปรับค่าความเร็ว
        _, speed_value = imgui.slider_float("Speed Hack", speed_value, 0.5, 3.0)
        imgui.text(f"Current Speed: {speed_value:.2f}x")

        # ปุ่มกด
        if imgui.button("Reset Speed"):
            speed_value = 1.0

        imgui.end()

    # ตรวจสอบการกดปุ่มเพื่อเปิด/ปิดเมนู
    if imgui.is_key_pressed(glfw.KEY_INSERT):
        show_menu = not show_menu

    # วาด ImGui บนหน้าจอ
    gl.glClearColor(0.2, 0.2, 0.2, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    imgui.render()
    imgui_renderer.render(imgui.get_draw_data())

    glfw.swap_buffers(window)

# ปิดโปรแกรม
imgui_renderer.shutdown()
glfw.terminate()