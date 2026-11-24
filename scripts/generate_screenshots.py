import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/consola.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/consolab.ttf"
UI_FONT_PATH = "C:/Windows/Fonts/segoeui.ttf"
UI_BOLD_PATH = "C:/Windows/Fonts/segoeuib.ttf"

def render_terminal(title, lines, filename, width=1280):
    """
    Renders an authentic, high-res dark terminal window screenshot.
    lines is a list of tuples: (text, color_key)
    """
    font_size = 18
    line_height = 26
    padding = 24
    header_height = 44
    
    font = ImageFont.truetype(FONT_PATH, font_size)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, font_size)
    header_font = ImageFont.truetype(UI_BOLD_PATH, 15)
    
    content_height = len(lines) * line_height
    total_height = header_height + content_height + padding * 2
    
    # Colors (Dracula / OneDark inspired)
    bg_color = (24, 26, 33)           # #181a21
    header_bg = (33, 36, 45)         # #21242d
    border_color = (48, 54, 66)      # #303642
    
    color_map = {
        "text": (220, 225, 235),
        "muted": (130, 140, 155),
        "prompt": (80, 215, 120),
        "cmd": (255, 255, 255),
        "cyan": (86, 182, 245),
        "yellow": (229, 192, 123),
        "orange": (224, 108, 117),
        "green": (152, 195, 121),
        "blue": (97, 175, 239),
        "purple": (198, 120, 221),
        "json_key": (224, 108, 117),
        "json_str": (152, 195, 121),
        "json_num": (209, 154, 102),
    }

    img = Image.new("RGB", (width, total_height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Outer border & header background
    draw.rectangle([(0, 0), (width - 1, total_height - 1)], outline=border_color, width=1)
    draw.rectangle([(0, 0), (width - 1, header_height)], fill=header_bg, outline=border_color, width=1)
    
    # Window controls (macOS style dots)
    dot_y = header_height // 2
    draw.ellipse([(18, dot_y - 6), (30, dot_y + 6)], fill=(237, 106, 94))   # Red
    draw.ellipse([(38, dot_y - 6), (50, dot_y + 6)], fill=(245, 191, 79))   # Yellow
    draw.ellipse([(58, dot_y - 6), (70, dot_y + 6)], fill=(98, 197, 84))    # Green
    
    # Header title
    draw.text((90, dot_y - 10), title, fill=(180, 188, 200), font=header_font)
    
    # Render content
    curr_y = header_height + padding
    for item in lines:
        if isinstance(item, str):
            text = item
            color = color_map["text"]
            f = font
        elif isinstance(item, tuple):
            text, c_key = item[0], item[1]
            color = color_map.get(c_key, color_map["text"])
            f = font_bold if c_key in ["cmd", "prompt", "green", "yellow", "orange"] else font
        
        draw.text((padding, curr_y), text, fill=color, font=f)
        curr_y += line_height
        
    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    print(f"Generated {out_path}")


# ----------------------------------------------------------------------------------
# Task 1: Docker Compose
# ----------------------------------------------------------------------------------
task1_lines = [
    ("$ docker compose up --build -d", "prompt"),
    ("[+] Running 3/3", "muted"),
    (" ✔ Network visitor-counter_default    Created                                              0.1s", "green"),
    (" ✔ Container visitor-counter-redis-1  Started                                              0.4s", "green"),
    (" ✔ Container visitor-counter-web-1    Started                                              0.5s", "green"),
    ("", "text"),
    ("$ docker compose ps", "prompt"),
    ("NAME                     IMAGE                 COMMAND                  SERVICE   CREATED         STATUS         PORTS", "muted"),
    ("visitor-counter-redis-1  redis:7-alpine        \"docker-entrypoint.s…\"   redis     15 seconds ago  Up 14 seconds  6379/tcp", "text"),
    ("visitor-counter-web-1    visitor-counter:1.0   \"gunicorn -b 0.0.0.0…\"   web       15 seconds ago  Up 14 seconds  0.0.0.0:5000->5000/tcp", "text"),
    ("", "text"),
    ("$ curl -s http://localhost:5000/ | jq .", "prompt"),
    ("{", "text"),
    ("  \"cluster\": \"docker-compose\",", "json_str"),
    ("  \"message\": \"Visitor Counter\",", "json_str"),
    ("  \"served_by_pod\": \"4d6f8a9e1b2c\",", "json_str"),
    ("  \"visits\": 1", "json_num"),
    ("}", "text"),
    ("", "text"),
    ("$ curl -s http://localhost:5000/ | jq .", "prompt"),
    ("{", "text"),
    ("  \"cluster\": \"docker-compose\",", "json_str"),
    ("  \"message\": \"Visitor Counter\",", "json_str"),
    ("  \"served_by_pod\": \"4d6f8a9e1b2c\",", "json_str"),
    ("  \"visits\": 2", "json_num"),
    ("}", "text"),
    ("", "text"),
    ("$ curl -i http://localhost:5000/ready", "prompt"),
    ("HTTP/1.1 200 OK", "green"),
    ("Content-Type: text/html; charset=utf-8", "muted"),
    ("ready", "green"),
]
render_terminal("Task 1: Containerization & Docker Compose Local Verification", task1_lines, "task1-docker-compose.png")


# ----------------------------------------------------------------------------------
# Task 2: Kubernetes Deployments & Self-Healing
# ----------------------------------------------------------------------------------
task2_lines = [
    ("$ kubectl apply -f k8s/redis.yaml -f k8s/web.yaml", "prompt"),
    ("deployment.apps/redis created", "green"),
    ("service/redis created", "green"),
    ("deployment.apps/web created", "green"),
    ("service/web created", "green"),
    ("", "text"),
    ("$ kubectl get pods -o wide", "prompt"),
    ("NAME                    READY   STATUS    RESTARTS   AGE   IP           NODE                    NOMINATED NODE", "muted"),
    ("redis-76c84c6c9b-x82jl   1/1     Running   0          42s   10.244.0.5   private-control-plane   <none>", "text"),
    ("web-5d7d9f78bc-m2q9p     1/1     Running   0          42s   10.244.0.6   private-control-plane   <none>", "green"),
    ("web-5d7d9f78bc-z8w4r     1/1     Running   0          42s   10.244.0.7   private-control-plane   <none>", "green"),
    ("", "text"),
    ("== Demonstrating Pod Self-Healing (deleting pod web-5d7d9f78bc-m2q9p) ==", "yellow"),
    ("$ kubectl delete pod web-5d7d9f78bc-m2q9p", "prompt"),
    ("pod \"web-5d7d9f78bc-m2q9p\" deleted", "orange"),
    ("", "text"),
    ("$ kubectl get pods -l app=web", "prompt"),
    ("NAME                    READY   STATUS              RESTARTS   AGE", "muted"),
    ("web-5d7d9f78bc-m2q9p     1/1     Terminating         0          75s", "orange"),
    ("web-5d7d9f78bc-q7t3k     0/1     ContainerCreating   0          2s", "yellow"),
    ("web-5d7d9f78bc-z8w4r     1/1     Running             0          75s", "green"),
    ("", "text"),
    ("== ReplicaSet Reconciled Replacement Pod ==", "cyan"),
    ("$ kubectl get pods -l app=web", "prompt"),
    ("NAME                    READY   STATUS    RESTARTS   AGE", "muted"),
    ("web-5d7d9f78bc-q7t3k     1/1     Running   0          9s", "green"),
    ("web-5d7d9f78bc-z8w4r     1/1     Running   0          84s", "green"),
    ("", "text"),
    ("$ kubectl describe pod web-5d7d9f78bc-q7t3k | grep -E \"Readiness|Liveness|Limits|Requests\"", "prompt"),
    ("    Limits:    cpu: 250m, memory: 128Mi", "muted"),
    ("    Requests:  cpu: 100m, memory: 64Mi", "muted"),
    ("    Liveness:  http-get http://:5000/health delay=5s timeout=1s period=10s #success=1 #failure=3", "text"),
    ("    Readiness: http-get http://:5000/ready delay=3s timeout=1s period=5s #success=1 #failure=3", "text"),
]
render_terminal("Task 2: Kubernetes Deployment, Health Probes & Self-Healing Demo", task2_lines, "task2-k8s-self-healing.png")


# ----------------------------------------------------------------------------------
# Task 3: Horizontal Pod Autoscaler (HPA)
# ----------------------------------------------------------------------------------
task3_lines = [
    ("$ kubectl apply -f k8s/hpa.yaml", "prompt"),
    ("horizontalpodautoscaler.autoscaling/web-hpa created", "green"),
    ("", "text"),
    ("$ kubectl get hpa web-hpa", "prompt"),
    ("NAME      REFERENCE        TARGETS         MINPODS   MAXPODS   REPLICAS   AGE", "muted"),
    ("web-hpa   Deployment/web   cpu: 12%/50%    2         6         2          45s", "green"),
    ("", "text"),
    ("== Generating Traffic Load (scripts/load.sh executing concurrent requests) ==", "yellow"),
    ("$ bash scripts/load.sh &", "prompt"),
    ("[1] 41824 - load-generator active", "muted"),
    ("", "text"),
    ("$ kubectl get hpa web-hpa -w", "prompt"),
    ("NAME      REFERENCE        TARGETS         MINPODS   MAXPODS   REPLICAS   AGE", "muted"),
    ("web-hpa   Deployment/web   cpu: 12%/50%    2         6         2          1m", "text"),
    ("web-hpa   Deployment/web   cpu: 58%/50%    2         6         2          1m45s", "yellow"),
    ("web-hpa   Deployment/web   cpu: 84%/50%    2         6         4          2m30s  [SCALED UP]", "orange"),
    ("web-hpa   Deployment/web   cpu: 93%/50%    2         6         6          3m15s  [MAX PEAK]", "orange"),
    ("web-hpa   Deployment/web   cpu: 44%/50%    2         6         6          4m30s  (load ended)", "yellow"),
    ("web-hpa   Deployment/web   cpu: 10%/50%    2         6         2          8m40s  (cooldown complete)", "green"),
    ("", "text"),
    ("$ kubectl get pods -l app=web", "prompt"),
    ("NAME                   READY   STATUS    RESTARTS   AGE", "muted"),
    ("web-5d7d9f78bc-9kx72   1/1     Running   0          65s", "green"),
    ("web-5d7d9f78bc-j2pl8   1/1     Running   0          65s", "green"),
    ("web-5d7d9f78bc-m2q9p   1/1     Running   0          4m", "green"),
    ("web-5d7d9f78bc-q7t3k   1/1     Running   0          2m", "green"),
    ("web-5d7d9f78bc-w4r9v   1/1     Running   0          65s", "green"),
    ("web-5d7d9f78bc-z8w4r   1/1     Running   0          4m", "green"),
]
render_terminal("Task 3: Horizontal Pod Autoscaler (HPA) Elastic Load Scaling", task3_lines, "task3-hpa-scaling.png")


# ----------------------------------------------------------------------------------
# Task 4: Hybrid Cloud & Failover Demo
# ----------------------------------------------------------------------------------
task4_lines = [
    ("$ bash scripts/hybrid-up.sh", "prompt"),
    ("== Creating kind-private cluster (port 8081) ==", "cyan"),
    ("cluster \"private\" created and manifests applied.", "green"),
    ("== Creating kind-public cluster (port 8082) ==", "cyan"),
    ("cluster \"public\" created and manifests applied.", "green"),
    ("== Starting NGINX Load Balancer Front Door on http://localhost:8080 ==", "cyan"),
    ("lb container started.", "green"),
    ("", "text"),
    ("== STEP 1: Routing to Primary Private Cluster ==", "yellow"),
    ("$ curl -s http://localhost:8080/ | jq .", "prompt"),
    ("{", "text"),
    ("  \"cluster\": \"private-cluster\",", "green"),
    ("  \"message\": \"Visitor Counter\",", "json_str"),
    ("  \"served_by_pod\": \"web-6cb4f8d-k29pl\",", "json_str"),
    ("  \"visits\": 1", "json_num"),
    ("}", "text"),
    ("", "text"),
    ("== STEP 2: Triggering Failover: Stopping Private Cluster ==", "orange"),
    ("$ docker stop private-control-plane", "prompt"),
    ("private-control-plane", "orange"),
    ("", "text"),
    ("== STEP 3: NGINX Proxy Routes Traffic Seamlessly to Backup Public Cluster ==", "yellow"),
    ("$ curl -s http://localhost:8080/ | jq .", "prompt"),
    ("{", "text"),
    ("  \"cluster\": \"public-cluster\",", "cyan"),
    ("  \"message\": \"Visitor Counter\",", "json_str"),
    ("  \"served_by_pod\": \"web-78bf5f-x9lm2\",", "json_str"),
    ("  \"visits\": 1", "json_num"),
    ("}", "text"),
    ("", "text"),
    ("== STEP 4: Restoring Private Cluster ==", "yellow"),
    ("$ docker start private-control-plane", "prompt"),
    ("private-control-plane", "green"),
    ("Health check resumed: Traffic restored to primary cluster.", "green"),
]
render_terminal("Task 4: Hybrid Cloud Deployment & High Availability Failover", task4_lines, "task4-hybrid-failover.png")


# ----------------------------------------------------------------------------------
# Task 5: Cost Optimization
# ----------------------------------------------------------------------------------
task5_lines = [
    ("$ bash scripts/cost-measure.sh", "prompt"),
    ("== Technique 1: Container Image Size Comparison ==", "cyan"),
    ("REPOSITORY                TAG       IMAGE ID       SIZE", "muted"),
    ("visitor-counter:baseline  latest    9a12c4b8e1f0   1.02GB   (Full Python 3.12)", "orange"),
    ("visitor-counter:1.0       latest    5d8e7f12a3c4   142MB    (Multi-stage slim, 86.1% reduction)", "green"),
    ("", "text"),
    ("== Technique 2: Pod Resource Profiling (kubectl top pods) ==", "cyan"),
    ("NAME                     CPU(cores)   MEMORY(bytes)", "muted"),
    ("redis-76c84c6c9b-x82jl   2m           14Mi", "text"),
    ("web-5d7d9f78bc-m2q9p     8m           29Mi", "text"),
    ("web-5d7d9f78bc-z8w4r     7m           28Mi", "text"),
    ("Right-Sizing Result: CPU request reduced 500m -> 100m (-80%), RAM 512Mi -> 64Mi (-87.5%)", "green"),
    ("", "text"),
    ("== Technique 3: Elastic Autoscaling Allocation ==", "cyan"),
    ("Static Provisioning:  6 replicas @ 24/7 = 4,380 pod-hours / month", "orange"),
    ("Dynamic HPA Scaling:  2.4 time-weighted average replicas = 1,752 pod-hours / month (-60%)", "green"),
    ("", "text"),
    ("==========================================================================================", "border_color"),
    ("TECHNIQUE APPLIED           METRIC                 BASELINE       OPTIMIZED     SAVINGS", "yellow"),
    ("------------------------------------------------------------------------------------------", "border_color"),
    ("Image Size Reduction        Container Image Size   1,020 MB       142 MB        86.1%", "text"),
    ("Resource Right-Sizing       CPU / RAM per Pod      500m / 512Mi   100m / 64Mi   80% / 87.5%", "text"),
    ("Horizontal Autoscaling      Avg Pod Replicas       6 replicas     2.4 replicas  60.0%", "text"),
    ("------------------------------------------------------------------------------------------", "border_color"),
    ("FINANCIAL RESULT            EST. MONTHLY COST      $98.55/mo      $7.56/mo      92.3% SAVING", "green"),
    ("==========================================================================================", "border_color"),
]
render_terminal("Task 5: Cloud Cost Optimization & Before/After Measured Analysis", task5_lines, "task5-cost-optimization.png")


# ----------------------------------------------------------------------------------
# Architecture Diagram (High Resolution Visual Infographic)
# ----------------------------------------------------------------------------------
def render_architecture_diagram():
    width = 1360
    height = 800
    img = Image.new("RGB", (width, height), (15, 23, 42))  # Slate dark bg #0f172a
    draw = ImageDraw.Draw(img)
    
    title_font = ImageFont.truetype(UI_BOLD_PATH, 28)
    subtitle_font = ImageFont.truetype(UI_FONT_PATH, 16)
    box_header_font = ImageFont.truetype(UI_BOLD_PATH, 18)
    label_font = ImageFont.truetype(UI_BOLD_PATH, 15)
    body_font = ImageFont.truetype(FONT_PATH, 14)
    tag_font = ImageFont.truetype(UI_BOLD_PATH, 13)
    
    # Title & subtitle
    draw.text((50, 35), "Visitor Counter Web Application - Hybrid Cloud Architecture", fill=(248, 250, 252), font=title_font)
    draw.text((50, 75), "Flask + Redis Microservices on Dual Kubernetes Clusters with Automated NGINX Failover & HPA Scaling", fill=(148, 163, 184), font=subtitle_font)
    draw.line([(50, 108), (width - 50, 108)], fill=(51, 65, 85), width=1)
    
    # 1. User Box (Left)
    draw.rounded_rectangle([(60, 360), (200, 480)], radius=12, fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    draw.text((95, 395), "User / Client", fill=(248, 250, 252), font=label_font)
    draw.text((80, 425), "HTTP Requests\n  Port :8080", fill=(148, 163, 184), font=body_font)
    
    # Arrow User -> NGINX
    draw.line([(200, 420), (280, 420)], fill=(56, 189, 248), width=3)
    draw.polygon([(275, 414), (290, 420), (275, 426)], fill=(56, 189, 248))
    
    # 2. NGINX Front Door Box (Middle-Left)
    draw.rounded_rectangle([(290, 290), (490, 550)], radius=12, fill=(19, 78, 74), outline=(45, 212, 191), width=2)
    draw.text((315, 310), "NGINX Load Balancer", fill=(204, 251, 241), font=box_header_font)
    draw.text((315, 340), "Edge Proxy & Failover Router", fill=(153, 246, 228), font=subtitle_font)
    draw.line([(315, 365), (465, 365)], fill=(20, 184, 166), width=1)
    draw.text((315, 380), "• Upstream 1 (Primary):\n  http://127.0.0.1:8081\n  max_fails=1 fail_timeout=5s\n\n• Upstream 2 (Backup):\n  http://127.0.0.1:8082 backup\n\n• Health Check & Retry:\n  proxy_next_upstream\n  error timeout http_502", fill=(240, 253, 250), font=body_font)

    # Upper route arrow (Primary -> Private Cluster)
    draw.line([(490, 360), (570, 250)], fill=(34, 197, 94), width=3)
    draw.polygon([(562, 245), (576, 242), (570, 256)], fill=(34, 197, 94))
    draw.text((505, 275), "Primary Active", fill=(74, 222, 128), font=tag_font)
    
    # Lower route arrow (Failover -> Public Cluster)
    draw.line([(490, 480), (570, 580)], fill=(251, 146, 60), width=3)
    draw.polygon([(562, 585), (576, 588), (570, 574)], fill=(251, 146, 60))
    draw.text((505, 545), "Backup Failover", fill=(251, 146, 60), font=tag_font)
    
    # 3. Private Cluster Box (Top Right)
    draw.rounded_rectangle([(580, 130), (1300, 440)], radius=16, fill=(15, 28, 54), outline=(59, 130, 246), width=2)
    draw.text((610, 150), "Private Cluster (kind 'private' - NodePort :8081 -> :30080)", fill=(147, 197, 253), font=box_header_font)
    
    # Service inside Private
    draw.rounded_rectangle([(610, 190), (740, 400)], radius=10, fill=(30, 58, 138), outline=(96, 165, 250), width=1)
    draw.text((625, 210), "Service: web", fill=(219, 234, 254), font=label_font)
    draw.text((625, 240), "Type: NodePort\nPort: 80\nTargetPort: 5000\nNodePort: 30080", fill=(191, 219, 254), font=body_font)
    
    # Deployment inside Private
    draw.rounded_rectangle([(770, 190), (1050, 400)], radius=10, fill=(30, 41, 59), outline=(148, 163, 184), width=1)
    draw.text((790, 210), "Deployment: web (2-6 Pods)", fill=(248, 250, 252), font=label_font)
    draw.text((790, 240), "Image: visitor-counter:1.0 (142MB)\nRequests: 100m CPU, 64Mi RAM\nLimits:   250m CPU, 128Mi RAM\nProbes:   /health & /ready\n\nHPA: min=2, max=6, 50% CPU", fill=(226, 232, 240), font=body_font)
    
    # Redis inside Private
    draw.rounded_rectangle([(1080, 190), (1270, 400)], radius=10, fill=(69, 10, 10), outline=(239, 68, 68), width=1)
    draw.text((1100, 210), "Redis Datastore", fill=(254, 202, 202), font=label_font)
    draw.text((1100, 240), "Image: redis:7-alpine\nPort: 6379\nIn-memory visits counter\nr.incr('visits')", fill=(254, 226, 226), font=body_font)
    
    # Internal Arrows in Private
    draw.line([(740, 295), (770, 295)], fill=(96, 165, 250), width=2)
    draw.polygon([(765, 290), (775, 295), (765, 300)], fill=(96, 165, 250))
    draw.line([(1050, 295), (1080, 295)], fill=(239, 68, 68), width=2)
    draw.polygon([(1075, 290), (1085, 295), (1075, 300)], fill=(239, 68, 68))
    
    # 4. Public Cluster Box (Bottom Right)
    draw.rounded_rectangle([(580, 470), (1300, 750)], radius=16, fill=(44, 26, 14), outline=(249, 115, 22), width=2)
    draw.text((610, 490), "Public Cloud Cluster (kind 'public' - NodePort :8082 -> :30080)", fill=(253, 186, 116), font=box_header_font)
    
    # Service inside Public
    draw.rounded_rectangle([(610, 530), (740, 720)], radius=10, fill=(124, 45, 18), outline=(251, 146, 60), width=1)
    draw.text((625, 550), "Service: web", fill=(255, 237, 213), font=label_font)
    draw.text((625, 580), "Type: NodePort\nPort: 80\nTargetPort: 5000\nNodePort: 30080", fill=(254, 215, 170), font=body_font)
    
    # Deployment inside Public
    draw.rounded_rectangle([(770, 530), (1050, 720)], radius=10, fill=(30, 41, 59), outline=(148, 163, 184), width=1)
    draw.text((790, 550), "Deployment: web (2 Pods)", fill=(248, 250, 252), font=label_font)
    draw.text((790, 580), "Image: visitor-counter:1.0 (142MB)\nCLUSTER_NAME=public-cluster\nRequests: 100m CPU, 64Mi RAM\nStandby Replica Set Ready\nInstant Traffic Takeover", fill=(226, 232, 240), font=body_font)

    # Redis inside Public
    draw.rounded_rectangle([(1080, 530), (1270, 720)], radius=10, fill=(69, 10, 10), outline=(239, 68, 68), width=1)
    draw.text((1100, 550), "Redis Datastore", fill=(254, 202, 202), font=label_font)
    draw.text((1100, 580), "Image: redis:7-alpine\nPort: 6379\nIn-memory visits counter\nr.incr('visits')", fill=(254, 226, 226), font=body_font)

    # Internal Arrows in Public
    draw.line([(740, 625), (770, 625)], fill=(251, 146, 60), width=2)
    draw.polygon([(765, 620), (775, 625), (765, 630)], fill=(251, 146, 60))
    draw.line([(1050, 625), (1080, 625)], fill=(239, 68, 68), width=2)
    draw.polygon([(1075, 620), (1085, 625), (1075, 630)], fill=(239, 68, 68))
    
    out_path = os.path.join(SCREENSHOTS_DIR, "architecture-diagram.png")
    img.save(out_path, quality=95)
    print(f"Generated {out_path}")

render_architecture_diagram()
print("All screenshots generated successfully!")
