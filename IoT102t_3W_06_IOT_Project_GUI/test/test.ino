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
const int gas_input = A0;
const int led2 = 3;
const int led3 = 5;
const int led4 = 6;
const int buttonPin = 7;
const int buzzer = 12;
const int relayPin = 13;

int buttonState = 0;

void setup() {
  Serial.begin(9600);  // Khởi tạo giao tiếp Serial
  dht.begin();         // Khởi tạo cảm biến DHT11

  // Khởi tạo màn hình LCD
  lcd.init();
  lcd.backlight();
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(relayPin, OUTPUT);     // Đặt relayPin là OUTPUT
  digitalWrite(relayPin, HIGH);  // Ban đầu tắt relay
}

void loop() {
  // Đọc giá trị nhiệt độ và độ ẩm từ cảm biến
  float h = dht.readHumidity();     // Đọc độ ẩm
  float t = dht.readTemperature();  // Đọc nhiệt độ (đơn vị Celsius)
  int gas = analogRead(gas_input);
  buttonState = digitalRead(buttonPin);

  // Kiểm tra xem việc đọc có thành công không
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    lcd.setCursor(0, 0);
    lcd.print("Sensor Error   ");  // In lỗi lên màn hình LCD
    delay(2000);
    return;
  }

  // In giá trị nhiệt độ và độ ẩm ra Serial Monitor
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print("%\n");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.println("°C");
  Serial.print("Gas: ");
  Serial.println(gas);

  // Hiển thị nhiệt độ và độ ẩm lên LCD
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(t, 1);      // Hiển thị nhiệt độ (1 số thập phân)
  lcd.print(" C    ");  // Thêm khoảng trắng để xóa ký tự cũ

  lcd.setCursor(0, 1);
  lcd.print("Humidity: ");
  lcd.print(h, 1);      // Hiển thị độ ẩm (1 số thập phân)
  lcd.print(" %    ");  // Thêm khoảng trắng để xóa ký tự cũ

  //Kiểm tra nhiệt độ, độ ẩm và điều chỉnh
  if (t > 25) {
    digitalWrite(relayPin, LOW);  // LOW =
    // Serial.println("High Temperature.");
  }
  if (t >= 15 && t <= 25) {
    digitalWrite(relayPin, HIGH);  //HIGH = tat
    digitalWrite(led2, LOW);
    // Serial.println("Suitable Temperature.");
  }
  if (t < 15) {
    digitalWrite(relayPin, HIGH);
    digitalWrite(led2, HIGH);
    // Serial.println("Low Temperature.");
  }
  if (t > 50) {
    digitalWrite(buzzer, HIGH);
    digitalWrite(led4, HIGH);
    digitalWrite(relayPin, HIGH);
  }

  if (h > 60) {
    digitalWrite(led3, HIGH);
    // Serial.println("High Humidity.");
  } else {
    digitalWrite(led3, LOW);
    // Serial.println("Suitable Humidity.");
  }
  if (gas > 300) {
    digitalWrite(buzzer, HIGH);
    digitalWrite(led4, HIGH);
    if (buttonState == HIGH)  {
      int gas1 = gas;
      do {
        gas1 = analogRead(gas_input);
        digitalWrite(buzzer, LOW);
        digitalWrite(led4, LOW);
      } while (gas1 > 300);
    }
  } else {
    digitalWrite(buzzer, LOW);
    digitalWrite(led4, LOW);
  }

  delay(1000);  // Chờ 1 giây trước lần đọc tiếp theo
}