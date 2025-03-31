import tkinter as tk
from tkinter import ttk
import numpy as np
from CoreProcess import KalmanFilter

class MatrixDisplayWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Display Window")
        self.create_widgets()

        # Initialize Kalman Filter
        dt = 0.1
        process_noise = np.diag([1, 1, 1, 1, 1, 1])
        measurement_noise = np.diag([1, 1, 1, 1])
        initial_state = np.array([0, 0, 0, 50, 0, 50])
        initial_covariance = np.eye(6)
        self.kf = KalmanFilter(dt, process_noise, measurement_noise, initial_state, initial_covariance)
        self.observer_position = np.array([0, 250, 0])
        self.observations = []

        self.update_display()

    def create_widgets(self):
        self.state_label = ttk.Label(self.root, text="State Vector")
        self.state_label.pack()
        self.state_text = tk.Text(self.root, height=6, width=80)  # Increased width
        self.state_text.pack()

        self.matrix_A_label = ttk.Label(self.root, text="Matrix A")
        self.matrix_A_label.pack()
        self.matrix_A_text = tk.Text(self.root, height=6, width=80)  # Increased width
        self.matrix_A_text.pack()

        self.matrix_P_label = ttk.Label(self.root, text="Covariance Matrix P")
        self.matrix_P_label.pack()
        self.matrix_P_text = tk.Text(self.root, height=6, width=80)  # Increased width
        self.matrix_P_text.pack()

        self.process_noise_label = ttk.Label(self.root, text="Process Noise Matrix Q")
        self.process_noise_label.pack()
        self.process_noise_text = tk.Text(self.root, height=6, width=80)  # Increased width
        self.process_noise_text.pack()

        self.measurement_noise_label = ttk.Label(self.root, text="Measurement Noise Matrix R")
        self.measurement_noise_label.pack()
        self.measurement_noise_text = tk.Text(self.root, height=6, width=80)  # Increased width
        self.measurement_noise_text.pack()

        self.update_button = ttk.Button(self.root, text="Update", command=self.update_display)
        self.update_button.pack()

    def update_display(self):
        self.kf.predict()
        if self.observations:
            observation = self.observations.pop(0)
            self.kf.update(observation, self.observer_position)
        
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

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixDisplayWindow(root)
    root.mainloop()