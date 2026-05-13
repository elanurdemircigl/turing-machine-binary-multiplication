class TuringMachine:
    def __init__(self, multiplicand, multiplier):
        self.multiplicand = multiplicand
        self.multiplier = multiplier

        self.tape = list(f"{multiplicand}*{multiplier}=")
        self.head = 0
        self.state = "q0"

        self.result = 0
        self.step = 1

    def print_step(self, read_symbol, write_symbol):
        tape_str = ""
        for i, symbol in enumerate(self.tape):
            if i == self.head:
                tape_str += f"[{symbol}]"
            else:
                tape_str += f"{symbol}"

        print("~~" * 10)
        print(f"ADIM: {self.step}")
        print(f"Durum: {self.state}")
        print(f"Okunan Sembol: {read_symbol}")
        print(f"Kafa Hareketi: {self.head}")
        print(f"Yazılan Sembol: {write_symbol}")
        print(f"Bant İçeriği: {tape_str}")

        self.step += 1
    def validate_binary(self, value):
        for ch in value:
            if ch not in ['0', '1']:
                return False
        return True

    def run(self):

        if not self.validate_binary(self.multiplicand):
            self.state = "q_reject"
            print("0 ve 1lerden oluşan bir sayı girmelisiniz")
            return

        if not self.validate_binary(self.multiplier):
            self.state = "q_reject"
            print("0 ve 1lerden oluşan bir sayı girmelisiniz")
            return

        #q0 * karakterini bul
        while self.head < len(self.tape):
            current = self.tape[self.head]

            if current == '*':
                self.state = "q1"
                self.print_step(current, '*')
                self.head += 1
                break

            self.print_step(current, current)
            self.head += 1

        multiplicand_decimal = int(self.multiplicand, 2)

        reversed_multiplier = self.multiplier[::-1]

        shift = 0

        for bit in reversed_multiplier:

            if bit == '1':
                shifted_value = multiplicand_decimal << shift
                self.result += shifted_value
                self.state = "q3"
                self.print_step(bit, bit)
            else:
                self.state = "q2"
                self.print_step(bit, bit)
            shift += 1
            self.head += 1
        binary_result = bin(self.result)[2:]

        #sonucu banda yaz
        for ch in binary_result:
            self.tape.append(ch)
        self.state = "q_accept"
        self.print_step('=', binary_result)

        print("\nişlem sonucu:")
        print(f"Binary Sonuç: {binary_result}")
        print(f"Decimal Sonuç: {self.result}")
multiplicand = input("Birinci binary sayıyı giriniz: ")
multiplier = input("İkinci binary sayıyı giriniz: ")

machine = TuringMachine(multiplicand, multiplier)
machine.run()
