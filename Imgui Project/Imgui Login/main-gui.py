# main.py

import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
from database import DatabaseManager  # Import the DatabaseManager class


def main():
    # Initialize GLFW
    if not glfw.init():
        return

    # Create a window
    window = glfw.create_window(400, 300, "Login", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Initialize ImGui
    imgui.create_context()
    renderer = GlfwRenderer(window)

    # Use default font, no custom font loading needed.

    # Initialize database manager
    db = DatabaseManager()

    # State variables
    username = ""
    password = ""
    status_message = ""
    show_register_form = False

    # Main application loop
    while not glfw.window_should_close(window):
        glfw.poll_events()
        renderer.process_inputs()

        # Start a new ImGui frame
        imgui.new_frame()

        if not show_register_form:
            # Login Form
            imgui.begin("Login", True)

            imgui.text("Username:")
            changed, username = imgui.input_text("##username_input", username, 256)

            imgui.text("Password:")
            changed, password = imgui.input_text("##password_input", password, 256,
                                                 imgui.INPUT_TEXT_PASSWORD)

            if imgui.button("Login"):
                success, msg = db.login_user(username, password)
                status_message = msg
                if success:
                    print(msg)

            if imgui.button("Register"):
                show_register_form = True
                status_message = ""

            imgui.text(status_message)
            imgui.end()
        else:
            # Registration Form
            imgui.begin("Register New User", True)

            imgui.text("Username:")
            changed, username = imgui.input_text("##reg_username_input", username, 256)

            imgui.text("Password:")
            changed, password = imgui.input_text("##reg_password_input", password, 256,
                                                 imgui.INPUT_TEXT_PASSWORD)

            if imgui.button("Register"):
                success, msg = db.register_user(username, password)
                status_message = msg
                if success:
                    show_register_form = False

            if imgui.button("Back"):
                show_register_form = False
                status_message = ""

            imgui.text(status_message)
            imgui.end()

        # Rendering
        gl.glClearColor(0.2, 0.2, 0.2, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        renderer.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    db.close()
    renderer.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()