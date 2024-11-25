import cv2
import easyocr
import numpy as np
import veiculo
import conector

conexao = conector.Conector()

veiculos = veiculo.Veiculo()

reader = easyocr.Reader(['pt', 'en']) 

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)

    result = reader.readtext(binary)

    detected_texts = [] 

    for detection in result:
        coordinates, text, confidence = detection
        detected_texts.append(text) 

        (top_left, top_right, bottom_right, bottom_left) = coordinates
        cv2.polylines(frame, [np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(frame, text, (int(top_left[0]), int(top_left[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    if detected_texts:
        print("Textos detectados:", detected_texts)
        if len(detected_texts) > 1:
            detected_texts = ''.join(detected_texts).upper()
        else:
            detected_texts = detected_texts[0]

        if veiculos.verificar_cadastrados(detected_texts):
            conexao.abrir_cancela()
            conexao.fechar_cancela()

    cv2.imshow('Texto Detectado', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
