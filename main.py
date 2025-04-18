import customtkinter as ctk
import db
import asyncio
from xivapi2 import XivApiClient


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

        ctk.CTkLabel(self, text="Initial Setup", font=("Arial", 20)).pack(pady=20)
        ctk.CTkLabel(
            self,
            text="Please select if you're doing regular runs or splits:",
            font=("Arial", 15)
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Regular Setup",
            command=lambda: controller.show_frame(RegularSetupPage)
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Splits Setup",
            command=lambda: controller.show_frame(SplitsSetupPage)
        ).pack(pady=10)

        def on_regular_click(self):
            print("Regular Setup Activated!")

        def on_static_click(self):
            print("Splits Setup Activated!")
            db.add_member("Khado", "GNB", 1, 3, 2, 3, 2, 3, 3, 2, 3, 3, 2, 3, )


#icon fetching
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
