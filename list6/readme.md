Program został napiany w języku Python3.

Uruchamianie:

`python3 task1.py <input_file> <--encode/--decode> [k - liczba bitów kwantyzatora, domyślnie 2]`

Program podczas kodowania tworzy następujące pliki:
- output_high.tga - obrazek po przepuszczeniu przez filtry górnoprzepustowe
- output_high_encoded.tga - obrazek po przepuszczeniu przez filtry górnoprzepustowe i po kwantyzacji
- output_low.tga - obrazek po przepuszczeniu przez filtry dolnoprzepustowe
- output_low_encoded - obrazek po przepuszczeniu przez filtry dolnoprzepustowe i zakodowany różnicowo

Dekoder dekoduje tylko `output_low_encoded` tworząc plik `output_low_decoded.tga`, gdyż obrazek przepuszczony przez filtry górnoprzepustowe i kwantyzator nie wymaga dekodowania.
