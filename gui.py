import customtkinter as ctk
import tkinter as tk
import db
import asyncio
from xivapi2 import XivApiClient
from PIL import Image, ImageTk

# Frame for raid member entry
class StaticSetupFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Main layout structure
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # -------------------------
        # Fixed Header Section
        # -------------------------
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        self.header_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Row 0-2 content here
        labels = [
            "DPS One", "DPS Two", "DPS Three", "DPS Four",
            "Tank One", "Tank Two", "Healer One", "Healer Two"
        ]

        for i, text in enumerate(labels):
            ctk.CTkLabel(self.header_frame, text=text, font=("Segoe UI", 20)).grid(row=0, column=i, padx=10, pady=10)

        for i in range(8):
            ctk.CTkLabel(self.header_frame, text="Name: ", font=("Segoe UI", 15)).grid(row=1, column=i, sticky="w", padx=10)

        nameone_entry = ctk.CTkEntry(self.header_frame, placeholder_text="DPS One")
        nameone_entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        nametwo_entry = ctk.CTkEntry(self.header_frame, placeholder_text="DPS Two")
        nametwo_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        namethree_entry = ctk.CTkEntry(self.header_frame, placeholder_text="DPS Three")
        namethree_entry.grid(row=3, column=2, padx=20, pady=10, sticky="ew")

        namefour_entry = ctk.CTkEntry(self.header_frame, placeholder_text="DPS Four")
        namefour_entry.grid(row=3, column=3, padx=20, pady=10, sticky="ew")

        namefive_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Tank One")
        namefive_entry.grid(row=3, column=4, padx=20, pady=10, sticky="ew")

        namesix_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Tank Two")
        namesix_entry.grid(row=3, column=5, padx=20, pady=10, sticky="ew")

        nameseven_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Healer One")
        nameseven_entry.grid(row=3, column=6, padx=20, pady=10, sticky="ew")

        nameeight_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Healer Two")
        nameeight_entry.grid(row=3, column=7, padx=20, pady=10, sticky="ew")

        for i in range(8):
            label = ctk.CTkLabel(self.header_frame, text=f"Loot priority: {i + 1}", font=("Segoe UI", 20))
            label.grid(row=4, column=i, padx=20, sticky="w")

        # Job selection
        tanks = ["PLD", "WAR", "DRK", "GNB"]
        healers = ["WHM", "SCH", "AST", "SGE"]
        dps = ["MNK", "DRG", "NIN", "SAM", "RPR", "VPR", "BRD", "MCH", "DNC", "BLM", "SMN", "RDM", "PCT"]

        # Create a frame in each row 5 column
        self.header_frame.job_selection_frames = []
        self.header_frame.job_icon_labels = []

        # DPS frames
        for col in range(4):
            frame = ctk.CTkFrame(self.header_frame, width=200, height=50, fg_color="#80211b", corner_radius=10)
            frame.grid(row=5, column=col, padx=10, pady=10, sticky="nsew")
            self.header_frame.job_selection_frames.append(frame)

            # Load initial icon
            if col == 0:
                icon_path = "assets/jobicons/SAM.png"
            elif col == 1:
                icon_path = "assets/jobicons/VPR.png"
            elif col == 2:
                icon_path = "assets/jobicons/BLM.png"
            else:
                icon_path = "assets/jobicons/BRD.png"

            icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(42, 42))

            # Create icon label and store it
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image  # Prevent garbage collection
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.header_frame.job_icon_labels.append(icon_label)

            # Define the change_icon function inline with label binding
            def change_icon(job, label=icon_label):
                new_icon = ctk.CTkImage(Image.open(f"assets/jobicons/{job}.png"), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon  # Preserve reference

            # Job selection dropdown
            job_dropdown = ctk.CTkOptionMenu(
                frame,
                values=dps,
                command=lambda value, label=icon_label: change_icon(value, label)
            )
            job_dropdown.pack(pady=15)

        # Tank Frames
        for col in range(4, 6):
            frame = ctk.CTkFrame(self.header_frame, width=200, height=50, fg_color="#1d1269", corner_radius=10)
            frame.grid(row=5, column=col, padx=10, pady=10, sticky="nsew")
            self.header_frame.job_selection_frames.append(frame)

            # Load initial icon
            if col == 4:
                icon_path = "assets/jobicons/WAR.png"
            else:
                icon_path = "assets/jobicons/DRK.png"

            icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(42, 42))

            # Create icon label and store it
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image  # Prevent garbage collection
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.header_frame.job_icon_labels.append(icon_label)

            # Define the change_icon function inline with label binding
            def change_icon(job, label=icon_label):
                new_icon = ctk.CTkImage(Image.open(f"assets/jobicons/{job}.png"), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon  # Preserve reference

            # Job selection dropdown
            job_dropdown = ctk.CTkOptionMenu(
                frame,
                values=tanks,
                command=lambda value, label=icon_label: change_icon(value, label)
            )
            job_dropdown.pack(pady=15)

        # Healer Frames
        for col in range(6,8):
            frame = ctk.CTkFrame(self.header_frame, width=200, height=50, fg_color="#0d610f", corner_radius=10)
            frame.grid(row=5, column=col, padx=10, pady=10, sticky="nsew")
            self.header_frame.job_selection_frames.append(frame)

            # Load initial icon
            if col == 0:
                icon_path = "assets/jobicons/AST.png"
            else:
                icon_path = "assets/jobicons/SCH.png"

            icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(42, 42))

            # Create icon label and store it
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image  # Prevent garbage collection
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.header_frame.job_icon_labels.append(icon_label)

            # Define the change_icon function inline with label binding
            def change_icon(job, label):
                new_icon = ctk.CTkImage(Image.open(f"assets/jobicons/{job}.png"), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon  # Preserve reference

            # Job selection dropdown
            job_dropdown = ctk.CTkOptionMenu(
                frame,
                values=healers,
                command=lambda value, label=icon_label: change_icon(value, label)
            )
            job_dropdown.pack(pady=15)

        # -------------------------
        # Scrollable Body Section
        # -------------------------
        self.body_frame = ctk.CTkScrollableFrame(self, label_text="", height=800)
        self.body_frame.grid(row=1, column=0, sticky="nsew")
        self.body_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Starting Gear Selection

        for col in range(8):
            label = ctk.CTkLabel(self.body_frame, text=f"Current Gear: ", font=("Segoe UI", 20))
            label.grid(row=6, column=col, padx=20, sticky="w")

            w_label = ctk.CTkLabel(self.body_frame, text="Weapon: ", font=("Segoe UI", 15))
            w_label.grid(row=7, column=col, padx=20, sticky="w")

        # Starting Weapon Selection

        weapons = ["Crafted", "Trial", "Tome", "Aug.Tome", "Savage"]

        # Create a frame in each row 5 column
        self.body_frame.curr_weapon_selection_frames = []
        self.body_frame.curr_weapon_icon_labels = []

        for col in range(8):
            frame = ctk.CTkFrame(self.body_frame, width=200, height=50, fg_color="transparent", corner_radius=10)
            frame.grid(row=8, column=col, padx=10, pady=10, sticky="nsew")
            self.body_frame.curr_weapon_selection_frames.append(frame)

            icon_path = "assets/looticons/craftedgear_icon.png"

            icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(42, 42))

            # Create icon label and store it
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image  # Prevent garbage collection
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.body_frame.curr_weapon_icon_labels.append(icon_label)

            # Define the change_icon function inline with label binding
            def change_weapon_icon(weapon, label=icon_label):
                if weapon == "Crafted":
                    icon_path = "assets/looticons/craftedgear_icon.png"

                elif weapon == "Trial":
                    icon_path = "assets/looticons/trial_icon.png"

                elif weapon == "Tome":
                    icon_path = "assets/looticons/tome_icon.png"

                elif weapon == "Aug.Tome":
                    icon_path = "assets/looticons/tomewep_icon.png"

                elif weapon == "Savage":
                    icon_path = "assets/looticons/savraid_icon.png"

                new_icon = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon  # Preserve reference

            # Weapon selection dropdown
            weapon_dropdown = ctk.CTkOptionMenu(
                frame,
                values=weapons,
                command=lambda value, label=icon_label: change_weapon_icon(value, label)
            )
            weapon_dropdown.pack(pady=15)

        # Remaining gear options
        gear = ["Crafted", "Tome", "Aug.Tome", "Nm Raid", "Savage"]

        # Create a frame in each row 5 column
        self.body_frame.curr_head_selection_frames = []
        self.body_frame.curr_head_icon_labels = []

        # Head
        for col in range(8):

            w_label = ctk.CTkLabel(self.body_frame, text="Head: ", font=("Segoe UI", 15))
            w_label.grid(row=9, column=col, padx=20, sticky="w")

            frame = ctk.CTkFrame(self.body_frame, width=200, height=50, fg_color="transparent", corner_radius=10)
            frame.grid(row=10, column=col, padx=10, pady=10, sticky="nsew")
            self.body_frame.curr_head_selection_frames.append(frame)

            icon_path = "assets/looticons/craftedgear_icon.png"

            icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(42, 42))

            # Create icon label and store it
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image  # Prevent garbage collection
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.body_frame.curr_head_icon_labels.append(icon_label)

            # Define the change_icon function inline with label binding
            def change_head_icon(head, label=icon_label):
                if head == "Crafted":
                    icon_path = "assets/looticons/craftedgear_icon.png"

                elif head == "Tome":
                    icon_path = "assets/looticons/tome_icon.png"

                elif head == "Aug.Tome":
                    icon_path = "assets/looticons/tomeleft_icon.png"

                elif head == "Nm Raid":
                    icon_path = "assets/looticons/raid_icon.png"

                elif head == "Savage":
                    icon_path = "assets/looticons/savraid_icon.png"

                new_icon = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon  # Preserve reference

            # Head selection dropdown
            head_dropdown = ctk.CTkOptionMenu(
                frame,
                values=gear,
                command=lambda value, label=icon_label: change_head_icon(value, label)
            )
            head_dropdown.pack(pady=15)

        # Chest
        # Create a frame in each row 5 column
        self.body_frame.curr_chest_selection_frames = []
        self.body_frame.curr_chest_icon_labels = []

        for col in range(8):

            w_label = ctk.CTkLabel(self.body_frame, text="Chest: ", font=("Segoe UI", 15))
            w_label.grid(row=11, column=col, padx=20, sticky="w")

            frame = ctk.CTkFrame(self.body_frame, width=200, height=50, fg_color="transparent", corner_radius=10)
            frame.grid(row=12, column=col, padx=10, pady=10, sticky="nsew")
            self.body_frame.curr_chest_selection_frames.append(frame)

            icon_path = "assets/looticons/craftedgear_icon.png"

            icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(42, 42))

            # Create icon label and store it
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image  # Prevent garbage collection
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.body_frame.curr_chest_icon_labels.append(icon_label)

            # Define the change_icon function inline with label binding
            def change_chest_icon(chest, label=icon_label):
                if chest == "Crafted":
                    icon_path = "assets/looticons/craftedgear_icon.png"

                elif chest == "Tome":
                    icon_path = "assets/looticons/tome_icon.png"

                elif chest == "Aug.Tome":
                    icon_path = "assets/looticons/tomeleft_icon.png"

                elif chest == "Nm Raid":
                    icon_path = "assets/looticons/raid_icon.png"

                elif chest == "Savage":
                    icon_path = "assets/looticons/savraid_icon.png"

                new_icon = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon  # Preserve reference

            # Arm selection dropdown
            chest_dropdown = ctk.CTkOptionMenu(
                frame,
                values=gear,
                command=lambda value, label=icon_label: change_chest_icon(value, label)
            )
            chest_dropdown.pack(pady=15)

        # Arm
        # Create a frame in each row 5 column
        self.body_frame.curr_arm_selection_frames = []
        self.body_frame.curr_arm_icon_labels = []

        for col in range(8):

            w_label = ctk.CTkLabel(self.body_frame, text="Arm: ", font=("Segoe UI", 15))
            w_label.grid(row=13, column=col, padx=20, sticky="w")

            frame = ctk.CTkFrame(self.body_frame, width=200, height=50, fg_color="transparent", corner_radius=10)
            frame.grid(row=14, column=col, padx=10, pady=10, sticky="nsew")
            self.body_frame.curr_arm_selection_frames.append(frame)

            icon_path = "assets/looticons/craftedgear_icon.png"

            icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(42, 42))

            # Create icon label and store it
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image  # Prevent garbage collection
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.body_frame.curr_arm_icon_labels.append(icon_label)

            # Define the change_icon function inline with label binding
            def change_arm_icon(arm, label=icon_label):
                if arm == "Crafted":
                    icon_path = "assets/looticons/craftedgear_icon.png"

                elif arm == "Tome":
                    icon_path = "assets/looticons/tome_icon.png"

                elif arm == "Aug.Tome":
                    icon_path = "assets/looticons/tomeleft_icon.png"

                elif arm == "Nm Raid":
                    icon_path = "assets/looticons/raid_icon.png"

                elif arm == "Savage":
                    icon_path = "assets/looticons/savraid_icon.png"

                new_icon = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon  # Preserve reference

            # Arm selection dropdown
            arm_dropdown = ctk.CTkOptionMenu(
                frame,
                values=gear,
                command=lambda value, label=icon_label: change_arm_icon(value, label)
            )
            arm_dropdown.pack(pady=15)

        # Leg
        # Create a frame in each row 5 column
        self.body_frame.curr_leg_selection_frames = []
        self.body_frame.curr_leg_icon_labels = []

        for col in range(8):

            w_label = ctk.CTkLabel(self.body_frame, text="Leg: ", font=("Segoe UI", 15))
            w_label.grid(row=15, column=col, padx=20, sticky="w")

            frame = ctk.CTkFrame(self.body_frame, width=200, height=50, fg_color="transparent", corner_radius=10)
            frame.grid(row=16, column=col, padx=10, pady=10, sticky="nsew")
            self.body_frame.curr_leg_selection_frames.append(frame)

            icon_path = "assets/looticons/craftedgear_icon.png"

            icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(42, 42))

            # Create icon label and store it
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image  # Prevent garbage collection
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.body_frame.curr_leg_icon_labels.append(icon_label)

            # Define the change_icon function inline with label binding
            def change_leg_icon(leg, label=icon_label):
                if leg == "Crafted":
                    icon_path = "assets/looticons/craftedgear_icon.png"

                elif leg == "Tome":
                    icon_path = "assets/looticons/tome_icon.png"

                elif leg == "Aug.Tome":
                    icon_path = "assets/looticons/tomeleft_icon.png"

                elif leg == "Nm Raid":
                    icon_path = "assets/looticons/raid_icon.png"

                elif leg == "Savage":
                    icon_path = "assets/looticons/savraid_icon.png"

                new_icon = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon  # Preserve reference

            # Arm selection dropdown
            leg_dropdown = ctk.CTkOptionMenu(
                frame,
                values=gear,
                command=lambda value, label=icon_label: change_leg_icon(value, label)
            )
            leg_dropdown.pack(pady=15)

        # Ear
        self.body_frame.curr_ear_selection_frames = []
        self.body_frame.curr_ear_icon_labels = []
        for col in range(8):
            ctk.CTkLabel(self.body_frame, text="Ear: ", font=("Segoe UI", 15)).grid(row=17, column=col, padx=20, sticky="w")
            frame = ctk.CTkFrame(self.body_frame, width=200, height=50, fg_color="transparent", corner_radius=10)
            frame.grid(row=18, column=col, padx=10, pady=10, sticky="nsew")
            self.body_frame.curr_ear_selection_frames.append(frame)

            icon_path = "assets/looticons/craftedgear_icon.png"
            icon_image = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.body_frame.curr_ear_icon_labels.append(icon_label)

            def change_ear_icon(ear, label=icon_label):
                if ear == "Crafted":
                    icon_path = "assets/looticons/craftedgear_icon.png"
                elif ear == "Tome":
                    icon_path = "assets/looticons/tome_icon.png"
                elif ear == "Aug.Tome":
                    icon_path = "assets/looticons/tomeacc_icon.png"
                elif ear == "Nm Raid":
                    icon_path = "assets/looticons/raid_icon.png"
                elif ear == "Savage":
                    icon_path = "assets/looticons/savraid_icon.png"
                new_icon = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon

            ctk.CTkOptionMenu(frame, values=gear, command=lambda value, label=icon_label: change_ear_icon(value, label)).pack(pady=15)


        # Neck
        self.body_frame.curr_neck_selection_frames = []
        self.body_frame.curr_neck_icon_labels = []
        for col in range(8):
            ctk.CTkLabel(self.body_frame, text="Neck: ", font=("Segoe UI", 15)).grid(row=19, column=col, padx=20, sticky="w")
            frame = ctk.CTkFrame(self.body_frame, width=200, height=50, fg_color="transparent", corner_radius=10)
            frame.grid(row=20, column=col, padx=10, pady=10, sticky="nsew")
            self.body_frame.curr_neck_selection_frames.append(frame)

            icon_path = "assets/looticons/craftedgear_icon.png"
            icon_image = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.body_frame.curr_neck_icon_labels.append(icon_label)

            def change_neck_icon(neck, label=icon_label):
                if neck == "Crafted":
                    icon_path = "assets/looticons/craftedgear_icon.png"
                elif neck == "Tome":
                    icon_path = "assets/looticons/tome_icon.png"
                elif neck == "Aug.Tome":
                    icon_path = "assets/looticons/tomeacc_icon.png"
                elif neck == "Nm Raid":
                    icon_path = "assets/looticons/raid_icon.png"
                elif neck == "Savage":
                    icon_path = "assets/looticons/savraid_icon.png"
                new_icon = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon

            ctk.CTkOptionMenu(frame, values=gear, command=lambda value, label=icon_label: change_neck_icon(value, label)).pack(pady=15)


        # Wrist
        self.body_frame.curr_wrist_selection_frames = []
        self.body_frame.curr_wrist_icon_labels = []
        for col in range(8):
            ctk.CTkLabel(self.body_frame, text="Wrist: ", font=("Segoe UI", 15)).grid(row=21, column=col, padx=20, sticky="w")
            frame = ctk.CTkFrame(self.body_frame, width=200, height=50, fg_color="transparent", corner_radius=10)
            frame.grid(row=22, column=col, padx=10, pady=10, sticky="nsew")
            self.body_frame.curr_wrist_selection_frames.append(frame)

            icon_path = "assets/looticons/craftedgear_icon.png"
            icon_image = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.body_frame.curr_wrist_icon_labels.append(icon_label)

            def change_wrist_icon(wrist, label=icon_label):
                if wrist == "Crafted":
                    icon_path = "assets/looticons/craftedgear_icon.png"
                elif wrist == "Tome":
                    icon_path = "assets/looticons/tome_icon.png"
                elif wrist == "Aug.Tome":
                    icon_path = "assets/looticons/tomeacc_icon.png"
                elif wrist == "Nm Raid":
                    icon_path = "assets/looticons/raid_icon.png"
                elif wrist == "Savage":
                    icon_path = "assets/looticons/savraid_icon.png"
                new_icon = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon

            ctk.CTkOptionMenu(frame, values=gear, command=lambda value, label=icon_label: change_wrist_icon(value, label)).pack(pady=15)


        # Ring One
        self.body_frame.curr_ring1_selection_frames = []
        self.body_frame.curr_ring1_icon_labels = []
        for col in range(8):
            ctk.CTkLabel(self.body_frame, text="Ring 1: ", font=("Segoe UI", 15)).grid(row=23, column=col, padx=20, sticky="w")
            frame = ctk.CTkFrame(self.body_frame, width=200, height=50, fg_color="transparent", corner_radius=10)
            frame.grid(row=24, column=col, padx=10, pady=10, sticky="nsew")
            self.body_frame.curr_ring1_selection_frames.append(frame)

            icon_path = "assets/looticons/craftedgear_icon.png"
            icon_image = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.body_frame.curr_ring1_icon_labels.append(icon_label)

            def change_ring1_icon(ring, label=icon_label):
                if ring == "Crafted":
                    icon_path = "assets/looticons/craftedgear_icon.png"
                elif ring == "Tome":
                    icon_path = "assets/looticons/tome_icon.png"
                elif ring == "Aug.Tome":
                    icon_path = "assets/looticons/tomeacc_icon.png"
                elif ring == "Nm Raid":
                    icon_path = "assets/looticons/raid_icon.png"
                elif ring == "Savage":
                    icon_path = "assets/looticons/savraid_icon.png"
                new_icon = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon

            ctk.CTkOptionMenu(frame, values=gear, command=lambda value, label=icon_label: change_ring1_icon(value, label)).pack(pady=15)


        # Ring Two
        self.body_frame.curr_ring2_selection_frames = []
        self.body_frame.curr_ring2_icon_labels = []
        for col in range(8):
            ctk.CTkLabel(self.body_frame, text="Ring 2: ", font=("Segoe UI", 15)).grid(row=25, column=col, padx=20, sticky="w")
            frame = ctk.CTkFrame(self.body_frame, width=200, height=50, fg_color="transparent", corner_radius=10)
            frame.grid(row=26, column=col, padx=10, pady=10, sticky="nsew")
            self.body_frame.curr_ring2_selection_frames.append(frame)

            icon_path = "assets/looticons/craftedgear_icon.png"
            icon_image = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
            icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
            icon_label.image_ref = icon_image
            icon_label.pack(padx=(5, 0), pady=10, side="left")
            self.body_frame.curr_ring2_icon_labels.append(icon_label)

            def change_ring2_icon(ring, label=icon_label):
                if ring == "Crafted":
                    icon_path = "assets/looticons/craftedgear_icon.png"
                elif ring == "Tome":
                    icon_path = "assets/looticons/tome_icon.png"
                elif ring == "Aug.Tome":
                    icon_path = "assets/looticons/tomeacc_icon.png"
                elif ring == "Nm Raid":
                    icon_path = "assets/looticons/raid_icon.png"
                elif ring == "Savage":
                    icon_path = "assets/looticons/savraid_icon.png"
                new_icon = ctk.CTkImage(Image.open(icon_path), size=(42, 42))
                label.configure(image=new_icon)
                label.image_ref = new_icon

            ctk.CTkOptionMenu(frame, values=gear, command=lambda value, label=icon_label: change_ring2_icon(value, label)).pack(pady=15)
