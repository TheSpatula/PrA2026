#sensors - work by raycasting

the breeding feels week, the gens dont get much better.
--> when one gets far, it can be that the next gen is dummer and wont reach as far as the previous did

implement :

    Elitism
    Random Immigrants
    Start-Variation

    make the fitness more inteligant
        this code rewards also for how far the car got tho the next checkpoint (only minor improvements)

        def generate_breeding_pool(elements, checkpoints):
            breeding_pool = []
            for element in elements:
                # Basis-Fitness durch geschaffte Checkpoints und Laps
                base_fitness = (element.car.lap_count * 25) + element.car.checkpoint_reached
                
                # ZUSATZ: Finde heraus, welcher Checkpoint als nächstes dran ist
                next_cp_index = element.car.checkpoint_reached % len(checkpoints)
                target_checkpoint = checkpoints[next_cp_index]
                
                # Berechne die Distanz vom Auto zum nächsten Checkpoint (Mittelpunkt des Rects)
                cp_center_x = target_checkpoint.rect.centerx
                cp_center_y = target_checkpoint.rect.centery
                distance = math.hypot(element.car.x - cp_center_x, element.car.y - cp_center_y)
                
                # Je kleiner die Distanz, desto höher der Bonus (wir skalieren das herunter, z.B. / 1000)
                # Wenn es nah am Checkpoint war, kriegt es einen kleinen Dezimal-Bonus (z.B. +0.5 Punkte)
                distance_bonus = max(0, 1.0 - (distance / 1000.0))
                
                total_fitness = base_fitness + distance_bonus
                
                # Füge das Auto entsprechend seiner Gesamt-Fitness in den Pool ein
                for _ in range(math.floor(max(0, total_fitness * 10))): # *10 damit die Nachkommastellen greifen
                    breeding_pool.append(element)
                    
            if not breeding_pool:
                print("Niemand hat Fortschritt erzielt! Starte neue Zufalls-Population...")
                breeding_pool = generate_population(N, HIDDEN_LAYER_NEURONS)
                
            return breeding_pool