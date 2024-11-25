import cv2
import easyocr
import numpy as np
import veiculo
import conector


conexao = conector.Conector()


veiculos = veiculo.Veiculo()


reader = easyocr.Reader(['en'], quantize=True)


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def lerImagem(binary, detected_texts, frame):
    result = reader.readtext(binary, batch_size=10)
   
    for detection in result:
        coordinates, text, confidence = detection


        detected_texts.append(text)
       
        operarPortao(detected_texts, confidence)


        (top_left, top_right, bottom_right, bottom_left) = coordinates
        cv2.polylines(frame, [np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(frame, text, (int(top_left[0]), int(top_left[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


def operarPortao(detected_texts, confidence):
    if detected_texts:
        if confidence > 0.5:
            print("Textos detectados:", detected_texts, "Precisão:", confidence)
        if len(detected_texts) > 1:
            detected_texts = ''.join(detected_texts).upper()
        else:
            detected_texts = detected_texts[0]


        if veiculos.verificar_cadastrados(detected_texts):
            conexao.abrir_cancela()
            conexao.fechar_cancela()


def ligarCam():
    frame_counter = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if ret:
            frame_counter += 1
           
            stretch_near = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            gray = cv2.cvtColor(stretch_near, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            th3 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            _, binary = cv2.threshold(th3, 0, 255 ,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


       
            if frame_counter % 1 == 0:
                detected_texts = []
                lerImagem(binary, detected_texts, frame)
           
            cv2.imshow('Leitor de Placas', frame)
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


ligarCam()




cap.release()
cv2.destroyAllWindows()



