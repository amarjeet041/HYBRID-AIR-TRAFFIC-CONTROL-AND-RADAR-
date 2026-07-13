import tkinter as tk
import subprocess
import random
import math
import requests

flights = []

# 🌍 Fetch real flights
def fetch_real_flights():
    try:
        url = "https://opensky-network.org/api/states/all"
        response = requests.get(url)
        data = response.json()

        flights.clear()

        for state in data["states"][:10]:
            if state[1]:
                flights.append({
                    "id": state[1].strip(),
                    "fuel": random.randint(20, 100),
                    "emergency": random.choice([0, 0, 1]),
                    "angle": random.uniform(0, 2*math.pi),
                    "speed": random.uniform(0.02, 0.05),
                    "radius": random.randint(100, 180)
                })

        output_box.insert(tk.END, "🌍 Real flights loaded\n")

    except:
        output_box.insert(tk.END, "❌ API Error\n")

# ➕ Add manual flight
def add_flight():
    user_input = entry.get()
    parts = user_input.split()

    if len(parts) == 3:
        flight_id, fuel, emergency = parts

        flights.append({
            "id": flight_id,
            "fuel": float(fuel),
            "emergency": int(emergency),
            "angle": random.uniform(0, 2*math.pi),
            "speed": random.uniform(0.02, 0.05),
            "radius": random.randint(100, 180)
        })

        entry.delete(0, tk.END)

# 🔗 Run C++
def run_cpp(choice):
    try:
        result = subprocess.run(
            ["C:/Users/Urvashi/atc.exe"],
            input=f"{choice}\n",
            text=True,
            capture_output=True
        )

        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, result.stdout)

    except Exception as e:
        output_box.insert(tk.END, f"Error: {e}")

# 🎯 Priority sorting
def sort_flights():
    flights.sort(key=lambda f: (f["emergency"] == 0, f["fuel"]))

# ✈️ Radar update + Collision Avoidance
def update_radar():
    canvas.delete("plane")

    sort_flights()

    for f in flights:

        # 🛬 Landing effect
        if f["radius"] > 20:
            f["radius"] -= 0.2 if f["emergency"] == 0 else 0.5

        x = 200 + f["radius"] * math.cos(f["angle"])
        y = 200 + f["radius"] * math.sin(f["angle"])

        color = "red" if f["emergency"] else "lime"

        if f["emergency"] and int(f["angle"]*10) % 2 == 0:
            color = "white"

        canvas.create_oval(x, y, x+12, y+12, fill=color, tags="plane")
        canvas.create_text(x+10, y-10, text=f["id"],
                           fill="white", font=("Arial", 8),
                           tags="plane")

        f["angle"] += f["speed"]
        f["fuel"] -= 0.1

    # ✈️ Remove landed flights
    flights[:] = [f for f in flights if f["radius"] > 10]

    # 🚨 COLLISION DETECTION + AVOIDANCE
    for i in range(len(flights)):
        for j in range(i+1, len(flights)):

            dx = abs(flights[i]["radius"] * math.cos(flights[i]["angle"]) -
                     flights[j]["radius"] * math.cos(flights[j]["angle"]))
            dy = abs(flights[i]["radius"] * math.sin(flights[i]["angle"]) -
                     flights[j]["radius"] * math.sin(flights[j]["angle"]))

            if dx < 15 and dy < 15:

                output_box.insert(tk.END,
                    f"⚠️ Avoiding Collision: {flights[i]['id']} & {flights[j]['id']}\n")

                # 🔥 Emergency gets priority
                if flights[i]["emergency"]:
                    flights[j]["angle"] += 0.5
                elif flights[j]["emergency"]:
                    flights[i]["angle"] += 0.5
                else:
                    flights[i]["angle"] += random.uniform(0.3, 0.6)
                    flights[j]["angle"] -= random.uniform(0.3, 0.6)

                # Speed reduction
                flights[i]["speed"] *= 0.9
                flights[j]["speed"] *= 0.9

    root.after(50, update_radar)

# 📋 Flight list
def update_list():
    flight_list.delete(1.0, tk.END)

    for f in flights:
        status = "🚨 EMERGENCY" if f["emergency"] else "NORMAL"
        flight_list.insert(tk.END,
            f"{f['id']} | Fuel: {int(f['fuel'])} | {status}\n")

    root.after(1000, update_list)

# 🔄 Auto API refresh
def auto_update():
    fetch_real_flights()
    root.after(15000, auto_update)

# UI
root = tk.Tk()
root.title("✈️ REAL ATC RADAR SYSTEM")
root.geometry("1100x720")
root.configure(bg="#020617")

tk.Label(root, text="✈️ AIR TRAFFIC CONTROL SYSTEM",
         font=("Arial", 20, "bold"),
         fg="#38bdf8", bg="#020617").pack(pady=10)

main = tk.Frame(root, bg="#020617")
main.pack(fill="both", expand=True)

# LEFT PANEL
left = tk.Frame(main, bg="#020617")
left.pack(side="left", padx=20)

tk.Label(left, text="Enter Flight (ID Fuel Emergency):",
         fg="white", bg="#020617").pack()

entry = tk.Entry(left, width=30)
entry.pack(pady=5)

tk.Button(left, text="➕ Add Flight",
          bg="#22c55e", fg="white",
          width=25, height=2,
          command=add_flight).pack(pady=5)

tk.Button(left, text="🌍 Load Real Flights",
          bg="#f59e0b", fg="black",
          width=25, height=2,
          command=fetch_real_flights).pack(pady=5)

buttons = ["Duplicate", "Aircraft", "Signal", "Radar", "Route"]

for i, text in enumerate(buttons):
    tk.Button(left, text=text, width=25, height=2,
              bg="#2563eb", fg="white",
              command=lambda v=i+2: run_cpp(v)).pack(pady=4)

# RIGHT PANEL
right = tk.Frame(main, bg="#020617")
right.pack(side="right", padx=20)

canvas = tk.Canvas(right, width=400, height=400, bg="black")
canvas.pack()

# 🌍 Grid
for i in range(0, 400, 40):
    canvas.create_line(i, 0, i, 400, fill="#022c22")
    canvas.create_line(0, i, 400, i, fill="#022c22")

# Radar circles
for i in range(60, 180, 40):
    canvas.create_oval(200-i, 200-i, 200+i, 200+i, outline="green")

# Runway
canvas.create_rectangle(180, 180, 220, 220, fill="gray")
canvas.create_text(200, 200, text="RUNWAY", fill="white", font=("Arial", 8))

# Sweep
line = canvas.create_line(200, 200, 200, 20, fill="lime")

def rotate(angle=0):
    x = 200 + 180 * math.cos(angle)
    y = 200 + 180 * math.sin(angle)
    canvas.coords(line, 200, 200, x, y)
    root.after(30, lambda: rotate(angle + 0.1))

rotate()

update_radar()

# Flight list
flight_list = tk.Text(right, height=8, width=50,
                      bg="black", fg="cyan")
flight_list.pack(pady=5)

update_list()

# Output
output_box = tk.Text(root, height=6,
                     bg="black", fg="lime")
output_box.pack(fill="x", padx=20, pady=10)

auto_update()

root.mainloop()