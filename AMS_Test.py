import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox
import os

# Main class for the IdentiTech application
class IdentiTechApp:

    def __init__(self, root):
        self.root = root
        self.root.title("IdentiTech")
        self.root.iconbitmap("Logo.ico")

        self.menu_open = False
        self.enroll_frame_visible = False
        self.edit_frame_visible = False
        self.delete_frame_visible = False
        self.menu_frame_width = 200
        self.scenery_visible = False  
        self.is_admin_signed_in = False
        self.password_visible = False 

    # Initialize angles for loader animation
        self.angle1 = 0
        self.angle2 = 0
        self.angle3 = 0
        self.angle4 = 0

    # Cache for resized images
        self.image_cache = {}

    # Initialize GUI components
        self.set_window_size()
        self.load_icons()
        self.create_canvas()
        self.create_menu_button()
        self.animate_loader()
        self.root.bind("<Configure>", self.on_resize)

# Set the window size to 90% of the screen size
    def set_window_size(self, width_percentage=0.8, height_percentage=0.):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * width_percentage)
        window_height = int(screen_height * height_percentage)
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Load the icons and resize them as needed
    def load_icons(self):
        self.icons = {}
        icon_files = {
            "Menu_icon": ("Menuicon.png", 30, 30, False),
            "Menu_iconL": ("MenuiconL.png", 30, 30, False),
            "Logo_icon": ("IdentiTech.png", 50, 50, True),
            "Enroll_icon": ("Enrollicon.png", 30, 30, True),
            "Edit_icon": ("Editicon.png", 30, 30, True),
            "Delete_icon": ("Deleteicon.png", 30, 30, True),
            "Exit_icon": ("Exiticon.png", 30, 30, True),
            "Eye_icon": ("Eye.png", 30, 30, True),
            "NCF_icon": ("NCF.png", 100, 100, False),
            "ICpEP_icon": ("ICpEP.png", 100, 100, False),
        }

        for key, (path, width, height, remove_bg) in icon_files.items():
            self.icons[key] = self.resize_image(path, width, height, remove_bg)

# Resize the image and remove the background if needed
    def resize_image(self, image_path, width, height, remove_bg=True):
        cache_key = (image_path, width, height, remove_bg)
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        if not os.path.exists(image_path):
            print(f"Image file {image_path} not found.")
            return None

        with Image.open(image_path).convert("RGBA") as img:
            img = img.resize((width, height), Image.Resampling.LANCZOS)

            if remove_bg:
                data = img.getdata()
                new_data = []
                for item in data:
                    if item[:3] == (255, 255, 255):
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                img.putdata(new_data)

        # Convert to ImageTk
            image_tk = ImageTk.PhotoImage(img)
            self.image_cache[cache_key] = image_tk
            return image_tk

# Create the canvas for the background image
    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.background_image_tk = None
        self.update_background_image()

# Create the menu button
    def create_menu_button(self):
        self.menu_button = tk.Button(
            self.root,
            image=self.icons.get("Menu_icon"),
            borderwidth=0,
            command=self.toggle_menu,
            bg='#003600',
            highlightthickness=0
        )
        self.menu_button.place(x=0, y=self.root.winfo_height() // 2 + 200)

# Update the background image when the window is resized
    def on_resize(self, event):
        if hasattr(self, 'resize_after_id'):
            self.root.after_cancel(self.resize_after_id)
        self.resize_after_id = self.root.after(100, self.update_background_image)
# Update the background image based on the window size
    def update_background_image(self, event=None):
        screen_width = self.root.winfo_width()
        screen_height = self.root.winfo_height()

        if self.menu_open:
            available_width = screen_width - self.menu_frame_width
            bg_x_position = self.menu_frame_width
        else:
            available_width = screen_width
            bg_x_position = 5

        margin_in_pixels = 5
        background_width = available_width - 2 * margin_in_pixels
        background_height = screen_height - 2 * margin_in_pixels
        bg_y_position = margin_in_pixels 

        # Resize and round the background image
        background_image = self.resize_image("BG2.jpg", background_width, background_height)
        if background_image is None:
            return 
        radius = 30

        # Create rounded image
        with Image.open("BG2.jpg").convert("RGBA") as img:
            img = img.resize((background_width, background_height), Image.Resampling.LANCZOS)
            mask = Image.new('L', (background_width, background_height), 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, background_width, background_height), radius=radius, fill=255)
            img.putalpha(mask)
            rounded_bg_image = ImageTk.PhotoImage(img)
            self.image_cache[("BG2.jpg", background_width, background_height, False)] = rounded_bg_image

        # Update the canvas with the new background image
        self.canvas.background_image_tk = rounded_bg_image
        self.canvas.delete("all")
        self.bg_image_id = self.canvas.create_image(bg_x_position, bg_y_position, anchor=tk.NW, image=rounded_bg_image)
        self.bg_x_position = bg_x_position
        self.bg_y_position = bg_y_position
        self.background_width = background_width
        self.background_height = background_height

        corner_image = self.resize_image("tap.png", 100, 100)
        if corner_image:
            corner_x = self.bg_x_position + self.background_width // 2 
            corner_y = self.bg_y_position + self.background_height // 2  
            self.tap_image_id = self.canvas.create_image(corner_x, corner_y, image=corner_image)

        if self.scenery_visible:
            self.canvas.background_image_tk = background_image
            self.canvas.delete("all")
            self.bg_image_id = self.canvas.create_image(bg_x_position, bg_y_position, anchor=tk.NW, image=background_image)

        corner_image = self.resize_image("ICpEP.png", 150, 150)
        if corner_image:
            corner_x = bg_x_position + background_width - 150
            corner_y = bg_y_position  
            self.canvas.create_image(corner_x, corner_y, anchor=tk.NW, image=corner_image)
            self.canvas.corner_image_tk = corner_image
        
        corner_image = self.resize_image("NCF.png", 150, 150)  
        if corner_image:
            corner_x = bg_x_position + 10 
            corner_y = bg_y_position + 10 
            self.canvas.create_image(corner_x, corner_y, anchor=tk.NW, image=corner_image)
            self.canvas.corner_image_tk = corner_image

