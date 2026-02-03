import tkinter as tk
import random

WIDTH, HEIGHT = 400, 600
GRAVITY = 2
BIRD_JUMP = -20
PIPE_SPEED = 5
PIPE_GAP = 150

class Bird:
    def __init__(self, canvas):
        self.canvas = canvas
        self.y = HEIGHT // 2
        self.velocity = 0
        self.shape = canvas.create_oval(50, self.y, 80, self.y+30, fill="yellow")

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.canvas.coords(self.shape, 50, self.y, 80, self.y+30)

    def jump(self, event=None):
        self.velocity = BIRD_JUMP

class Pipe:
    def __init__(self, canvas, x):
        self.canvas = canvas
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
        self.top = canvas.create_rectangle(x, 0, x+50, self.height, fill="green")
        self.bottom = canvas.create_rectangle(x, self.height+PIPE_GAP, x+50, HEIGHT, fill="green")
        self.x = x

    def update(self):
        self.x -= PIPE_SPEED
        self.canvas.move(self.top, -PIPE_SPEED, 0)
        self.canvas.move(self.bottom, -PIPE_SPEED, 0)

    def collides(self, bird):
        bx1, by1, bx2, by2 = bird.canvas.coords(bird.shape)
        px1, py1, px2, py2 = self.canvas.coords(self.top)
        qx1, qy1, qx2, qy2 = self.canvas.coords(self.bottom)

        # Collision check
        if bx2 > px1 and bx1 < px2 and by1 < py2:
            return True
        if bx2 > qx1 and bx1 < qx2 and by2 > qy1:
            return True
        return False

def main():
    root = tk.Tk()
    root.title("Flappy Bird (Tkinter)")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
    canvas.pack()

    bird = Bird(canvas)
    pipes = [Pipe(canvas, WIDTH)]
    score = 0
    score_text = canvas.create_text(WIDTH//2, 20, text="0", font=("Arial", 24), fill="white")

    def game_loop():
        nonlocal score, pipes

        bird.update()

        
        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe(canvas, WIDTH))

        
        for pipe in pipes:
            pipe.update()

       
        pipes = [p for p in pipes if p.x > -50]

       
        for pipe in pipes:
            if pipe.collides(bird):
                canvas.itemconfig(score_text, text="Game Over!")
                return

        if bird.y <= 0 or bird.y >= HEIGHT:
            canvas.itemconfig(score_text, text="Game Over!")
            return

        score += 1
        canvas.itemconfig(score_text, text=str(score))

        root.after(50, game_loop)

    root.bind("<space>", bird.jump)
    game_loop()
    root.mainloop()

if __name__ == "__main__":
    main()
