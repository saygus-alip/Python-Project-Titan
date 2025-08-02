import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer

# --- ตั้งค่าโปรแกรมหลัก (GLFW) ---
if not glfw.init():
    raise SystemExit("Could not initialize GLFW")

# กำหนดเวอร์ชัน OpenGL ที่จะใช้ (เวอร์ชันที่รองรับ Imgui)
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

window = glfw.create_window(800, 600, "My ImGui Program", None, None)
if not window:
    glfw.terminate()
    raise SystemExit("Could not create GLFW window")

glfw.make_context_current(window)

# สร้าง ImGui context และ renderer
imgui.create_context()
imgui_renderer = GlfwRenderer(window)

# --- ตัวแปรสำหรับ UI ---
show_gui = True
text_input = "Hello, ImGui!"
slider_value = 50.0
is_checked = False

# --- Main loop ---
while not glfw.window_should_close(window):
    # จัดการ input
    glfw.poll_events()
    imgui_renderer.process_inputs()

    # เริ่มต้น frame ใหม่ของ ImGui
    imgui.new_frame()

    # วาด UI ของเรา
    if show_gui:
        imgui.begin("Sample Window", True)

        imgui.text("This is a working ImGui window!")
        imgui.text(f"FPS: {glfw.get_time():.2f}")

        changed, text_input = imgui.input_text("Text", text_input, 256)

        changed, slider_value = imgui.slider_float("Slider", slider_value, 0.0, 100.0)

        changed, is_checked = imgui.checkbox("Checkbox", is_checked)
        if is_checked:
            imgui.text("The checkbox is ticked!")

        if imgui.button("Click me!"):
            print("Button was clicked!")

        imgui.end()

    # แสดงผล
    gl.glClearColor(0.2, 0.2, 0.2, 1)  # พื้นหลังสีเทา
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    imgui.render()
    imgui_renderer.render(imgui.get_draw_data())

    glfw.swap_buffers(window)

# ปิดโปรแกรม
imgui_renderer.shutdown()
glfw.terminate()