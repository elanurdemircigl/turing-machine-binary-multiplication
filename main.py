class FormalTuringMachine:
    BLANK = '_'
    
    def __init__(self, a_str, b_str):
        self.a_str = a_str
        self.b_str = b_str
        
        tape_input = f"{a_str}*{b_str}="
        self.tape = list(self.BLANK + tape_input + self.BLANK)
        self.head = 1
        self.state = 'q0'
        self.halted = False
        self.step = 0
        
        self.transitions = self._build_transitions()

    def _build_transitions(self):
        t = {}
        
        t[('q0', '0')] = ('q0', '0', 'R', "Sağa doğru ilerle, '=' işaretini ara")
        t[('q0', '1')] = ('q0', '1', 'R', "Sağa doğru ilerle, '=' işaretini ara")
        t[('q0', '*')] = ('q0', '*', 'R', "Sağa doğru ilerle, '=' işaretini ara")
        t[('q0', '=')] = ('q1', '=', 'L', "'=' bulundu, çarpana (sola) dön")

        t[('q1', '0')] = ('q_shift_start', 'x', 'L', "0 okundu, 'x' yapıldı. (Kaydırma başlatılıyor)")
        t[('q1', '1')] = ('q_shift_start', 'y', 'L', "1 okundu, 'y' yapıldı. (Kaydırma başlatılıyor)")
        t[('q1', 'x')] = ('q1', 'x', 'L', "İşlenmiş bit (x) atla, sola git")
        t[('q1', 'y')] = ('q1', 'y', 'L', "İşlenmiş bit (y) atla, sola git")
        t[('q1', '*')] = ('q_clean', '*', 'R', "Çarpanın tüm bitleri bitti. Bant temizleniyor...")

        symbols = ['0', '1', 'x', 'y', '=']
        for sym in symbols:
            t[('q_shift_start', sym)] = ('q_shift_start', sym, 'L', "Sola git, '*' ara")
        
        t[('q_shift_start', '*')] = ('q_carry_*', '0', 'R', "KAYDIRMA: * yerine 0 yazıldı, * sağa kaydırılıyor")

        all_symbols = ['0', '1', 'x', 'y', '=', self.BLANK]
        for carry in ['*', '0', '1', 'x', 'y', '=']:
            for read_sym in all_symbols:
                if read_sym == self.BLANK:
                    t[(f'q_carry_{carry}', self.BLANK)] = ('q1', carry, 'L', f"Boşluğa {carry} yaz, sıradaki çarpan bitine dön")
                else:
                    t[(f'q_carry_{carry}', read_sym)] = (f'q_carry_{read_sym}', carry, 'R', f"{read_sym} okundu, yerine {carry} yazıldı")

        t[('q_clean', 'x')] = ('q_clean', '0', 'R', "Banttaki geçici x işaretleri 0 yapılıyor")
        t[('q_clean', 'y')] = ('q_clean', '1', 'R', "Banttaki geçici y işaretleri 1 yapılıyor")
        t[('q_clean', '0')] = ('q_clean', '0', 'R', "Temizlik: Sağa hareket")
        t[('q_clean', '1')] = ('q_clean', '1', 'R', "Temizlik: Sağa hareket")
        t[('q_clean', '=')] = ('q_clean', '=', 'R', "Temizlik: Sağa hareket")
        t[('q_clean', self.BLANK)] = ('q_accept', self.BLANK, 'N', "Sonuç yazıldı")

        return t

    def read(self):
        return self.tape[self.head]

    def write(self, symbol):
        self.tape[self.head] = symbol

    def move(self, direction):
        if direction == 'R':
            self.head += 1
            if self.head >= len(self.tape):
                self.tape.append(self.BLANK)
        elif direction == 'L':
            self.head -= 1
            if self.head < 0:
                self.tape.insert(0, self.BLANK)
                self.head = 0 

    def get_tape_string_with_head(self):
        tape_copy = self.tape.copy()
        tape_copy[self.head] = f"[{tape_copy[self.head]}]"
        return ''.join(tape_copy)

    def print_step(self, current_symbol, action):
        next_state, write_symbol, direction, description = action

        print("------------------------------")
        print(f"ADIM: {self.step}")
        print(f"Durum: {self.state}")
        print(f"Okunan Sembol: {current_symbol}")
        print(f"Kafa Hareketi: {self.head}")
        print(f"Bant İçeriği: {self.get_tape_string_with_head()}")

    def run(self, max_steps=1500):
        print("Bant İçeriği:", self.get_tape_string_with_head())

        while not self.halted:
            self.step += 1
            current_symbol = self.read()
            key = (self.state, current_symbol)

            if key not in self.transitions:
                print("\n------------------------------")
                print(f"HATA: Tanımsız geçiş! Durum={self.state}, Okunan={current_symbol}")
                break

            action = self.transitions[key]
            self.print_step(current_symbol, action)
            next_state, write_symbol, direction, description = action

            self.write(write_symbol)
            if direction != 'N':
                self.move(direction)
            self.state = next_state

            if self.state == 'q_accept':
                self.halted = True
                print("\n------------------------------")
                print(f"ADIM: {self.step + 1}")
                print(f"Durum: {self.state}")
                print(f"Okunan Sembol: {self.read()}")
                print(f"Kafa Hareketi: {self.head}")
                print(f"Bant İçeriği: {self.get_tape_string_with_head()}")
                print("------------------------------")
                break

            if self.step > max_steps:
                print("\nMaksimum adım sınırı aşıldı!")
                print("------------------------------")
                break

        self.print_final_results()

    def print_final_results(self):
        val_a = int(self.a_str, 2)
        val_b = int(self.b_str, 2)
        decimal_result = val_a * val_b
        
        if decimal_result == 0:
            binary_result = "0"
        else:
            binary_result = bin(decimal_result)[2:] 

        print("İşlem Sonucu:")
        print(f"Binary Sonuç: {binary_result}")
        print(f"Decimal Karşılığı: {decimal_result}")


if __name__ == '__main__':
    a = input("Birinci binary sayı: ").strip()
    b = input("İkinci binary sayı: ").strip()

    tm = FormalTuringMachine(a, b)
    tm.run()
