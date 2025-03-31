import tkinter as tk
from tkinter import ttk
import numpy as np
from CoreProcess import KalmanFilter
import time

class MatrixDisplayWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Display Window")
        self.width = 100  # Set width to 100
        self.create_widgets()

        # Initialize Kalman Filter
        self.dt = 0.1
        process_noise = np.diag([1, 1, 1, 1, 1, 1])
        measurement_noise = np.diag([1, 1, 1, 1])
        initial_state = np.array([0, 0, 0, 50, 0, 50])
        initial_covariance = np.eye(6)
        self.kf = KalmanFilter(self.dt, process_noise, measurement_noise, initial_state, initial_covariance)
        self.observer_position = np.array([0, 250, 0])
        self.observations = []
        self.epoch = 0  # Initialize epoch

        self.update_display()

    def create_widgets(self):
        # Create a main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a left frame for matrices
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.state_label = ttk.Label(left_frame, text="State Vector")
        self.state_label.pack()
        self.state_text = tk.Text(left_frame, height=6, width=self.width)
        self.state_text.pack()

        self.matrix_A_label = ttk.Label(left_frame, text="Matrix A")
        self.matrix_A_label.pack()
        self.matrix_A_text = tk.Text(left_frame, height=6, width=self.width)
        self.matrix_A_text.pack()

        self.matrix_P_label = ttk.Label(left_frame, text="Covariance Matrix P")
        self.matrix_P_label.pack()
        self.matrix_P_text = tk.Text(left_frame, height=6, width=self.width)
        self.matrix_P_text.pack()

        self.process_noise_label = ttk.Label(left_frame, text="Process Noise Matrix Q")
        self.process_noise_label.pack()
        self.process_noise_text = tk.Text(left_frame, height=6, width=self.width)
        self.process_noise_text.pack()

        # Create a right frame for measurement noise and observation
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.measurement_noise_label = ttk.Label(right_frame, text="Measurement Noise Matrix R")
        self.measurement_noise_label.pack()
        self.measurement_noise_text = tk.Text(right_frame, height=6, width=self.width)
        self.measurement_noise_text.pack()

        self.observation_label = ttk.Label(right_frame, text="Current Observation")
        self.observation_label.pack()
        self.observation_text = tk.Text(right_frame, height=6, width=self.width)
        self.observation_text.pack()

        # Create a frame for the update button, time counter, and epoch counter
        update_frame = ttk.Frame(self.root)
        update_frame.pack()

        self.update_button = ttk.Button(update_frame, text="Update", command=self.update_display)
        self.update_button.pack(side=tk.LEFT)

        self.time_label = ttk.Label(update_frame, text="")
        self.time_label.pack(side=tk.LEFT, padx=10)

        self.epoch_label = ttk.Label(update_frame, text="Epoch: 0")
        self.epoch_label.pack(side=tk.LEFT, padx=10)

    def update_display(self):
        self.kf.predict()
        if self.observations:
            observation = self.observations.pop(0)
            self.kf.update(observation, self.observer_position)
            self.observation_text.delete(1.0, tk.END)
            self.observation_text.insert(tk.END, str(observation))
        
        state = self.kf.get_state()
        self.state_text.delete(1.0, tk.END)
        self.state_text.insert(tk.END, str(state))

        matrix_A = self.kf.A
        self.matrix_A_text.delete(1.0, tk.END)
        self.matrix_A_text.insert(tk.END, str(matrix_A))

        matrix_P = self.kf.P
        self.matrix_P_text.delete(1.0, tk.END)
        self.matrix_P_text.insert(tk.END, str(matrix_P))

        process_noise = self.kf.Q
        self.process_noise_text.delete(1.0, tk.END)
        self.process_noise_text.insert(tk.END, str(process_noise))

        measurement_noise = self.kf.R
        self.measurement_noise_text.delete(1.0, tk.END)
        self.measurement_noise_text.insert(tk.END, str(measurement_noise))

        # Update the epoch
        self.epoch += self.dt
        self.epoch_label.config(text=f"Epoch: {self.epoch:.1f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixDisplayWindow(root)
    root.mainloop()