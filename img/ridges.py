# Draws img/ridges.svg, the figure of the home page: mountain ridges whose profiles are Brownian paths (seeded), and a
# climbing route to the highest summit. Run: python img/ridges.py
import math, os, random

W, H, N = 960, 640, 240
random.seed(2017)
layers = [("#16204a", 0.30, 360, 150, 0.9), ("#1d2f6b", 0.42, 430, 190, 1.0), ("#27458f", 0.58, 500, 240, 1.15), ("#2f5fc0", 0.78, 580, 300, 1.3)]
paths = []
for k, (color, light, base, amp, vol) in enumerate(layers):
    x0 = random.uniform(0.25, 0.75)
    w = [0.0]
    for _ in range(N):
        w.append(w[-1] + random.gauss(0, 1) * vol / math.sqrt(N) * 3.2)
    pts = []
    for i in range(N + 1):
        x = i / N
        envelope = math.exp(-((x - x0) ** 2) / (2 * 0.16 ** 2))
        y = base - amp * envelope - 38 * (w[i] - w[0]) / 3 + (k * 18)
        pts.append((x * W, y))
    paths.append((color, pts))
front = paths[-1][1]
summit = min(front, key=lambda p: p[1])
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Mountain ridges drawn from Brownian paths, with a climbing route to the summit">',
       '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f8cff" stop-opacity="0.18"/><stop offset="1" stop-color="#0b1020" stop-opacity="0"/></linearGradient>',
       '<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0.75" stop-color="#0b1020" stop-opacity="0"/><stop offset="1" stop-color="#0b1020" stop-opacity="1"/></linearGradient></defs>',
       f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
for i in range(70):
    x, y, r = random.uniform(0, W), random.uniform(0, 260), random.choice([0.8, 1, 1.2, 1.6])
    out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#f5f7fa" opacity="{random.uniform(0.2, 0.7):.2f}"/>')
for color, pts in paths:
    d = "M0," + str(H) + " " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts) + f" L{W},{H} Z"
    out.append(f'<path d="{d}" fill="{color}"/>')
    ridge = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<polyline points="{ridge}" fill="none" stroke="#38cfff" stroke-opacity="0.35" stroke-width="1.2"/>')
# the route: from the foot to the summit along the front ridge, zigzagging a little below it
i_s = front.index(summit)
start = max(0, i_s - 70)
route = []
for j, i in enumerate(range(start, i_s + 1, 3)):
    x, y = front[i]
    route.append((x, y + 26 * (1 - (i - start) / max(1, i_s - start)) + (6 if j % 2 else -2)))
route.append(summit)
out.append('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in route) + '" fill="none" stroke="#ffb84d" stroke-width="2.4" stroke-dasharray="2 7" stroke-linecap="round"/>')
for x, y in route[:-1:6]:
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#ffb84d"/>')
sx, sy = summit
out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="6" fill="#ffb84d" stroke="#0b1020" stroke-width="2"/>')
out.append(f'<path d="M{sx:.1f},{sy - 6:.1f} V{sy - 34:.1f} L{sx + 18:.1f},{sy - 28:.1f} L{sx:.1f},{sy - 22:.1f}" fill="#00d4aa" stroke="#00d4aa" stroke-width="1.6" stroke-linejoin="round"/>')
out.append(f'<rect width="{W}" height="{H}" fill="url(#fade)"/>')
out.append("</svg>")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ridges.svg"), "w", encoding="utf-8").write("\n".join(out))
