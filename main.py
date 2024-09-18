import pygame, json, sys, math, time

# Helper functions
def dist(a = tuple, b = tuple):
    return math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)

animName = input("Animation name: ")

appSettings = {}

animationSettings = {}
animation = []

with open(f"animations/{animName}.json", "r") as animFile:
    data = json.load(animFile)
    animationSettings = data["settings"]
    animation = data["anim"]

with open("settings.json", "r") as settingsFile:
    appSettings = json.load(settingsFile)

frame = 0

win = pygame.display.set_mode((animationSettings["window"]["x"], animationSettings["window"]["y"]))

win.fill(animationSettings["bgcol"])


def eventSystem():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


animStarted = False
while not pygame.key.get_pressed()[pygame.key.key_code(appSettings["playerKey"])]:
    eventSystem()

start = time.time()
print("Animation Started")

for step in animation:
    eventSystem()

    if step["type"] == "drawLine":
        if step["meta"]["time"] > 0:
            lineLen = dist(step["meta"]["start"], step["meta"]["end"])
            stepLen = lineLen / step["meta"]["time"]
            for frame in range(step["meta"]["time"]-1):
                eventSystem()

                start = step["meta"]["start"]
                end = step["meta"]["end"]
                vec = (end[0]-start[0], end[1]-start[1])
                mag = math.sqrt(vec[0]**2 + vec[1]**2)
                vec = (vec[0]/mag, vec[1]/mag)
                vec = (vec[0]*stepLen*frame, vec[1]*stepLen*frame)
                pt = (vec[0] + start[0], vec[1] + start[1])
                pygame.draw.line(win, step["meta"]["color"], start, pt, step["meta"]["width"])

                pygame.display.update()

                pygame.time.Clock().tick(animationSettings["framerate"])

            pygame.draw.line(win, step["meta"]["color"], start, end, step["meta"]["width"])

            pygame.display.update()

    if step["type"] == "drawCircle":
        if step["meta"]["time"] > 0:
            segLen = 360/step["meta"]["time"]/step["meta"]["resolution"]
            for frame in range(step["meta"]["time"]):
                for segment in range(step["meta"]["resolution"]):
                    a0 = segLen*frame*(segment)
                    a1 = segLen*frame*segment
                    pt0 = (math.sin(a1) * 100, math.cos(a1) * 100)
                    pt1 = (math.sin(a0) * 100, math.cos(a0) * 100)
                    print(a1, pt0)
                    print(a0, pt1)
                    pygame.draw.line(
                        win, 
                        step["meta"]["color"],
                        pt0,
                        pt1,
                        step["meta"]["width"]
                    )
                
                pygame.display.update()

                pygame.time.Clock().tick(animationSettings["framerate"])

    if step["type"] == "erase":
        win.fill(animationSettings["bgcol"])
        pygame.display.update()

    if step["type"] == "wait":
        for frame in range(step["meta"]["time"]):
            pygame.time.Clock().tick(animationSettings["framerate"])


    pygame.display.update()

    pygame.time.Clock().tick(animationSettings["framerate"])

end = time.time()
elapsed = end-start
print(f"Animation finished ({elapsed}s)")

while True:
    eventSystem()