# Toggle the scenery visibility
    def toggle_change_scenery(self):
        self.scenery_visible = not self.scenery_visible
        self.update_background_image()
        
        corner_image = self.resize_image("rectangle.png", 350, 550)
        if corner_image:
            corner_x = self.bg_x_position + self.background_width - 370
            corner_y = self.bg_y_position + self.background_height - 300 
            self.rectangle_image_id = self.canvas.create_image(corner_x, corner_y, image=corner_image)
        
        if not self.scenery_visible:
            if hasattr(self, 'rectangle_image_id'):
                self.canvas.delete(self.rectangle_image_id)
            

# Toggle the menu
    def toggle_menu(self):
        if not self.menu_open:
            self.open_menu()
        else:
            self.close_menu()

# Create the menu frame
    def open_menu(self):
        self.menu_frame = tk.Frame(self.root, bg="white", bd=0)
        self.menu_frame.place(relx=0.0, rely=0.0, anchor="nw", height=self.root.winfo_height(), width=self.menu_frame_width)

        Logo_lbl = tk.Label(
            self.menu_frame,
            text="  IdentiTech",
            font=("Roboto mono", 15),
            bg='white',
            fg='black',
            image=self.icons.get("Logo_icon"),
            compound="left"
        )
        Logo_lbl.place(x=10, y=10)

        buttons_info = [
            ("Enroll", "Enroll_icon", self.toggle_enroll_frame, 100),
            ("Edit", "Edit_icon", self.toggle_edit_frame, 150),
            ("Delete", "Delete_icon", self.toggle_delete_frame, 200),
            ("Scenery", "Eye_icon", self.toggle_change_scenery, 250),
            ("Exit", "Exit_icon", self.root.quit, 300),
        ]

        for text, icon_key, command, y in buttons_info:
            btn = tk.Button(
                self.menu_frame,
                text=f"   {text}",
                font=("Roboto mono", 15),
                bg='white',
                fg='black',
                image=self.icons.get(icon_key),
                borderwidth=0,
                compound="left",
                command=command
            )
            btn.place(x=10, y=y)

    # Sign In Button
        SignIn_btn = tk.Button(
            self.menu_frame,
            text="Sign In",
            font=("Roboto mono", 15),
            bg='Green',
            fg='black',
            command=self.sign_in 
        )
        SignIn_btn.place(x=40, y=600)

    # Update Menu button to close icon
        self.menu_button.place(x=self.menu_frame_width, y=self.root.winfo_height() // 2 )
        self.menu_button.config(image=self.icons.get("Menu_iconL"), command=self.close_menu)
        self.menu_open = True
        self.update_background_image()

    def close_menu(self):
        self.menu_frame.destroy()
        self.menu_button.config(image=self.icons.get("Menu_icon"), command=self.toggle_menu)
        self.menu_button.place(x=0, y=self.root.winfo_height() // 2 )
        self.menu_open = False
        self.update_background_image()
        
# Create the admin sign-in form
    def sign_in(self):
        self.open_signin_window()

    def submit_enroll(self):
        name = self.enroll_name_entry.get()
    # Call the sign-in form before enrolling
        print(f"Enrolling user: {name}")
        self.enroll_name_entry.delete(0, tk.END)
        self.open_signin_window()

# Check if the window is already open to avoid multiple instances
    def open_signin_window(self):
        if hasattr(self, 'signin_window') and self.signin_window.winfo_exists():
            self.signin_window.lift()
            return

        # Create a new top-level window (popup)
        self.signin_window = tk.Toplevel(self.root)
        self.signin_window.title("Admin Sign-In")
        self.signin_window.geometry("300x200")  # Set the size of the window
        self.signin_window.iconbitmap("Logo.ico")

        # Create a frame for the sign-in form
        signin_frame = tk.Frame(self.signin_window, bg="lightgray", padx=25, pady=40)
        signin_frame.pack(expand=True, fill=tk.BOTH)

         # Define custom fonts
        label_font = ("Arial", 10, "bold")  # Font for labels
        entry_font = ("Arial", 10)          # Font for input boxes
        button_font = ("Arial", 10, "bold") # Font for buttons

        # Username label and entry
        username_label = tk.Label(signin_frame, text="Username: ", bg="lightgray", font=label_font)
        username_label.grid(row=0, column=0, sticky="w", pady=10)
        self.username_entry = tk.Entry(signin_frame, font=entry_font, width=20)
        self.username_entry.grid(row=0, column=1, pady=10)

        # Password label and entry
        password_label = tk.Label(signin_frame, text="Password: ", bg="lightgray", font=label_font)
        password_label.grid(row=1, column=0, sticky="w", pady=10)
        self.password_entry = tk.Entry(signin_frame, show="*", font=entry_font, width=20)
        self.password_entry.grid(row=1, column=1, pady=10)

        # Resize the eye icon using Pillow
        eye_image = Image.open("Eye.png")  # Load the eye icon
        resized_eye_image = eye_image.resize((16, 16),  Image.Resampling.LANCZOS)  # Resize to 20x20 pixels
        self.eye_icon = ImageTk.PhotoImage(resized_eye_image)  # Convert to PhotoImage

        # Eye icon button to show/hide the password
        self.eye_button = tk.Button(signin_frame, image=self.eye_icon, command=self.toggle_password_visibility, borderwidth=0)
        self.eye_button.grid(row=1, column=1, pady=0, padx=(130, 0))

        # Sign In button
        signin_btn = tk.Button(signin_frame, text="Sign In", command=self.process_signin, font=button_font)
        signin_btn.grid(row=2, column=1, pady=15, padx=(0, 50))

    def toggle_password_visibility(self):
        if self.password_visible:
            self.password_entry.config(show="*")
            self.password_visible = False
        else:
            self.password_entry.config(show="")
            self.password_visible = True

    def process_signin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "ADMIN" and password == "pass1234":
            messagebox.showinfo("Success", "Signed in as Admin!")
            self.signin_window.destroy()
            self.is_admin_signed_in = True  
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

# Enroll Frame
    def toggle_enroll_frame(self):
        if not self.enroll_frame_visible:
            self.close_all_frames(exclude="enroll")
            self.enroll_frame = tk.Frame(
                self.root,
                bg="Green",
                width=400,
                height=self.root.winfo_height()
            )
            self.enroll_frame.place(x=self.menu_frame_width, y=0, anchor="nw")
            self.enroll_frame.pack_propagate(False)

            label = tk.Label(
                self.enroll_frame,
                text="Enroll User",
                font=("Roboto mono", 15),
                bg='green',
                fg='black'
            )
            label.pack(padx=10, pady=10)
            name_label = tk.Label(self.enroll_frame, text="Name:", bg="Green", fg="black")
            name_label.pack(pady=(20, 5))
            self.enroll_name_entry = tk.Entry(self.enroll_frame)
            self.enroll_name_entry.pack(pady=5)

            submit_btn = tk.Button(self.enroll_frame, text="Submit", command=self.submit_enroll)
            submit_btn.pack(pady=20)

            self.enroll_frame_visible = True
        else:
            self.enroll_frame.destroy()
            self.enroll_frame_visible = False

# Edit Frame
    def toggle_edit_frame(self):
        if not self.edit_frame_visible:
            self.close_all_frames(exclude="edit")
            self.edit_frame = tk.Frame(
                self.root,
                bg="Green",
                width=400,
                height=self.root.winfo_height()
            )
            self.edit_frame.place(x=self.menu_frame_width, y=0, anchor="nw")
            self.edit_frame.pack_propagate(False)

            label = tk.Label(
                self.edit_frame,
                text="Edit User",
                font=("Roboto mono", 15),
                bg='Green',
                fg='black'
            )
            label.pack(padx=10, pady=10)
            user_label = tk.Label(self.edit_frame, text="User ID:", bg="Green", fg="black")
            user_label.pack(pady=(20, 5))
            self.edit_user_entry = tk.Entry(self.edit_frame)
            self.edit_user_entry.pack(pady=5)

            update_btn = tk.Button(self.edit_frame, text="Update", command=self.submit_edit)
            update_btn.pack(pady=20)

            self.edit_frame_visible = True
        else:
            self.edit_frame.destroy()
            self.edit_frame_visible = False

# Deletion Frame
    def toggle_delete_frame(self):
        if not self.delete_frame_visible:
            self.close_all_frames(exclude="delete")
            self.delete_frame = tk.Frame(
                self.root,
                bg="Green",
                width=400,
                height=self.root.winfo_height()
            )
            self.delete_frame.place(x=self.menu_frame_width, y=0, anchor="nw")
            self.delete_frame.pack_propagate(False)

            label = tk.Label(
                self.delete_frame,
                text="Delete User",
                font=("Roboto mono", 15),
                bg='Green',
                fg='black'
            )
            label.pack(padx=10, pady=10)
            user_label = tk.Label(self.delete_frame, text="User ID:", bg="Green", fg="black")
            user_label.pack(pady=(20, 5))
            self.delete_user_entry = tk.Entry(self.delete_frame)
            self.delete_user_entry.pack(pady=5)

            delete_btn = tk.Button(self.delete_frame, text="Delete", command=self.submit_delete)
            delete_btn.pack(pady=20)

            self.delete_frame_visible = True
        else:
            self.delete_frame.destroy()
            self.delete_frame_visible = False

# Close all frames except the one specified in exclude
    def close_all_frames(self, exclude=None):
        """Close all frames except the one specified in exclude."""
        if exclude != "enroll" and self.enroll_frame_visible:
            self.enroll_frame.destroy()
            self.enroll_frame_visible = False
        if exclude != "edit" and self.edit_frame_visible:
            self.edit_frame.destroy()
            self.edit_frame_visible = False
        if exclude != "delete" and self.delete_frame_visible:
            self.delete_frame.destroy()
            self.delete_frame_visible = False

# Clear previous loader arcs if any
    def animate_loader(self):
        if self.scenery_visible == False:
            loader_tags = ["loader_arc1", "loader_arc2", "loader_arc3", "loader_arc4",
                        "loader_outline1", "loader_outline2", "loader_outline3", "loader_outline4"]
            for tag in loader_tags:
                self.canvas.delete(tag)

            if not hasattr(self, 'bg_x_position'):
            # If background position not set yet, skip animation
                self.root.after(50, self.animate_loader)
                return

            center_x = self.bg_x_position + self.background_width // 2
            center_y = self.bg_y_position + self.background_height // 2

            loaders = [
                {"radius": 150, "angle": self.angle1, "extent": 90, "outline": "lightblue", "width": 30, "speed": 2, "tag_arc": "loader_arc1", "tag_outline": "loader_outline1"},
                {"radius": 120, "angle": -self.angle2, "extent": 90, "outline": "#6FC0D8", "width": 20, "speed": 4, "tag_arc": "loader_arc2", "tag_outline": "loader_outline2"},
                {"radius": 90,  "angle": self.angle3, "extent": 90, "outline": "#3B9EBF", "width": 15, "speed": 3, "tag_arc": "loader_arc3", "tag_outline": "loader_outline3"},
                {"radius": 60,  "angle": -self.angle4, "extent": 90, "outline": "#187593", "width": 10, "speed": 6, "tag_arc": "loader_arc4", "tag_outline": "loader_outline4"},
            ]

            for loader in loaders:
                r = loader["radius"]
                self.canvas.create_oval(
                    center_x - r, center_y - r,
                    center_x + r, center_y + r,
                    outline=loader["outline"],
                    width=1,
                    tag=loader["tag_outline"]
                )
                self.canvas.create_arc(
                    center_x - r, center_y - r,
                    center_x + r, center_y + r,
                    start=loader["angle"],
                    extent=loader["extent"],
                    outline=loader["outline"],
                    width=loader["width"],
                    style=tk.ARC,
                    tag=loader["tag_arc"]
                )
        # Update angles for next frame
            self.angle1 = (self.angle1 + 2) % 360
            self.angle2 = (self.angle2 + 4) % 360
            self.angle3 = (self.angle3 + 3) % 360
            self.angle4 = (self.angle4 + 6) % 360
        else:
            self.hide_loaders()
        # Schedule next animation frame
        self.root.after(10, self.animate_loader)

    def hide_loaders(self):
        loader_tags = ["loader_arc1", "loader_arc2", "loader_arc3", "loader_arc4",
                      "loader_outline1", "loader_outline2", "loader_outline3", "loader_outline4"]
        for tag in loader_tags:
            self.canvas.delete(tag)

    def submit_edit(self):
        user_id = self.edit_user_entry.get()
        print(f"Editing user with ID: {user_id}")
        self.edit_user_entry.delete(0, tk.END)

    def submit_delete(self):
        user_id = self.delete_user_entry.get()
        print(f"Deleting user with ID: {user_id}")
        self.delete_user_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = IdentiTechApp(root)
    root.mainloop()
