import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import copy as brutal_copy
from planes import aircraft_data, iff_check, russian as rs

russian = rs
data = aircraft_data.copy()
keys = list(data.keys())
choose = random.randint(0, len(keys) - 1)
plane = data[keys[choose]]

target_change_timer = 0.0
defense_missile_fired = False
defense_missile_ctd = [0, 0, 0]
defense_missile_xy_move = 0
defense_missile_z_move = 0
defense_missile_fuel = 500
defense_missile_base_speed = 12000
defense_missile_max_speed = 18000
used_defense_missiles = 0
max_defense_missiles = 2
plane_missile_fired = False
plane_missile_ctd = [0, 0, 0]
plane_missile_xy_move = 0
plane_missile_z_move = 0
plane_missile_fuel = 600
plane_missile_base_speed = 10000
plane_missile_max_speed = 15000
s400_destroyed = False
no_fuel_timer = 0.0
no_fuel_mode = False
missile_fuel = 700
plane_min_speed = plane['min_speed']
plane_base_speed = plane['avg_speed']
plane_max_speed = plane['max_speed']
plane_max_altitude = plane['max_altitutde']
plane_accelerating = plane['accelerating']
missile_min_speed = 5000
plane_jammer = plane['jammer']
missile_base_speed = plane_base_speed * 1.5
missile_max_speed = plane_max_speed * 2.2
max_spawn_dist = 400000
min_spawn_dist = 200000
max_spawn_altitude = 15000
min_spawn_altitude = 9000
loss_time = plane['signal_killer']
h_max_rate = plane['h_max_rate']
v_max_rate = plane['v_max_rate']
plane_type = plane['military']
plane_stealth = plane['stealth']
xy_move = random.uniform(0, 2 * math.pi)
z_move = 0
t = 0.5
timer = 0.5
rounder = 2
radio = 0
missile_h_max_rate = 12
missile_v_max_rate = 8
missile_fired = False
missile_ctd = [0, 0, 0]
missile_xy_move = random.uniform(0, 2 * math.pi)
missile_z_move = 0
missile_target = None
last_known_target = None
current_plane_speed = plane_base_speed
current_missile_speed = missile_base_speed
current_plane_missile_speed = plane_missile_base_speed
plane_shot_down = False
buttonfire = False
buttondestruct = False
used_missiles = 0
inner_radius = 150000  # 150 km inner circle
signal_mode = {'mode': False, 'time': 0.0}
lock_mode = {'mode': False, 'max_altitude': 30000, 'min_altitude': 250}
panel_offset = 0
scanner_offset = 0

