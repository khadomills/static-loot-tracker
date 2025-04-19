import customtkinter as ctk
import db
import asyncio
from xivapi2 import XivApiClient
from PIL import Image, ImageTk


# --- Main App ---
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Static Loot Tracker")
        self.geometry("1920x1080")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Configure layout grid to center child frames
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.show_frame(StaticSelectionFrame)

    def show_frame(self, page_class):
        # Create the frame if not already created
        if page_class not in self.frames:
            frame = page_class(parent=self.container, controller=self)
            self.frames[page_class] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Hide all frames
        for frame in self.frames.values():
            frame.grid_remove()

        # Show the requested frame
        self.frames[page_class].grid()


class StaticSelectionFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # load and create background image

        self.bg_image = ctk.CTkImage(Image.open("assets/m8bg.png"),
                                     size=(1920, 1080))
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # Add overlay for widgets
        self.overlay_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.overlay_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Add prompt and buttons for regular or split static
        ctk.CTkLabel(self.overlay_frame, text="Initial Setup", font=("Arial", 20)).pack(pady=20)
        ctk.CTkLabel(
            self.overlay_frame,
            text="Please select if you're doing regular runs or splits:",
            font=("Arial", 15)
        ).pack(padx=20, pady=20)

        ctk.CTkButton(
            self.overlay_frame,
            text="Regular Setup",
            command=lambda: self.on_click_regular(controller)
        ).pack(pady=10)

        ctk.CTkButton(
            self.overlay_frame,
            text="Splits Setup",
            command=lambda: self.on_click_splits(controller)
        ).pack(pady=10)

    # Button handlers to set static type and continue setup
    def on_click_regular(self, controller):
        db.set_type(1)
        controller.show_frame(StaticSetupFrame)

    def on_click_splits(self, controller):
        db.set_type(2)
        controller.show_frame(StaticSetupFrame)


# Frame for static member entry
class StaticSetupFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure the grid columns to be equally spaced
        for i in range(8):  # 8 roles
            self.grid_columnconfigure(i, weight=1)

        # Add each label to its own column in the same row
        labels = [
            "DPS One", "DPS Two", "DPS Three", "DPS Four",
            "Tank One", "Tank Two", "Healer One", "Healer Two"
        ]

        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(self, text=label_text, font=("Arial", 20))
            label.grid(row=0, column=i, padx=10, pady=(20, 0), sticky="ew")

        # If splits, add split group labels
        if db.check_type() == 2:

            # Add each label to its own column in the same row
            labels = [
                "Split Group 1", "Split Group 2", "Split Group 1", "Split Group 2",
                "Split Group 1", "Split Group 2", "Split Group 1", "Split Group 2"
            ]

            for i, label_text in enumerate(labels):
                label = ctk.CTkLabel(self, text=label_text, font=("Arial", 15))
                label.grid(row=1, column=i, padx=10, pady=5, sticky="ew")



# icon fetching from xivapi
async def main():
    client = XivApiClient()
    async for row in client.sheet_rows("Item", fields=["Name", "LevelItem", "Icon"]):
        if int(row.fields["LevelItem"]["value"]) >= 740:
            print(
                f"ID: {row.row_id}, Name: {row.fields["Name"]}, Item Level: {row.fields["LevelItem"]["value"]}, Icon id: {row.fields["Icon"]["id"]}")


if __name__ == "__main__":
    db.init_db()
    app = MainApp()
    app.mainloop()

# asyncio.run(main())


# db.add_member(
#     name="Alisaie",
#     job="RDM",
#     priority=1,
#     curr_weapon=1001,
#     bis_weapon=2001,
#     curr_head=1002,
#     bis_head=2002,
#     curr_body=1003,
#     bis_body=2003,
#     curr_gloves=1004,
#     bis_gloves=2004,
#     curr_feet=1005,
#     bis_feet=2005,
#     curr_earring=1006,
#     bis_earring=2006,
#     curr_neck=1007,
#     bis_neck=2007,
#     curr_wrist=1008,
#     bis_wrist=2008,
#     curr_ring1=1009,
#     bis_ring1=2009,
#     curr_ring2=1010,
#     bis_ring2=2010
# )
