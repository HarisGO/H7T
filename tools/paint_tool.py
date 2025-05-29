# tools/paint_tool_gui.py

import turtle
import time

def main():
    """
    A simple GUI Paint Tool using the turtle module.
    This tool opens a NEW graphical window and does NOT run in the terminal.
    Press the ESC key on the drawing window to close it.
    """
    print("--- GUI Paint Tool (Separate Window) ---")
    print("Launching the drawing window now...")
    print("Draw using the arrow keys (Up, Down, Left, Right) and spacebar.")
    print("Press the 'ESC' key on the drawing window to exit.")
    print("--------------------------------------")

    try:
        # Set up the screen
        screen = turtle.Screen()
        screen.setup(width=600, height=600)
        screen.title("H7T Simple Paint Tool")
        screen.bgcolor("white")
        screen.tracer(0) # Turn off screen updates for smoother drawing

        # Set up the turtle (pen)
        pen = turtle.Turtle()
        pen.speed(0) # Fastest speed
        pen.penup() # Start with pen up
        pen.goto(0, 0) # Start at center
        pen.pendown() # Pen down to start drawing
        pen.pencolor("black")
        pen.pensize(2)

        # Drawing controls
        move_distance = 10 # Pixels to move
        current_pen_down = True

        def toggle_pen():
            nonlocal current_pen_down
            if current_pen_down:
                pen.penup()
                current_pen_down = False
            else:
                pen.pendown()
                current_pen_down = True

        def move_up():
            pen.setheading(90)
            pen.forward(move_distance)
            screen.update()

        def move_down():
            pen.setheading(270)
            pen.forward(move_distance)
            screen.update()

        def move_left():
            pen.setheading(180)
            pen.forward(move_distance)
            screen.update()

        def move_right():
            pen.setheading(0)
            pen.forward(move_distance)
            screen.update()

        def clear_drawing():
            pen.clear()
            screen.update()

        def increase_size():
            new_size = pen.pensize() + 1
            if new_size <= 10: # Max pen size
                pen.pensize(new_size)

        def decrease_size():
            new_size = pen.pensize() - 1
            if new_size >= 1: # Min pen size
                pen.pensize(new_size)

        def change_color_red():
            pen.pencolor("red")

        def change_color_green():
            pen.pencolor("green")

        def change_color_blue():
            pen.pencolor("blue")

        def exit_drawing():
            # This will break the mainloop
            # It's important to do this for clean exit
            screen.bye()


        # Keyboard bindings
        screen.listen()
        screen.onkey(move_up, "Up")
        screen.onkey(move_down, "Down")
        screen.onkey(move_left, "Left")
        screen.onkey(move_right, "Right")
        screen.onkey(toggle_pen, "space") # Spacebar to toggle pen up/down
        screen.onkey(clear_drawing, "c")   # 'c' to clear drawing
        screen.onkey(increase_size, "plus") # '+' to increase pen size
        screen.onkey(increase_size, "equal") # '=' also works for plus
        screen.onkey(decrease_size, "minus") # '-' to decrease pen size
        screen.onkey(change_color_red, "r")
        screen.onkey(change_color_green, "g")
        screen.onkey(change_color_blue, "b")
        screen.onkey(exit_drawing, "Escape") # ESC key to exit

        # Keep the window open until closed manually or by ESC key
        # Using a loop with screen.update() and time.sleep() as screen.mainloop() can block
        # the program in ways that interfere with H7T's simple execution model.
        while True:
            screen.update()
            time.sleep(0.01) # Small delay to prevent busy-waiting
            if not turtle.Screen()._RUNNING: # Check if screen is still running
                break

    except turtle.Terminator:
        print("\nDrawing window closed by user (ESC key detected).")
    except Exception as e:
        print(f"\nAn error occurred in the drawing tool: {e}")
    finally:
        # Ensure cleanup in case of unexpected exit
        if turtle.Screen()._RUNNING:
            turtle.done() # This can cause issues in some environments.
                          # screen.bye() is usually safer for programmatic close.
            print("Cleanup: turtle.done() called.")
        print("GUI Paint Tool finished its execution.")


# Do NOT call main() here. H7T does that automatically.