class S400_Russian_Missile:
    def __init__(self):
        # Initialize matplotlib figure and axes
        self.fig, self.ax = plt.subplots(figsize=(12, 6), facecolor='black')
        self.ax.set_facecolor('#003300')
        self.ax.set_xlim(-max_spawn_dist, max_spawn_dist)
        self.ax.set_ylim(-max_spawn_dist, max_spawn_dist)
        self.ax.set_xlabel('X (m)', color='white')
        self.ax.set_ylabel('Y (m)', color='white')
        self.ax.tick_params(axis='both', colors='white')
        self.ax.grid(True, color='green', alpha=0.3)

        # Draw spawn boundaries
        theta = np.linspace(0, 2 * np.pi, 100)
        outer_x = max_spawn_dist * np.cos(theta)
        outer_y = max_spawn_dist * np.sin(theta)
        self.ax.plot(outer_x, outer_y, 'w-', linewidth=1.5, label='400 km')

        inner_x = inner_radius * np.cos(theta)
        inner_y = inner_radius * np.sin(theta)
        self.ax.plot(inner_x, inner_y, 'w--', linewidth=1, label='150 km')

        self.ax.plot(0, 0, 'ko', markersize=8, label='S400 Location')

        # Plot elements
        self.plane_dot, = self.ax.plot([], [], 'go', markersize=8, label='Plane', alpha=0.8)
        self.missile_dot, = self.ax.plot([], [], 'ro', markersize=8, label='Attack Missile', alpha=0.8)
        self.plane_missile_dot, = self.ax.plot([], [], 'yo', markersize=8, label='Plane Missile', alpha=0.8)
        self.defense_missile_dot, = self.ax.plot([], [], 'mo', markersize=8, label='Defense Missile', alpha=0.8)
        self.radar_point, = self.ax.plot([], [], 'co', markersize=10, label='Radar Target', alpha=0.8)

        self.target_text = self.ax.text(0, -50000, "", ha='center', va='center', fontsize=12, color='white', alpha=0.7, fontfamily='monospace')
        self.locked_text = self.ax.text(0, -70000, "", ha='center', va='center', fontsize=12, color='red', alpha=0.7, fontfamily='monospace')

        self.info_text = self.ax.annotate('', xy=(0.75, 0.98), xycoords='figure fraction',
                                         fontsize=12, fontweight='bold', color='#0DF517',
                                         bbox=dict(facecolor='black', edgecolor='gray', alpha=0.7),
                                         verticalalignment='top')

        self.top_panel, = self.ax.plot([], [], 'w-', linewidth=2, alpha=0.5)
        self.bottom_panel, = self.ax.plot([], [], 'w-', linewidth=2, alpha=0.5)
        self.left_line, = self.ax.plot([-max_spawn_dist * 0.8, -max_spawn_dist * 0.8], [max_spawn_dist * 0.95, max_spawn_dist * 0.85],
                                       'w-', linewidth=2, alpha=0.7)
        self.right_line, = self.ax.plot([max_spawn_dist * 0.8, max_spawn_dist * 0.8], [max_spawn_dist * 0.95, max_spawn_dist * 0.85],
                                        'w-', linewidth=2, alpha=0.7)
        self.scanner_line, = self.ax.plot([], [], 'w-', linewidth=1.5, alpha=0.6)

        # Buttons
        self.ax_fire_button = plt.axes([0.85, 0.05, 0.1, 0.075])
        self.fire_button = Button(self.ax_fire_button, 'FIRE', color='darkred', hovercolor='red')
        self.ax_destruct_button = plt.axes([0.70, 0.05, 0.1, 0.075])
        self.destruct_button = Button(self.ax_destruct_button, 'DESTRUCT', color='purple', hovercolor='magenta')

        # Initial plane spawn and targets
        self.plane_ctd = self.spawner()
        self.target_ctds = self.checkpoints_generator(self.plane_ctd)
        self.targets_saver = brutal_copy.deepcopy(self.target_ctds)
        self.current_target_idx = 0
        self.iff_data = 'No Data'
        self.status = 'No Data'

        # Button event handlers
        self.fire_button.on_clicked(self.triggerfire)
        self.destruct_button.on_clicked(self.triggerdestruct)

    def triggerfire(self, event):
        global buttonfire, missile_fired, plane_shot_down
        if not missile_fired and not plane_shot_down and not buttonfire:
            buttonfire = True

    def triggerdestruct(self, event):
        global buttondestruct, missile_fired
        if missile_fired:
            buttondestruct = True

    def target_speed(self, target, speed, differ):
        if target == 'No Signal':
            return 'No Data'
        difference = abs(speed * differ - speed)
        difference_with_mode = difference * random.choice([-1, 1])
        modded_speed = round(speed + difference_with_mode)
        return modded_speed

    def fuel_consumption_rate(self, v_current, is_defense=False):
        global missile_fuel, defense_missile_fuel
        fuel = defense_missile_fuel if is_defense else missile_fuel
        base_speed = defense_missile_base_speed if is_defense else missile_base_speed
        fuel -= (500 / 60.0 if is_defense else 700 / 60.0) * (v_current / base_speed) * 0.25 * timer
        fuel = max(0, fuel)
        if is_defense:
            defense_missile_fuel = fuel
        else:
            missile_fuel = fuel

    def dist_calc(self, x, y, z):
        return math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def direction_dist_calc(self, a, b):
        return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))

    def xy_dist_calc(self, x, y):
        return math.sqrt(x ** 2 + y ** 2)

    def calculate_accuracy(self, t, B, H):
        time_effect = (60 - t) / 60
        distance_effect = B / 400000 // 2
        altitude = abs(H - 10000) * 0.00010
        combined_effect = (time_effect + distance_effect + altitude) / 2
        accuracy = 1.1 + 0.1 * combined_effect + plane_stealth
        return max(accuracy, 1.005)

    def radar_logic(self, t, ctd):
        global signal_mode
        if lock_mode['mode']:
            evade = int(abs(10000 - ctd[2]) * float(plane_jammer))
            x = ctd[0] + random.randint(-evade, evade)
            y = ctd[1] + random.randint(-evade, evade)
            z = ctd[2] + random.randint(0, evade // 2)
            return [x, y, z], 1.005
        if signal_mode['mode']:
            if t - signal_mode['time'] < loss_time:
                return 'No Signal', 0
            else:
                signal_mode['mode'] = False
        radar_mode = random.random()
        if radar_mode < 0.05:
            signal_mode['mode'] = True
            signal_mode['time'] = t
            return 'No Signal', 0
        elif radar_mode < 0.10:
            x = random.randint(-max_spawn_dist, max_spawn_dist)
            y = random.randint(-max_spawn_dist, max_spawn_dist)
            z = random.randint(100, 20000)
            return [x, y, z], random.uniform(1, 2)
        else:
            radar = []
            differs = []
            for i in ctd:
                differ = self.calculate_accuracy(t, i, ctd[2])
                diff = round(abs(differ * i) - abs(i))
                diff_with_mode = diff * random.choice([-1, 1])
                pos = round(i + diff_with_mode)
                radar.append(pos)
                differs.append(differ)
            differs = sum(differs) / len(differs)
            return radar, differs

    def tracking_percentage(self, actual, radar):
        global radio, lock_mode, plane_base_speed, t
        if lock_mode['mode']:
            if self.dist_calc(actual[0], actual[1], actual[2]) < 250000 and 350 < actual[2] < 28000:
                max_error = 40000
                error = self.direction_dist_calc(actual, radar)
                perc = max(0.0, (100 * (1 - error / max_error)))
                return round(perc, 2)
            else:
                lock_mode['mode'] = False
                t = 0
                return 'N/A'
        if radar == 'No Signal':
            return "N/A"
        max_error = 40000
        error = self.direction_dist_calc(actual, radar)
        perc = max(0.0, (100 * (1 - error / max_error)))
        if perc > 85:
            lock_mode['mode'] = True
            return round(perc, 2)
        return round(perc, 2)

    def spawner(self):
        while True:
            x = random.randint(0, max_spawn_dist) * random.choice([-1, 1])
            y = random.randint(0, max_spawn_dist) * random.choice([-1, 1])
            z = random.randint(min_spawn_altitude, max_spawn_altitude)
            if min_spawn_dist < self.dist_calc(x, y, z) < max_spawn_dist:
                return [x, y, z]

    def checkpoints_generator(self, plane_ctd):
        checkpoints = []
        mod1 = [150000, [10000, 90000]]
        mod2 = [350000, [170000, 350000]]

        def modder(start, randomer, checkers):
            while True:
                x = random.randint(0, randomer) * random.choice([-1, 1])
                y = random.randint(0, randomer) * random.choice([-1, 1])
                z = start[2] + random.randint(0, 2000) * random.choice([-1, 1])
                if checkers[0] < self.dist_calc(x, y, z) < checkers[1]:
                    return [x, y, z]

        for i in range(1, 6):
            if i % 2 == 1:
                checkpoints.append(modder(plane_ctd, mod1[0], mod1[1]))
            else:
                checkpoints.append(modder(plane_ctd, mod2[0], mod2[1]))
        return checkpoints

    def plane_acceleration(self, altitude, min_speed, base_speed, max_speed, altitude_loss, straight_move):
        global current_plane_speed
        if altitude <= 350:
            target_speed = min_speed
        elif straight_move and min_spawn_altitude <= altitude <= max_spawn_altitude:
            target_speed = base_speed
        elif altitude > min_spawn_altitude and not altitude_loss:
            speeder = (max_speed - base_speed) * (altitude - min_spawn_altitude) / (max_spawn_altitude - min_spawn_altitude)
            target_speed = base_speed + speeder
            target_speed = min(max_speed, target_speed)
        elif altitude_loss and altitude >= min_spawn_altitude:
            target_speed = base_speed
        else:
            speedlower = (base_speed - min_speed) * (min_spawn_altitude - altitude) / (min_spawn_altitude - 250)
            target_speed = base_speed - speedlower
            target_speed = max(min_speed, target_speed)
        speed_change = random.uniform(plane_accelerating - 10, plane_accelerating)
        if current_plane_speed < target_speed:
            current_plane_speed = min(current_plane_speed + speed_change, target_speed)
        elif current_plane_speed > target_speed:
            current_plane_speed = max(current_plane_speed - speed_change, target_speed)
        return max(min_speed, min(max_speed, current_plane_speed))

    def plane_missile_acceleration(self, altitude, previous_altitude):
        global current_plane_missile_speed
        base_speed = plane_missile_base_speed
        max_speed = plane_missile_max_speed
        altitude_change = altitude - previous_altitude
        if altitude_change < 0:
            speed_increase = base_speed * (abs(altitude_change) / 1000)
            target_speed = base_speed + speed_increase
        else:
            target_speed = base_speed
        target_speed = min(max_speed, target_speed)
        speed_change = random.uniform(200, 210)
        if current_plane_missile_speed < target_speed:
            current_plane_missile_speed = min(current_plane_missile_speed + speed_change, target_speed)
        elif current_plane_missile_speed > target_speed:
            current_plane_missile_speed = max(current_plane_missile_speed - speed_change, target_speed)
        return current_plane_missile_speed

    def missile_acceleration(self, altitude):
        global current_missile_speed
        if altitude <= 350:
            target_speed = missile_min_speed
        elif altitude >= 10000:
            speed_increase = (missile_max_speed - missile_base_speed) * (altitude - 10000) / (max_spawn_altitude - 10000)
            target_speed = missile_base_speed + speed_increase
            target_speed = min(missile_max_speed, target_speed)
        else:
            speed_range = missile_base_speed - missile_min_speed
            altitude_range = 10000 - 250
            speed_decrease = speed_range * (10000 - altitude) / altitude_range
            target_speed = missile_base_speed - speed_decrease
        speed_change = random.uniform(200, 210)
        if current_missile_speed < target_speed:
            current_missile_speed = min(current_missile_speed + speed_change, target_speed)
        elif current_missile_speed > target_speed:
            current_missile_speed = max(current_missile_speed - speed_change, target_speed)
        return max(missile_min_speed, min(missile_max_speed, current_missile_speed))

    def movement(self, current_ctd, target_ctd, h_max_rate, v_max_rate, xy_move, z_move, timer, it_is_missile=False, is_plane_missile=False):
        direction = [target_ctd[i] - current_ctd[i] for i in range(3)]
        d_length = math.sqrt(sum(i ** 2 for i in direction))
        altitude_loss = direction[2] < 0
        straight_move = abs(z_move) < 0.01
        if it_is_missile:
            if is_plane_missile:
                speed = self.plane_missile_acceleration(current_ctd[2], current_ctd[2] - direction[2] * timer)
            else:
                speed = self.missile_acceleration(current_ctd[2])
        else:
            speed = self.plane_acceleration(current_ctd[2], plane_min_speed, plane_base_speed, plane_max_speed, altitude_loss, straight_move)
        if d_length < speed * timer:
            return target_ctd, xy_move, z_move, speed
        xy_target = math.atan2(direction[1], direction[0])
        xy_move_diff = (xy_target - xy_move + math.pi) % (2 * math.pi) - math.pi
        h_max = h_max_rate * math.pi / 180 * timer
        angle = max(min(xy_move_diff, h_max), -h_max)
        xy_new_move = (xy_move + angle) % (2 * math.pi)
        h_dist = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        if h_dist > 0:
            z_target = math.atan2(direction[2], h_dist)
        else:
            z_target = math.copysign(math.pi / 2, direction[2])
        z_move_diff = (z_target - z_move + math.pi) % (2 * math.pi) - math.pi
        max_z = v_max_rate * math.pi / 180 * timer
        z_angle = max(min(z_move_diff, max_z), -max_z)
        z_new_move = (z_move + z_angle) % (2 * math.pi)
        h_speed = speed * math.cos(z_new_move)
        v_speed = speed * math.sin(z_new_move)
        new_x = current_ctd[0] + h_speed * math.cos(xy_new_move) * timer
        new_y = current_ctd[1] + h_speed * math.sin(xy_new_move) * timer
        new_z = current_ctd[2] + v_speed * timer
        return [round(new_x), round(new_y), round(new_z)], xy_new_move, z_new_move, speed

    def update(self, frame):
        global plane_ctd, xy_move, z_move, missile_ctd, missile_xy_move, missile_z_move, missile_fired, missile_target, last_known_target, missile_fuel
        global t, rounder, radio, target_change_timer, no_fuel_mode, no_fuel_timer, plane_shot_down, buttonfire, buttondestruct, used_missiles
        global plane_missile_fired, plane_missile_ctd, plane_missile_xy_move, plane_missile_z_move, plane_missile_fuel, s400_destroyed
        global defense_missile_fired, defense_missile_ctd, defense_missile_xy_move, defense_missile_z_move, defense_missile_fuel, used_defense_missiles
        global plane_base_speed, panel_offset, scanner_offset

        self.plane_ctd = self.plane_ctd  # giving to global again
        target_ctd = self.target_ctds[self.current_target_idx]

        if not plane_shot_down:
            if s400_destroyed:
                tspeed = "No Data"
                radar = "No Signal"
                percentage = "N/A"
                self.plane_ctd, xy_move, z_move, pspeed = self.movement(self.plane_ctd, target_ctd, h_max_rate, v_max_rate, xy_move, z_move, timer)
            else:
                radar, differ = self.radar_logic(t, self.plane_ctd)
                percentage = self.tracking_percentage(self.plane_ctd, radar)
                self.plane_ctd, xy_move, z_move, pspeed = self.movement(self.plane_ctd, target_ctd, h_max_rate, v_max_rate, xy_move, z_move, timer)
                tspeed = self.target_speed(radar, pspeed, differ)
        else:
            tspeed = 'No Data'
            radar = "No Signal"
            percentage = "N/A"
            pspeed = 0
            self.plane_ctd = [0, 0, 0]

        target_change_timer += timer
        if not plane_shot_down and not missile_fired:
            if target_change_timer >= 50.0:
                self.current_target_idx = (self.current_target_idx + 1) % len(self.target_ctds)
                target_change_timer = 0.0

        if radar != "No Signal" and percentage != 'N/A':
            if percentage > 70:
                self.iff_data = iff_check(choose)
            else:
                self.iff_data = 'No Data'
            if percentage > 85:
                self.status = 'Locked On'
            elif percentage > 0:
                self.status = 'Tracking'
            else:
                self.status = 'No Data'
        else:
            self.iff_data = 'No Data'
            self.status = 'No Data'

        if buttonfire and not missile_fired and used_missiles < 2 and not s400_destroyed:
            plane_base_speed = plane_max_speed
            used_missiles += 1
            missile_ctd = [0, 0, 0]
            missile_xy_move = random.uniform(0, 2 * math.pi)
            missile_z_move = 0
            radio = 1
            missile_fired = True
            if radar != 'No Signal':
                missile_target = radar
            else:
                missile_target = self.spawner()
            last_known_target = missile_target

        if missile_fired and radio == 1:
            evader = self.spawner()
            if rounder % 2 == 0:
                evader[2] = plane_max_altitude + random.randint(-500, 250)
            else:
                evader[2] = 250 + random.randint(-50, 50)
            rounder += 1
            self.target_ctds[self.current_target_idx][:] = evader
            radio = 0

        mspeed = 0
        if missile_fired:
            if missile_fuel > 0 and not no_fuel_mode and not buttondestruct and not s400_destroyed:
                if radar != 'No Signal':
                    missile_target = radar
                    last_known_target = missile_target
                else:
                    last_known_target[1] += 10000
                    missile_target = last_known_target
                missile_ctd, missile_xy_move, missile_z_move, mspeed = self.movement(
                    missile_ctd, missile_target, missile_h_max_rate, missile_v_max_rate,
                    missile_xy_move, missile_z_move, timer, True
                )
                self.fuel_consumption_rate(mspeed)
                if self.direction_dist_calc(missile_ctd, self.plane_ctd) < (missile_base_speed * timer):
                    plane_shot_down = True
                    lock_mode['mode'] = False
                    missile_fired = False
                    missile_target = None
                    buttonfire = False
                    missile_fuel = 700
                elif missile_fuel <= 0:
                    no_fuel_mode = True
                    no_fuel_timer = 0.0
            elif no_fuel_mode or buttondestruct or s400_destroyed:
                fall_speed = -500
                h_speed = current_missile_speed * math.cos(missile_z_move)
                new_x = missile_ctd[0] + h_speed * math.cos(missile_xy_move) * timer
                new_y = missile_ctd[1] + h_speed * math.sin(missile_xy_move) * timer
                new_z = missile_ctd[2] + fall_speed * timer
                missile_ctd = [round(new_x), round(new_y), round(new_z)]
                mspeed = h_speed
                no_fuel_timer += timer
                if no_fuel_timer >= 5.0 or missile_ctd[2] <= 2500:
                    buttondestruct = False
                    buttonfire = False
                    missile_fired = False
                    no_fuel_mode = False
                    missile_fuel = 700
                    missile_target = None
                    radio = 2

        if used_missiles >= 1 and not missile_fired and not plane_shot_down and plane_type and not plane_missile_fired and not s400_destroyed and random.random() < 0.05:
            if (choose in {1, 3} and russian == -1) or choose not in {1, 3, 4}:
                plane_missile_fired = True
                plane_missile_ctd = self.plane_ctd.copy()
                plane_missile_xy_move = random.uniform(0, 2 * math.pi)
                plane_missile_z_move = 0
                plane_missile_fuel = 500

        plane_mspeed = 0
        if plane_missile_fired and not s400_destroyed:
            if plane_missile_fuel > 0:
                plane_missile_target = [0, 0, 0]
                plane_missile_ctd, plane_missile_xy_move, plane_missile_z_move, plane_mspeed = self.movement(
                    plane_missile_ctd, plane_missile_target, missile_h_max_rate, missile_v_max_rate,
                    plane_missile_xy_move, plane_missile_z_move, timer, True, True
                )
                plane_missile_fuel -= (400 / 60.0) * (plane_mspeed / plane_missile_base_speed) * 1 * timer
                plane_missile_fuel = max(0, plane_missile_fuel)
                if self.direction_dist_calc(plane_missile_ctd, [0, 0, 0]) < (plane_missile_base_speed * timer):
                    s400_destroyed = True
                    plane_missile_fired = False
                elif plane_missile_fuel <= 0:
                    plane_missile_fired = False

        def_mspeed = 0
        if plane_missile_fired and not defense_missile_fired and not s400_destroyed and used_defense_missiles < max_defense_missiles:
            distance_to_s400 = self.direction_dist_calc(plane_missile_ctd, [0, 0, 0])
            if distance_to_s400 <= 200000:
                defense_missile_fired = True
                used_defense_missiles += 1
                defense_missile_ctd = [0, 0, 0]
                defense_missile_xy_move = random.uniform(0, 2 * math.pi)
                defense_missile_z_move = 0
                defense_missile_fuel = 500

        if defense_missile_fired and not s400_destroyed:
            if defense_missile_fuel > 0:
                defense_missile_target = plane_missile_ctd
                defense_missile_ctd, defense_missile_xy_move, defense_missile_z_move, def_mspeed = self.movement(
                    defense_missile_ctd, defense_missile_target, missile_h_max_rate, missile_v_max_rate,
                    defense_missile_xy_move, defense_missile_z_move, timer, True
                )
                self.fuel_consumption_rate(def_mspeed, True)
                if self.direction_dist_calc(defense_missile_ctd, plane_missile_ctd) < (defense_missile_base_speed * timer):
                    plane_missile_fired = False
                    defense_missile_fired = False
                elif self.direction_dist_calc(defense_missile_ctd, [0, 0, 0]) > 200000:
                    defense_missile_fired = False
            elif defense_missile_fuel <= 0:
                defense_missile_fired = False

        if not plane_shot_down:
            self.plane_dot.set_data([self.plane_ctd[0]], [self.plane_ctd[1]])
        else:
            self.plane_dot.set_data([], [])

        if missile_fired:
            self.missile_dot.set_data([missile_ctd[0]], [missile_ctd[1]])
        else:
            self.missile_dot.set_data([], [])

        if plane_missile_fired:
            self.plane_missile_dot.set_data([plane_missile_ctd[0]], [plane_missile_ctd[1]])
        else:
            self.plane_missile_dot.set_data([], [])

        if defense_missile_fired:
            self.defense_missile_dot.set_data([defense_missile_ctd[0]], [defense_missile_ctd[1]])
        else:
            self.defense_missile_dot.set_data([], [])

        if radar != "No Signal":
            self.radar_point.set_data([radar[0]], [radar[1]])
        else:
            self.radar_point.set_data([], [])

        if radar != "No Signal":
            self.target_text.set_text("Target Detected")
            if self.xy_dist_calc(radar[0], radar[1]) <= inner_radius and lock_mode['mode']:
                self.locked_text.set_text("Locked On")
            else:
                self.locked_text.set_text("")
        else:
            self.target_text.set_text("")
            self.locked_text.set_text("")

        table_content = (
            f"Radar Coords: {radar}\n"
            f"Plane Altitude: {str(radar[2]) + 'm' if radar != 'No Signal' else 'No Data'}\n"
            f"Target Speed: {str(tspeed) + 'm/s' if tspeed != 'No Data' else tspeed}\n"
            f"Accuracy: {str(percentage) + '%' if percentage != 'N/A' else percentage}\n"
            f"Iff Match: {str(self.iff_data) + '%' if self.iff_data != 'No Data' else self.iff_data}\n"
            f"Status: {self.status}\n"
            f"Missile Coords: {missile_ctd}\n"
            f"Plane Missile: {plane_missile_ctd if plane_missile_fired else 'N/A'}\n"
            f"Defense Missile: {defense_missile_ctd if defense_missile_fired else 'N/A'}\n"
            f"Missile Speed: {round(mspeed)} m/s\n"
            f"Defense Missile Speed: {round(def_mspeed)} m/s\n"
            f"Missile Fuel: {round(missile_fuel, 1)} L\n"
            f"Defense Missile Fuel: {round(defense_missile_fuel, 1)} L\n"
            f"Missiles Fired: {used_missiles}/2\n"
            f"Defense Missiles Fired: {used_defense_missiles}/{max_defense_missiles}\n"
            f"S-400 Status: {'Destroyed' if s400_destroyed else 'Operational'}\n"
            f"-------- Spectator mode --------\n"
            f"Plane Missile Speed: {round(plane_mspeed)} m/s\n"
            f"Plane : {keys[choose]}\n"
            f"Russian? : {russian}\n"
            f"Plane target : {target_ctd}\n"
        )
        self.info_text.set_text(table_content)

        panel_offset = (panel_offset + 20000) % (max_spawn_dist * 2)
        panel_x = np.linspace(-max_spawn_dist + panel_offset, max_spawn_dist + panel_offset, 50)
        top_y = np.full_like(panel_x, max_spawn_dist * 0.9)
        bottom_y = np.full_like(panel_x, -max_spawn_dist * 0.9)
        self.top_panel.set_data(panel_x - max_spawn_dist, top_y)
        self.bottom_panel.set_data(panel_x - max_spawn_dist, bottom_y)

        scanner_offset = (scanner_offset + 10000) % (max_spawn_dist * 0.2) - (max_spawn_dist * 0.1)
        scanner_x = np.linspace(-max_spawn_dist * 0.8, max_spawn_dist * 0.8, 50)
        scanner_y = np.full_like(scanner_x, max_spawn_dist * 0.9 + scanner_offset)
        self.scanner_line.set_data(scanner_x, scanner_y)

        if not plane_shot_down and self.direction_dist_calc(self.plane_ctd, self.target_ctds[self.current_target_idx]) < plane_base_speed * timer:
            self.current_target_idx = (self.current_target_idx + 1) % len(self.target_ctds)
            radio = 1
            target_change_timer = 0.0

        if not missile_fired and radio == 2:
            self.target_ctds = brutal_copy.deepcopy(self.targets_saver)
            t = 0
            radio = 0

        t += timer
        return (self.plane_dot, self.missile_dot, self.plane_missile_dot, self.defense_missile_dot, self.radar_point, self.info_text, self.target_text, self.locked_text,
                self.top_panel, self.bottom_panel, self.left_line, self.right_line, self.scanner_line)

    def main(self):
        ani = FuncAnimation(self.fig, self.update, frames=None, interval=50, blit=False)
        self.ax.legend(loc='upper left', facecolor='black', edgecolor='white', labelcolor='white')
        plt.show()

obj1 = S400_Russian_Missile()
obj1.main()
