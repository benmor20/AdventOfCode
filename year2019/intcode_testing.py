from intcode import Intcode


def main():
    code_str = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    code = [int(i) for i in code_str.split(',')]
    ic = Intcode(code)
    ic.run(inputs=[98], verbose=True)
    print(ic.outputs)
    # assert ic.outputs == code


if __name__ == '__main__':
    main()
