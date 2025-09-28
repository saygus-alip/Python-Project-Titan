# นำเข้าไลบรารีที่จำเป็น
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
import numpy as np

# --- ขั้นตอนที่ 1: การเตรียมข้อมูล (Data Preparation) ---

# สร้างข้อมูลตัวอย่างขึ้นมา (แทนข้อมูลจริงของคุณ)
# ในที่นี้เราสร้างข้อมูลที่มี 1,000 ตัวอย่าง แต่ละตัวอย่างมี 20 ฟีเจอร์
X_data = np.random.rand(1000, 20).astype(np.float32)

# สร้างป้ายกำกับ (labels) ตัวอย่าง
# ในที่นี้เราสร้างป้ายกำกับสำหรับ 10 คลาส
y_labels = np.random.randint(0, 10, size=1000)

# แบ่งข้อมูลออกเป็น 2 ส่วน: สำหรับฝึกสอน (training) และสำหรับทดสอบ (testing)
# โดยแบ่ง 80% สำหรับเทรน และ 20% สำหรับทดสอบ
X_train, X_test, y_train, y_test = train_test_split(X_data, y_labels, test_size=0.2, random_state=42)

print("ข้อมูลพร้อมสำหรับการเทรนแล้ว!")
print(f"ขนาดข้อมูลสำหรับฝึกสอน: {X_train.shape}")
print(f"ขนาดป้ายกำกับสำหรับฝึกสอน: {y_train.shape}")

# --- ขั้นตอนที่ 2: การสร้างโมเดล (Model Building) ---

# สร้างโครงสร้างของโมเดล Neural Network แบบง่ายๆ
# Sequential หมายถึงการเรียงชั้นของเลเยอร์ต่อกัน
model = keras.Sequential([
    # Layer แรก: Dense Layer มี 128 หน่วย และใช้ ReLU เป็น activation function
    keras.layers.Dense(units=128, activation='relu', input_shape=(20,)),

    # Layer ที่สอง: Dense Layer มี 64 หน่วย และใช้ ReLU
    keras.layers.Dense(units=64, activation='relu'),

    # Output Layer: มี 10 หน่วย (เท่ากับจำนวนคลาส) และใช้ Softmax
    # Softmax จะแปลงค่าให้เป็นความน่าจะเป็นของแต่ละคลาส
    keras.layers.Dense(units=10, activation='softmax')
])

# คอมไพล์โมเดล: กำหนดว่าจะใช้อัลกอริทึมอะไรในการปรับปรุงโมเดล
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy', # ฟังก์ชันคำนวณความผิดพลาด
              metrics=['accuracy']) # สิ่งที่เราต้องการวัด เช่น ความแม่นยำ

# --- ขั้นตอนที่ 3: การเทรนโมเดล (Model Training) ---

# เริ่มการฝึกสอนโมเดลด้วยข้อมูลที่เราเตรียมไว้
# epochs=10 หมายถึงการฝึกซ้ำ 10 รอบ
print("\n--- เริ่มการเทรนโมเดล ---")
history = model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# --- ขั้นตอนที่ 4: การประเมินผล (Model Evaluation) ---

# ประเมินประสิทธิภาพของโมเดลด้วยข้อมูลทดสอบ
print("\n--- ประเมินประสิทธิภาพของโมเดล ---")
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"ความแม่นยำของโมเดล: {test_acc:.4f}")

# --- การทำให้ AI โต้ตอบ (Simulating Conversation) ---

print("\n--- ลองคุยกับ AI ได้เลย! (พิมพ์ 'หยุด' เพื่อจบการสนทนา) ---")
while True:
    user_input = input("คุณ: ")
    user_input = user_input.lower().strip() # แปลงข้อความเป็นตัวพิมพ์เล็กและลบช่องว่าง

    if user_input == 'หยุด':
        print("AI: ลาก่อนครับ!")
        break

    if "สวัสดี" in user_input:
        print("AI: สวัสดีครับ! เป็นไงบ้าง?")
    elif "สบายดีไหม" in user_input or "เป็นไงบ้าง" in user_input:
        print("AI: ผมสบายดีครับ ขอบคุณที่ถามนะ!")
    elif "ชื่ออะไร" in user_input:
        print("AI: ผมยังไม่มีชื่อเรียกเป็นทางการครับ")
    elif "ขอบคุณ" in user_input:
        print("AI: ยินดีครับ!")
    else:
        print("AI: ผมไม่ค่อยเข้าใจที่คุณพูดครับ ลองพิมพ์คำอื่นดูไหม?")
