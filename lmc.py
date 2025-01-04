class IllegalInstructionError(Exception):
    """Sollevata quando viene incontrata un'istruzione non valida."""
    pass

class LMC:
    """
    Classe principale che implementa il Little Man Computer.
    Gestisce la memoria, l'accumulatore, il program counter e tutte le operazioni della macchina.
    """
    def __init__(self):
        # Inizializziamo 100 celle di memoria tutte a 0
        self.memory = [0] * 100
        # L'accumulatore è il registro principale per le operazioni
        self.accumulator = 0
        # Il program counter tiene traccia dell'istruzione corrente
        self.program_counter = 0
        # Il flag indica se l'ultima operazione aritmetica ha generato un overflow
        self.flag = False
        # Code per input e output
        self.input_queue = []
        self.output_queue = []
        # Indica se il programma è terminato
        self.halted = False

    def load_program(self, program):
        """
        Carica un programma in memoria.
        Args:
            program: Lista di numeri che rappresentano il programma
        """
        # Verifichiamo che il programma non sia troppo grande
        if len(program) > 100:
            raise ValueError("Il programma è troppo grande per la memoria")
        # Copiamo il programma nella memoria
        self.memory[:len(program)] = program
        # Resettiamo lo stato della macchina
        self.reset_state()

    def reset_state(self):
        """Resetta lo stato della CPU ai valori iniziali."""
        self.accumulator = 0
        self.program_counter = 0
        self.flag = False
        self.halted = False
        
    def set_input(self, input_values):
        """
        Imposta i valori di input per il programma.
        Args:
            input_values: Lista di numeri da usare come input
        """
        # Verifichiamo che tutti i valori siano nel range corretto
        if not all(0 <= x <= 999 for x in input_values):
            raise ValueError("I valori di input devono essere tra 0 e 999")
        self.input_queue = list(input_values)

    def execute_instruction(self):
        """
        Esegue una singola istruzione.
        Returns:
            bool: True se il programma deve continuare, False se deve terminare
        """
        if self.halted:
            return False

        # Leggiamo l'istruzione corrente dalla memoria
        instruction = self.memory[self.program_counter]
        # Estraiamo opcode (primi due numeri) e operando (ultimi due numeri)
        opcode = instruction // 100
        operand = instruction % 100

        # Verifichiamo se l'istruzione è valida
        if 400 <= instruction <= 499:
            raise IllegalInstructionError(f"Istruzione non valida: {instruction}")

        # Implementazione di tutte le istruzioni
        if opcode == 0:  # HALT - Ferma il programma
            self.halted = True
            return False
        elif opcode == 1:  # ADD - Somma il contenuto della memoria all'accumulatore
            self.accumulator += self.memory[operand]
            if self.accumulator > 999:
                self.flag = True
                self.accumulator %= 1000
            else:
                self.flag = False
        elif opcode == 2:  # SUB - Sottrae il contenuto della memoria dall'accumulatore
            self.accumulator -= self.memory[operand]
            if self.accumulator < 0:
                self.flag = True
                self.accumulator %= 1000
            else:
                self.flag = False
        elif opcode == 3:  # STA - Memorizza il valore dell'accumulatore in memoria
            self.memory[operand] = self.accumulator
        elif opcode == 5:  # LDA - Carica un valore dalla memoria nell'accumulatore
            self.accumulator = self.memory[operand]
        elif opcode == 6:  # BRA - Salto incondizionato
            self.program_counter = operand
            return True
        elif opcode == 7:  # BRZ - Salto se l'accumulatore è zero
            if self.accumulator == 0 and not self.flag:
                self.program_counter = operand
                return True
        elif opcode == 8:  # BRP - Salto se il flag è assente
            if not self.flag:
                self.program_counter = operand
                return True
        elif instruction == 901:  # INP - Legge un valore dall'input
            if not self.input_queue:
                raise RuntimeError("La coda di input è vuota")
            self.accumulator = self.input_queue.pop(0)
        elif instruction == 902:  # OUT - Scrive un valore nell'output
            self.output_queue.append(self.accumulator)

        # Incrementa il program counter (con wrap-around a 100)
        self.program_counter = (self.program_counter + 1) % 100
        return True

    def run(self):
        """
        Esegue il programma fino al termine.
        Returns:
            list: La coda di output contenente tutti i valori prodotti
        """
        while self.execute_instruction():
            pass
        return self.output_queue

class Assembler:
    """
    Classe che converte il codice assembly in codice macchina per LMC.
    """
    def __init__(self):
        # Dizionario che mappa le istruzioni assembly ai loro codici operativi
        self.instructions = {
            'ADD': 1, 'SUB': 2, 'STA': 3, 'LDA': 5,
            'BRA': 6, 'BRZ': 7, 'BRP': 8, 'INP': 901,
            'OUT': 902, 'HLT': 0
        }

    def parse_line(self, line):
        """
        Analizza una singola linea di codice assembly.
        Args:
            line: La linea di codice da analizzare
        Returns:
            tuple: (etichetta, istruzione) dove entrambi possono essere None
        """
        # Rimuove i commenti
        line = line.split('//')[0].strip()
        if not line:
            return None, None

        # Divide la linea in etichetta e istruzione
        parts = line.split()
        if len(parts) == 1:
            return None, parts[0].upper()
        if len(parts) == 2:
            return None, f"{parts[0].upper()} {parts[1]}"
        return parts[0], f"{parts[1].upper()} {parts[2]}"

    def assemble(self, source):
        """
        Converte il codice sorgente assembly in codice macchina.
        Args:
            source: Il codice sorgente assembly
        Returns:
            list: Il programma in codice macchina
        """
        # Primo passaggio: raccoglie le etichette
        labels = {}
        current_address = 0
        
        lines = source.splitlines()
        for line in lines:
            label, instruction = self.parse_line(line)
            if instruction:
                if label:
                    labels[label] = current_address
                current_address += 1

        # Secondo passaggio: genera il codice
        program = []
        for line in lines:
            label, instruction = self.parse_line(line)
            if not instruction:
                continue

            parts = instruction.split()
            op = parts[0]
            
            if op not in self.instructions:
                raise ValueError(f"Istruzione sconosciuta: {op}")

            code = self.instructions[op]
            if code >= 900:  # INP/OUT/HLT
                program.append(code)
            else:  # Istruzioni con operando
                if len(parts) != 2:
                    raise ValueError(f"Formato istruzione non valido: {instruction}")
                operand = parts[1]
                if operand in labels:
                    operand = str(labels[operand])
                program.append(code * 100 + int(operand))

        return program