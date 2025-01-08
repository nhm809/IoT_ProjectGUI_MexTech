#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

// Định nghĩa chân kết nối cảm biến DHT11
#define DHTPIN 2       // Chân số 2 kết nối với cảm biến DHT11
#define DHTTYPE DHT11  // Chọn loại cảm biến là DHT11

// Khởi tạo đối tượng DHT
DHT dht(DHTPIN, DHTTYPE);

// Khởi tạo LCD I2C (Địa chỉ LCD là 0x27, màn hình 16x2)
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int MQ_2 = A0;
const int heater = 3;
const int dehumidifier = 5;
const int warning_lights = 6;
const int buttonPin = 7;
const int buzzer = 12;
const int air_conditioner = 13;

String command = "";
bool isGasHigh = false;
int buttonState = LOW;
int lastButtonState = LOW;  // Biến trạng thái của nút bấm lần trước

// Biến thời gian
unsigned long previousReadMillis = 0;
unsigned long previousDisplayMillis = 0;
const long readInterval = 500;    // Thời gian giữa mỗi lần đọc dữ liệu (0.5 giây)
const long displayInterval = 3000; // Thời gian giữa mỗi lần đổi màn hình hiển thị (3 giây)
bool isAlertActive = false; // Biến để theo dõi trạng thái cảnh báo
int displayState = 0;  // Biến trạng thái hiển thị trên LCD (Temp/Humidity/Gas)

// Giá trị cảm biến
float temperature = 0.0;
float humidity = 0.0;
int gas = 0;


// Hàm đọc lệnh từ Serial
void handleSerialCommand() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n'); // Đọc lệnh từ Serial

    command.trim();  // Loại bỏ khoảng trắng thừa

    if (command == "DANGER") {  
        digitalWrite(air_conditioner, HIGH);
        digitalWrite(dehumidifier, LOW);
        digitalWrite(heater, LOW); 
        if(lastButtonState == LOW)
        {
            if(buttonState == HIGH)
            {
              digitalWrite(buzzer, LOW);
              digitalWrite(warning_lights, LOW);
              lastButtonState = buttonState;
            }
            else {
              digitalWrite(buzzer, HIGH);
              digitalWrite(warning_lights, HIGH);
              lastButtonState = buttonState;
            }
        }
        else if (lastButtonState == HIGH) {
            digitalWrite(buzzer, LOW);
            digitalWrite(warning_lights, LOW);
        }
    } 
    if (command == "FAN_ON") {
    digitalWrite(air_conditioner, LOW); 
    } 
    if (command == "FAN_OFF") {
      digitalWrite(air_conditioner, HIGH); 
    } 
    if (command == "WARM_ON") {
      digitalWrite(heater, HIGH); 
    } 
    if (command == "WARM_OFF") {
      digitalWrite(heater, LOW); 
    } 
    if (command == "HIGH_HUMID") {
      digitalWrite(dehumidifier, HIGH); 
    } 
    if (command == "NOR_HUMID") {
      digitalWrite(dehumidifier, LOW); 
    }
    if (command == "NOR_GAS" || command == "NOR_TEMP")
    {
      digitalWrite(buzzer, LOW);
      digitalWrite(warning_lights, LOW);
      lastButtonState = LOW;
    }
  }
}


void setup() {
  Serial.begin(9600);  // Khởi tạo giao tiếp Serial
  dht.begin();         // Khởi tạo cảm biến DHT11

  // Khởi tạo màn hình LCD
  lcd.init();
  lcd.backlight();

  pinMode(heater, OUTPUT);
  pinMode(dehumidifier, OUTPUT);
  pinMode(warning_lights, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(air_conditioner, OUTPUT);
  digitalWrite(air_conditioner, HIGH);  // Ban đầu tắt relay
}


void loop() {
  unsigned long currentMillis = millis();

  buttonState = digitalRead(buttonPin);

  // Đọc cảm biến mỗi giây
  if (currentMillis - previousReadMillis >= readInterval) {
    previousReadMillis = currentMillis;

    // Đọc dữ liệu từ DHT11
    humidity = dht.readHumidity();
    temperature = dht.readTemperature();
    gas = analogRead(MQ_2);
    // Kiểm tra lỗi cảm biến
    if (isnan(humidity) || isnan(temperature)) {
      Serial.println("Failed to read from DHT sensor!");
      humidity = 0.0;
      temperature = 0.0;
    }
    if(isnan(gas)){
      Serial.println("Failed to read from MQ-2 sensor!");
      gas = 0;
    }

    // Đọc giá trị gas
    // gas = 400;

    // Debug dữ liệu ra Serial
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.print("%\n");
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println("°C");
    Serial.print("Gas: ");
    Serial.println(gas);


    if (gas > 300) isAlertActive = true;
    else isAlertActive = false;


    // Xử lý lệnh từ Serial
    handleSerialCommand();
  }


  // Cập nhật hiển thị trên LCD
  if (currentMillis - previousDisplayMillis >= displayInterval) {
    previousDisplayMillis = currentMillis;

    lcd.clear();
    if (displayState == 0) {
      lcd.setCursor(0, 0);
      lcd.print("Temp: ");
      lcd.print(temperature, 1);
      lcd.print(" C");

      lcd.setCursor(0, 1);
      lcd.print("Humidity: ");
      lcd.print(humidity, 1);
      lcd.print(" %");
      displayState = 1;  // Chuyển sang hiển thị Gas
    } else {
      lcd.setCursor(0, 0);
      lcd.print("Gas: ");
      lcd.print(gas);
      lcd.print(" PPM");

      lcd.setCursor(0, 1);
      lcd.print(isAlertActive ? "Gas ALERT!" : "Gas Normal");
      displayState = 0;  // Quay lại hiển thị Temp và Humidity
    }
  }
}

