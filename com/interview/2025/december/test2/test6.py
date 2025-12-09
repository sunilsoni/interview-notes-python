from json import dumps, loads
import sys
from typing import List


def decrypt(clear_msg_ab: str, ciphered_msg_ab: str, clear_msg_bc: str, ciphered_msg_bc: str,
            ciphered_msg_cba: str) -> str:
    # Build Alice-Bob decrypt mapping (cipher -> clear)
    ab_decrypt = {}
    for i in range(len(clear_msg_ab)):
        if clear_msg_ab[i] != ' ':
            ab_decrypt[ciphered_msg_ab[i]] = clear_msg_ab[i]

    # Build Bob-Carol decrypt mapping (cipher -> clear)
    bc_decrypt = {}
    for i in range(len(clear_msg_bc)):
        if clear_msg_bc[i] != ' ':
            bc_decrypt[ciphered_msg_bc[i]] = clear_msg_bc[i]

    # Decrypt: first reverse BC mapping, then reverse AB mapping
    result = []
    for ch in ciphered_msg_cba:
        if ch == ' ':
            result.append(' ')
        else:
            intermediate = bc_decrypt.get(ch, ch)
            final = ab_decrypt.get(intermediate, intermediate)
            result.append(final)

    return ''.join(result)


def main():
    test_cases = [
        {
            "clear_msg_ab": "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
            "ciphered_msg_ab": "FWK CYTIN AROXL BOD MYHSV OZKR FWK PQUG EOJ",
            "clear_msg_bc": "PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS",
            "ciphered_msg_bc": "YCAR HX MKZ OTJU STNW BKIWL FTDEKV QEPG",
            "ciphered_msg_cba": "SOJN TYDNN JN CKVJFQ DFW SOR SRDTORV JN WXUC",
            "expected": "THIS CLASS IS BORING AND THE TEACHER IS DUMB"
        },
        {
            "clear_msg_ab": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ciphered_msg_ab": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "clear_msg_bc": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ciphered_msg_bc": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ciphered_msg_cba": "HELLO WORLD",
            "expected": "HELLO WORLD"
        },
        {
            "clear_msg_ab": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ciphered_msg_ab": "ZYXWVUTSRQPONMLKJIHGFEDCBA",
            "clear_msg_bc": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ciphered_msg_bc": "ZYXWVUTSRQPONMLKJIHGFEDCBA",
            "ciphered_msg_cba": "HELLO",
            "expected": "HELLO"
        },
        {
            "clear_msg_ab": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ciphered_msg_ab": "BCDEFGHIJKLMNOPQRSTUVWXYZA",
            "clear_msg_bc": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ciphered_msg_bc": "CDEFGHIJKLMNOPQRSTUVWXYZAB",
            "ciphered_msg_cba": "DEF",
            "expected": "ABC"
        },
        {
            "clear_msg_ab": "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
            "ciphered_msg_ab": "FWK CYTIN AROXL BOD MYHSV OZKR FWK PQUG EOJ",
            "clear_msg_bc": "PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS",
            "ciphered_msg_bc": "YCAR HX MKZ OTJU STNW BKIWL FTDEKV QEPG",
            "ciphered_msg_cba": "",
            "expected": ""
        },
        {
            "clear_msg_ab": "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
            "ciphered_msg_ab": "FWK CYTIN AROXL BOD MYHSV OZKR FWK PQUG EOJ",
            "clear_msg_bc": "PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS",
            "ciphered_msg_bc": "YCAR HX MKZ OTJU STNW BKIWL FTDEKV QEPG",
            "ciphered_msg_cba": "   ",
            "expected": "   "
        },
    ]

    all_passed = True
    for idx, tc in enumerate(test_cases):
        result = decrypt(
            tc["clear_msg_ab"],
            tc["ciphered_msg_ab"],
            tc["clear_msg_bc"],
            tc["ciphered_msg_bc"],
            tc["ciphered_msg_cba"]
        )
        status = "PASS" if result == tc["expected"] else "FAIL"
        print(f"Test {idx + 1}: {status}")
        if status == "FAIL":
            all_passed = False
            print(f"  Expected: {tc['expected']}")
            print(f"  Got: {result}")

    print()
    if all_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")


if __name__ == "__main__":
    main()