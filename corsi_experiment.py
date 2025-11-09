import pygame
import sys
import random
import pandas as pd
from datetime import datetime
import time

class CorsiTaskPygame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test de Memoria Espacial Corsi")
        self.clock = pygame.time.Clock()
        
        # Colores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 100, 200)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 200, 0)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (180, 70, 200)
        self.ORANGE = (255, 165, 0)
        self.CYAN = (0, 255, 255)
        self.PINK = (255, 105, 180)
        self.BROWN = (165, 42, 42)
        
        # Colores para Test 2 (cuando se iluminan)
        self.test2_highlight_colors = [
            self.RED, self.YELLOW, self.GREEN, self.PURPLE, 
            self.ORANGE, self.CYAN, self.PINK, self.BROWN, self.WHITE
        ]
        
        self.font = pygame.font.Font(None, 32)  # Fuente más pequeña para botones
        self.small_font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 24)  # Fuente más pequeña específica para botones
        
        self.data = []
        self.current_test = None
        
    def show_main_menu(self):
        while True:
            self.screen.fill(self.BLACK)
            
            # Título
            title = self.title_font.render("TEST DE MEMORIA ESPACIAL CORSI", True, self.WHITE)
            self.screen.blit(title, (400 - title.get_width() // 2, 100))
            
            # Botones más grandes para acomodar texto
            test1_rect = pygame.Rect(200, 200, 400, 60)  # Botones más grandes
            test2_rect = pygame.Rect(200, 280, 400, 60)
            exit_rect = pygame.Rect(200, 360, 400, 60)
            
            pygame.draw.rect(self.screen, self.BLUE, test1_rect, border_radius=12)
            pygame.draw.rect(self.screen, self.GREEN, test2_rect, border_radius=12)
            pygame.draw.rect(self.screen, self.RED, exit_rect, border_radius=12)
            
            # Texto de botones con fuente más pequeña
            test1_text = self.button_font.render("TEST 1 - Secuencia Única", True, self.WHITE)
            test2_text = self.button_font.render("TEST 2 - Secuencia con Colores", True, self.WHITE)
            exit_text = self.button_font.render("SALIR", True, self.WHITE)
            
            self.screen.blit(test1_text, (400 - test1_text.get_width() // 2, 225))
            self.screen.blit(test2_text, (400 - test2_text.get_width() // 2, 305))
            self.screen.blit(exit_text, (400 - exit_text.get_width() // 2, 385))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if test1_rect.collidepoint(pos):
                        return "test1"
                    elif test2_rect.collidepoint(pos):
                        return "test2"
                    elif exit_rect.collidepoint(pos):
                        pygame.quit()
                        sys.exit()
    
    def generate_random_positions(self, count=9):
        positions = []
        for _ in range(count):
            # Asegurar que los círculos no se solapen demasiado
            valid_position = False
            attempts = 0
            while not valid_position and attempts < 100:
                x = random.randint(70, 730)
                y = random.randint(100, 500)
                
                # Verificar distancia mínima con otros círculos
                too_close = False
                for existing_pos in positions:
                    distance = ((x - existing_pos[0])**2 + (y - existing_pos[1])**2)**0.5
                    if distance < 80:  # Distancia mínima entre círculos
                        too_close = True
                        break
                
                if not too_close:
                    positions.append((x, y))
                    valid_position = True
                
                attempts += 1
            
            # Si no encontró posición válida, agregar una por defecto
            if not valid_position:
                default_positions = [
                    (100, 150), (250, 120), (400, 150), (550, 120), (700, 150),
                    (150, 300), (300, 330), (450, 300), (600, 330)
                ]
                if len(positions) < len(default_positions):
                    positions.append(default_positions[len(positions)])
        
        return positions
    
    def show_instructions(self, test_type):
        if test_type == "test1":
            instructions = [
                "TEST 1 - SECUENCIA ÚNICA",
                "",
                "Verás una secuencia de círculos que se iluminarán.",
                "Debes hacer clic en los mismos círculos en el mismo orden.",
                "",
                "La secuencia comenzará con 2 elementos y aumentará",
                "hasta 9 elementos. Cada nivel tiene 2 rondas.",
                "",
                "Presiona ESPACIO para la sesión de práctica..."
            ]
        else:
            instructions = [
                "TEST 2 - SECUENCIA CON COLORES",
                "",
                "Verás círculos de diferentes colores que se iluminarán.",
                "Debes hacer clic en los mismos círculos en el mismo orden.",
                "",
                "Cada nivel agrega nuevos colores a la secuencia.",
                "Los círculos estarán en azul y cambiarán de color",
                "cuando se iluminen en la secuencia.",
                "",
                "Presiona ESPACIO para la sesión de práctica..."
            ]
        
        self.show_text_screen(instructions)
    
    def show_text_screen(self, lines):
        waiting = True
        while waiting:
            self.screen.fill(self.BLACK)
            
            for i, line in enumerate(lines):
                if i == 0 and "TEST" in line:
                    text = self.font.render(line, True, self.YELLOW)
                else:
                    text = self.small_font.render(line, True, self.WHITE)
                self.screen.blit(text, (400 - text.get_width() // 2, 150 + i * 35))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # También permitir clic para continuar
                    waiting = False
    
    def show_countdown(self):
        for i in range(3, 0, -1):
            self.screen.fill(self.BLACK)
            text = self.font.render(str(i), True, self.WHITE)
            self.screen.blit(text, (400 - text.get_width() // 2, 300))
            pygame.display.flip()
            pygame.time.wait(1000)
        
        self.screen.fill(self.BLACK)
        text = self.font.render("¡GO!", True, self.GREEN)
        self.screen.blit(text, (400 - text.get_width() // 2, 300))
        pygame.display.flip()
        pygame.time.wait(500)
    
    def practice_session(self, test_type):
        instructions = [
            "SESIÓN DE PRÁCTICA",
            "",
            "Ahora realizarás una secuencia de práctica",
            "con 3 elementos para que te familiarices.",
            "",
            "Presiona ESPACIO para comenzar..."
        ]
        self.show_text_screen(instructions)
        
        # Posiciones aleatorias para práctica
        positions = self.generate_random_positions(9)
        sequence = random.sample(range(9), 3)
        
        # Mostrar secuencia de práctica
        self.show_sequence(sequence, positions, test_type)
        
        # Capturar respuesta
        start_time = time.time()
        user_sequence = self.get_user_sequence(3, positions, test_type)
        end_time = time.time()
        duration = end_time - start_time
        
        # Feedback
        correct = user_sequence == sequence
        self.show_feedback(correct, duration, practice=True)
    
    def show_sequence(self, sequence, positions, test_type, current_level=None):
        # Mostrar todos los círculos primero
        self.draw_circles(positions, test_type, current_level)
        pygame.display.flip()
        pygame.time.wait(800)
        
        # Mostrar la secuencia
        for i, circle_index in enumerate(sequence):
            self.draw_circles(positions, test_type, current_level, highlight_index=circle_index, sequence_index=i)
            pygame.display.flip()
            pygame.time.wait(800)  # Tiempo iluminado
            
            self.draw_circles(positions, test_type, current_level)
            pygame.display.flip()
            pygame.time.wait(400)  # Pausa entre iluminaciones
    
    def draw_circles(self, positions, test_type, current_level=None, highlight_index=None, sequence_index=0):
        self.screen.fill(self.BLACK)
        
        for i, pos in enumerate(positions):
            if test_type == "test1":
                # Test 1: siempre azul, se iluminan en amarillo
                if highlight_index == i:
                    color = self.YELLOW
                else:
                    color = self.BLUE
            else:  # test2
                # Test 2: siempre azul en estado normal
                if highlight_index == i:
                    # Cuando se ilumina, usa colores diferentes según la posición en la secuencia
                    color = self.test2_highlight_colors[sequence_index % len(self.test2_highlight_colors)]
                else:
                    color = self.BLUE  # Todos azules cuando no están iluminados
            
            pygame.draw.circle(self.screen, color, pos, 25)
            pygame.draw.circle(self.screen, self.WHITE, pos, 25, 2)
    
    def get_user_sequence(self, sequence_length, positions, test_type, current_level=None):
        user_sequence = []
        
        self.draw_circles(positions, test_type, current_level)
        text = self.font.render("¡Tu turno!", True, self.WHITE)
        self.screen.blit(text, (400 - text.get_width() // 2, 50))
        pygame.display.flip()
        
        for _ in range(sequence_length):
            clicked = self.get_clicked_circle(positions)
            if clicked is not None and clicked not in user_sequence:
                user_sequence.append(clicked)
                # Mostrar feedback del clic
                self.draw_circles(positions, test_type, current_level, highlight_index=clicked)
                text = self.font.render("¡Tu turno!", True, self.WHITE)
                self.screen.blit(text, (400 - text.get_width() // 2, 50))
                pygame.display.flip()
                pygame.time.wait(200)
        
        return user_sequence
    
    def get_clicked_circle(self, positions):
        clock = pygame.time.Clock()
        clicked_index = None
        
        # Timeout de 30 segundos para prevenir bloqueos
        start_time = time.time()
        timeout = 30
        
        while clicked_index is None and (time.time() - start_time) < timeout:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    for i, circle_pos in enumerate(positions):
                        distance = ((pos[0] - circle_pos[0])**2 + (pos[1] - circle_pos[1])**2)**0.5
                        if distance <= 30:  # Radio un poco mayor para facilitar clic
                            clicked_index = i
                            break
                    if clicked_index is not None:
                        break
            
            clock.tick(60)  # 60 FPS para mejor responsividad
        
        # Si hubo timeout, seleccionar aleatoriamente para evitar bloqueo
        if clicked_index is None:
            print("Timeout - seleccionando aleatoriamente")
            clicked_index = random.randint(0, len(positions) - 1)
        
        return clicked_index
    
    def show_feedback(self, correct, duration, practice=False):
        if practice:
            feedback_text = "✓ PRÁCTICA CORRECTA" if correct else "✗ PRÁCTICA INCORRECTA"
        else:
            feedback_text = "✓ CORRECTO" if correct else "✗ INCORRECTO"
        
        color = self.GREEN if correct else self.RED
        
        self.screen.fill(self.BLACK)
        text1 = self.font.render(feedback_text, True, color)
        text2 = self.small_font.render(f"Tiempo: {duration:.2f} segundos", True, self.WHITE)
        
        self.screen.blit(text1, (400 - text1.get_width() // 2, 250))
        self.screen.blit(text2, (400 - text2.get_width() // 2, 300))
        
        if practice:
            text3 = self.small_font.render("Presiona ESPACIO para continuar con el test...", True, self.WHITE)
            self.screen.blit(text3, (400 - text3.get_width() // 2, 350))
        
        pygame.display.flip()
        
        if practice:
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            waiting = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
        else:
            pygame.time.wait(2000)
    
    def run_test1(self):
        self.current_test = "test1"
        self.show_instructions("test1")
        self.practice_session("test1")
        
        instructions = [
            "¡Fin de la práctica!",
            "",
            "Ahora comenzará el test real.",
            "Recuerda: mantén la concentración.",
            "",
            "Presiona ESPACIO para comenzar el test..."
        ]
        self.show_text_screen(instructions)
        
        self.show_countdown()
        
        test_data = []
        max_level = 9
        
        for level in range(2, max_level + 1):
            print(f"Iniciando nivel {level}")  # Debug
            # Nuevas posiciones para cada nivel
            positions = self.generate_random_positions(9)
            
            for round_num in range(1, 3):  # 2 rondas por nivel
                print(f"  Ronda {round_num}")  # Debug
                # Generar secuencia para esta ronda
                sequence = random.sample(range(9), level)
                
                # Mostrar secuencia
                self.show_sequence(sequence, positions, "test1")
                
                # Capturar respuesta y tiempo
                start_time = time.time()
                user_sequence = self.get_user_sequence(level, positions, "test1")
                end_time = time.time()
                duration = end_time - start_time
                
                # Verificar si es correcto
                correct = user_sequence == sequence
                
                # Guardar datos
                round_data = {
                    'test_type': 'Test1',
                    'level': level,
                    'round': round_num,
                    'sequence_length': level,
                    'correct_sequence': str(sequence),
                    'user_sequence': str(user_sequence),
                    'correct': correct,
                    'duration': round(duration, 2),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                test_data.append(round_data)
                
                # Mostrar feedback
                self.show_feedback(correct, duration)
                
                # Pequeña pausa entre rondas
                if level < max_level or round_num < 2:
                    pygame.time.wait(1000)
        
        # Calcular resultado final
        correct_count = sum(1 for data in test_data if data['correct'])
        total_rounds = len(test_data)
        corsi_span = max([data['level'] for data in test_data if data['correct']] + [0])
        
        # Mostrar resultados finales
        self.show_final_results(test_data, corsi_span, correct_count, total_rounds)
        
        # Guardar datos
        self.save_data(test_data, "test1")
        
        return test_data
    
    def run_test2(self):
        self.current_test = "test2"
        self.show_instructions("test2")
        self.practice_session("test2")
        
        instructions = [
            "¡Fin de la práctica!",
            "",
            "Ahora comenzará el test real.",
            "Recuerda: mantén la concentración.",
            "",
            "Presiona ESPACIO para comenzar el test..."
        ]
        self.show_text_screen(instructions)
        
        self.show_countdown()
        
        test_data = []
        max_level = 9
        
        for level in range(2, max_level + 1):
            print(f"Iniciando nivel {level}")  # Debug
            # Nuevas posiciones para cada nivel
            positions = self.generate_random_positions(9)
            
            # Generar secuencia para este nivel
            sequence = random.sample(range(9), level)
            
            # Mostrar secuencia
            self.show_sequence(sequence, positions, "test2", level)
            
            # Capturar respuesta y tiempo
            start_time = time.time()
            user_sequence = self.get_user_sequence(level, positions, "test2", level)
            end_time = time.time()
            duration = end_time - start_time
            
            # Verificar si es correcto
            correct = user_sequence == sequence
            
            # Guardar datos
            level_data = {
                'test_type': 'Test2',
                'level': level,
                'round': 1,  # Solo una ronda por nivel en Test 2
                'sequence_length': level,
                'correct_sequence': str(sequence),
                'user_sequence': str(user_sequence),
                'correct': correct,
                'duration': round(duration, 2),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            test_data.append(level_data)
            
            # Mostrar feedback
            self.show_feedback(correct, duration)
            
            # CONTINÚA INDEPENDIENTEMENTE DE SI ES CORRECTO O INCORRECTO
            # Pequeña pausa entre niveles
            if level < max_level:
                pygame.time.wait(1000)
        
        # Calcular resultado final
        correct_levels = [data['level'] for data in test_data if data['correct']]
        corsi_span = max(correct_levels) if correct_levels else 0
        
        # Mostrar resultados finales
        self.show_final_results(test_data, corsi_span, len(correct_levels), len(test_data))
        
        # Guardar datos
        self.save_data(test_data, "test2")
        
        return test_data
    
    def show_final_results(self, test_data, corsi_span, correct_count, total_count):
        results = [
            "¡FIN DEL TEST!",
            "",
            f"Tu span de Corsi: {corsi_span} elementos",
            f"Respuestas correctas: {correct_count}/{total_count}",
            "",
            "Presiona ESPACIO para volver al menú..."
        ]
        
        self.show_text_screen(results)
    
    def save_data(self, test_data, test_name):
        filename = f"corsi_{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df = pd.DataFrame(test_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Datos guardados en: {filename}")
    
    def run_experiment(self):
        while True:
            selected_test = self.show_main_menu()
            
            if selected_test == "test1":
                self.run_test1()
            elif selected_test == "test2":
                self.run_test2()

# Ejecutar el experimento
if __name__ == "__main__":
    try:
        experiment = CorsiTaskPygame()
        experiment.run_experiment()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")