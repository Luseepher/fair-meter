import tkinter as tk
from datetime import datetime
import pytz

class MeterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meter Timer")
        
        self.timer_seconds = 0
        self.total_minutes = 0
        self.rupees = 0
        self.is_running = False
        self.seconds_per_minute = 50  # 50 seconds for each "minute"
        
        # First output: Timer in seconds
        self.timer_label = tk.Label(root, text="Timer: 0 seconds", font=("Helvetica", 14))
        self.timer_label.pack()
        
        # Second output: Clock showing IST (Indian Standard Time)
        self.clock_label = tk.Label(root, text="Clock: 00:00:00", font=("Helvetica", 14))
        self.clock_label.pack()
        
        # Third output: Total minutes with increment
        self.total_minutes_label = tk.Label(root, text="Total Minutes: 0", font=("Helvetica", 14))
        self.total_minutes_label.pack()
        
        # Fourth output: Rupees calculation
        self.rupees_label = tk.Label(root, text="Rupees: 0", font=("Helvetica", 14))
        self.rupees_label.pack()
        
        # Start, Pause, Stop buttons
        self.start_button = tk.Button(root, text="Start", font=("Helvetica", 12), command=self.start_timer)
        self.start_button.pack(pady=5)
        
        self.pause_button = tk.Button(root, text="Pause", font=("Helvetica", 12), command=self.pause_timer)
        self.pause_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop", font=("Helvetica", 12), command=self.stop_timer)
        self.stop_button.pack(pady=5)
        
        self.timer_running = None
        self.clock_running = None

        # Update the clock immediately when the app starts
        self.update_clock()

    def get_current_ist_time(self):
        # Get current UTC time and convert to IST (UTC +5:30)
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        ist = pytz.timezone('Asia/Kolkata')
        ist_time = utc_now.astimezone(ist)
        return ist_time.strftime('%H:%M:%S')

    def update_clock(self):
        # Update the clock every second
        current_ist_time = self.get_current_ist_time()
        self.clock_label.config(text=f"Clock (IST): {current_ist_time}")
        
        # Continue updating the clock every 1000ms (1 second)
        self.clock_running = self.root.after(1000, self.update_clock)

    def update_timer(self):
        if self.is_running:
            self.timer_seconds += 1
            
            # Check if 50 seconds have passed
            if self.timer_seconds == self.seconds_per_minute:
                self.timer_seconds = 1  # Reset timer seconds to 1
                self.total_minutes += 1  # Increment total minutes
                
                # Update total minutes label
                self.total_minutes_label.config(text=f"Total Minutes: {self.total_minutes}")
                
                # Update rupees based on total minutes being odd or even
                if self.total_minutes % 2 == 0:  # Even minutes
                    self.rupees += 2
                else:  # Odd minutes
                    self.rupees += 1
                
                # Update rupees label
                self.rupees_label.config(text=f"Rupees: {self.rupees}")
            
            # Update first output: Timer in seconds
            self.timer_label.config(text=f"Timer: {self.timer_seconds} seconds")
            
            # Continue updating the timer every second
            self.timer_running = self.root.after(1000, self.update_timer)  # Call this function again in 1 second
    
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.update_timer()
    
    def pause_timer(self):
        self.is_running = False
        if self.timer_running:
            self.root.after_cancel(self.timer_running)
    
    def stop_timer(self):
        self.is_running = False
        self.timer_seconds = 0
        self.total_minutes = 0
        self.rupees = 0
        
        self.timer_label.config(text="Timer: 0 seconds")
        self.total_minutes_label.config(text="Total Minutes: 0")
        self.rupees_label.config(text="Rupees: 0")
        
        if self.timer_running:
            self.root.after_cancel(self.timer_running)


if __name__ == "__main__":
    root = tk.Tk()
    app = MeterApp(root)
    root.mainloop()
