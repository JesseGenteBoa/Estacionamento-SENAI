#define ledAzul D3 // Leds para simular o acionamento da cancela.
#define ledAmarelo D4
#define TRIG_PIN D2  // Pino de disparo (Trig)
#define ECHO_PIN D1  // Pino de recepção (Echo)
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Ultrasonic.h>


const char* ssid = "Redmi harri";        // Nome da rede Wi-Fi
const char* password = "jedifutur3";  // Senha da rede Wi-Fi
ESP8266WebServer server(80); // Porta HTTP (80)
Ultrasonic us(TRIG_PIN, ECHO_PIN);


void setup() {
  pinMode(ledAzul, OUTPUT);
  pinMode(ledAmarelo, OUTPUT);
  Serial.begin(115200);
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
  long distance = us.Ranging(CM); // Medição de distância diretamente da biblioteca
  
  server.on("/abrir", []() {
    Serial.println("Comando recebido: Abrir cancela");
    abrirCancela();
    server.send(200, "text/plain", "Cancela aberta");
  });
  
  server.on("/fechar", []() {
    Serial.println("Comando recebido: Fechar cancela");
    unsigned long time = 0;
    long distance = us.Ranging(CM); // Medição inicial da distância
    while (distance > 10 || time <= 15000) {
      distance = us.Ranging(CM); // Atualiza a distância a cada iteração
      Serial.print("Distância dentro do loop: ");
      Serial.println(distance);
      delay(500);
      time += 100;
    }
    if (distance <= 10) {
      fecharCancela();
      server.send(200, "text/plain", "Cancela fechada");
    } else {
      server.send(200, "text/plain", "Distância ainda maior que 10cm, cancela não fechada.");
    }
  });

  // Rota para fechar a cancela manualmente
  server.on("/fechar_manualmente", []() {
    Serial.println("Comando recebido: Fechar cancela manualmente");
    fecharCancela();
    server.send(200, "text/plain", "Cancela fechada manualmente.");
  });

  delay(400); // Tempo para processar a requisição
  server.handleClient(); // Processa requisições HTTP
}


void abrirCancela() {
  digitalWrite(ledAzul, HIGH);
  delay(500);
  Serial.println("Abertura da cancela...");
}


void fecharCancela() {
  digitalWrite(ledAzul, LOW);
  digitalWrite(ledAmarelo, HIGH);
  delay(5000);
  digitalWrite(ledAmarelo, LOW);
  Serial.println("Fechamento da cancela...");
}


