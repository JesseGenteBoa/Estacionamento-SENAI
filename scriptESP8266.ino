#define TRIG_PIN D2  // Pino de disparo (Trig)
#define ECHO_PIN D1  // Pino de recepção (Echo)
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

Servo m1;
int servoPin1 = D3;
int pos = 0;

const char* ssid = "Redmi harri";        // Nome da rede Wi-Fi
const char* password = "jedifutur3";  // Senha da rede Wi-Fi
 
ESP8266WebServer server(80); // Porta HTTP (80)


void setup() {
  m1.attach(servoPin1);
  // Inicializa a comunicação serial
  Serial.begin(115200);
 
  // Configura os pinos como saída e entrada
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("Conectando ao WiFi...");
 }
    Serial.println("Conectado ao WiFi!");
    Serial.println(WiFi.localIP()); // Mostra o IP do ESP8266
    
    // Iniciar o servidor
    server.begin();
    Serial.println("Servidor HTTP iniciado!");
}


void loop() {
  delay(200);
    // Rota para abrir a cancela
  server.on("/abrir", []() {
      Serial.println("Comando recebido: Abrir cancela");
      abrirCancela();
      server.send(200, "text/plain", "Cancela aberta");
  });
  // Rota para fechar a cancela
  server.on("/fechar", []() {
    Serial.println("Comando recebido: Fechar cancela");
    // Lógica para fechar a cancela
    float time = 0.0
    float distance = 20.0;
    while(distance > 10 || time <= 15000){
      digitalWrite(TRIG_PIN, LOW);
      delayMicroseconds(2);
      digitalWrite(TRIG_PIN, HIGH);
      delayMicroseconds(10);
      digitalWrite(TRIG_PIN, LOW);
      long duration = pulseIn(ECHO_PIN, HIGH);
      distance = (duration / 2.0) * 0.0343;
      Serial.print(distance);
      delay(500);
      time+=500;
    }
    if (distance <= 10){
      fecharCancela();
      server.send(200, "text/plain", "Cancela fechada");
    }
  });
  // Rota para fechar a cancela manualmente
  server.on("/fechar_manualmente", []() {
    Serial.println("Comando recebido: Fechar cancela manualmente");
    delay(200);
    fecharCancela();
    server.send(200, "text/plain", "Cancela fechada manualmente.");
  });
  delay(400);
  server.handleClient(); // Processa requisições HTTP
}


void abrirCancela() {
  for (pos = 0; pos <= 75; pos++) { // Vai de 0 até 75 graus
    m1.write(pos);             // Envia a posição ao servo
    delay(15);                    // Aguarda 15 ms para o servo se mover
  }
    Serial.println("Abertura da cancela...");
}


void fecharCancela() {
    for (pos = 75; pos >= 0; pos--) { // Vai de 75 até 0 graus
    m1.write(pos);             // Envia a posição ao servo
    delay(15);                    // Aguarda 15 ms para o servo se mover
  }
    Serial.println("Fechamento da cancela...");
}


