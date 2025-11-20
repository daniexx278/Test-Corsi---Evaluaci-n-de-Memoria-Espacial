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
        pygame.display.set_caption("Test de Memoria De Trabajo Corsi")
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
        
        # Colores para Test 2 (colores base de los círculos)
        self.test2_base_colors = [
            self.RED, self.YELLOW, self.GREEN, self.PURPLE, 
            self.ORANGE, self.CYAN, self.PINK, self.BROWN, self.BLUE
        ]
        
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 24)
        
        self.data = []
        self.current_test = None
        
    def show_main_menu(self):
        while True:
            self.screen.fill(self.BLACK)
            
            # Título
            title = self.title_font.render("TEST DE MEMORIA DE TRABAJO CORSI", True, self.WHITE)
            self.screen.blit(title, (400 - title.get_width() // 2, 100))
            
            # Botones más grandes para acomodar texto
            test1_rect = pygame.Rect(200, 200, 400, 60)
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
        """Genera posiciones aleatorias evitando solapamientos"""
        positions = []
        for _ in range(count):
            valid_position = False
            attempts = 0
            while not valid_position and attempts < 50:
                x = random.randint(70, 730)
                y = random.randint(100, 500)
                
                # Verificar distancia mínima con otros círculos
                too_close = False
                for existing_pos in positions:
                    distance = ((x - existing_pos[0])**2 + (y - existing_pos[1])**2)**0.5
                    if distance < 80:
                        too_close = True
                        break
                
                if not too_close:
                    positions.append((x, y))
                    valid_position = True
                
                attempts += 1
            
            # Si no encontró posición válida, usar posición por defecto
            if not valid_position:
                default_positions = [
                    (100, 150), (250, 120), (400, 150), (550, 120), (700, 150),
                    (150, 300), (300, 330), (450, 300), (600, 330)
                ]
                if len(positions) < len(default_positions):
                    positions.append(default_positions[len(positions)])
                else:
                    # Último recurso: posición aleatoria simple
                    positions.append((random.randint(70, 730), random.randint(100, 500)))
        
        return positions
    
    def show_instructions(self, test_type):
        if test_type == "test1":
            instructions = [
                "TEST 1 - SECUENCIA ÚNICA",
                "",
                "Se presentarán 9 círculos de color azul en la pantalla.",
                "Esos círculos se iluminarán de color amarillo en una",
                "secuencia específica, que irá incrementando de dificultad.",
                "Tu trabajo es presionar los círculos en el mismo orden",
                "en que se iluminaron.",
                "",
                "Presiona ESPACIO para la sesión de práctica..."
            ]
        else:
            instructions = [
                "TEST 2 - SECUENCIA CON COLORES",
                "",
                "Se presentarán 9 círculos de diferentes colores en la pantalla.",
                "Esos círculos se iluminarán de color blanco en una",
                "secuencia específica, que irá incrementando de dificultad.",
                "Tu trabajo es presionar los círculos en el mismo orden",
                "en que se iluminaron.",
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
        """Muestra la secuencia de círculos iluminándose - VERSIÓN CORREGIDA"""
        # Mostrar todos los círculos primero
        self.draw_circles(positions, test_type, current_level)
        pygame.display.flip()
        pygame.time.wait(800)
        
        # Mostrar la secuencia con manejo de eventos para evitar congelación
        for i, circle_index in enumerate(sequence):
            # Dibujar el círculo resaltado
            self.draw_circles(positions, test_type, current_level, highlight_index=circle_index, sequence_index=i)
            pygame.display.flip()
            
            # Espera con manejo de eventos para evitar congelación
            start_time = time.time()
            while time.time() - start_time < 0.8:  # 800ms
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.time.wait(10)
            
            # Volver a normal
            self.draw_circles(positions, test_type, current_level)
            pygame.display.flip()
            
            # Pausa entre iluminaciones
            start_time = time.time()
            while time.time() - start_time < 0.4:  # 400ms
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.time.wait(10)
    
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
                # Test 2: MODIFICACIÓN - círculos con colores diferentes de inicio
                if highlight_index == i:
                    # Cuando se ilumina, usa color BLANCO
                    color = self.WHITE
                else:
                    # Cada círculo tiene un color diferente de la lista
                    color = self.test2_base_colors[i % len(self.test2_base_colors)]
            
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
                        if distance <= 30:
                            clicked_index = i
                            break
                    if clicked_index is not None:
                        break
            
            clock.tick(60)
        
        # Si hubo timeout, seleccionar aleatoriamente para evitar bloqueo
        if clicked_index is None:
            available_positions = [i for i in range(len(positions))]
            if available_positions:
                clicked_index = random.choice(available_positions)
        
        return clicked_index
    
    def show_feedback(self, correct, duration, practice=False):
        # MODIFICACIÓN: No mostrar el tiempo en pantalla, solo guardarlo en Excel
        if practice:
            feedback_text = "✓ PRÁCTICA CORRECTA" if correct else "✗ PRÁCTICA INCORRECTA"
        else:
            feedback_text = "✓ CORRECTO" if correct else "✗ INCORRECTO"
        
        color = self.GREEN if correct else self.RED
        
        self.screen.fill(self.BLACK)
        text1 = self.font.render(feedback_text, True, color)
        
        self.screen.blit(text1, (400 - text1.get_width() // 2, 250))
        
        if practice:
            text3 = self.small_font.render("Presiona ESPACIO para continuar con el test...", True, self.WHITE)
            self.screen.blit(text3, (400 - text3.get_width() // 2, 300))
        
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
        """TEST 1 - Con regla de 2 fallos seguidos por nivel"""
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
        consecutive_failures = 0  # Contador de fallos seguidos
        
        for level in range(2, max_level + 1):
            print(f"TEST 1 - Nivel {level}")
            # Nuevas posiciones para cada nivel
            positions = self.generate_random_positions(9)
            
            # Reiniciar contador de fallos seguidos por nivel
            level_consecutive_failures = 0
            
            # SOLO 2 RONDAS POR NIVEL
            for round_num in range(1, 3):
                print(f"  Ronda {round_num}")
                
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
                
                # Mostrar feedback (sin tiempo en pantalla)
                self.show_feedback(correct, duration)
                
                # MODIFICACIÓN: Control de fallos seguidos
                if not correct:
                    level_consecutive_failures += 1
                    consecutive_failures += 1
                else:
                    level_consecutive_failures = 0
                    consecutive_failures = 0
                
                # Si hay 2 fallos seguidos en este nivel, terminar el test
                if level_consecutive_failures >= 2:
                    print("2 fallos seguidos en el nivel - terminando test")
                    # Mostrar mensaje de fin por fallos
                    self.show_early_termination(level)
                    # Calcular resultados hasta donde llegó
                    correct_count = sum(1 for data in test_data if data['correct'])
                    total_rounds = len(test_data)
                    corsi_span = max([data['level'] for data in test_data if data['correct']] + [0])
                    
                    # Mostrar resultados finales
                    self.show_final_results(test_data, corsi_span, correct_count, total_rounds, early_termination=True)
                    
                    # Guardar datos
                    self.save_data(test_data, "test1")
                    return test_data
                
                # Pequeña pausa entre rondas
                if level < max_level or round_num < 2:
                    pygame.time.wait(1000)
            
            # Pausa entre niveles
            if level < max_level:
                pygame.time.wait(500)
        
        # Calcular resultado final (si completó todos los niveles)
        correct_count = sum(1 for data in test_data if data['correct'])
        total_rounds = len(test_data)
        corsi_span = max([data['level'] for data in test_data if data['correct']] + [0])
        
        # Mostrar resultados finales
        self.show_final_results(test_data, corsi_span, correct_count, total_rounds)
        
        # Guardar datos
        self.save_data(test_data, "test1")
        
        return test_data
    
    def run_test2(self):
        """TEST 2 - Con regla de 2 niveles fallados seguidos"""
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
        consecutive_failed_levels = 0  # NUEVO: Contador de niveles fallados seguidos
        
        for level in range(2, max_level + 1):
            print(f"TEST 2 - Nivel {level}")
            # MODIFICACIÓN: Nuevas posiciones aleatorias para cada nivel (patrón desordenado)
            positions = self.generate_random_positions(9)
            
            # SOLO 1 RONDA POR NIVEL
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
                'round': 1,
                'sequence_length': level,
                'correct_sequence': str(sequence),
                'user_sequence': str(user_sequence),
                'correct': correct,
                'duration': round(duration, 2),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            test_data.append(level_data)
            
            # Mostrar feedback (sin tiempo en pantalla)
            self.show_feedback(correct, duration)
            
            # NUEVA MODIFICACIÓN: Control de niveles fallados seguidos
            if not correct:
                consecutive_failed_levels += 1
                print(f"Nivel {level} fallado. Fallos seguidos: {consecutive_failed_levels}")
            else:
                consecutive_failed_levels = 0  # Reiniciar contador si acierta
            
            # Si hay 2 niveles fallados seguidos, terminar el test
            if consecutive_failed_levels >= 2:
                print("2 niveles fallados seguidos - terminando test")
                # Mostrar mensaje de fin por fallos
                self.show_early_termination_test2(level)
                # Calcular resultados hasta donde llegó
                correct_levels = [data['level'] for data in test_data if data['correct']]
                corsi_span = max(correct_levels) if correct_levels else 0
                
                # Mostrar resultados finales
                self.show_final_results(test_data, corsi_span, len(correct_levels), len(test_data), early_termination=True)
                
                # Guardar datos
                self.save_data(test_data, "test2")
                return test_data
            
            # Pequeña pausa entre niveles (solo si no es el último y no terminó por fallos)
            if level < max_level:
                pygame.time.wait(1000)
        
        # Calcular resultado final (si completó todos los niveles)
        correct_levels = [data['level'] for data in test_data if data['correct']]
        corsi_span = max(correct_levels) if correct_levels else 0
        
        # Mostrar resultados finales
        self.show_final_results(test_data, corsi_span, len(correct_levels), len(test_data))
        
        # Guardar datos
        self.save_data(test_data, "test2")
        
        return test_data
    
    def show_early_termination(self, level):
        """Muestra mensaje cuando el test termina por 2 fallos seguidos (Test 1)"""
        message = [
            "TEST TERMINADO",
            "",
            f"Has fallado 2 veces seguidas en el nivel {level}.",
            "El test ha finalizado.",
            "",
            "Presiona ESPACIO para ver los resultados..."
        ]
        self.show_text_screen(message)
    
    def show_early_termination_test2(self, level):
        """Muestra mensaje cuando el test termina por 2 niveles fallados seguidos (Test 2)"""
        message = [
            "TEST TERMINADO",
            "",
            f"Has fallado 2 niveles seguidos (niveles {level-1} y {level}).",
            "El test ha finalizado.",
            "",
            "Presiona ESPACIO para ver los resultados..."
        ]
        self.show_text_screen(message)
    
    def show_final_results(self, test_data, corsi_span, correct_count, total_count, early_termination=False):
        if early_termination:
            results = [
                "¡FIN DEL TEST!",
                "",
                "El test terminó antes por fallos consecutivos.",
                f"Tu span de Corsi: {corsi_span} elementos",
                f"Respuestas correctas: {correct_count}/{total_count}",
                "",
                "Presiona ESPACIO para volver al menú..."
            ]
        else:
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