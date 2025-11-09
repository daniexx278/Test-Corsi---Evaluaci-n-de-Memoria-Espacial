import pygame
import sys
import random
import pandas as pd
from datetime import datetime

class CorsiTaskPygame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test Corsi - Memoria Espacial")
        self.clock = pygame.time.Clock()
        
        # Colores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 100, 200)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 200, 0)
        self.RED = (255, 0, 0)
        
        # Posiciones de los círculos (9 posiciones)
        self.circle_positions = [
            (150, 150), (400, 150), (650, 150),
            (150, 300), (400, 300), (650, 300),
            (150, 450), (400, 450), (650, 450)
        ]
        self.circle_radius = 40
        
        # Variables del experimento
        self.sequence_count = 2
        self.corsi_span = 0
        self.error_count = 0
        self.data = []
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def show_instructions(self):
        instructions = [
            "TEST DE MEMORIA ESPACIAL",
            "",
            "Verás una secuencia de círculos que se iluminarán.",
            "Debes hacer clic en los mismos círculos en el mismo orden.",
            "",
            "La secuencia comenzará corta y se hará más larga.",
            "",
            "Presiona ESPACIO para comenzar..."
        ]
        
        running = True
        while running:
            self.screen.fill(self.BLACK)
            
            # Dibujar texto de instrucciones
            for i, line in enumerate(instructions):
                text = self.small_font.render(line, True, self.WHITE)
                self.screen.blit(text, (50, 100 + i * 30))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
    
    def show_countdown(self):
        for i in range(3, 0, -1):
            self.screen.fill(self.BLACK)
            text = self.font.render(str(i), True, self.WHITE)
            self.screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(1000)
    
    def draw_circles(self, highlight_index=None):
        self.screen.fill(self.BLACK)
        for i, pos in enumerate(self.circle_positions):
            color = self.YELLOW if highlight_index == i else self.BLUE
            pygame.draw.circle(self.screen, color, pos, self.circle_radius)
            pygame.draw.circle(self.screen, self.WHITE, pos, self.circle_radius, 2)
    
    def show_sequence(self, sequence):
        # Mostrar todos los círculos en azul primero
        self.draw_circles()
        pygame.display.flip()
        pygame.time.wait(500)
        
        # Mostrar la secuencia
        for circle_index in sequence:
            self.draw_circles(highlight_index=circle_index)
            pygame.display.flip()
            pygame.time.wait(800)  # Tiempo iluminado
            
            self.draw_circles()
            pygame.display.flip()
            pygame.time.wait(300)  # Pausa entre iluminaciones
    
    def get_clicked_circle(self):
        waiting = True
        clicked_index = None
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    # Verificar clic en círculos
                    for i, circle_pos in enumerate(self.circle_positions):
                        distance = ((pos[0] - circle_pos[0])**2 + (pos[1] - circle_pos[1])**2)**0.5
                        if distance <= self.circle_radius:
                            clicked_index = i
                            waiting = False
                            
                            # Feedback visual del clic
                            self.draw_circles(highlight_index=i)
                            pygame.display.flip()
                            pygame.time.wait(200)
            
            self.clock.tick(30)
        
        return clicked_index
    
    def check_sequence_correct(self, user_sequence, correct_sequence):
        if len(user_sequence) != len(correct_sequence):
            return False
        
        for user_click, correct_click in zip(user_sequence, correct_sequence):
            if user_click != correct_click:
                return False
        
        return True
    
    def show_feedback(self, correct):
        feedback_text = "✓ CORRECTO" if correct else "✗ INCORRECTO"
        color = self.GREEN if correct else self.RED
        
        text = self.font.render(feedback_text, True, color)
        self.screen.blit(text, (400 - text.get_width() // 2, 550))
        pygame.display.flip()
        pygame.time.wait(1500)
    
    def run_trial(self):
        # Generar secuencia aleatoria
        sequence = random.sample(range(len(self.circle_positions)), self.sequence_count)
        
        # Mostrar secuencia
        self.show_sequence(sequence)
        
        # Señal de inicio para respuesta
        self.draw_circles()
        text = self.font.render("¡Tu turno!", True, self.WHITE)
        self.screen.blit(text, (400 - text.get_width() // 2, 50))
        pygame.display.flip()
        
        # Capturar respuesta del usuario
        user_sequence = []
        for _ in range(self.sequence_count):
            clicked = self.get_clicked_circle()
            if clicked is not None:
                user_sequence.append(clicked)
        
        # Verificar si es correcto
        correct = self.check_sequence_correct(user_sequence, sequence)
        self.show_feedback(correct)
        
        # Guardar datos
        trial_data = {
            'sequence_length': self.sequence_count,
            'correct_sequence': str(sequence),
            'user_sequence': str(user_sequence),
            'correct': correct,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data.append(trial_data)
        
        # Actualizar variables
        if correct:
            self.corsi_span = self.sequence_count
            self.sequence_count += 1
            self.error_count = 0
        else:
            self.error_count += 1
        
        return correct
    
    def show_final_results(self):
        self.screen.fill(self.BLACK)
        lines = [
            "FIN DEL EXPERIMENTO",
            "",
            f"Tu span de Corsi es: {self.corsi_span} elementos",
            "",
            "Presiona ESPACIO para salir..."
        ]
        
        for i, line in enumerate(lines):
            text = self.small_font.render(line, True, self.WHITE)
            self.screen.blit(text, (400 - text.get_width() // 2, 200 + i * 30))
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
    
    def save_data(self):
        filename = f"corsi_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"Datos guardados en: {filename}")
    
    def run_experiment(self):
        self.show_instructions()
        self.show_countdown()
        
        while self.sequence_count <= 9 and self.error_count < 2:
            self.run_trial()
            pygame.time.wait(1000)
        
        self.show_final_results()
        self.save_data()
        pygame.quit()

# Ejecutar el experimento
if __name__ == "__main__":
    try:
        experiment = CorsiTaskPygame()
        experiment.run_experiment()
    except Exception as e:
        print(f"Error: {e}")
        print("Asegúrate de tener pygame y pandas instalados: pip install pygame pandas")