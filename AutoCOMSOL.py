import sys
import customtkinter
from no_combinations import solving
import os
import time
import pandas as pd
import numpy as np
import mph
from threading import Thread
from PIL import Image


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

header_list = [ "Time","Volt_n1_V_out","Volt_p1_V_out","Volt_n2_V_out","Volt_n3_V_out","Volt_p2_V_out",
"Volt_p3_V_out","PVDF1","PVDF2", "PVDF3", "PVDF4", "PVDF5", "PVDF6","PVDF7", "PVDF8", "PVDF9"
]
parameters_names = ['active_1','active_2','active_3','active_4','active_5','active_6','active_7','active_8','active_9',]



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.no_points_to_activate = 0
        self.current_combination = ()
        self.all_combinations: any = None
        self.no_combinations = 0
        self.tabs_text = []
        self.optionvalues = []
        self.time_elapsed = 0
        self.mean_sim_time = 0
        i = 0


        # configure window
        self.title("AutoCOMSOL")
        self.geometry(f"{1200}x{550}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure((1, 2), weight=3)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        customtkinter.set_widget_scaling(1.2)
        customtkinter.set_appearance_mode("dark")

        # Left frme 
        self.left_sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.left_sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.left_sidebar_frame.grid_rowconfigure(7, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.left_sidebar_frame,text_color = "#EEC23E", text="AutoCOMSOL", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0,padx=20, pady=(20, 0))
        self.author_mark = customtkinter.CTkLabel(self.left_sidebar_frame,text_color = "#EEC23E",text="By: Joao Folhadela", anchor="w", font=customtkinter.CTkFont(size=10, weight="bold"))
        self.author_mark.grid(row=1, column=0, padx=20, pady=(0, 20))
        

        self.appearance_mode_label = customtkinter.CTkLabel(self.left_sidebar_frame,text="Appearance Mode:", anchor="w", font=customtkinter.CTkFont(size=10, weight="bold"))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(50, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.left_sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event, width= 100, height = 25)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(0, 15))



        self.ifimup_image = customtkinter.CTkImage(dark_image = Image.open("IFIMUP.png"),size=(120, 40))
        self.ifimup = customtkinter.CTkButton(self.left_sidebar_frame, image = self.ifimup_image, text = "", bg_color=("gray10", "#DCE4EE"), fg_color="transparent", state = "disabled")
        self.ifimup.grid(row=9, column=0, padx=(10,10), pady=(10, 5))


        # Right frame
        self.right_sidebar_frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)
        self.right_sidebar_frame.grid(row=0, column=4, rowspan=6)
        self.right_sidebar_frame.grid_rowconfigure(10, weight=1)

        
        self.skip = customtkinter.CTkButton(master= self.right_sidebar_frame, text= "Points to skip",
                                                     fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                     command = self.dialog_start_points)
        self.skip.grid(row=4, column=0, padx=(15, 15), pady=(5, 5), sticky = "ew")

        self.path_button = customtkinter.CTkButton(master= self.right_sidebar_frame, text= "Files path",
                                                     fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                     command = self.dialog_set_path)
        self.path_button.grid(row=5, column=0, padx=(15, 15), pady=(5, 5), sticky = "ew")

        self.no_points = customtkinter.CTkButton(master= self.right_sidebar_frame, text= "Points to activate",
                                                     fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                     command = self.dialog_points_activate)
        self.no_points.grid(row=6, column=0, padx=(15, 15), pady=(5, 5), sticky = "ew")

        self.start_sims = customtkinter.CTkButton(master= self.right_sidebar_frame, text= "Start!",
                                                     fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), 
                                                     command = self.threading)
        self.start_sims.grid(row=7, column=0, padx=(15, 15), pady=(5, 5), sticky = "ew")


        # Progress bar
        self.progressbar = customtkinter.CTkProgressBar(self, width=250, height = 20, corner_radius= 15, progress_color="Green")
        self.progressbar.grid(row=5, column=1, columnspan = 2,padx=(20, 0), pady=(20, 20), sticky = "ew")
        self.progressbar.set(0)

        self.simulation_info = customtkinter.CTkLabel(self.left_sidebar_frame, text = f"Simulation {i}/{self.no_combinations} \n Time elapsed: {round(self.time_elapsed / 60 / 60, 2)} \n ETA: {self.no_combinations - self.mean_sim_time * i}",
                                                        font=customtkinter.CTkFont(size=15, weight="bold"), fg_color= "transparent" )
        self.simulation_info.grid(row = 4, column = 0, pady = (50,5), sticky = "ew")

        self.reset_button = customtkinter.CTkButton(self.left_sidebar_frame, text = "Restart APP", bg_color= "transparent", fg_color= "red", corner_radius=5, command= self.restart_program)
        self.reset_button.grid(row = 5, column = 0, pady = (10,30), padx= (5,5))


        
        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=500)
        self.textbox.grid(row=0, column=1,rowspan = 2,columnspan = 2, padx=(10, 10), pady=(10,10), sticky="nsew")

        # create tabview
        #self.tabview = customtkinter.CTkTabview(self, width=500)
        #self.tabview.grid(row=4, column=1, rowspan = 1, columnspan = 2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        #self.tabview.grid_rowconfigure(3, weight=1)
        #self.tabview.grid_columnconfigure(2, weight=1)

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Results")
        self.scrollable_frame.grid(row=4, column=2, rowspan = 1, columnspan = 1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []

        # Add tab views for each simulation
        self.result_text_box = customtkinter.CTkTextbox(master = self)
        self.result_text_box.grid(row=4, column=1, rowspan = 1, columnspan = 1, padx=(10, 10), pady=(10, 10), sticky="ew")
    
            
        

        # Create e-tattoo image
        self.image_frame = customtkinter.CTkFrame(self.right_sidebar_frame, width = 250, height = 500,bg_color="transparent", fg_color="transparent")
        self.image_frame.grid(row=0, column=0, rowspan=3, sticky="nsew", pady = (0, 0))
        self.image_frame.grid_rowconfigure(120, weight=1)
        self.image_frame.grid_columnconfigure(120,weight=1)

        background = customtkinter.CTkImage(dark_image=Image.open("bg.png"),size=(250, 250))
        bg = customtkinter.CTkButton(self.image_frame, image=background,fg_color="transparent", text="", state = "disabled")
        bg.grid(row = 0, column = 0, rowspan = 120,columnspan = 120 , padx = (20,0), pady = (10,0))

        active_1 = customtkinter.CTkButton(self.image_frame,bg_color="#EEC23E" ,border_color="black",corner_radius= 0,
                                          border_width=2,fg_color="transparent", text="1",text_color="black", width = 25, height = 10,
                                          font=customtkinter.CTkFont(size=13, weight="bold", family = "Cascadia Code"), state = "disabled")
        
        active_2 = customtkinter.CTkButton(self.image_frame,bg_color="#EEC23E" ,border_color="black", corner_radius= 0,
                                          border_width=2,fg_color="transparent", text="2",text_color="black", width = 25, height = 10,
                                          font=customtkinter.CTkFont(size=13, weight="bold", family = "Cascadia Code"), state = "disabled")
        
        active_3 = customtkinter.CTkButton(self.image_frame,bg_color="#EEC23E" ,border_color="black", corner_radius= 0,
                                          border_width=2,fg_color="transparent", text="3",text_color="black", width = 25, height = 10,
                                          font=customtkinter.CTkFont(size=13, weight="bold", family = "Cascadia Code"), state = "disabled")
        
        active_4 = customtkinter.CTkButton(self.image_frame,bg_color="#EEC23E" ,border_color="black", corner_radius= 0,
                                          border_width=2,fg_color="transparent", text="4",text_color="black", width = 25, height = 10,
                                          font=customtkinter.CTkFont(size=13, weight="bold", family = "Cascadia Code"), state = "disabled")
        
        active_5 = customtkinter.CTkButton(self.image_frame,bg_color="#EEC23E" ,border_color="black", corner_radius= 0,
                                          border_width=2,fg_color="transparent", text="5",text_color="black", width = 25, height = 10,
                                          font=customtkinter.CTkFont(size=13, weight="bold", family = "Cascadia Code"), state = "disabled")
        
        active_6 = customtkinter.CTkButton(self.image_frame,bg_color="#EEC23E" ,border_color="black", corner_radius= 0,
                                          border_width=2,fg_color="transparent", text="6",text_color="black", width = 25, height = 10,
                                          font=customtkinter.CTkFont(size=13, weight="bold", family = "Cascadia Code"), state = "disabled")
        
        active_7 = customtkinter.CTkButton(self.image_frame,bg_color="#EEC23E" ,border_color="black", corner_radius= 0,
                                          border_width=2,fg_color="transparent", text="7",text_color="black", width = 25, height = 10,
                                          font=customtkinter.CTkFont(size=13, weight="bold", family = "Cascadia Code"), state = "disabled")
        
        active_8 = customtkinter.CTkButton(self.image_frame,bg_color="#EEC23E" ,border_color="black", corner_radius= 0,
                                          border_width=2,fg_color="transparent", text="8",text_color="black", width = 25, height = 10,
                                          font=customtkinter.CTkFont(size=13, weight="bold", family = "Cascadia Code"), state = "disabled")
        
        active_9 = customtkinter.CTkButton(self.image_frame,bg_color="#EEC23E" ,border_color="black", corner_radius= 0,
                                          border_width=2,fg_color="transparent", text="9",text_color="black", width = 25, height = 10,
                                          font=customtkinter.CTkFont(size=13, weight="bold", family = "Cascadia Code"), state = "disabled")

        self.point_imgs = [active_1, active_2, active_3, active_4, active_5, active_6, active_7, active_8, active_9]   
        active_1.grid(row = 44, column = 44)
        active_4.grid(row = 66, column = 44)                   
        active_7.grid(row = 87, column = 44)

        active_8.grid(row = 87, column = 65)
        active_5.grid(row = 66, column = 65)
        active_2.grid(row = 44, column = 65)

        active_9.grid(row = 87, column = 86)
        active_6.grid(row = 66, column = 86)
        active_3.grid(row = 44, column = 86)

    def plot_image_loop(self, parameters):
        activated_params = np.empty(9)
        for i, parameter in enumerate(parameters):   
            for j in range(0,9):
                if parameter == j+1:
                    activated_params[parameter - 1] = 1
                    self.plot_active(parameter)
                elif activated_params[parameter - 1] == 1:
                    pass
                else:
                    self.plot_inactive(parameter)

    def plot_etattoo_result(self):
        index_param = self.optionMenu.get()
        parameters = self.all_combinations[index_param - 1]
        activated_params = np.empty(9)
        for i, parameter in enumerate(parameters):   
            for j in range(0,9):
                if parameter == j+1:
                    activated_params[parameter - 1] = 1
                    self.plot_active(parameter)
                elif activated_params[parameter - 1] == 1:
                    pass
                else:
                    self.plot_inactive(parameter)
    
    def plot_image_tab(self):
        if self.tabview.get().isnumeric():
            self.active_tab = int(self.tabview.get())
            self.plot_image_loop(parameters= self.all_combinations[self.active_tab])
        else:
            self.active_tab = 0
        
    def reset_image(self, img):
        for img in self.point_imgs:
            img.configure(bg_color = "#EEC23E")

    def plot_inactive(self, parameters):
        self.point_imgs[parameters - 1].configure(bg_color = "#EEC23E")

    def plot_active(self, parameters):
        self.point_imgs[parameters - 1].configure(bg_color = "#92D050")

    def tab_handle(self, tab:tuple):
        for i in tab:
            self.plot_image_loop(parameters = i)

    def dialog_points_activate(self):
        dialog = customtkinter.CTkInputDialog(text="Type in the number of wanted activated PVDF points to simulate all combinations:", title="CTkInputDialog")
        self.no_points_to_activate = dialog.get_input()
        self.textbox.insert("0.0", f"Number of points to activate: {self.no_points_to_activate} \n")

    def dialog_set_path(self):
        dialog = customtkinter.CTkInputDialog(text="Set the path to save simulations.", title="Set path")
        self.path = dialog.get_input()
        self.textbox.insert("4.0", f"Saved files path: {self.path} \n")

    def dialog_start_points(self):
        dialog = customtkinter.CTkInputDialog(text="Set the points you want to skip", title="Set path")
        self.start_point = dialog.get_input()
        self.textbox.insert("2.0", f"Starting simulation at iteration number: {self.start_point} \n")

    def switch_toggle(self):
        self.result_text_box.delete("0.100000", "1000.1000")

        for i,switch in enumerate(self.scrollable_frame_switches):
            if switch.get():
                self.result_text_box.insert("0.0", self.tabs_text[i])
                print(f"Switch {i} toggled!")

            
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def threading(self):
        self.sim_thread=Thread(target=self.solve)
        self.sim_thread.start()

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    
    def solve(self) -> None:

        self.mean_sim_time = 0
        self.time_elapsed = 0

        output = self.textbox

        if not self.no_points_to_activate.isnumeric():
            output.insert("0.0", "Insert a valid number, from 1 to 9.")
            return
        elif int(self.no_points_to_activate) > 9:
            output.insert("0.0", "Insert a valid number, from 1 to 9.")
            return
            
            

        if not self.start_point.isnumeric():
            output.insert("2.0", "Insert a valid starting point.")
            return
        elif int(self.start_point) > 126:
            output.insert("2.0", "Insert a valid starting point.")
            return
                

        no_points_to_activate = int(self.no_points_to_activate)
        start_point = int(self.start_point)
        
        
        output.insert("6.0", "Connecting to client...\n")
        self.update()
        solver = solving(no_points_to_activate)
        client = mph.start() # may use cores = x inside, when ommitted uses all cores in the machine.
        model = client.load('automate_etattoo.mph')

        output.insert("8.0", "Connection Established, initiating simulations! \n\n")
        self.update()

        self.all_combinations = solver.all_combinations
        self.no_combinations = len(solver.all_combinations)


        for i in range(self.no_combinations):

            if start_point != 0 and i < start_point - 1:
                solver.update_active_points()

            elif i >= start_point - 1:

                print(f"Simulation {i+ 1}/{self.no_combinations}")

                self.simulation_info.configure(text = f"Simulation {i + 1}/{self.no_combinations} \n Time elapsed: {round(self.time_elapsed / 60 / 60, 1)}h \n ETA: {round((self.mean_sim_time * (self.no_combinations - start_point) - self.time_elapsed)/ 60 / 60 , 1)}h")
                self.current_combination = i
                self.optionvalues.append(i + 1)

                time_ii = time.time()

                output.insert(f"{10.0 * (i*4+1)}", f"\n Beginning simulation: {i + 1} \n")


                # Reset all PVDFs to stationary status.
                for parameter_name in parameters_names:
                    model.parameter(f'{parameter_name}', '0')

                # Activate the wanted PVDF.
                solver.update_active_points()

                for name, value in solver.parameters.items():
                    model.parameter(name, value)

                output.insert(f"{12.0 * (i*4+1)}", f"Activated PVDF points: {solver.current_combination} \n")

                self.current_combination = solver.current_combination

                self.plot_image_loop(solver.current_combination)

                self.update()

                #Create a mesh and solve the solutions.
                model.mesh()  # we need to make a new mesh as the previous was cleared in the last line.
                model.solve() # Solve all studies.
                time_i_taken = time.time() - time_ii

                


                output.insert(f"{14.0 * (i*4+1)}", f"\n Model Solved for configuration {solver.current_combination}. Time elapsed: {int(time_i_taken/60)}min.\n")

                model.export(node = 'raw_data', file = self.path + "/Untitled.txt") # node is the name of the desired export.

                #old_path = f"E:/mph_test/Untitled.txt"
                old_path = self.path + f"/Untitled.txt"
                new_path = self.path + f"/{solver.current_combination}.csv"

                #old_path = "C:/Users/pc/Desktop/JoaoFolhadela/data/Untitled.txt"
                #new_path = f"C:/Users/pc/Desktop/JoaoFolhadela/data/{solver.current_combination}.csv"

                # Put the Headers, convert to CSV and eliminate the txt file
                df = pd.read_csv(old_path, header= None, sep = ';')                     # Read the file to add.
                df.to_csv(new_path, header=header_list, index=False, sep = ';')         # Convert to csv and put the headers.
                os.remove(old_path)                                                     # Remove the unwanted file.


                output.insert(f"{16.0 * (4+1)}", f"\n Model exported to \'{new_path}\'.\n New simulation will begin. \n")

                # Clear all stored solutions, mesh, and plot data.
                model.clear()

                
                # Add tab views for each simulation
                ##self.tabview.add(f"{i + 1}")
                ##self.tabs_text.append(customtkinter.CTkTextbox(master = self.tabview.tab(f"{i + 1}"), width= 250))
                ##self.tabs_text[i - start_point].grid(row=0, column=0, rowspan = 3, padx=(10, 0), pady=(5, 5), sticky="ew")
                ##self.tabs_text[i - start_point].insert("0.0", f"Time Taken: {round(time_i_taken / 60 , 2)}mins. \n")
                ##self.tabs_text[i - start_point].insert(f"2.0", f"Parameters from model: \n")

                text = []
                text.append(f"Simulation index:{i} \n")
                text.append(f"Time Taken: {round(time_i_taken / 60 , 2)}mins. \n")
                text.append(f"\n Parameters from model: \n")

                d = {}
                for j, x in enumerate((list(model.parameters())[-9:])):
                    d[x] = (model.parameters(x)[x])
                    #self.tabs_text[i - start_point].insert(f"{4.0+j*2}", f"{x}: {int(d[x])}\n")
                    text.append(f"{x}: {int(d[x])} \n")


                self.tabs_text.append(text)

                switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"{self.current_combination}")
                self.scrollable_frame_switches.append(switch)
                self.scrollable_frame_switches[i - start_point].configure(command = self.switch_toggle)
                switch.grid(row=i, column=0, padx=10, pady=(0, 20))
                
                


                #Update progress bar
                self.progressbar.set((i - start_point) / (self.no_combinations- start_point))

                self.time_elapsed += time_i_taken
                self.mean_sim_time = self.time_elapsed / (i - start_point + 2)
                self.simulation_info.configure(text = f"Simulation {i + 1}/{self.no_combinations} \n Time elapsed: {round(self.time_elapsed / 60 / 60, 1)}h \n ETA: {round(self.mean_sim_time * (self.no_combinations - i) / 60 / 60 , 1)}h")
                
                self.update()

                for p in range(1,10):
                    self.plot_inactive(p)




app = App()
app.mainloop()